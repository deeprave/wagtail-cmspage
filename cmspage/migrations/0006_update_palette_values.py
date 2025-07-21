# Updates palette values in StreamField data
# This migration has no effect unless the previous palette setup was used

from django.db import migrations
import json


def migrate_palette_values(apps, schema_editor):
    """
    Migrate old palette values to new semantic values using direct SQL
    """
    from django.db import connection

    # Skip if table doesn't exist
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_name = 'cmspage_cmspage'
        """)
        if not cursor.fetchone():
            print("Table cmspage_cmspage does not exist, skipping migration")
            return

    # Mapping from old palette values to new semantic values
    PALETTE_MAPPING = {
        "bg-transparent links-dark text-dark title-dark": "cp-transparent",
        "bg-body links-dark text-dark title-dark": "cp-page",
        "bg-light links-dark text-dark title-dark": "cp-light",
        "bg-dark links-light text-light title-light": "cp-dark",
        "bg-light links-dark text-black title-dark": "cp-white",
        "bg-white links-dark text-white title-light": "cp-black",
        "bg-primary links-dark text-dark title-dark": "cp-highlight",
        "bg-secondary links-dark text-dark title-dark": "cp-standout",
        "bg-tertiary links-dark text-dark title-dark": "cp-info",
        "bg-success-subtle links-dark text-dark title-dark": "cp-success",
        "bg-warning-subtle links-dark text-dark title-dark": "cp-warning",
        "bg-info-subtle links-dark text-dark title-dark": "cp-info",
        "bg-danger-subtle links-dark text-dark title-dark": "cp-danger",
    }

    # Execute the updates using raw SQL
    with connection.cursor() as cursor:
        for old_value, new_value in PALETTE_MAPPING.items():
            cursor.execute(
                """
                UPDATE cmspage_cmspage
                SET body = REPLACE(body::text, %s, %s)::jsonb
                WHERE body::text LIKE %s
            """,
                [f'"palette": "{old_value}"', f'"palette": "{new_value}"', f'%"palette": "{old_value}"%'],
            )

            # Also update the footer field if it exists
            cursor.execute(
                """
                UPDATE cmspage_cmsfooterpage
                SET footer = REPLACE(footer::text, %s, %s)::jsonb
                WHERE footer::text LIKE %s
            """,
                [f'"palette": "{old_value}"', f'"palette": "{new_value}"', f'%"palette": "{old_value}"%'],
            ) if connection.vendor == "postgresql" else None


def reverse_migrate_palette_values(apps, schema_editor):
    """
    Reverse migration - convert back to old values if needed
    """
    # Skip reverse migration
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("cmspage", "0005_add_performance_indexes"),
    ]

    operations = [
        migrations.RunPython(migrate_palette_values, reverse_migrate_palette_values),
    ]
