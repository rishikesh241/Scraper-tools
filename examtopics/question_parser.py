import re
from html import unescape
from typing import Dict, List, Optional

from bs4 import BeautifulSoup


def _clean(text: str) -> str:
    if not text:
        return ""
    cleaned = (
        text.replace("\xa0", " ")
        .replace("ג€", '"')
        .replace("`˜", "'")
        .replace("ֳ—", "×")
    )
    cleaned = re.sub(r'"instances"\s+\[\[', '"instances": [[', cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def _parse_inline_options(opts_blob: str) -> Dict[str, str]:
    """
    Parse inline options 'A. ... B. ... C. ... D. ...' strictly in sequential
    letter order so internal phrases like 'feature A.' never split options.
    """
    options: Dict[str, str] = {}
    letters = ["A", "B", "C", "D", "E", "F"]
    positions = []
    search_start = 0

    for idx, letter in enumerate(letters):
        if idx == 0:
            pat = re.compile(rf"(?:^|\s)({letter})\.\s+")
        else:
            pat = re.compile(rf"(?:(?<=[.?!\)\]\"'])\s+|\n\s*)({letter})\.\s+")
        m = pat.search(opts_blob, search_start)
        if not m and idx >= 1:
            pat_fallback = re.compile(rf"\s+({letter})\.\s+")
            m = pat_fallback.search(opts_blob, search_start)
        if m:
            positions.append((letter, m.start(1), m.end()))
            search_start = m.end()
        else:
            break

    for i, (letter, start_pos, content_start) in enumerate(positions):
        content_end = positions[i + 1][1] if i + 1 < len(positions) else len(opts_blob)
        options[letter] = _clean(opts_blob[content_start:content_end])

    return options


def parse_question_page(html: str, url: str = "") -> Dict:
    """
    Returns a dict:
    {
        "url": str,
        "question_no": str,          # e.g. "Topic 1 / Question 23"
        "question": str,             # question text only, options stripped out
        "options": {"A": "...", "B": "...", ...},
        "is_multi": bool,            # True if multi-select (Choose two / three)
        "most_voted": str,           # e.g. "B" or "AD"
        "vote_counts": {"A": 5, "B": 12, ...},
        "community_answer": str,     # most_voted letter(s) + text
        "discussion": [str, ...],    # list of comment strings
    }
    """
    soup = BeautifulSoup(html, "html.parser")
    result: Dict = {"url": url}

    # ── Question number ──────────────────────────────────────────────
    q_label = soup.select_one(".question-title-topic-details, .question-number, h1")
    result["question_no"] = _clean(q_label.get_text()) if q_label else ""

    # ── Question body ─────────────────────────────────────────────────
    q_body = (
        soup.select_one(".question-body")
        or soup.select_one(".card-text p")
        or soup.select_one(".question-text")
    )
    if q_body:
        q_body_copy = BeautifulSoup(str(q_body), "html.parser")
        for junk in q_body_copy.select(
            "li.multi-choice-item, ul, ol, .multi-choice-letter, "
            ".answer, .options, .vote-button, .answer-vote-button"
        ):
            junk.decompose()

        for img in q_body_copy.select("img"):
            src = img.get("src") or ""
            if src:
                img_tag = src.lstrip("/")
                img.replace_with(f" [{img_tag}] ")

        question_text = _clean(q_body_copy.get_text(" "))
        question_text = re.sub(r"\s*Show Suggested Answer\s*$", "", question_text, flags=re.I).strip()
        result["question"] = question_text
    else:
        result["question"] = ""

    # ── Options ───────────────────────────────────────────────────────
    options: Dict[str, str] = {}
    # Strategy 1: li.multi-choice-item
    for li in soup.select("li.multi-choice-item"):
        letter_el = li.select_one(".multi-choice-letter, strong")
        if letter_el:
            letter = _clean(letter_el.get_text()).strip(".")
            letter_el.decompose()
            text = _clean(li.get_text(" "))
            options[letter] = text

    # Strategy 2: fallback — lines starting with A. B. C. D. inside question card
    if not options:
        card = soup.select_one(".question-card, .card")
        if card:
            raw = card.get_text("\n")
            for line in raw.splitlines():
                m = re.match(r"^\s*([A-F])\s*[.)]\s*(.+)", line)
                if m:
                    options[m.group(1)] = _clean(m.group(2))

    # Strategy 3: fallback — sequential inline "A. ... B. ... C. ... D. ..." inside question text
    if not options and result["question"]:
        q_text = result["question"]
        m_inline = re.search(r"(?:^|\s)A\.\s+.+?\s+B\.\s+.+?\s+C\.\s+.+?\s+D\.\s+.+$", q_text)
        if m_inline:
            split_idx = m_inline.start()
            opts_blob = q_text[split_idx:].strip()
            parsed_inline = _parse_inline_options(opts_blob)
            if len(parsed_inline) >= 4:
                result["question"] = q_text[:split_idx].strip()
                options = parsed_inline

    result["options"] = options

    # Detect multi-select requirements (e.g. "(Choose two.)" or "(Choose three.)")
    q_lower = result["question"].lower()
    num_choices = 1
    if re.search(r"choose\s+(?:three|3)|select\s+(?:three|3)", q_lower):
        num_choices = 3
    elif re.search(r"choose\s+(?:two|2)|select\s+(?:two|2)", q_lower) or len(options) >= 5:
        if "choose" in q_lower or "two" in q_lower or "2" in q_lower:
            num_choices = 2
    is_multi = num_choices > 1
    result["is_multi"] = is_multi

    # ── Votes ─────────────────────────────────────────────────────────
    vote_counts: Dict[str, int] = {}
    most_voted = ""

    for btn in soup.select(".vote-button, .answer-vote-button"):
        letter_el = btn.select_one(".vote-letter, .answer-letter")
        count_el  = btn.select_one(".vote-count, .answer-votes")
        if letter_el:
            letter = _clean(letter_el.get_text())
            count  = int(re.sub(r"\D", "", count_el.get_text() or "0") or 0) if count_el else 0
            vote_counts[letter] = count

    badge = soup.select_one(".most-voted-answer, .community-vote-result")
    if badge:
        m = re.search(r"\b([A-F]{1,3})\b", badge.get_text().strip())
        if m:
            most_voted = "".join(sorted(dict.fromkeys(m.group(1))))

    # ── Discussion comments ───────────────────────────────────────────
    comments: List[str] = []
    for comment in soup.select(".comment-body, .discussion-comment, .card-comment"):
        text = _clean(comment.get_text(" "))
        if text and len(text) > 10:
            comments.append(text)
    result["discussion"] = comments[:10]

    # ── Derive vote_counts from "Selected Answer: X" in discussion if empty ────
    if not vote_counts and comments:
        tally: Dict[str, int] = {}
        for c in comments:
            m = re.search(r"Selected Answer:\s*([A-F,\s]+)", c, re.I)
            if m:
                letters_found = re.findall(r"[A-F]", m.group(1).upper())
                for letter in letters_found[:num_choices]:
                    tally[letter] = tally.get(letter, 0) + 1
        if tally:
            vote_counts = tally

    # ── Determine most_voted (supporting multi-select) ────────────────
    if vote_counts:
        sorted_votes = sorted(vote_counts.items(), key=lambda kv: (-kv[1], kv[0]))
        if is_multi and len(sorted_votes) >= num_choices:
            top_letters = sorted(k for k, _ in sorted_votes[:num_choices])
            most_voted = "".join(top_letters)
        elif not most_voted:
            most_voted = sorted_votes[0][0]

    result["vote_counts"] = vote_counts
    result["most_voted"] = most_voted
    if most_voted:
        ans_lines = []
        for ch in most_voted:
            if ch in options:
                ans_lines.append(f"{ch}. {options[ch]}")
            else:
                ans_lines.append(ch)
        result["community_answer"] = "\n  ".join(ans_lines)
    else:
        result["community_answer"] = "Not available"

    return result
