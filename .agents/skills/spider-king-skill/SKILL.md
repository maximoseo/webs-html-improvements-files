---
name: Spider-King (Web Protocol Recovery)
source: https://github.com/aoyunyang/spider-king-skill
category: Coding
purpose: Chinese reverse engineering skill — recovers web protocols from any app/site, delivers pure protocol spec without browser automation
when_to_use: When you need the underlying HTTP/WebSocket protocol of an app, not a Selenium/Playwright scraper
tags: [reverse-engineering, web-protocol, http, websocket, api-recovery, chinese]
---
# Spider-King (Web Protocol Recovery)

## Purpose
Reverse engineering skill for web protocols. Instead of web scraping (fragile), recovers the underlying API/protocol so data can be fetched directly.

## Philosophy
"Pure protocol delivery" — never use browser automation as the solution.
Goal: understand the protocol → call it directly.

## Process
1. **Observe** — capture traffic (Charles/mitmproxy/DevTools)
2. **Analyze** — identify auth, sessions, signatures, encryption
3. **Reconstruct** — reproduce the exact request sequence
4. **Deliver** — clean Python/JS code calling the protocol directly

## Output
```python
# Clean protocol client (no browser, no Selenium)
import requests

def fetch_data(keyword: str, page: int = 1) -> dict:
    headers = {"User-Agent": "...", "Referer": "..."}
    params = {"wd": keyword, "pn": page * 10}
    r = requests.get("https://target.com/api/endpoint", 
                     headers=headers, params=params)
    return r.json()
```

## When To Use vs When Not To
| Use Spider-King | Don't Use |
|---|---|
| Data aggregation at scale | Single page loads |
| API recovery for integration | Public APIs already documented |
| Protocol reverse engineering | Simple HTML parsing (use BeautifulSoup) |
| Bypass aggressive bot detection | Ethical gray area targets |

## Integration Notes
- Language: Python-first, JavaScript secondary
- Auth patterns covered: JWT, cookie-based sessions, HMAC signatures, timestamp nonces
- Chinese platform expertise: Baidu, Douyin, JD, Taobao, WeChat Mini Programs
