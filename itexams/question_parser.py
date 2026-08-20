import re
from html import unescape
from typing import Dict, List, Optional

from bs4 import BeautifulSoup, Tag


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("\xa0", " ")).strip()


def parse_question_page(html: str, url: str = "") -> List[Dict]:
    """
    Parses all question blocks from an ITExams page and returns a list of question dicts:
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
            "vote_counts": {},
            "community_answer": str,
            "discussion": [],
        },
        ...
    ]
    """
    soup = BeautifulSoup(html, "html.parser")
    q_divs = soup.find_all("div", class_="examsPage__question")
    
    questions = []
    for q in q_divs:
        q_data = parse_single_question_div(q, url=url)
        if q_data and q_data.get("question"):
            questions.append(q_data)
            
    return questions


def parse_single_question_div(q: Tag, url: str = "") -> Dict:
    result: Dict = {"url": url}

    # ── Question Number ───────────────────────────────────────────────
    title_el = q.find(class_="title")
    result["question_no"] = _clean(title_el.get_text()) if title_el else ""

    # ── Question ID ───────────────────────────────────────────────────
    result["question_id"] = q.get("id", "")

    # ── Question Body, Options & Answer ───────────────────────────────
    body_el = q.find(class_="examsPage__question-body")
    q_text = ""
    options: Dict[str, str] = {}
    correct_ans = ""

    if body_el:
        ans_div = body_el.find(class_="examsPage__question-answers")
        if ans_div:
            for opt_span in ans_div.find_all(class_="examsPage__question-answer"):
                opt_txt = _clean(opt_span.get_text(" "))
                m = re.match(r"^\s*([A-F])\s*[.)]\s*(.*)", opt_txt, re.I)
                if m:
                    options[m.group(1).upper()] = m.group(2)

        correct_div = body_el.find(class_="examsPage__question-correct-answer")
        if correct_div:
            correct_ans = _clean(correct_div.get_text(" ")).replace("Answer:", "").strip()

        b_copy = BeautifulSoup(str(body_el), "html.parser")
        for junk in b_copy.select(
            ".examsPage__question-answers, .examsPage__question-correct-answer, .examsPage__question-nav"
        ):
            junk.decompose()
        q_text = _clean(b_copy.get_text(" "))

    result["question"] = q_text
    result["options"] = options
    result["correct_answer"] = correct_ans
    result["explanation"] = ""
    result["vote_counts"] = {}
    result["most_voted"] = correct_ans

    if correct_ans and correct_ans in options:
        result["community_answer"] = f"{correct_ans}. {options[correct_ans]}"
    elif correct_ans:
        result["community_answer"] = correct_ans
    else:
        result["community_answer"] = "Not available"

    result["discussion"] = []
    return result
