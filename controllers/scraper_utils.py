"""
Scraper and URL Validation Utilities
"""

import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from fastapi import HTTPException

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

def is_valid_url(url: str) -> bool:
    """Checks if a string is a well-formed HTTP/HTTPS URL."""
    try:
        parsed = urlparse(url.strip())
        return parsed.scheme in ('http', 'https') and bool(parsed.netloc)
    except Exception:
        return False

def scrape_url_content(url: str) -> tuple[str, str]:
    """
    Fetches and extracts the headline and body text from a webpage URL.
    Returns:
        tuple (headline, body_text)
    Raises:
        HTTPException if the URL cannot be fetched or contains no text.
    """
    clean_url = url.strip()
    if not is_valid_url(clean_url):
        raise HTTPException(
            status_code=422,
            detail=f"Invalid URL format: '{clean_url}'. Must start with http:// or https://"
        )

    resp = None
    try:
        # Primary request with standard gzip/deflate encoding
        resp = requests.get(clean_url, headers=HEADERS, timeout=12)
        if resp.status_code >= 400:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to access URL. Server responded with HTTP status {resp.status_code}."
            )
    except (requests.exceptions.ContentDecodingError, Exception) as e:
        # Fallback: Retry with uncompressed plain text encoding if CDN compression fails
        try:
            fallback_headers = {**HEADERS, 'Accept-Encoding': 'identity'}
            resp = requests.get(clean_url, headers=fallback_headers, timeout=12)
            if resp.status_code >= 400:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to access URL. Server responded with HTTP status {resp.status_code}."
                )
        except requests.exceptions.Timeout:
            raise HTTPException(
                status_code=408,
                detail="Request timed out while trying to reach the provided URL."
            )
        except Exception as retry_err:
            raise HTTPException(
                status_code=400,
                detail=f"Network error while fetching URL: {str(retry_err)}"
            )

    soup = BeautifulSoup(resp.text, 'html.parser')

    # Remove script, style, and navigation tags
    for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'noscript', 'aside']):
        tag.decompose()

    # 1. Extract Headline
    headline = ""
    # Try OpenGraph title first
    og_title = soup.find('meta', property='og:title')
    if og_title and og_title.get('content'):
        headline = og_title['content'].strip()
    elif soup.find('h1'):
        headline = soup.find('h1').get_text(strip=True)
    elif soup.find('title'):
        headline = soup.find('title').get_text(strip=True)

    # 2. Extract Body Text
    paragraphs = [p.get_text(separator=' ', strip=True) for p in soup.find_all('p')]
    body_text = " ".join([p for p in paragraphs if len(p) > 20])

    if not body_text and not headline:
        raise HTTPException(
            status_code=422,
            detail="No readable article text or headline could be extracted from this webpage."
        )

    # If body is empty, fallback to headline
    if not body_text:
        body_text = headline

    return headline, body_text
