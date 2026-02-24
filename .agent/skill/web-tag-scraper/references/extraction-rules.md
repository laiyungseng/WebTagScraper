# Extraction Rules

## Meta Robots
- Match `<meta>` tags where `name` equals `robots` case-insensitively.
- Return the raw `content` string as `robots_raw`.
- Parse directives into lowercase tokens split on commas/whitespace.
- Preserve uncommon directives (for example `max-snippet:-1`) in `robots_directives`.

## Target Anchor Matching
- Resolve relative `href` values against `published_url`.
- Normalize scheme/host casing, strip fragments, and normalize trailing slash before compare.
- Mark `target_link_found=true` if any normalized href equals normalized `target_url`.
- Count all matching anchors as `target_link_count`.

## Anchor Evidence Fields
- `anchor_texts`: deduplicated visible text for matching anchors.
- `anchor_rels`: deduplicated `rel` values for matching anchors.
- `link_context`: short snippet around the first matching anchor for manual QA.

## Request Behavior
- Use timeout and retry with exponential backoff.
- Record transport or parse exceptions in `error`.
- Continue processing remaining rows when a single URL fails.
