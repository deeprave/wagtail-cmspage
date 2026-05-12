# Palette Migration Mapping Log

This document is historical migration guidance for sites that still store the old Bootstrap-era palette strings in StreamField JSON.
The live `cmspage` contract is the semantic `cp-*` palette defined in `cmspage.blocks.themes.Palette`.
Do not use the old `bg-* text-* title-* links-*` class stacks in new content, templates, or seed data.

## Historical Mapping

### Original Enum → New Enum Mappings


| Historical Enum Key | Historical CSS Value                               | Current Enum Key | Current CSS Value | Description                                     |
| ------------------- | -------------------------------------------------- | ---------------- | ----------------- | ----------------------------------------------- |
| `NONE`              | `bg-transparent links-dark text-dark title-dark`   | `NONE`           | `cp-transparent`  | Transparent wrapper using semantic foregrounds  |
| `PAGE`              | `bg-body links-dark text-dark title-dark`          | `PAGE`           | `cp-page`         | Page-surface wrapper that follows the site mode |
| `LIGHT`             | `bg-light links-dark text-dark title-dark`         | `LIGHT`          | `cp-light`        | Fixed light theme wrapper                       |
| `DARK`              | `bg-dark links-light text-light title-light`       | `DARK`           | `cp-dark`         | Fixed dark theme wrapper                        |
| `WHITE`             | `bg-light links-dark text-black title-dark`        | `WHITE`          | `cp-white`        | Black on white                                  |
| `BLACK`             | `bg-white links-dark text-white title-light`       | `BLACK`          | `cp-black`        | White on black                                  |
| `PRIMARY`           | `bg-primary links-dark text-dark title-dark`       | `HIGHLIGHT`      | `cp-highlight`    | Highlight / alternate surface                   |
| `SECONDARY`         | `bg-secondary links-dark text-dark title-dark`     | `STANDOUT`       | `cp-standout`     | Standout / secondary alternate surface          |
| `TERTIARY`          | `bg-tertiary links-dark text-dark title-dark`      | `INFO`           | `cp-info`         | Informational site-colored surface              |
| `SUCCESS`           | `bg-success-subtle links-dark text-dark title-dark`| `SUCCESS`        | `cp-success`      | Positive / success state                        |
| `WARNING`           | `bg-warning-subtle links-dark text-dark title-dark`| `WARNING`        | `cp-warning`      | Warning / caution state                         |
| `INFO`              | `bg-info-subtle links-dark text-dark title-dark`   | `INFO`           | `cp-info`         | Informational state                             |
| `DANGER`            | `bg-danger-subtle links-dark text-dark title-dark` | `DANGER`         | `cp-danger`       | Error / destructive state                       |

## Migration Queries

These queries are only for one-time cleanup of old stored palette strings. They are not part of normal theming.

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
