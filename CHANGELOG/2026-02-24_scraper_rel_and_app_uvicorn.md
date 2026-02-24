# 2026-02-24 Update: Enhancements to Scraper and App Executable Setup

## New Features
- **Scraper Enhancements (`src/scraper.py`)**: Added extraction for the `rel` attribute from `<a>` tags (e.g., `nofollow`, `noopener`). The `rel` values are now correctly extracted and appended to the `target_links_data` dictionary.
- **Application Startup (`app.py`)**: Appended the usual `if __name__== "__main__":` block to start the FastAPI server via `uvicorn.run`. The server defaults to running on `127.0.0.1` at port `5000` when the script is executed directly.
