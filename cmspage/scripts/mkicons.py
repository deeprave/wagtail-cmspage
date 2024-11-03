#!/usr/bin/env python3
"""
Generate a Django model.TextChoices for SVG icons.

This script scans one or more directories for SVG files and creates
a module containing a Django TextChoices class with entries for each icon.

If using the default output, this must be run from the root of the cmspage app directory.
"""

import sys
from pathlib import Path
from typing import List, Set, Generator
import argparse

OUTFILE_NAME = "models/choice_icon.py"
TEMPLATES_PREFIX = "templates/"


def generate_icons_module(icon_dirs: List[str], recursive: bool = False) -> (int, int, str):
    dir_count = 0

    def _icons_in_directory(directory: Path) -> Generator[str, None, None]:
        if not directory.is_dir():
            raise ValueError(f"Directory '{directory}' does not exist")
        for icon_path in directory.glob("*.svg"):
            icon_str = icon_path.as_posix()
            # Strip icon path prefix - only need the path relative to the templates dir
            if TEMPLATES_PREFIX in icon_str:
                pos = icon_str.index(TEMPLATES_PREFIX) + len(TEMPLATES_PREFIX)
                icon_str = icon_str[pos:]
            yield icon_str

    def _search_dir(directory: Path) -> Generator[str, None, None]:
        nonlocal dir_count
        dir_count += 1
        # Search current directory
        yield from _icons_in_directory(directory)
        if recursive:
            # Search subdirectories recursively
            for subdirectory in directory.iterdir():
                if subdirectory.is_dir():
                    yield from _search_dir(subdirectory)

    def icon_list(dirs: List[str]) -> Generator[str, None, None]:
        for icon_dir in dirs:
            directory = Path(icon_dir)
            icon_count = 0
            for icon_name in _search_dir(directory):
                icon_count += 1
                yield icon_name

    # create a map of icon name to icon path to eliminate duplicate stem names
    icon_map = {Path(icon_path).stem: icon_path for icon_path in icon_list(icon_dirs)}
    # sort the icon names using the stem path for consistent output
    icons = [icon_map[icon_key] for icon_key in sorted(icon_map.keys())]

    content = ["from django.db import models", "", "class IconChoices(models.TextChoices):", '    NONE = "", "No Icon"']

    count = 0
    for icon in icons:
        # determine the root icon name (last component of the path)
        icon_stem = Path(icon).stem
        enum_value = icon_stem.upper().replace("-", "_")
        file_name = icon
        display_name = icon_stem.replace("-", " ").title()
        content.append(f'    {enum_value} = "{file_name}", "{display_name}"')
        count += 1

    return count, dir_count, "\n".join(content)


def write_module(content: str, filename: str):
    if filename == "-":
        sys.stdout.write(content)
        sys.stdout.write("\n")
    else:
        output_path = Path(filename)
        output_path.write_text(content + "\n")
        print(f"Icons module has been generated in '{output_path.absolute()}'", file=sys.stderr)


def process_paths(paths: List[str], icon_dirs: Set[str]) -> Set[str]:
    if paths is not None:
        for path in paths:
            if ":" not in path:
                icon_dirs.add(path)
            else:
                for p in path.split(":"):
                    icon_dirs.add(p)
    return icon_dirs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o", "--output", default=OUTFILE_NAME, help=f"Output to ('-' = stdout, default={OUTFILE_NAME})"
    )
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively search for SVG icons")
    parser.add_argument("paths", type=str, nargs="*", help="Directories containing SVG icons (multiple allowed)")
    args = parser.parse_args()

    icon_dirs = process_paths(args.paths, {"./templates/cmspage/icons"})

    count, dir_count, module_content = generate_icons_module(list(icon_dirs), args.recursive or False)
    print(f"Generated {count} icons from {dir_count} directories", file=sys.stderr)
    write_module(module_content, args.output)


if __name__ == "__main__":
    main()
