import pandas as pd
import os
from typing import List, Dict, Union
import io

def read_input_excel(filepath_or_buffer: Union[str, io.BytesIO]) -> List[Dict[str, str]]:
    """
    Reads an Excel file and returns a list of dictionaries with published_url and target_url.
    Assumes columns 'published_url' and 'target_url' exist.
    """
    if isinstance(filepath_or_buffer, str) and not os.path.exists(filepath_or_buffer):
        print(f"Error: Target input file not found at {filepath_or_buffer}")
        return []

    try:
        df = pd.read_excel(filepath_or_buffer)
        # Ensure column names exist
        columns = df.columns.str.lower()
        if 'published_url' not in columns or 'target_url' not in columns:
            print(f"Error: Missing required columns 'published_url' and/or 'target_url'")
            return []

        # Convert column names to lower for case-insensitive access
        df.columns = columns
        
        # Drop rows with empty published_url
        df = df.dropna(subset=['published_url'])
        
        return df[['published_url', 'target_url']].to_dict('records')
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []
