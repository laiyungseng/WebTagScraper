import pandas as pd
import json
import io
from typing import Optional

def write_output_excel(data: list, filepath: str = None) -> Optional[io.BytesIO]:
    """
    Writes the scraped data list of dictionaries into an Excel output file or returns BytesIO.
    Flattens complex data structures like target_links_data to be readable in Excel.
    """
    if not data:
        print("No data to write.")
        if filepath is None:
            return io.BytesIO()
        return None

    flattened_data = []
    for row in data:
        # Create a deep copy to manipulate
        flat_row = {
            "published_url": row.get("published_url"),
            "target_url": row.get("target_url"),
            "status_code": row.get("status_code"),
            "meta_robots": row.get("meta_robots"),
            "target_links_found": row.get("target_links_found"),
            "error": row.get("error", "")
        }
        
        # Format the links list as a JSON string or simplified string for Excel readability
        links_data = row.get("target_links_data", [])
        if links_data:
            flat_row["link_details"] = json.dumps(links_data, ensure_ascii=False)
        else:
            flat_row["link_details"] = ""
            
        flattened_data.append(flat_row)

    try:
        df = pd.DataFrame(flattened_data)
        if filepath:
            df.to_excel(filepath, index=False)
            print(f"Successfully wrote {len(flattened_data)} records to {filepath}")
            return None
        else:
            output = io.BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)
            return output
    except Exception as e:
        print(f"Error writing to Excel: {e}")
        return None
