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


def is_login_page(html: str) -> bool:
    text = (html or "").lower()
    return "log in - itexams.com" in text and "examspage__question" not in text


def is_paywalled_page(html: str) -> bool:
    text = (html or "").lower()
    return "unlock all features" in text and "examspage__question" not in text


