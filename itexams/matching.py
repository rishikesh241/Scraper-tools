import re
from typing import Iterable, List, Tuple
from urllib.parse import urljoin, urlparse

from .settings import BASE_URL


def normalize_provider(provider: str) -> str:
    provider = (provider or "").strip()
    if not provider:
        return ""

    parsed = urlparse(provider)
    path = parsed.path if parsed.scheme else provider

    match = re.search(r"(?:^|/)vendor/([^/]+)", path.strip("/"), re.I)
    if match:
        return match.group(1).capitalize()

    return provider.strip("/").capitalize()


def normalize_exam_code(exam_code: str) -> str:
    exam_code = (exam_code or "").strip()
    if not exam_code:
        return ""

    parsed = urlparse(exam_code)
    path = parsed.path if parsed.scheme else exam_code
    parts = [p for p in path.strip("/").split("/") if p]
    if parts:
        return parts[-1]

    return exam_code


def normalize_search(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip().upper()


def normalize_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def display_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (value or "").lower()).strip("-")


def dedupe(values: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def provider_exam_url(exam_code: str, page_number: int = 1) -> str:
    e = normalize_exam_code(exam_code)
    if page_number > 1:
        return f"{BASE_URL}/exam/{e}/{page_number}"
    return f"{BASE_URL}/exam/{e}"


def extract_topic_question(text_or_url: str) -> Tuple[int, int]:
    match = re.search(r"question\s*#?\s*(\d+)", text_or_url, re.I)
    if match:
        return (1, int(match.group(1)))
    return (10**9, 10**9)


def slug_from_url(url: str) -> str:
    path = urlparse(url).path.strip("/").replace("/", "-")
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", path).strip("-")
    return slug or "itexams-page"
