# Web Scrapper Development Guide

## Objective
Develop a flexible web scraper that extracts specific tag information based on a `published_url` and `target_url` provided via an Excel file or Google Sheets.

### Scraper Priorities
1. `<meta name="robots">`: Detect if the website specifies `noindex`, `nofollow` or `index`, `follow` and extract all the information.
2. `<a href="target_url">`: Extract the information within an anchor tag that points to the specific `target_url` (e.g., anchor text, surrounding context).

## Workflow
1. **Analyze and Plan**: Analyze the scraping process, outline requirements, and document them in the planning file (`implementation_plan.md`).
2. **Loop Back**: Reinforce the thinking process and continuously loop back to debug or refine logic during development if errors occur.
3. **Skill Utilization**: Prioritize implementing skills if necessary (e.g., specific web design or frontend skills, though this primarily focuses on backend scraping logic).

## File Structure
- `.agent/skill/`: Stores downloaded skills that the agent can utilize.
- `.env`: Stores credentials (e.g., Google Drive or Sheets APIs).
- `file/`: Stores uploaded Excel files (input data) and retrieved information (output datasets).
- `CHANGELOG/`: Stores update logs.
- `requirements.txt`: Records installed libraries (alternatively managed natively by `uv` via `pyproject.toml`).

## Installation
- **Library Manager**: Use `uv` for Python package management. To install a library, use: `uv add "<library>"`. This adds the new library to the virtual environment.
- **Skills**: Download necessary skills from [Antigravity Awesome Skills](https://github.com/sickn33/antigravity-awesome-skills).
