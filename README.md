# WebTagScraper
A flexible web scraper developed in Python to extract specific tag information (`<meta name="robots">` and `<a href="target_url">`) based on a `published_url` and `target_url` provided via Excel. 

## Features
- **Scrape Robots Meta Tags**: Checks if a URL specifies `noindex, nofollow` or `index, follow`.
- **Target Link Extraction**: Identifies and extracts information from within `<a href="target_url">` tags, including anchor text and surrounding context.
- **Web UI**: Offers an intuitive Web UI (replacing the CLI version) to easily upload datasets and configure scraping.
- **Standalone Executable**: The scraper can be built into a standalone `.exe` using PyInstaller for seamless distribution.

## Setup and Installation

### Prerequisites
- Python 3.12+ 
- `uv` (Fast Python package installer)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/laiyungseng/WebTagScraper.git
   cd "WebTagScraper"
   ```
2. Create and switch to a virtual environment:
   ```bash
   uv venv
   # On Windows:
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

## Usage

### Run Web Server
Start the web interface using:
```bash
python app.py
```
Then visit `http://127.0.0.1:5000` or the provided local URL in your browser to start using the tool.

### Build Executable (Windows)
To build a standalone `.exe` file from the main script:
```bash
pyinstaller main.spec
```
The final standalone application will be located inside the `dist/` directory.

## Repository Structure

- `.env` - Environment configurations (ignored from version control)
- `CHANGELOG/` - Directory for update logs
- `app.py` - Flask web application
- `main.py` - Main scraper CLI/backend
- `requirements.txt` - Project dependencies snapshot
- `src/` - Backend scraping and parsing logic
- `static/` - Web assets (CSS/JS)
- `tests/` - Unit and integration tests
