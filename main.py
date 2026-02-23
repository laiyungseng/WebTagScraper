import os
from src.reader import read_input_excel
from src.scraper import scrape_url
from src.writer import write_output_excel
import time

def main():
    input_file = os.path.join("file", "input.xlsx")
    output_file = os.path.join("file", "output.xlsx")

    print(f"Reading tasks from {input_file}...")
    tasks = read_input_excel(input_file)
    
    if not tasks:
        print("No tasks found. Please ensure file/input.xlsx exists and has data.")
        return

    print(f"Found {len(tasks)} tasks.")
    results = []

    for idx, task in enumerate(tasks, 1):
        pub_url = str(task['published_url']).strip()
        target_url = str(task['target_url']).strip() if pd.notna(task['target_url']) else ""
        
        print(f"[{idx}/{len(tasks)}] Scraping {pub_url} for target {target_url}...")
        
        result = scrape_url(pub_url, target_url)
        results.append(result)
        
        # Small delay to be polite to servers
        time.sleep(1)

    print(f"Finished scraping. Writing results to {output_file}...")
    write_output_excel(results, output_file)
    print("Done!")

if __name__ == "__main__":
    import pandas as pd # used locally for notna
    main()
