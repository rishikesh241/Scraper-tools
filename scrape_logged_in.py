import json
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from examtopics.cache import HtmlCache
from examtopics.fast_scanner import FastDiscussionScanner
from examtopics.http_client import HttpFetcher, SessionFactory
from examtopics.matching import build_page_numbers, extract_topic_question
from examtopics.output import write_questions_to_json, write_questions_to_txt
from examtopics.question_parser import parse_question_page


class AuthSessionFactory(SessionFactory):
    def __init__(self, pool_size: int = 64):
        super().__init__(pool_size)
        self._auth_cookies = {}
        self._init_login()

    def _init_login(self):
        session = super().get()
        res = session.get("https://www.examtopics.com/login/", timeout=20)
        soup = BeautifulSoup(res.text, "html.parser")
        csrf = soup.find("input", {"name": "csrfmiddlewaretoken"})
        if csrf:
            email = os.environ.get("EXAMTOPICS_EMAIL", "")
            password = os.environ.get("EXAMTOPICS_PASSWORD", "")
            post_data = {
                "csrfmiddlewaretoken": csrf["value"],
                "email": email,
                "password": password,
            }
            session.post(
                "https://www.examtopics.com/login/",
                data=post_data,
                headers={"Referer": "https://www.examtopics.com/login/"},
                allow_redirects=True,
                timeout=20,
            )
            if not session.cookies.get("sessionid"):
                print("Warning: Login failed (no sessionid cookie).")
            else:
                print("Authenticated with ExamTopics successfully.")
                self._auth_cookies = session.cookies.get_dict()

    def get(self) -> requests.Session:
        session = getattr(self._thread_local, "session", None)
        if session is None:
            session = super().get()
            if self._auth_cookies:
                session.cookies.update(self._auth_cookies)
            self._thread_local.session = session
        return session


def get_question_sort_key(q: dict):
    q_no = q.get("question_no", "")
    m_topic = re.search(r"topic\s+(\d+)", q_no, re.I)
    m_qnum = re.search(r"question\s+(\d+)", q_no, re.I)
    if m_topic and m_qnum:
        return (int(m_topic.group(1)), int(m_qnum.group(1)))
    if m_qnum:
        return (1, int(m_qnum.group(1)))
    url = q.get("url", "")
    return extract_topic_question(url)


def main():
    print("Starting authenticated scrape for PMLE...")
    txt_file = "PROFESSIONAL-MACHINE-LEARNING-ENGINEER questions.txt"
    json_file = "PROFESSIONAL-MACHINE-LEARNING-ENGINEER questions.json"

    # Load existing questions so any non-ExamTopics fallback questions (e.g. Q343, Q344) aren't lost
    existing_by_key = {}
    if os.path.exists(json_file):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                for q in json.load(f):
                    existing_by_key[get_question_sort_key(q)] = q
        except Exception as exc:
            print(f"Warning: could not read existing {json_file}: {exc}")

    cache = HtmlCache(Path(".examtopics_cache_auth"), 0)
    session_factory = AuthSessionFactory()

    fetcher = HttpFetcher(
        timeout=20,
        retries=5,
        cache=cache,
        refresh_cache=True,
        session_factory=session_factory,
    )

    provider = "google"
    exam_code = "professional-machine-learning-engineer"

    scanner = FastDiscussionScanner(provider, fetcher, delay_range=(0.5, 0.8))
    total_pages = scanner.get_num_pages()
    print(f"Total discussion pages: {total_pages}")

    page_numbers = build_page_numbers(total_pages, 1, None, None)
    print(f"Scanning {len(page_numbers)} pages for links...")

    links = scanner.scan(page_numbers, exam_code, workers=2)

    if not links:
        print("No links found.")
        return

    links = sorted(links, key=lambda u: extract_topic_question(u))
    print(f"Found {len(links)} links. Fetching question pages...")

    scraped_by_key = {}
    failed = 0

    def fetch_and_parse(url: str):
        import time
        time.sleep(0.5)
        html = fetcher.fetch_html(url)
        return parse_question_page(html, url=url)

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(fetch_and_parse, url): url for url in links}
        with tqdm(total=len(links), desc="Fetching Questions", unit="q") as pbar:
            for future in as_completed(futures):
                url = futures[future]
                try:
                    q = future.result()
                    scraped_by_key[get_question_sort_key(q)] = q
                except Exception as exc:
                    failed += 1
                    tqdm.write(f"✗ {url} — {exc}")
                pbar.update(1)

    # Merge: prefer fresh scraped data, fall back to existing questions for any missing keys
    merged_by_key = dict(existing_by_key)
    merged_by_key.update(scraped_by_key)

    questions = [merged_by_key[k] for k in sorted(merged_by_key.keys())]

    write_questions_to_txt(txt_file, questions)
    write_questions_to_json(json_file, questions)

    # Clean up temporary auth cache directory
    try:
        import shutil
        if os.path.exists(".examtopics_cache_auth"):
            shutil.rmtree(".examtopics_cache_auth")
    except Exception:
        pass

    print(f"\nDone! {len(questions)} total questions saved ({len(scraped_by_key)} scraped live, {failed} failed).")
    print(f"  → {txt_file}")
    print(f"  → {json_file}")


if __name__ == "__main__":
    main()

