import json
from typing import Dict, List

from .matching import dedupe, extract_topic_question


# ── Link-only output (kept for backwards compat) ──────────────────────────────

def write_grouped_links_to_file(filename: str, links: List[str]):
    grouped_links: Dict[int, List[str]] = {}
    for link in sorted(dedupe(links), key=lambda item: (*extract_topic_question(item), item)):
        topic, _ = extract_topic_question(link)
        grouped_links.setdefault(topic, []).append(link)

    with open(filename, "w", encoding="utf-8") as file:
        for topic, topic_links in grouped_links.items():
            topic_label = "Unknown Topic" if topic == 10**9 else f"Topic {topic}"
            file.write(f"{topic_label}:\n")
            for link in topic_links:
                file.write(f" - {link}\n")
            print(f"{topic_label} links added to file.")


# ── Student-friendly output ───────────────────────────────────────────────────

_DIVIDER = "═" * 60


def _format_option_letters(letters: str, options: Dict[str, str]) -> str:
    if not letters:
        return "Not available"
    parts = []
    for ch in letters:
        if ch in options:
            parts.append(f"{ch}. {options[ch]}")
        else:
            parts.append(ch)
    return "\n  ".join(parts)


def format_question(q: Dict, index: int) -> str:
    """Format one parsed question dict into a readable text block."""
    lines = []
    lines.append(_DIVIDER)
    lines.append(f"QUESTION #{index}    {q.get('question_no', '')}")
    lines.append(_DIVIDER)
    lines.append("")
    lines.append(f"Question:\n{q.get('question', '(not found)')}")
    lines.append("")

    options = q.get("options", {})
    if options:
        lines.append("Options:")
        for letter, text in options.items():
            lines.append(f"  {letter}. {text}")
        lines.append("")

    vote_counts = q.get("vote_counts", {})
    if vote_counts:
        lines.append("Community Votes:")
        for letter, count in sorted(vote_counts.items()):
            lines.append(f"  {letter} → {count} vote(s)")
        lines.append("")

    most_voted = q.get("most_voted", "")
    community_answer = _format_option_letters(most_voted, options) if most_voted else q.get("community_answer", "")
    verified_answer = q.get("verified_answer", "")
    counter_note = q.get("counter_note", "")

    if counter_note or (verified_answer and verified_answer != most_voted):
        v_letters = verified_answer or most_voted
        v_full = _format_option_letters(v_letters, options)
        lines.append(f"Most Accepted / Verified Answer:\n  {v_full}")
        if most_voted and most_voted != v_letters:
            orig_one_line = "; ".join(
                f"{ch}. {options.get(ch, '')}".strip() for ch in most_voted
            )
            lines.append(f"  (Original Community Most Voted: {orig_one_line})")
        lines.append("")
        if counter_note:
            lines.append(f"Counter / Study Note:\n  {counter_note}")
            lines.append("")
    elif community_answer:
        lines.append(f"Most Accepted Answer:\n  {community_answer}")
        lines.append("")

    discussion = q.get("discussion", [])
    if discussion:
        lines.append("Discussion:")
        for i, comment in enumerate(discussion, 1):
            if len(comment) > 120:
                comment = comment[:117] + "..."
            lines.append(f"  {i}. {comment}")
        lines.append("")

    lines.append(f"URL: {q.get('url', '')}")
    lines.append("")

    return "\n".join(lines)


def write_questions_to_txt(filename: str, questions: List[Dict]):
    """Write all parsed questions to a student-friendly .txt file."""
    with open(filename, "w", encoding="utf-8") as f:
        for i, q in enumerate(questions, 1):
            f.write(format_question(q, i))
            f.write("\n")
    print(f"\n✓ Saved {len(questions)} questions → {filename}")


def write_questions_to_json(filename: str, questions: List[Dict]):
    """Write all parsed questions to a JSON file."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved {len(questions)} questions → {filename}")
