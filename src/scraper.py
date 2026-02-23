import httpx
from bs4 import BeautifulSoup
import re
from typing import Dict, Any

def scrape_url(published_url: str, target_url: str) -> Dict[str, Any]:
    """
    Scrapes the published_url to find the meta robots tag and any anchor tags pointing to target_url.
    Returns a dictionary of findings.
    """
    result = {
        "published_url": published_url,
        "target_url": target_url,
        "status_code": None,
        "meta_robots": None,
        "target_links_found": 0,
        "target_links_data": []
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = httpx.get(published_url, headers=headers, timeout=15.0, follow_redirects=True)
        result["status_code"] = response.status_code
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. Scrape <meta name="robots">
            robots_meta = soup.find('meta', attrs={'name': lambda x: x and x.lower() == 'robots'})
            if robots_meta and robots_meta.get('content'):
                result["meta_robots"] = robots_meta.get('content')
            
            # 2. Scrape <a href="target_url">
            # We look for exact matches or cases where the href contains the target_url (flexible matching)
            target_links = soup.find_all('a', href=lambda href: href and target_url in href)
            
            result["target_links_found"] = len(target_links)
            for a_tag in target_links:
                href = a_tag.get('href')
                text = a_tag.get_text(strip=True)
                
                # Optionally get surrounding context by getting parent's text
                parent_context = ""
                if a_tag.parent:
                    parent_text = a_tag.parent.get_text(strip=True)
                    # Limit the context size
                    parent_context = parent_text[:200] + "..." if len(parent_text) > 200 else parent_text
                
                result["target_links_data"].append({
                    "href": href,
                    "anchor_text": text,
                    "surrounding_context": parent_context
                })
                
    except Exception as e:
        result["error"] = str(e)
        
    return result
