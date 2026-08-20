import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple

from tqdm import tqdm

from .http_client import HttpFetcher
from .matching import normalize_exam_code, provider_exam_url
from .parsers import is_login_page, is_paywalled_page
from .question_parser import parse_question_page
from .settings import DEFAULT_DELAY_RANGE


class FastExamScanner:
    def __init__(
        self,
        fetcher: HttpFetcher,
        *,
        delay_range: Tuple[float, float] = DEFAULT_DELAY_RANGE,
    ):
        self.fetcher = fetcher
        self.delay_range = delay_range

    def get_page_url(self, exam_code: str, page_number: int) -> str:
        return provider_exam_url(normalize_exam_code(exam_code), page_number)

    def fetch_page_questions(self, exam_code: str, page_number: int) -> List[Dict]:
        url = self.get_page_url(exam_code, page_number)
        html = self.fetcher.fetch_html(url)
        if is_login_page(html) or is_paywalled_page(html):
            return []
        return parse_question_page(html, url=url)


    def scan_pages(
        self,
        exam_code: str,
        start_page: int = 1,
        max_pages: int = 75,
        workers: int = 4,
    ) -> List[Dict]:
        questions_by_page: Dict[int, List[Dict]] = {}
        pages = list(range(start_page, max_pages + 1))
        
        with ThreadPoolExecutor(max_workers=max(1, workers)) as executor:
            futures = {
                executor.submit(self.fetch_page_questions, exam_code, p): p
                for p in pages
            }
            with tqdm(total=len(pages), desc="Fetching ITExams Pages", unit="page") as pbar:
                for future in as_completed(futures):
                    page_num = futures[future]
                    try:
                        qs = future.result()
                        if qs:
                            questions_by_page[page_num] = qs
                    except Exception as exc:
                        tqdm.write(f"✗ Page {page_num} error: {exc}")
                    pbar.update(1)

        # Re-assemble questions in strict page order
        all_questions = []
        for p in sorted(questions_by_page.keys()):
            all_questions.extend(questions_by_page[p])

        return all_questions
