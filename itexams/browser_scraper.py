import os
import random
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from tqdm import tqdm

from .matching import normalize_exam_code, provider_exam_url
from .parsers import is_login_page, raise_if_blocked
from .question_parser import parse_question_page
from .settings import (
    BLOCKED_URL_PARTS,
    DEFAULT_DELAY_RANGE,
    DEFAULT_RETRIES,
    DEFAULT_TIMEOUT_MS,
)

try:
    from camoufox.sync_api import Camoufox
    from camoufox.pkgman import LAUNCH_FILE, OS_NAME, launch_path
    from playwright.sync_api import Error as PlaywrightError
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
except ImportError:  # pragma: no cover
    Camoufox = None
    LAUNCH_FILE = {}
    OS_NAME = ""
    launch_path = None
    PlaywrightError = Exception
    PlaywrightTimeoutError = TimeoutError


class CamoufoxScraper:
    def __init__(
        self,
        *,
        headless: bool = True,
        timeout_ms: int = DEFAULT_TIMEOUT_MS,
        retries: int = DEFAULT_RETRIES,
        delay_range: Tuple[float, float] = DEFAULT_DELAY_RANGE,
        cookies: Optional[List[dict]] = None,
        storage_state: Optional[str] = None,
    ):
        self.headless = headless
        self.timeout_ms = timeout_ms
        self.retries = retries
        self.delay_range = delay_range
        self.cookies = cookies
        self.storage_state = storage_state
        self._manager = None
        self.browser = None
        self.context = None
        self.page = None

    def __enter__(self):
        if Camoufox is None:
            raise RuntimeError(
                "Camoufox missing. Run: pip install camoufox playwright beautifulsoup4 tqdm"
            )

        self._manager = Camoufox(
            headless=self.headless,
            humanize=True,
            locale="en-US",
            enable_cache=True,
            window=(1366, 900),
            executable_path=resolve_camoufox_executable(),
        )
        self.browser = self._manager.__enter__()
        context_kwargs = {
            "locale": "en-US",
            "viewport": {"width": 1366, "height": 900},
        }
        if self.storage_state:
            context_kwargs["storage_state"] = self.storage_state

        self.context = self.browser.new_context(**context_kwargs)
        if self.cookies:
            self.context.add_cookies(self.cookies)

        self.page = self.context.new_page()
        self.page.set_default_timeout(self.timeout_ms)
        self.page.route("**/*", self._route_request)
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.context:
            self.context.close()
        if self._manager:
            self._manager.__exit__(exc_type, exc, tb)

    def fetch_html(self, url: str) -> str:
        last_error = None
        for attempt in range(1, self.retries + 1):
            try:
                response = self.page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
                status = response.status if response else None
                if status and status >= 500:
                    raise RuntimeError(f"HTTP {status}")

                try:
                    self.page.wait_for_load_state("networkidle", timeout=8_000)
                except PlaywrightTimeoutError:
                    pass

                html = self.page.content()
                raise_if_blocked(html)
                return html
            except (PlaywrightError, RuntimeError, TimeoutError) as exc:
                last_error = exc
                if attempt < self.retries:
                    time.sleep(1.5 * attempt)

        raise RuntimeError(f"Failed to load {url}: {last_error}")

    def scan_pages(self, exam_code: str, start_page: int = 1, max_pages: int = 75) -> List[Dict]:
        questions = []
        for page in tqdm(range(start_page, max_pages + 1), desc="Fetching Pages (Camoufox)", unit="page"):
            url = provider_exam_url(normalize_exam_code(exam_code), page)
            try:
                html = self.fetch_html(url)
                if is_login_page(html):
                    tqdm.write(f"Page {page} requested login. Stopping.")
                    break
                qs = parse_question_page(html, url=url)
                if not qs:
                    tqdm.write(f"Page {page} returned 0 questions. Stopping.")
                    break
                questions.extend(qs)
            except Exception as exc:
                tqdm.write(f"Page {page} error: {exc}")
        return questions

    def _route_request(self, route):
        url = route.request.url.lower()
        if any(part in url for part in BLOCKED_URL_PARTS):
            route.abort()
            return
        route.continue_()


def resolve_camoufox_executable() -> Optional[str]:
    if launch_path is None:
        return None

    raw_path = Path(launch_path())
    if sys.platform == "win32":
        package_id = Path(sys.executable).parent.name
        local_app_data = os.environ.get("LOCALAPPDATA")
        if package_id.startswith("PythonSoftwareFoundation.") and local_app_data:
            store_cache_path = (
                Path(local_app_data)
                / "Packages"
                / package_id
                / "LocalCache"
                / "Local"
                / "camoufox"
                / "camoufox"
                / "Cache"
                / LAUNCH_FILE.get(OS_NAME, "camoufox.exe")
            )
            if store_cache_path.exists():
                return str(store_cache_path)

    return str(raw_path)
