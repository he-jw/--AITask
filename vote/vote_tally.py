#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tally votes from a saved lists.apache.org thread HTML (modern rendering).

Output:
  - Prints a Markdown report to stdout.

Design goals:
  - Use stdlib only (no BeautifulSoup dependency)
  - Avoid counting votes inside quoted blocks (<blockquote class="email_quote">)
  - Avoid counting ballot option lines like "[ ] +1 ..."
"""

from __future__ import annotations

import html as html_lib
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional


@dataclass(frozen=True)
class VoteRecord:
    msg_id: str
    link: str
    author: str
    date_text: str
    date_key: tuple
    vote: str  # "+1" | "-1" | "0" | "abstain"
    excerpt: str


_RE_SPLIT_EMAIL = re.compile(r'<div class="email_wrapper"\s+id="email_')
_RE_AUTHOR = re.compile(r'<div class="chatty_author_name">\s*<b>(.*?)</b>', re.S)
_RE_AUTHOR_BLOCK = re.compile(r'<div class="chatty_author_name">(.*?)</div>', re.S)
_RE_PERMALINK = re.compile(
    r'<a\s+href="(https://lists\.apache\.org/thread/[^"]+)"[^>]*title="Permanent link to this email"',
    re.S,
)
_RE_BODY = re.compile(r'<pre class="chatty_body"[^>]*>(.*?)</pre>', re.S)
_RE_BLOCKQUOTE = re.compile(r"<blockquote class=\"email_quote\".*?</blockquote>", re.S)
_RE_BR = re.compile(r"<br\s*/?>|<br\s+[^>]*?>", re.I)
_RE_TAG = re.compile(r"<[^>]+>")

_RE_DATE_CN = re.compile(
    r"(?P<y>\d{4})年(?P<m>\d{1,2})月(?P<d>\d{1,2})日.*?(?P<h>\d{1,2}):(?P<mi>\d{2}):(?P<s>\d{2})"
)

_RE_VOTE_PLUS = re.compile(r"^\s*\+1\b", re.I)
_RE_VOTE_MINUS = re.compile(r"^\s*-1\b")
_RE_VOTE_ZERO = re.compile(r"^\s*[+-]?0\b")
_RE_VOTE_ABSTAIN = re.compile(r"^\s*(abstain|abstention)\b", re.I)


def _strip_tags_keep_newlines(html_fragment: str) -> str:
    # Remove quoted blocks entirely first to prevent counting quoted votes.
    html_fragment = _RE_BLOCKQUOTE.sub("", html_fragment)
    # Convert <br> to newline before stripping tags.
    html_fragment = _RE_BR.sub("\n", html_fragment)
    # Drop remaining tags.
    text = _RE_TAG.sub("", html_fragment)
    text = html_lib.unescape(text)
    # Normalize line endings.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text


def _parse_date_key(date_text: str) -> tuple:
    """
    Best-effort sortable key.
    If parsing fails, return (9999, 12, 31, 23, 59, 59) to keep it at the end.
    """
    m = _RE_DATE_CN.search(date_text)
    if not m:
        return (9999, 12, 31, 23, 59, 59)
    y = int(m.group("y"))
    mo = int(m.group("m"))
    d = int(m.group("d"))
    h = int(m.group("h"))
    mi = int(m.group("mi"))
    s = int(m.group("s"))
    return (y, mo, d, h, mi, s)


def _clean_author_block(author_block_html: str) -> tuple[str, str]:
    """
    Returns (author, date_text).
    """
    # Remove tags to text.
    text = _strip_tags_keep_newlines(author_block_html)
    text = " ".join(text.split())
    # Expected: "Name - 2026年1月6日星期二 GMT+8 04:34:47"
    if " - " in text:
        author, date_text = text.split(" - ", 1)
        author = author.strip()
        date_text = date_text.strip()
        # Some saved pages include duplicated translated author/date text, e.g.:
        # "Justin Mclean - <date> Justin Mclean - <date>"
        dup_marker = f"{author} - "
        dup_idx = date_text.find(dup_marker)
        if dup_idx != -1:
            date_text = date_text[:dup_idx].strip()
        return author, date_text
    return text.strip(), ""


def _extract_vote_from_text(text: str) -> Optional[tuple[str, str]]:
    """
    Returns (vote, excerpt_line) or None.
    """
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        # Skip typical quoted-text remnants (just in case)
        if line.startswith(">"):
            continue
        # Skip ballot option lines in the initial vote email, e.g. "[ ] +1 ..."
        if line.startswith("[") and "+1" in line:
            continue
        if line.startswith("[") and "-1" in line:
            continue
        if line.startswith("[") and "0" in line:
            continue

        # Common mailing list footer
        if line.startswith("To unsubscribe,"):
            continue
        if line.startswith("For additional commands,"):
            continue

        if _RE_VOTE_ABSTAIN.match(line) or ("弃权" in line):
            return ("abstain", line)
        if _RE_VOTE_PLUS.match(line):
            return ("+1", line)
        if _RE_VOTE_MINUS.match(line):
            return ("-1", line)
        # "+0" / "-0" / "0" treated as 0
        if _RE_VOTE_ZERO.match(line):
            return ("0", line)
    return None


def parse_votes_from_thread_html(html_text: str) -> list[VoteRecord]:
    parts = _RE_SPLIT_EMAIL.split(html_text)
    if len(parts) <= 1:
        return []

    records: list[VoteRecord] = []
    # parts[0] is preamble; each subsequent part begins with: "<msgid>" ...
    for part in parts[1:]:
        try:
            msg_id = part.split('"', 1)[0]
        except Exception:
            continue

        # author/date
        author = ""
        date_text = ""
        m_auth_block = _RE_AUTHOR_BLOCK.search(part)
        if m_auth_block:
            author, date_text = _clean_author_block(m_auth_block.group(1))
        else:
            m_auth = _RE_AUTHOR.search(part)
            if m_auth:
                author = _strip_tags_keep_newlines(m_auth.group(1)).strip()

        # permalink
        link = f"https://lists.apache.org/thread/{msg_id}"
        m_link = _RE_PERMALINK.search(part)
        if m_link:
            link = html_lib.unescape(m_link.group(1))

        # body
        m_body = _RE_BODY.search(part)
        if not m_body:
            continue
        body_html = m_body.group(1)
        body_text = _strip_tags_keep_newlines(body_html)

        vote_info = _extract_vote_from_text(body_text)
        if not vote_info:
            continue
        vote, excerpt = vote_info

        # Consider abstain as 0 for the user's "0 (including abstain)" requirement later.
        date_key = _parse_date_key(date_text)
        records.append(
            VoteRecord(
                msg_id=msg_id,
                link=link,
                author=author or "(unknown author)",
                date_text=date_text,
                date_key=date_key,
                vote=vote,
                excerpt=excerpt,
            )
        )

    return records


def _pick_last_vote_per_author(records: Iterable[VoteRecord]) -> tuple[list[VoteRecord], dict[str, list[VoteRecord]]]:
    by_author: dict[str, list[VoteRecord]] = {}
    for r in records:
        by_author.setdefault(r.author, []).append(r)

    final: list[VoteRecord] = []
    history: dict[str, list[VoteRecord]] = {}
    for author, rs in by_author.items():
        rs_sorted = sorted(rs, key=lambda x: x.date_key)
        history[author] = rs_sorted
        final.append(rs_sorted[-1])
    final_sorted = sorted(final, key=lambda x: x.date_key)
    return final_sorted, history


def render_markdown(records: list[VoteRecord]) -> str:
    final_votes, history = _pick_last_vote_per_author(records)

    plus = [r for r in final_votes if r.vote == "+1"]
    minus = [r for r in final_votes if r.vote == "-1"]
    abstain = [r for r in final_votes if r.vote == "abstain"]
    zero = [r for r in final_votes if r.vote == "0"]

    # User asked: 0 includes abstain
    zero_including_abstain = list(zero) + list(abstain)

    lines: list[str] = []
    lines.append("## 总览")
    lines.append(f"- **有效投票人数**：{len(final_votes)}")
    lines.append(f"- **+1**：{len(plus)}")
    lines.append(f"- **-1**：{len(minus)}")
    lines.append(f"- **0（含 abstain）**：{len(zero_including_abstain)}（其中 abstain：{len(abstain)}）")
    lines.append("")

    def render_group(title: str, rs: list[VoteRecord]) -> None:
        lines.append(f"## {title}")
        if not rs:
            lines.append("- （无）")
            lines.append("")
            return
        for r in rs:
            date_part = f"（{r.date_text}）" if r.date_text else ""
            lines.append(f"- **{r.author}** {date_part}：[{r.vote}]({r.link})")
            lines.append(f"  - 摘录：`{r.excerpt}`")
        lines.append("")

    render_group("+1", plus)
    render_group("0（含 abstain）", sorted(zero_including_abstain, key=lambda x: x.date_key))
    render_group("-1", minus)

    # Changed votes (same author, multiple vote emails)
    changed = {a: rs for a, rs in history.items() if len(rs) > 1}
    if changed:
        lines.append("## 改票/多次投票记录（以最后一票计入）")
        for author, rs in sorted(changed.items(), key=lambda kv: kv[0].lower()):
            lines.append(f"- **{author}**：")
            for r in rs:
                date_part = f"（{r.date_text}）" if r.date_text else ""
                lines.append(f"  - {date_part} [{r.vote}]({r.link}) ` {r.excerpt} `")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    import argparse
    import pathlib

    ap = argparse.ArgumentParser()
    ap.add_argument("html_path", help="Saved thread HTML file")
    args = ap.parse_args()

    html_path = pathlib.Path(args.html_path)
    html_text = html_path.read_text(encoding="utf-8", errors="replace")
    records = parse_votes_from_thread_html(html_text)
    md = render_markdown(records)
    print(md)


if __name__ == "__main__":
    main()

