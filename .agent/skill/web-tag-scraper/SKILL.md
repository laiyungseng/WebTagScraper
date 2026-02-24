---
name: web-tag-scraper
description: Scrape webpages listed in Excel or Google Sheets to extract SEO-relevant tags and link evidence, especially meta robots directives and anchor tags pointing to a target URL. Use when tasks include validating index/follow behavior, checking backlinks in page HTML, or producing structured scrape outputs from published_url and target_url columns.
---

# Web Tag Scraper

## Overview
Use this skill to run a repeatable scrape workflow for rows containing `published_url` and `target_url`, then return structured results for robots metadata and matching anchor tags.

## Workflow
1. Load input rows from Excel or Google Sheets.
2. Normalize URLs before requests.
3. Fetch each `published_url` with timeout, retries, and polite delay.
4. Parse HTML and extract robots + target-link evidence.
5. Write results to output sheet and log failures.

## Extraction Rules
Read [references/extraction-rules.md](references/extraction-rules.md) before parsing logic changes.

## Execution Checklist
1. Validate input columns: `published_url`, `target_url`.
2. Skip blank or invalid `published_url` and report the row status.
3. Parse `<meta name="robots">` and return raw content plus normalized directives.
4. Find `<a>` tags whose resolved `href` matches `target_url`.
5. Capture anchor text, rel attribute, and a short surrounding HTML context snippet.
6. Record request status code, final URL, and error details per row.
7. Save deterministic output columns so downstream analysis stays stable.

## Output Contract
Return one row per input URL with at least:
- `published_url`
- `target_url`
- `status`
- `status_code`
- `final_url`
- `robots_raw`
- `robots_directives`
- `target_link_found`
- `target_link_count`
- `anchor_texts`
- `anchor_rels`
- `link_context`
- `error`

## Debugging
- If robots data is missing, inspect page source and fallback to case-insensitive attribute matching.
- If target links are missed, compare normalized absolute URLs and trailing slash differences.
- If sites block requests, rotate headers/user-agent and increase retry backoff.
- If output is inconsistent, enforce fixed column order in writer logic.
