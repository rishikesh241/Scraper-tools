import sys
from pathlib import Path

# Ensure workspace root is in sys.path when running script directly
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from examice.browser_scraper import CamoufoxScraper
from examice.cache import HtmlCache
from examice.fast_scanner import FastExamScanner
from examice.http_client import HttpFetcher
from examice.matching import display_slug, normalize_exam_code, normalize_provider
from examice.output import write_questions_to_json, write_questions_to_txt
from examice.settings import (
    DEFAULT_CACHE_DIR,
    DEFAULT_CACHE_TTL_SECONDS,
    DEFAULT_DELAY_RANGE,
    DEFAULT_RETRIES,
    DEFAULT_TIMEOUT_MS,
)



import os

def main():
    print_header()

    default_provider = "google"
    default_exam_code = "professional-machine-learning-engineer"
    cookie_str = os.environ.get("EXAMICE_COOKIE", "")

    args = [a for a in sys.argv[1:] if not a.startswith("--cookie=")]
    for a in sys.argv[1:]:
        if a.startswith("--cookie="):
            cookie_str = a.split("=", 1)[1]

    if len(args) >= 2:
        provider = args[0]
        exam_code = args[1]
    else:
        provider_in = input(f"Provider [{default_provider}]: ").strip()
        provider = provider_in if provider_in else default_provider

        exam_code_in = input(f"Exam code [{default_exam_code}]: ").strip()
        exam_code = exam_code_in if exam_code_in else default_exam_code

    provider = normalize_provider(provider)
    exam_code = normalize_exam_code(exam_code)
    cache = HtmlCache(Path(DEFAULT_CACHE_DIR), DEFAULT_CACHE_TTL_SECONDS)

    print(f"\nTarget Provider: {provider}")
    print(f"Target Exam Code: {exam_code}")
    if cookie_str:
        print("Auth Cookie: [Provided]")
    else:
        print("Notice: Unauthenticated session. Examice limits guest preview to the first 5 questions.")
        print("To fetch all 375 questions, pass --cookie='session=...' or set EXAMICE_COOKIE environment variable.")
    print("Fetching questions & discussions from Examice...\n")

    questions = scrape_examice(provider, exam_code, cache, cookie_str=cookie_str)

    if not questions:
        print("No questions found.")
        return

    slug = display_slug(exam_code).upper()
    txt_file = f"{slug} questions.txt"
    json_file = f"{slug} questions.json"

    write_questions_to_txt(txt_file, questions)
    write_questions_to_json(json_file, questions)

    print(f"\nDone! {len(questions)} questions saved.")
    print(f"  → {txt_file}")
    print(f"  → {json_file}")


def print_header():
    print()
    print("=" * 60)
    print("  Examice Scraper")
    print("=" * 60)
    print()


def parse_cookie_str(cookie_str: str) -> dict:
    cookies = {}
    if not cookie_str:
        return cookies
    for part in cookie_str.split(";"):
        if "=" in part:
            k, v = part.strip().split("=", 1)
            cookies[k.strip()] = v.strip()
    return cookies


def build_fetcher(cache: HtmlCache, cookie_str: str = "") -> HttpFetcher:
    cookies = parse_cookie_str(cookie_str)
    return HttpFetcher(
        timeout=DEFAULT_TIMEOUT_MS // 1000,
        retries=DEFAULT_RETRIES,
        cache=cache,
        refresh_cache=bool(cookie_str),
        cookies=cookies if cookies else None,
    )


def scrape_examice(provider: str, exam_code: str, cache: HtmlCache, cookie_str: str = ""):
    fetcher = build_fetcher(cache, cookie_str=cookie_str)
    try:
        scanner = FastExamScanner(provider, fetcher, delay_range=DEFAULT_DELAY_RANGE)
        questions = scanner.fetch_questions(exam_code)
        if questions:
            return questions
    except Exception as exc:
        print(f"Fast scan failed; trying Camoufox fallback: {exc}")

    try:
        cookies_list = []
        if cookie_str:
            for k, v in parse_cookie_str(cookie_str).items():
                cookies_list.append({"name": k, "value": v, "domain": "examice.com", "path": "/"})

        with CamoufoxScraper(
            provider,
            headless=True,
            timeout_ms=DEFAULT_TIMEOUT_MS,
            retries=DEFAULT_RETRIES,
            delay_range=DEFAULT_DELAY_RANGE,
            cookies=cookies_list if cookies_list else None,
        ) as scraper:
            return scraper.fetch_questions(exam_code)
    except Exception as exc:
        print(f"Camoufox scraper failed: {exc}")
        return []



if __name__ == "__main__":
    main()
