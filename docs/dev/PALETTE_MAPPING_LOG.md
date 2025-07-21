# Palette Migration Mapping Log

This document provides the exact mappings between old Bootstrap-based palette values and new semantic cp-* values for database migration.
It is of no interest otherwise unless you have previously built a site using cmspage and need to migrate the palette values.

## Complete Value Mappings

### Original Enum → New Enum Mappings


| Original Enum Key | Original CSS Value                                  | New Enum Key | New CSS Value    | Description                                    |
| ----------------- | --------------------------------------------------- | ------------ | ---------------- | ---------------------------------------------- |
| `NONE`            | `bg-transparent links-dark text-dark title-dark`    | `NONE`       | `cp-transparent` | Dark on Transparent → Transparent Background  |
| `PAGE`            | `bg-body links-dark text-dark title-dark`           | `PAGE`       | `cp-page`        | Dark on Page Background → Page Theme          |
| `LIGHT`           | `bg-light links-dark text-dark title-dark`          | `LIGHT`      | `cp-light`       | Dark on Light Background → Light Theme        |
| `DARK`            | `bg-dark links-light text-light title-light`        | `DARK`       | `cp-dark`        | Light on Dark Background → Dark Theme         |
| `WHITE`           | `bg-light links-dark text-black title-dark`         | `WHITE`      | `cp-white`       | Black on White Background → Black on White    |
| `BLACK`           | `bg-white links-dark text-white title-light`        | `BLACK`      | `cp-black`       | White on Black Background → White on Black    |
| `PRIMARY`         | `bg-primary links-dark text-dark title-dark`        | `HIGHLIGHT`  | `cp-highlight`   | Dark on Primary Background → Highlight Theme  |
| `SECONDARY`       | `bg-secondary links-dark text-dark title-dark`      | `STANDOUT`   | `cp-standout`    | Dark on Secondary Background → Standout Theme |
| `TERTIARY`        | `bg-tertiary links-dark text-dark title-dark`       | `INFO`       | `cp-info`        | Dark on Tertiary Background → Info Theme      |
| `SUCCESS`         | `bg-success-subtle links-dark text-dark title-dark` | `SUCCESS`    | `cp-success`     | Dark on Success Background → Success          |
| `WARNING`         | `bg-warning-subtle links-dark text-dark title-dark` | `WARNING`    | `cp-warning`     | Dark on Warning Background → Warning          |
| `INFO`            | `bg-info-subtle links-dark text-dark title-dark`    | `INFO`       | `cp-info`        | Dark on Info Background → Info                |
| `DANGER`          | `bg-danger-subtle links-dark text-dark title-dark`  | `DANGER`     | `cp-danger`      | Dark on Danger Background → Danger            |

## SQL Query Templates

### PostgreSQL UPDATE Query

```sql
-- Update StreamField JSON data in CMS pages
UPDATE cmspage_cmspage SET
  body = replace(
    replace(
      replace(
        replace(
          replace(
            replace(
              replace(
                replace(
                  replace(
                    replace(
                      replace(
                        replace(
                          replace(body::text,
                            '"palette": "bg-transparent links-dark text-dark title-dark"',
                            '"palette": "cp-transparent"'
                          ),
                          '"palette": "bg-body links-dark text-dark title-dark"',
                          '"palette": "cp-page"'
                        ),
                        '"palette": "bg-light links-dark text-dark title-dark"',
                        '"palette": "cp-light"'
                      ),
                      '"palette": "bg-dark links-light text-light title-light"',
                      '"palette": "cp-dark"'
                    ),
                    '"palette": "bg-light links-dark text-black title-dark"',
                    '"palette": "cp-white"'
                  ),
                  '"palette": "bg-white links-dark text-white title-light"',
                  '"palette": "cp-black"'
                ),
                '"palette": "bg-primary links-dark text-dark title-dark"',
                '"palette": "cp-highlight"'
              ),
              '"palette": "bg-secondary links-dark text-dark title-dark"',
              '"palette": "cp-standout"'
            ),
            '"palette": "bg-tertiary links-dark text-dark title-dark"',
            '"palette": "cp-info"'
          ),
          '"palette": "bg-success-subtle links-dark text-dark title-dark"',
          '"palette": "cp-success"'
        ),
        '"palette": "bg-warning-subtle links-dark text-dark title-dark"',
        '"palette": "cp-warning"'
      ),
      '"palette": "bg-info-subtle links-dark text-dark title-dark"',
      '"palette": "cp-info"'
    ),
    '"palette": "bg-danger-subtle links-dark text-dark title-dark"',
    '"palette": "cp-danger"'
  )::jsonb
WHERE body::text LIKE '%"palette": "bg-%';
```

### Individual UPDATE Statements (Safer Approach)

```sql
-- Update each mapping individually for better control and verification

-- NONE maps to cp-transparent
UPDATE cmspage_cmspage SET
  body = replace(body::text, '"palette": "bg-transparent links-dark text-dark title-dark"', '"palette": "cp-transparent"')::jsonb
WHERE body::text LIKE '%"palette": "bg-transparent links-dark text-dark title-dark"%';

-- PAGE maps to cp-page
UPDATE cmspage_cmspage SET
  body = replace(body::text, '"palette": "bg-body links-dark text-dark title-dark"', '"palette": "cp-page"')::jsonb
WHERE body::text LIKE '%"palette": "bg-body links-dark text-dark title-dark"%';

-- LIGHT → cp-light
UPDATE cmspage_cmspage SET
  body = replace(body::text, '"palette": "bg-light links-dark text-dark title-dark"', '"palette": "cp-light"')::jsonb
WHERE body::text LIKE '%"palette": "bg-light links-dark text-dark title-dark"%';

-- DARK → cp-dark
UPDATE cmspage_cmspage SET
  body = replace(body::text, '"palette": "bg-dark links-light text-light title-light"', '"palette": "cp-dark"')::jsonb
WHERE body::text LIKE '%"palette": "bg-dark links-light text-light title-light"%';

-- WHITE → cp-white (Note: original WHITE used bg-light, not bg-white)
UPDATE cmspage_cmspage SET
  body = replace(body::text, '"palette": "bg-light links-dark text-black title-dark"', '"palette": "cp-white"')::jsonb
WHERE body::text LIKE '%"palette": "bg-light links-dark text-black title-dark"%';

-- BLACK → cp-black (Note: original BLACK used bg-white)
UPDATE cmspage_cmspage SET
  body = replace(body::text, '"palette": "bg-white links-dark text-white title-light"', '"palette": "cp-black"')::jsonb
WHERE body::text LIKE '%"palette": "bg-white links-dark text-white title-light"%';

-- PRIMARY → cp-highlight
UPDATE cmspage_cmspage SET
  body = replace(body::text, '"palette": "bg-primary links-dark text-dark title-dark"', '"palette": "cp-highlight"')::jsonb
WHERE body::text LIKE '%"palette": "bg-primary links-dark text-dark title-dark"%';

-- SECONDARY → cp-standout
UPDATE cmspage_cmspage SET
  body = replace(body::text, '"palette": "bg-secondary links-dark text-dark title-dark"', '"palette": "cp-standout"')::jsonb
WHERE body::text LIKE '%"palette": "bg-secondary links-dark text-dark title-dark"%';

-- TERTIARY → cp-info
UPDATE cmspage_cmspage SET
  body = replace(body::text, '"palette": "bg-tertiary links-dark text-dark title-dark"', '"palette": "cp-info"')::jsonb
WHERE body::text LIKE '%"palette": "bg-tertiary links-dark text-dark title-dark"%';

-- SUCCESS → cp-success
UPDATE cmspage_cmspage SET
  body = replace(body::text, '"palette": "bg-success-subtle links-dark text-dark title-dark"', '"palette": "cp-success"')::jsonb
WHERE body::text LIKE '%"palette": "bg-success-subtle links-dark text-dark title-dark"%';

-- WARNING → cp-warning
UPDATE cmspage_cmspage SET
  body = replace(body::text, '"palette": "bg-warning-subtle links-dark text-dark title-dark"', '"palette": "cp-warning"')::jsonb
WHERE body::text LIKE '%"palette": "bg-warning-subtle links-dark text-dark title-dark"%';

-- INFO → cp-info
UPDATE cmspage_cmspage SET
  body = replace(body::text, '"palette": "bg-info-subtle links-dark text-dark title-dark"', '"palette": "cp-info"')::jsonb
WHERE body::text LIKE '%"palette": "bg-info-subtle links-dark text-dark title-dark"%';

-- DANGER → cp-danger
UPDATE cmspage_cmspage SET
  body = replace(body::text, '"palette": "bg-danger-subtle links-dark text-dark title-dark"', '"palette": "cp-danger"')::jsonb
WHERE body::text LIKE '%"palette": "bg-danger-subtle links-dark text-dark title-dark"%';
```

### Verification Queries

```sql
-- Count occurrences of old palette values
SELECT
  'bg-transparent links-dark text-dark title-dark' as old_value,
  COUNT(*) as count
FROM cmspage_cmspage
WHERE body::text LIKE '%"palette": "bg-transparent links-dark text-dark title-dark"%'

UNION ALL

SELECT
  'bg-body links-dark text-dark title-dark' as old_value,
  COUNT(*) as count
FROM cmspage_cmspage
WHERE body::text LIKE '%"palette": "bg-body links-dark text-dark title-dark"%'

UNION ALL

SELECT
  'bg-light links-dark text-dark title-dark' as old_value,
  COUNT(*) as count
FROM cmspage_cmspage
WHERE body::text LIKE '%"palette": "bg-light links-dark text-dark title-dark"%'

-- Add similar UNION ALL statements for all other old values...
;

-- Count occurrences of new palette values (after migration)
SELECT
  'cp-page' as new_value,
  COUNT(*) as count
FROM cmspage_cmspage
WHERE body::text LIKE '%"palette": "cp-page"%'

UNION ALL

SELECT
  'cp-light' as new_value,
  COUNT(*) as count
FROM cmspage_cmspage
WHERE body::text LIKE '%"palette": "cp-light"%'

-- Add similar UNION ALL statements for all other new values...
;
```

### MySQL UPDATE Query (if using MySQL)

```sql
-- MySQL version (using JSON_REPLACE if MySQL 5.7+)
UPDATE cmspage_cmspage SET
  body = REPLACE(
    REPLACE(
      REPLACE(
        REPLACE(body,
          '"palette": "bg-transparent links-dark text-dark title-dark"',
          '"palette": "cp-transparent"'
        ),
        '"palette": "bg-body links-dark text-dark title-dark"',
        '"palette": "cp-page"'
      ),
      '"palette": "bg-light links-dark text-dark title-dark"',
      '"palette": "cp-light"'
    ),
    '"palette": "bg-dark links-light text-light title-light"',
    '"palette": "cp-dark"'
  )
-- Continue with additional REPLACE functions...
WHERE body LIKE '%"palette": "bg-%';
```

## Important Notes

1. **StreamField Storage**: Wagtail stores StreamField data as JSON in the database
2. **Table Name**: Use `cmspage_cmspage` table (not `wagtailcore_page`) as that's where the `body` field exists
3. **Multiple Fields**: Some pages may have multiple StreamField fields (body, footer, etc.)
4. **Nested Blocks**: Palette values may be nested within other blocks (cards, sections, etc.)
5. **Backup Recommendation**: Always backup your database before running these queries
6. **Testing**: Test on a small subset first using `LIMIT` clause

## Insets Migration (Bonus)

If you also need to update Insets values:

```sql
-- Update Insets to responsive versions
UPDATE cmspage_cmspage SET
  body = replace(
    replace(
      replace(
        replace(
          replace(body::text,
            '"inset": "p-1"', '"inset": "p-1 p-sm-2"'
          ),
          '"inset": "p-2"', '"inset": "p-2 p-sm-3"'
        ),
        '"inset": "p-3"', '"inset": "p-3 p-sm-4"'
      ),
      '"inset": "p-4"', '"inset": "p-4 p-sm-5"'
    ),
    '"inset": "p-5"', '"inset": "p-5 p-sm-6"'
  )::jsonb
WHERE body::text LIKE '%"inset": "p-%';
```
