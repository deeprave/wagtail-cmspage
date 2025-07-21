#!/bin/sh
# This is a helper script to compile SCSS files into CSS.
# It requires the sassc compiler to be installed.
#
# This script can be configured as a File Watcher in PyCharm to automatically recompile SCSS files on save.
#
# Usage: scss-compile.sh [-b basedir] [-d destdir] [-t format] [-I includedir]...
#   -b basedir     Source directory (default: cmspage)
#   -d destdir     Destination directory (default: cmspage/static/css)
#   -t format      Output style: nested, expanded, compact, compressed (default: compressed)
#   -I includedir  Additional include directories (default includes node_modules)

# Default values
src=cmspage
dest=${src}/static/css
format=compressed
extra_includes=""

# Parse command line arguments
while getopts "b:d:t:I:" opt; do
  case $opt in
    b)
      src="$OPTARG"
      ;;
    d)
      dest="$OPTARG"
      ;;
    t)
      format="$OPTARG"
      ;;
    I)
      extra_includes="$extra_includes:$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      echo "Usage: $0 [-b basedir] [-d destdir] [-t format] [-I includedir]..." >&2
      exit 1
      ;;
  esac
done

mkdir -p "$dest"

# Build the list of include paths
include_paths=$(find $src -name '*.scss' -exec dirname {} \; | sort | uniq | tr '\n' ':')

# Combine default node_modules with extra includes and discovered paths
all_includes="node_modules:$include_paths$extra_includes"

for scss_file in $(find $src -name '*.scss' -not -name '_*.scss')
do
  css_file=$(basename "$scss_file" .scss).css
  output_file=$dest/$css_file
  echo "$scss_file -> $output_file"
  sassc -I "$all_includes" -t "$format" -m "$scss_file" "$output_file"
done
