import os
import sys
from pathlib import Path

# Ensure workspace root is in sys.path when running script directly
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from itexams.browser_scraper import CamoufoxScraper
from itexams.cache import HtmlCache
from itexams.fast_scanner import FastExamScanner
from itexams.http_client import HttpFetcher
from itexams.matching import display_slug, normalize_exam_code, normalize_provider
from itexams.output import write_questions_to_json, write_questions_to_txt
from itexams.settings import (
    DEFAULT_CACHE_DIR,
    DEFAULT_CACHE_TTL_SECONDS,
    DEFAULT_DELAY_RANGE,
    DEFAULT_RETRIES,
    DEFAULT_TIMEOUT_MS,
)


def main():
    print_header()

    default_provider = "google"
    default_exam_code = "Professional-Machine-Learning-Engineer"
    max_pages = 75
    cookie_str = os.environ.get("ITEXAMS_COOKIE", "")
    username = os.environ.get("ITEXAMS_USER", "")
    password = os.environ.get("ITEXAMS_PASS", "")

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for a in sys.argv[1:]:
        if a.startswith("--cookie="):
            cookie_str = a.split("=", 1)[1]
        elif a.startswith("--user="):
            username = a.split("=", 1)[1]
        elif a.startswith("--pass="):
            password = a.split("=", 1)[1]
        elif a.startswith("--max-pages="):
            try:
                max_pages = int(a.split("=", 1)[1])
            except ValueError:
                pass

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

    print(f"Target Provider: {provider}")
    print(f"Target Exam Code: {exam_code}")
    print(f"Target Pages: 1 to {max_pages}")
    if username and password:
        print(f"Account: {username}")
    elif cookie_str:
        print("Auth Cookie: [Provided]")
    else:
        print("Notice: Unauthenticated session. ITExams serves 15 questions (3 pages) for guest visitors.")
        print("Pass --user='email' --pass='pass' or set ITEXAMS_USER/ITEXAMS_PASS to log in.")
    print("\nFetching questions from ITExams...\n")

    questions = scrape_itexams(
        exam_code,
        cache,
        max_pages=max_pages,
        cookie_str=cookie_str,
        username=username,
        password=password,
    )

    if not questions:
        print("No questions found.")
        return

    slug = display_slug(exam_code).upper()
    txt_file = f"ITEXAMS-{slug} questions.txt"
    json_file = f"ITEXAMS-{slug} questions.json"

    write_questions_to_txt(txt_file, questions)
    write_questions_to_json(json_file, questions)

    print(f"\nDone! {len(questions)} questions saved.")
    print(f"  → {txt_file}")
    print(f"  → {json_file}")


def print_header():
    print()
    print("=" * 60)
    print("  ITExams Scraper")
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


def build_fetcher(cache: HtmlCache, cookie_str: str = "", authenticated: bool = False) -> HttpFetcher:
    cookies = parse_cookie_str(cookie_str)
    return HttpFetcher(
        timeout=DEFAULT_TIMEOUT_MS // 1000,
        retries=DEFAULT_RETRIES,
        cache=cache,
        refresh_cache=authenticated or bool(cookie_str),
        cookies=cookies if cookies else None,
    )


def scrape_itexams(
    exam_code: str,
    cache: HtmlCache,
    max_pages: int = 75,
    cookie_str: str = "",
    username: str = "",
    password: str = "",
):
    fetcher = build_fetcher(cache, cookie_str=cookie_str, authenticated=bool(username and password))
    
    if username and password:
        print(f"Logging in as {username}...")
        ok = fetcher.login(username, password)
        if ok:
            print("✓ Login successful!")
        else:
            print("✗ Login failed; proceeding with current session.")

    try:
        scanner = FastExamScanner(fetcher, delay_range=DEFAULT_DELAY_RANGE)
        questions = scanner.scan_pages(exam_code, start_page=1, max_pages=max_pages, workers=4)
        if questions:
            return questions
    except Exception as exc:
        print(f"Fast scan failed; trying Camoufox fallback: {exc}")

    try:
        cookies_list = []
        if cookie_str:
            for k, v in parse_cookie_str(cookie_str).items():
                cookies_list.append({"name": k, "value": v, "domain": "itexams.com", "path": "/"})

        with CamoufoxScraper(
            headless=True,
            timeout_ms=DEFAULT_TIMEOUT_MS,
            retries=DEFAULT_RETRIES,
            delay_range=DEFAULT_DELAY_RANGE,
            cookies=cookies_list if cookies_list else None,
        ) as scraper:
            return scraper.scan_pages(exam_code, start_page=1, max_pages=max_pages)
    except Exception as exc:
        print(f"Camoufox scraper failed: {exc}")
        return []



if __name__ == "__main__":
    main()
