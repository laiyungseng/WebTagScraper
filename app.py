from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import io
import pandas as pd
import re

from src.reader import read_input_excel
from src.scraper import scrape_url
from src.writer import write_output_excel

app = FastAPI(title="Tag Scraper API")

# Mount frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

class SingleRequest(BaseModel):
    published_url: str
    target_url: str

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/scrape/single")
async def scrape_single(req: SingleRequest):
    if not req.published_url:
        raise HTTPException(status_code=400, detail="published_url is required")
    
    result = scrape_url(req.published_url, req.target_url)
    return {"status": "success", "data": result}

@app.post("/api/scrape/excel")
async def scrape_excel(file: UploadFile = File(...)):
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="File must be an Excel document (.xlsx or .xls)")
    
    contents = await file.read()
    buffer = io.BytesIO(contents)
    
    tasks = read_input_excel(buffer)
    if not tasks:
        raise HTTPException(status_code=400, detail="No valid tasks found in Excel. Ensure 'published_url' and 'target_url' columns exist.")
    
    results = []
    for task in tasks:
        pub_url = str(task.get('published_url', '')).strip()
        target_url = str(task.get('target_url', '')).strip()
        if pd.isna(pub_url) or pub_url.lower() == 'nan':
            continue
        if pd.isna(target_url) or target_url.lower() == 'nan':
            target_url = ""
            
        result = scrape_url(pub_url, target_url)
        results.append(result)
        
    output_buffer = write_output_excel(results)
    
    if output_buffer is None:
        raise HTTPException(status_code=500, detail="Failed to generate Excel file.")
    
    return StreamingResponse(
        output_buffer, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=scraped_results.xlsx"}
    )

@app.post("/api/scrape/sheet")
async def scrape_sheet(sheet_url: str = Form(...)):
    if not sheet_url:
        raise HTTPException(status_code=400, detail="sheet_url is required")
        
    # Attempt to convert to export CSV URL
    csv_url = sheet_url
    if "/edit" in sheet_url:
        # replace /edit... with /export?format=csv
        csv_url = re.sub(r'/edit.*$', '/export?format=csv', sheet_url)
        
    try:
        df = pd.read_csv(csv_url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read Google Sheet. Make sure the sheet is public. Error: {str(e)}")
        
    columns = df.columns.str.lower()
    df.columns = columns
    
    if 'published_url' not in columns:
        raise HTTPException(status_code=400, detail="Missing required column 'published_url' in the Google Sheet.")
        
    df = df.dropna(subset=['published_url'])
    tasks = df.to_dict('records')
    
    results = []
    for task in tasks:
        pub_url = str(task.get('published_url', '')).strip()
        target_url = str(task.get('target_url', '')).strip()
        if pd.isna(target_url) or target_url.lower() == 'nan':
            target_url = ""
            
        result = scrape_url(pub_url, target_url)
        results.append(result)
        
    output_buffer = write_output_excel(results)
    
    if output_buffer is None:
        raise HTTPException(status_code=500, detail="Failed to generate Excel file.")
    
    return StreamingResponse(
        output_buffer, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=scraped_results_sheet.xlsx"}
    )
if __name__== "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)