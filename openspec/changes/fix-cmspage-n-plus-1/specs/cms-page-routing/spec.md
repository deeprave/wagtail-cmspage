## Purpose

Resolves published CMS page URLs during request serve without repeating a page lookup and subclass fetch for every path segment.

## ADDED Requirements

### Requirement: Nested page serve uses bounded page lookups
The system SHALL resolve a live nested CMS page URL using a number of page-record and page-subclass fetches that does not grow with the number of path segments after the site root.

#### Scenario: Deep live page
- **WHEN** a visitor requests a live CMS page several segments below the site root
- **THEN** the page is served
- **AND** page-tree lookups for that request do not repeat a child-by-slug fetch for each remaining segment

### Requirement: URL and 404 behaviour matches default routing
The system SHALL serve the same live page, and return HTTP 404 for the same missing or unpublished leaf paths, as Wagtail’s default page router.

#### Scenario: Existing live page
- **WHEN** a visitor requests the published URL of a live CMS page
- **THEN** the response is that page’s normal serve result

#### Scenario: Unknown slug
- **WHEN** a visitor requests a path with no matching page
- **THEN** the response is HTTP 404

#### Scenario: Unpublished leaf
- **WHEN** a visitor requests the URL of a page that exists but is not live
- **THEN** the response is HTTP 404

### Requirement: Extra path after a page still routes
When a matching page’s URL is a prefix of the request path and that page accepts remaining path components, the system SHALL pass the unmatched suffix to that page’s router.

#### Scenario: Longest page prefix
- **WHEN** the full path is not itself a page but a shorter prefix is a page that handles extra path
- **THEN** that page receives the leftover components
- **AND** no deeper non-existent page is invented

### Requirement: Restricted pages stay restricted
The system SHALL continue to apply Wagtail page view restrictions after the page is resolved.

#### Scenario: Password or login restriction
- **WHEN** a live page has a view restriction
- **THEN** an unauthorized visitor is not served the page body
