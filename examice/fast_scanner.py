import random
import time
from typing import Dict, List, Optional, Tuple

from tqdm import tqdm

from .http_client import HttpFetcher
from .matching import normalize_exam_code, normalize_provider, provider_exam_url
from .question_parser import parse_question_sections
from .settings import DEFAULT_DELAY_RANGE


class FastExamScanner:
    def __init__(
        self,
        provider: str,
        fetcher: HttpFetcher,
        *,
        delay_range: Tuple[float, float] = DEFAULT_DELAY_RANGE,
    ):
        self.provider = normalize_provider(provider)
        self.fetcher = fetcher
        self.delay_range = delay_range

    def get_exam_url(self, exam_code: str) -> str:
        return provider_exam_url(self.provider, normalize_exam_code(exam_code))

    def fetch_questions(self, exam_code: str) -> List[Dict]:
        url = self.get_exam_url(exam_code)
        html = self.fetcher.fetch_html(url)
        questions = parse_question_sections(html, url=url, fetcher=self.fetcher)

        low, high = self.delay_range
        if high > 0:
            time.sleep(random.uniform(max(low, 0), max(high, low)))

        return questions
