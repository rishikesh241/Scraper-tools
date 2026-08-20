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

    match = re.search(r"(?:^|/)exams/([^/]+)", path.strip("/"), re.I)
    if match:
        return match.group(1).lower()

    return provider.strip("/").lower()


def normalize_exam_code(exam_code: str) -> str:
    exam_code = (exam_code or "").strip()
    if not exam_code:
        return ""

    parsed = urlparse(exam_code)
    path = parsed.path if parsed.scheme else exam_code
    parts = [p for p in path.strip("/").split("/") if p]
    if parts:
        return parts[-1].lower()

    return exam_code.lower()


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


def provider_exam_url(provider: str, exam_code: str = "") -> str:
    p = normalize_provider(provider)
    e = normalize_exam_code(exam_code)
    if e:
        return f"{BASE_URL}/exams/{p}/{e}"
    return f"{BASE_URL}/exams/{p}"


def extract_topic_question(text_or_url: str) -> Tuple[int, int]:
    match = re.search(r"(?:topic|t)[-_\s]*(\d+)[-_\s]*(?:question|q)[-_\s]*(\d+)", text_or_url, re.I)
    if match:
        return (int(match.group(1)), int(match.group(2)))

    match = re.search(r"question\s*(\d+)", text_or_url, re.I)
    if match:
        return (1, int(match.group(1)))

    return (10**9, 10**9)


def slug_from_url(url: str) -> str:
    path = urlparse(url).path.strip("/").replace("/", "-")
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", path).strip("-")
    return slug or "examice-page"
