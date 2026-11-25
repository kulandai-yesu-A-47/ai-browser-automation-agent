from playwright.sync_api import sync_playwright
from urllib.parse import urlparse, quote_plus
import re

_playwright = None
_browser = None
_page = None

def _get_page():
    global _playwright, _browser, _page
    if _page is None:
        _playwright = sync_playwright().start()
        _browser = _playwright.chromium.launch(headless=True)
        _page = _browser.new_page()
    return _page

def search_web(query: str):
    page = _get_page()

    search_url = "https://www.bing.com/search?q=" + quote_plus(query)

    page.goto(
        search_url,
        wait_until="domcontentloaded",
        timeout=30000
    )

    page.wait_for_timeout(2000)

    return {
        "url": page.url,
        "title": page.title(),
        "text": page.locator("body").inner_text()[:7000]
    }

def open_page(url: str):
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Only valid http/https URLs are allowed.")
    page = _get_page()
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    return {"url": page.url, "title": page.title(), "text": page.locator("body").inner_text()[:7000]}

def extract_page_text():
    page = _get_page()
    return {"url": page.url, "title": page.title(), "text": page.locator("body").inner_text()[:7000]}

def fill_form(fields: dict):
    page = _get_page()
    filled = []
    for label, value in fields.items():
        if not isinstance(value, (str, int, float)):
            continue
        selectors = [
            f'input[placeholder="{label}"]',
            f'textarea[placeholder="{label}"]',
            f'input[name="{label}"]',
            f'textarea[name="{label}"]',
        ]
        done = False
        for selector in selectors:
            locator = page.locator(selector).first
            try:
                if locator.count() and locator.is_visible():
                    locator.fill(str(value))
                    filled.append(label)
                    done = True
                    break
            except Exception:
                pass
        if not done:
            try:
                locator = page.get_by_label(label, exact=False).first
                if locator.count() and locator.is_visible():
                    locator.fill(str(value))
                    filled.append(label)
            except Exception:
                pass
    return {
        "filled_fields": filled,
        "message": "Fields were filled where matching inputs were found. Review them manually; nothing was submitted."
    }

def close_browser():
    global _playwright, _browser, _page
    if _browser:
        _browser.close()
    if _playwright:
        _playwright.stop()
    _playwright = _browser = _page = None
