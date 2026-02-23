import pandas as pd
import os

def create_mock():
    data = [
        {
            "published_url": "https://example.com",
            "target_url": "iana.org"
        },
        {
            "published_url": "https://httpbin.org/html",
            "target_url": "moby"
        }
    ]
    df = pd.DataFrame(data)
    filepath = os.path.join("file", "input.xlsx")
    os.makedirs("file", exist_ok=True)
    df.to_excel(filepath, index=False)
    print(f"Mock input created at {filepath}")

if __name__ == "__main__":
    create_mock()
