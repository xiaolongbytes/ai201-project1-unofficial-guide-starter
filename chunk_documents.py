"""chunk_documents.py

Reads every .txt file in documents/, splits it into overlapping character-based
chunks, and writes one JSON file per source into chunks/.

Tuning knobs (adjust here to change chunk behaviour globally):
"""

from pathlib import Path
import json
import re

# ---------------------------------------------------------------------------
# Constants — edit these to tune chunking
# ---------------------------------------------------------------------------
CHUNK_SIZE = 1000    # maximum characters per chunk
OVERLAP    = 100    # characters of overlap between consecutive chunks
# ---------------------------------------------------------------------------

DOCUMENTS_DIR = Path(__file__).resolve().parent / "documents"
CHUNKS_DIR    = Path(__file__).resolve().parent / "chunks"

# Separator inserted by html_to_clean_text.py to mark semantic boundaries
# (used in Reddit threads, ecatalog, etc.)
SECTION_SEP = re.compile(r"\n\n---\n\n")

# Filename stem of the course-reviews document (matched by substring)
COURSE_REVIEWS_STEM = "Course Reviews"


def sliding_window(text: str, chunk_size: int, overlap: int) -> list[tuple[int, int]]:
    """Return (start, end) character index pairs for a sliding-window split."""
    step = chunk_size - overlap
    spans = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        spans.append((start, end))
        if end == len(text):
            break
        start += step
    return spans


# ---------------------------------------------------------------------------
# Generic chunker (Reddit threads, ecatalog, requirements page, …)
# ---------------------------------------------------------------------------

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    """Split *text* into chunks, respecting `---` semantic boundaries.

    Sections shorter than chunk_size are emitted as a single chunk.
    Sections longer than chunk_size are split with a sliding window.
    """
    sections = SECTION_SEP.split(text.strip())
    chunks: list[str] = []

    for section in sections:
        section = section.strip()
        if not section:
            continue

        if len(section) <= chunk_size:
            chunks.append(section)
        else:
            for start, end in sliding_window(section, chunk_size, overlap):
                chunk = section[start:end].strip()
                if chunk:
                    chunks.append(chunk)

    return chunks


# ---------------------------------------------------------------------------
# Course-reviews custom chunker
# ---------------------------------------------------------------------------

def _split_review_block(block: str) -> list[str]:
    """Split one Timestamp block into one cleaned sub-chunk per course reviewed.

    Each student response can cover up to three courses.  This function emits
    one chunk per course, prefixed with the Timestamp line, with empty-answer
    field lines and "Did You Take a X Course?" metadata stripped out.

    A course section is only emitted when "What Course Did You Take?" has a
    non-empty answer (i.e. a real course was filled in).
    """
    lines = block.split("\n")
    timestamp_line = lines[0] if lines[0].startswith("Timestamp") else ""
    body = "\n".join(lines[1:])

    # Split into per-course sections on "What Course Did You Take? <SOMETHING>"
    # The \S ensures we only split where there's an actual course name.
    course_parts = re.split(r"\n(?=What Course Did You Take\? \S)", body)

    sub_chunks: list[str] = []
    for part in course_parts:
        part = part.strip()
        if not part or not part.startswith("What Course Did You Take?"):
            continue

        # Verify there's a real course name on the first line
        first_line = part.split("\n")[0]
        course_name = first_line.split("?", 1)[1].strip() if "?" in first_line else ""
        if not course_name:
            continue

        # Build the cleaned chunk: timestamp + course fields with actual answers
        clean_lines = ([timestamp_line] if timestamp_line else [])
        for line in part.split("\n"):
            line = line.strip()
            if not line:
                continue
            # Drop "Did You Take a Second/Third Course?" metadata lines
            if re.match(r"Did You Take a (Second|Third) Course", line):
                continue
            # Drop field labels where the answer is blank (line ends with "?")
            if line.endswith("?"):
                continue
            clean_lines.append(line)

        sub_chunk = "\n".join(clean_lines).strip()
        if sub_chunk:
            sub_chunks.append(sub_chunk)

    return sub_chunks


def chunk_course_reviews(
    text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP
) -> list[str]:
    """Chunk the course-reviews survey file.

    Strategy:
      1. Split on Timestamp boundaries → one block per student response.
      2. Within each block, split further into one sub-chunk per course reviewed.
         This keeps CS 261 data and CS 340 data in separate chunks.
      3. Sub-chunks that still exceed chunk_size (due to a very long tips field)
         get a sliding window applied, so they stay within the model's context.
    """
    response_blocks = re.split(r"\n(?=Timestamp )", text.strip())
    chunks: list[str] = []

    for block in response_blocks:
        block = block.strip()
        if not block:
            continue

        for sub_chunk in _split_review_block(block):
            if len(sub_chunk) <= chunk_size:
                chunks.append(sub_chunk)
            else:
                for start, end in sliding_window(sub_chunk, chunk_size, overlap):
                    c = sub_chunk[start:end].strip()
                    if c:
                        chunks.append(c)

    return chunks


# ---------------------------------------------------------------------------
# Per-file dispatcher
# ---------------------------------------------------------------------------

def process_file(txt_path: Path) -> list[dict]:
    """Chunk one document and return a list of chunk dicts."""
    text = txt_path.read_text(encoding="utf-8")
    source_name = txt_path.stem

    if COURSE_REVIEWS_STEM in txt_path.stem:
        raw_chunks = chunk_course_reviews(text)
    else:
        raw_chunks = chunk_text(text)

    records = []
    for i, chunk_content in enumerate(raw_chunks):
        records.append({
            "chunk_id":    f"{source_name}__{i}",
            "source":      source_name,
            "chunk_index": i,
            "text":        chunk_content,
            "char_length": len(chunk_content),
        })
    return records


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    CHUNKS_DIR.mkdir(exist_ok=True)

    txt_files = sorted(DOCUMENTS_DIR.glob("*.txt"))
    if not txt_files:
        raise SystemExit(f"No .txt files found in {DOCUMENTS_DIR}")

    total_chunks = 0
    summary_rows = []

    for txt_path in txt_files:
        records = process_file(txt_path)
        out_path = CHUNKS_DIR / f"{txt_path.stem}.json"
        out_path.write_text(
            json.dumps(records, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        count = len(records)
        total_chunks += count
        summary_rows.append({"source": txt_path.stem, "chunk_count": count})
        print(f"  {count:>4} chunks  ←  {txt_path.name}")

    summary = {
        "chunk_size":   CHUNK_SIZE,
        "overlap":      OVERLAP,
        "total_chunks": total_chunks,
        "sources":      summary_rows,
    }
    summary_path = CHUNKS_DIR / "_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"\nTotal chunks: {total_chunks}")
    print(f"Summary written to {summary_path}")
    print(f"Per-source JSON files written to {CHUNKS_DIR}/")


if __name__ == "__main__":
    main()
