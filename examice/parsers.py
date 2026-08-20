import re
from html import unescape
from typing import List, Tuple
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .settings import BASE_URL


def strip_html_text(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", unescape(text)).strip()


def is_blocked_html(html: str) -> bool:
    text = (html or "").lower()
    blocked_markers = (
        "checking your browser",
        "verify you are human",
        "please complete the security check",
        "g-recaptcha-response",
        "hcaptcha",
        "cf-chl",
        "access denied",
    )
    return any(marker in text for marker in blocked_markers)


def raise_if_blocked(html: str):
    if is_blocked_html(html):
        raise RuntimeError("Blocked by anti-bot/captcha page")


def extract_exam_links(html: str) -> List[Tuple[str, str]]:
    """Extract exam titles and links from vendor page on Examice."""
    soup = BeautifulSoup(html, "html.parser")
    results = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if "/exams/" in href and len(href.strip("/").split("/")) >= 3:
            full_url = urljoin(BASE_URL, href)
            title = strip_html_text(anchor.get_text(" ", strip=True))
            results.append((title, full_url))
    return results
