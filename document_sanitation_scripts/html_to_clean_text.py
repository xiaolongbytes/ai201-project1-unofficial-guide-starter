from pathlib import Path
import re
from html import unescape

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: beautifulsoup4. Install with `pip install beautifulsoup4`."
    )


def normalize_text(text: str) -> str:
    text = unescape(text or "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _tag_tokens(tag) -> set:
    """Return a set of lowercase tokens from a tag's class and id attributes only.

    Splits on any non-alphanumeric run so 'flex-nav-expanded' → {'flex','nav','expanded'}
    and 'comments-page' → {'comments','page'} (not matching the keyword 'comment').
    Only class and id are checked — checking href/src/style causes too many false positives.
    """
    classes = tag.attrs.get("class", [])
    if isinstance(classes, str):
        classes = [classes]
    tag_id = tag.attrs.get("id", "") or ""
    tokens: set = set()
    for cls in classes:
        tokens.update(t for t in re.split(r"[^a-z0-9]+", cls.lower()) if t)
    tokens.update(t for t in re.split(r"[^a-z0-9]+", tag_id.lower()) if t)
    return tokens


# Keywords matched as whole tokens against class/id (not substrings of all attrs).
_BOILERPLATE_KEYWORDS = {
    "cookie", "banner", "advert", "promo", "subscribe",
    "share", "social", "related", "breadcrumb",
    "footer", "header", "menu", "sidebar", "search",
    # "comment" and "nav" intentionally omitted:
    #   - "comment" is a literal class on every Reddit comment div.
    #   - "nav" appears inside utility CSS class names like "flex-nav-expanded".
    #   Both are handled by CSS selectors and role-attribute checks instead.
}


def remove_boilerplate(root) -> None:
    """Remove navigation, ads, and UI chrome from *root* in-place.

    *root* may be a BeautifulSoup object or a Tag (e.g. the content subtree).
    """
    selectors = [
        "script", "style", "nav", "footer", "header",
        "aside", "form", "noscript", "iframe", "svg",
        "button", "input", "textarea", "figure",
        ".cookie", ".cookies", ".banner", ".promo",
        ".advert", ".advertisement", ".ads", ".sidebar",
        ".related", ".share", ".social", ".subscribe",
        ".breadcrumb", ".comment", ".comments",
        ".header", ".footer", ".nav", ".menu",
    ]

    for selector in selectors:
        for tag in root.select(selector):
            tag.decompose()

    for tag in root.find_all(True):
        # Skip tags already removed as children of a decomposed ancestor.
        if tag.parent is None:
            continue

        # Token-based keyword matching on class/id only (no substring match on all attrs).
        tokens = _tag_tokens(tag)
        if tokens & _BOILERPLATE_KEYWORDS:
            tag.decompose()
            continue

        role = (tag.attrs.get("role", "") or "").lower()
        if role in {"navigation", "banner", "complementary", "contentinfo", "search", "form"}:
            tag.decompose()
            continue

        # Remove leaf elements whose sole visible text is a UI chrome label.
        if not tag.find(True):  # no child tags → leaf
            text = tag.get_text(separator=" ", strip=True).lower()
            if text in {
                "read more", "continue reading", "share", "share this",
                "comments", "view comments", "show more", "show less",
            }:
                tag.decompose()


def choose_content_root(soup):
    """Return the most specific semantic content container found in *soup*."""
    for selector in [
        "main",
        "article",
        "div[role=main]",
        "section[role=main]",
        "div.content",   # old Reddit and some CMS layouts
        "body",
    ]:
        element = soup.select_one(selector)
        if element:
            return element
    return soup


# ---------------------------------------------------------------------------
# Site-specific extractors
# ---------------------------------------------------------------------------

def _is_old_reddit(soup) -> bool:
    """Old Reddit pages (old.reddit.com) have a .commentarea div."""
    return bool(soup.select_one(".commentarea"))


def _is_new_reddit(soup) -> bool:
    """New Reddit pages use <shreddit-app> custom element."""
    return bool(soup.select_one("shreddit-app"))


def _is_osu_ecatalog(soup) -> bool:
    """OSU Ecampus schedule-of-classes pages use .coursedetailwrap divs."""
    return bool(soup.select_one("div.coursedetailwrap"))


# ------------------------------------------------------------------
# Regexes for OSU ecatalog class-notes cleanup
# ------------------------------------------------------------------
_PROCTORING_RE = re.compile(
    r"This course requires online proctored testing.*?"
    r"(?:ecampus\.oregonstate\.edu/services/proctoring/?\.?\s*)",
    re.DOTALL | re.IGNORECASE,
)
_INTERACT_RE = re.compile(
    r"[Ss]tudents in this section[s]? may be required to\s*interact.*",
    re.DOTALL | re.IGNORECASE,
)
_COMFORTABLE_RE = re.compile(
    r"This section is intended for students who are \w+\s*computers\.?",
    re.IGNORECASE,
)
_TEXTBOOKS_RE = re.compile(r"\[\s*Textbooks?\s*\]", re.IGNORECASE)
# Session date at the very start of a Class Notes value, e.g. "Jun 22-Aug 14Session 3"
_SESSION_DATE_RE = re.compile(
    r"^([A-Z][a-z]{2}\s+\d+[-–][A-Z][a-z]{2}\s+\d+)"  # "Jun 22-Aug 14"
    r"(?:\s*Session\s+\d+)?\s*",                         # optional "Session 3"
)
_TERM_MAP = {"Sp": "Spring", "Su": "Summer", "F": "Fall", "W": "Winter"}


def _expand_term(code: str) -> str:
    """'Sp26' → 'Spring 2026'"""
    m = re.match(r"^(Sp|Su|F|W)(\d{2})$", code)
    if m:
        return f"{_TERM_MAP[m.group(1)]} 20{m.group(2)}"
    return code


def _parse_section_details(rows: list) -> list[dict]:
    """Parse the detail rows that follow a section data row.

    Returns a list of section dicts, each with keys:
        term, crn, sec, credits, instructor, type, status, avail, cap,
        prereqs (str|None), proctored (bool), session (str|None), notes (str|None)
    """
    sections: list[dict] = []
    current: dict | None = None

    for row in rows:
        cells = row.find_all(["td", "th"])
        if not cells:
            continue
        # Header row — skip
        if cells[0].get_text(strip=True) == "Term":
            continue

        text = cells[0].get_text(separator=" ", strip=True)

        # 12-cell data row → new section
        if len(cells) == 12:
            current = {
                "term":       _expand_term(cells[0].get_text(strip=True)),
                "crn":        cells[1].get_text(strip=True),
                "sec":        cells[2].get_text(strip=True),
                "credits":    cells[3].get_text(strip=True),
                "instructor": cells[5].get_text(strip=True) or "Staff",
                "type":       cells[6].get_text(strip=True),
                "status":     cells[7].get_text(strip=True),
                "avail":      cells[9].get_text(strip=True),
                "cap":        cells[8].get_text(strip=True),
                "prereqs":    None,
                "proctored":  False,
                "session":    None,
                "notes":      None,
            }
            sections.append(current)
            continue

        if current is None:
            continue

        # Registration Restrictions row
        if text.startswith("Registration Restrictions"):
            prereq_m = re.search(
                r"Enforced Prereqs:\s*(.+?)(?:\n(?:Major|College|Level)|$)",
                cells[0].get_text(separator="\n", strip=True),
                re.DOTALL,
            )
            if prereq_m:
                current["prereqs"] = re.sub(r"\s+", " ", prereq_m.group(1)).strip()
            continue

        # Session row (standalone "Session: ..." row, not inside Class Notes)
        if text.startswith("Session:"):
            current["session"] = text[len("Session:"):].strip()
            continue

        # Syllabus row — discard
        if text.startswith("Syllabus:"):
            continue

        # Class Notes row
        if text.startswith("Class Notes:"):
            content = text[len("Class Notes:"):].strip()

            # Extract leading session date, e.g. "Jun 22-Aug 14Session 3"
            date_m = _SESSION_DATE_RE.match(content)
            if date_m:
                current["session"] = date_m.group(1).strip()
                content = content[date_m.end():]

            # Flag and strip proctoring boilerplate
            if _PROCTORING_RE.search(content):
                current["proctored"] = True
                content = _PROCTORING_RE.sub("", content)

            # Strip interaction boilerplate and textbook links
            content = _INTERACT_RE.sub("", content)
            content = _COMFORTABLE_RE.sub("", content)
            content = _TEXTBOOKS_RE.sub("", content)
            # Fix missing spaces from fused words caused by HTML line-break omissions
            content = re.sub(r"([a-z])([A-Z])", r"\1 \2", content)
            content = re.sub(r"\s+", " ", content).strip().strip(".")

            # Discard leftover content that is pure noise
            noise = {"see syllabus for details", ""}
            if content.lower() not in noise:
                current["notes"] = content
            continue

    return sections


def _extract_osu_ecatalog(soup) -> str:
    """Extract the OSU Ecampus schedule of classes into one chunk per course.

    Each chunk contains the course title followed by a compact inline listing
    of every section.  Boilerplate (proctoring paragraphs, syllabus lines,
    textbook links, column-header rows) is stripped; prerequisites and
    meaningful class notes are preserved.

    Output format per course:
        CS 161 – Introduction to Computer Science I (4 credits)

        Spring 2026 | CRN 53313 | Sec 400 | 4cr | Zhang, L. | Online | Open (66/122 seats)
          Prereqs: MTH 112* [C] or MTH 112Z* [C] or Placement Test MPT(33)
          Session: Jun 22–Aug 14

        Fall 2026 | CRN 11935 | Sec 400 | 4cr | Staff | Online | Open (69/75 seats)
          Requires proctored exams.
    """
    content_div = soup.select_one("div.content-658") or soup.select_one(".maincontent")
    if content_div is None:
        return soup.get_text(separator="\n", strip=True)

    chunks: list[str] = []
    current_title: str = ""

    children = [c for c in content_div.children if hasattr(c, "name") and c.name]

    for child in children:
        classes = child.attrs.get("class", [])
        tag = child.name

        # Course title paragraph — plain <p> whose text matches "CS NNN"
        if tag == "p" and "courseheading" not in classes:
            txt = child.get_text(strip=True)
            if re.match(r"^CS\s+\d", txt):
                current_title = txt
            continue

        # Skip textbook note divs and empty courseheading paragraphs
        if "textbooknote" in classes or "courseheading" in classes:
            continue

        # The section data lives here
        if "coursedetailwrap" in classes:
            if not current_title:
                continue

            table = child.select_one("table.coursedetail")
            if not table:
                continue

            sections = _parse_section_details(table.find_all("tr"))
            if not sections:
                continue

            lines: list[str] = [current_title, ""]

            for sec in sections:
                seats = (
                    f"Open ({sec['avail']}/{sec['cap']} seats)"
                    if sec["status"] == "Open"
                    else sec["status"]
                )
                header = (
                    f"{sec['term']} | CRN {sec['crn']} | Sec {sec['sec']} | "
                    f"{sec['credits']}cr | {sec['instructor']} | {sec['type']} | {seats}"
                )
                lines.append(header)

                if sec["session"]:
                    lines.append(f"  Session: {sec['session']}")
                if sec["prereqs"]:
                    lines.append(f"  Prereqs: {sec['prereqs']}")
                if sec["proctored"]:
                    lines.append("  Requires proctored exams.")
                if sec["notes"]:
                    lines.append(f"  Notes: {sec['notes']}")
                lines.append("")  # blank line between sections

            chunks.append("\n".join(lines).rstrip())
            current_title = ""  # reset; next course title will set it again

    return "\n\n---\n\n".join(chunks)


def _clean_md_text(md_tag) -> str:
    """Return normalized text from a .md tag."""
    text = md_tag.get_text(separator="\n", strip=True)
    text = unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _extract_old_reddit(soup) -> str:
    """Extract post title, body, and all comments from an old-Reddit page.

    Each comment is prefixed with its direct parent context so that the
    chunk fed to the retriever carries the conversational thread:
      - Top-level comments are prefixed with the post title.
      - Replies are prefixed with a truncated version of the parent comment.

    Format of each comment block:
        [In reply to: "<context>"]

        <comment text>
    """
    CONTEXT_MAX = 280  # chars to keep from parent text as context prefix

    title_tag = soup.select_one("a.title")
    title = title_tag.get_text(strip=True) if title_tag else ""

    parts: list[str] = []

    content_root = soup.select_one("div.content") or soup

    # Post body (OP selftext) — no reply prefix, it's the root content.
    post_md = content_root.select_one(".sitetable.linklisting .md")
    if title:
        parts.append(title)
    if post_md:
        post_text = _clean_md_text(post_md)
        if post_text:
            parts.append(post_text)

    def walk_comments(sitetable, parent_context: str) -> None:
        """Recursively walk a comment sitetable, prepending parent context."""
        for thing in sitetable.select(":scope > .thing.comment"):
            md = thing.select_one(":scope > .entry .md")
            if md is None:
                # Deleted/removed comment — still recurse in case children exist.
                child_sitetable = thing.select_one(":scope > .child > .sitetable")
                if child_sitetable:
                    walk_comments(child_sitetable, parent_context)
                continue

            comment_text = _clean_md_text(md)
            if not comment_text:
                continue

            # Truncate context for the prefix so it doesn't dominate the chunk.
            ctx = parent_context
            if len(ctx) > CONTEXT_MAX:
                ctx = ctx[:CONTEXT_MAX].rsplit(" ", 1)[0] + "…"

            block = f'[In reply to: "{ctx}"]\n\n{comment_text}'
            parts.append(block)

            # Recurse: children reply to this comment, so pass full text as context.
            child_sitetable = thing.select_one(":scope > .child > .sitetable")
            if child_sitetable:
                walk_comments(child_sitetable, comment_text)

    commentarea = content_root.select_one(".commentarea")
    if commentarea:
        top_sitetable = commentarea.select_one(":scope > .sitetable")
        if top_sitetable:
            walk_comments(top_sitetable, title)

    return "\n\n---\n\n".join(parts)


def _extract_new_reddit(soup) -> str:
    """Extract post content from a new-Reddit page.

    New Reddit renders comments client-side via JavaScript, so only the OP
    post is reliably present in a saved static HTML file.  We pull the
    <main> element and strip UI chrome tags before extracting text.
    """
    root = soup.select_one("main") or soup.select_one("shreddit-app") or soup.find("body")
    if root is None:
        return ""

    # Strip obvious chrome; leave shreddit-* custom elements so their
    # text content (title, post body) is preserved.
    for tag in root.find_all(["script", "style", "nav", "header", "aside",
                               "button", "svg", "iframe", "noscript", "input",
                               "textarea"]):
        tag.decompose()

    raw = root.get_text(separator="\n", strip=True)
    raw = unescape(raw)
    raw = re.sub(r"\r\n|\r", "\n", raw)

    # Deduplicate consecutive identical lines and drop very short noise lines
    # (single punctuation, lone bullets, etc.).
    seen_lines: list[str] = []
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line == seen_lines[-1] if seen_lines else False:
            continue
        seen_lines.append(line)

    return re.sub(r"\n{3,}", "\n\n", "\n".join(seen_lines)).strip()


# ---------------------------------------------------------------------------
# Generic extractor (non-Reddit pages)
# ---------------------------------------------------------------------------

def extract_clean_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Dispatch to site-specific extractors first.
    if _is_old_reddit(soup):
        return _extract_old_reddit(soup)
    if _is_new_reddit(soup):
        return _extract_new_reddit(soup)
    if _is_osu_ecatalog(soup):
        return _extract_osu_ecatalog(soup)

    # Generic path: boilerplate removal → content root selection → text.
    remove_boilerplate(soup)
    root = choose_content_root(soup)

    # Second pass: catch any remaining chrome tags inside the chosen root.
    for tag in root.find_all(True):
        if tag.parent is None:
            continue
        if tag.name in {
            "script", "style", "nav", "footer", "header", "aside",
            "form", "noscript", "iframe", "svg", "button", "input",
            "textarea", "figure",
        }:
            tag.decompose()

    raw_text = root.get_text(separator="\n", strip=True)
    raw_text = unescape(raw_text)
    raw_text = re.sub(r"\r\n|\r", "\n", raw_text)
    raw_text = re.sub(r"\n{3,}", "\n\n", raw_text)
    raw_text = re.sub(r"[ \t]+\n", "\n", raw_text)
    raw_text = re.sub(r"\n[ \t]+", "\n", raw_text)
    return raw_text.strip()


def sanitize_html_file(html_path: Path, output_path: Path) -> None:
    html = html_path.read_text(encoding="utf-8", errors="ignore")
    cleaned = extract_clean_text(html)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(cleaned + "\n", encoding="utf-8")


if __name__ == "__main__":
    import argparse

    workspace_root = Path(__file__).resolve().parent.parent
    input_dir = workspace_root / "raw_documentation_inputs"
    output_dir = workspace_root / "documents"

    parser = argparse.ArgumentParser(
        description="Convert each HTML file in raw_documentation_inputs into cleaned text files."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=input_dir,
        help="Directory containing HTML input files.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=output_dir,
        help="Directory to write cleaned text files.",
    )
    args = parser.parse_args()

    html_files = sorted(args.input_dir.glob("*.html"))
    if not html_files:
        raise SystemExit(f"No HTML files found in {args.input_dir}")

    for html_file in html_files:
        output_file = args.output_dir / f"{html_file.stem}.txt"
        sanitize_html_file(html_file, output_file)
        print(f"Wrote cleaned text file: {output_file}")
