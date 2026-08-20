import json
import re
from html import unescape
from typing import Dict, List, Optional

from bs4 import BeautifulSoup, Comment, Tag

from .http_client import HttpFetcher
from .settings import BASE_URL


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("\xa0", " ")).strip()


def parse_question_sections(
    html: str,
    url: str = "",
    fetcher: Optional[HttpFetcher] = None,
) -> List[Dict]:
    """
    Parses all question sections on an Examice exam page and returns a list of question dicts:
    [
        {
            "url": str,
            "question_no": str,
            "question_id": str,
            "question": str,
            "options": {"A": "...", "B": "...", ...},
            "correct_answer": str,
            "explanation": str,
            "most_voted": str,
            "vote_counts": {"A": "96%", "D": "4%", ...},
            "community_answer": str,
            "discussion": [str, ...],
        },
        ...
    ]
    """
    soup = BeautifulSoup(html, "html.parser")
    # Remove HTML comments to eliminate SSR artifacts
    for comment in soup.find_all(string=lambda s: isinstance(s, Comment)):
        comment.extract()

    # Find question sections by data-question attribute or by input q-ID name or section content
    sections = []
    for sec in soup.find_all("section"):
        cls = sec.get("class") or []
        if "bg-muted/60" in cls:
            continue
        if sec.get("data-question") == "true":
            sections.append(sec)
        elif sec.find("input", attrs={"name": re.compile(r"^q-")}):
            sections.append(sec)
        else:
            txt = _clean(sec.get_text(" "))
            if re.search(r"Question\s*\d+\s*of\s*\d+", txt, re.I) and len(sec.select("label")) > 0:
                sections.append(sec)


    questions = []
    seen_ids = set()
    for sec in sections:
        q_data = parse_single_question_section(sec, url=url, fetcher=fetcher)
        if q_data and q_data.get("question"):
            q_key = (q_data.get("question_id") or q_data.get("question_no") or q_data["question"][:50])
            if q_key not in seen_ids:
                seen_ids.add(q_key)
                questions.append(q_data)

    return questions


def parse_single_question_section(
    sec: Tag,
    url: str = "",
    fetcher: Optional[HttpFetcher] = None,
) -> Dict:
    result: Dict = {"url": url}
    sec_text = _clean(sec.get_text(" "))

    # ── Question Number ───────────────────────────────────────────────
    m_no = re.search(r"Question\s*(\d+)\s*of\s*(\d+)", sec_text, re.I)
    if m_no:
        result["question_no"] = f"Question {m_no.group(1)} of {m_no.group(2)}"
    else:
        h2 = sec.find("h2")
        result["question_no"] = _clean(h2.get_text(" ")) if h2 else ""

    # ── Question ID ───────────────────────────────────────────────────
    q_id = None
    input_el = sec.find("input", attrs={"name": re.compile(r"^q-")})
    if input_el and input_el.get("name"):
        q_id = input_el["name"].replace("q-", "")
    elif sec.get("id"):
        q_id = sec["id"]
    result["question_id"] = q_id or ""

    # ── Question Text ─────────────────────────────────────────────────
    prose = sec.select_one(".prose")
    result["question"] = _clean(prose.get_text(" ")) if prose else ""

    # ── Options ───────────────────────────────────────────────────────
    options: Dict[str, str] = {}
    for label in sec.select("label"):
        label_txt = _clean(label.get_text(" "))
        m_opt = re.match(r"^\s*([A-F])\s*[.)]\s*(.*)", label_txt, re.I)
        if m_opt:
            letter = m_opt.group(1).upper()
            text = re.sub(r"\s*Most voted\s*$", "", m_opt.group(2), flags=re.I).strip()
            options[letter] = text
        else:
            # Fallback using prose inside label
            letter_el = label.select_one("span")
            text_el = label.select_one(".prose")
            if letter_el and text_el:
                letter = _clean(letter_el.get_text()).upper()
                if re.match(r"^[A-F]$", letter):
                    options[letter] = _clean(text_el.get_text(" "))

    result["options"] = options

    # ── Correct Answer, Explanation & Vote Counts ─────────────────────
    correct_ans = ""
    explanation = ""
    vote_counts: Dict[str, str] = {}
    most_voted = ""

    details = sec.select_one("details")
    if details:
        details_txt = _clean(details.get_text(" "))
        m_ans = re.search(r"Correct answer:\s*([A-F]+)", details_txt, re.I)
        if m_ans:
            correct_ans = m_ans.group(1).upper()

        exp_div = details.select_one(".prose")
        if exp_div:
            explanation = _clean(exp_div.get_text(" "))

        grid = details.select_one(".grid")
        if grid:
            items = grid.find_all("p")
            current_letter = None
            for p in items:
                p_txt = _clean(p.get_text(" "))
                letter_match = re.search(r"^\s*([A-F])(?:\s+Suggested)?$", p_txt, re.I)
                if letter_match:
                    current_letter = letter_match.group(1).upper()
                elif "%" in p_txt and current_letter:
                    vote_counts[current_letter] = p_txt

    result["correct_answer"] = correct_ans
    result["explanation"] = explanation
    result["vote_counts"] = vote_counts

    if vote_counts:
        try:
            most_voted = max(vote_counts, key=lambda k: float(vote_counts[k].replace("%", "")))
        except ValueError:
            most_voted = list(vote_counts.keys())[0]

    result["most_voted"] = most_voted

    if most_voted and most_voted in options:
        result["community_answer"] = f"{most_voted}. {options[most_voted]}"
    elif correct_ans and correct_ans in options:
        result["community_answer"] = f"{correct_ans}. {options[correct_ans]}"
    elif most_voted:
        result["community_answer"] = most_voted
    elif correct_ans:
        result["community_answer"] = correct_ans
    else:
        result["community_answer"] = "Not available"

    # ── Discussion comments ───────────────────────────────────────────
    comments: List[str] = []
    if q_id:
        comments_url = f"{BASE_URL}/api/questions/{q_id}/comments"
        try:
            if fetcher:
                raw_json = fetcher.fetch_html(comments_url)
                c_json = json.loads(raw_json)
            else:
                import requests
                res = requests.get(comments_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
                c_json = res.json() if res.status_code == 200 else {}

            for c in c_json.get("comments", []):
                c_body = _clean(c.get("body", ""))
                user = _clean(c.get("userName", ""))
                upvotes = c.get("upvotes", 0)
                if c_body:
                    comment_str = f"{user} ({upvotes} upvotes): {c_body}"
                    comments.append(comment_str)
                    for r in c.get("replies", []):
                        r_body = _clean(r.get("body", ""))
                        r_user = _clean(r.get("userName", ""))
                        if r_body:
                            comments.append(f"  ↳ {r_user}: {r_body}")
        except Exception:
            pass

    result["discussion"] = comments[:15]
    return result
