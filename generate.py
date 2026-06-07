"""generate.py

Generation module for the OSU CS Unofficial Guide.

Wires together retrieval → prompt construction → Groq LLM → programmatic
source attribution.  Importable by app.py, or run directly for testing:

    python generate.py "What classes should I take first semester?"
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from retrieve import retrieve

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
LLM_MODEL   = "llama-3.3-70b-versatile"
MAX_TOKENS  = 1024
TEMPERATURE = 0.2   # low temperature → more faithful to context, less creative
# ---------------------------------------------------------------------------

load_dotenv()


def _get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY not found. Create a .env file in the project root "
            "with the line:  GROQ_API_KEY=your_key_here"
        )
    return Groq(api_key=api_key)


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a helpful mentor for Oregon State University's online Computer Science \
post-baccalaureate program (OSU CS Post-Bacc).

You will be given numbered context passages retrieved from student discussions, \
and course reviews. Your job is to answer the \
student's question using ONLY the information in those passages.

STRICT RULES — follow these exactly:
1. Base your answer exclusively on the provided context passages. \
   Do not use any outside knowledge or assumptions.
2. If the context contains enough information, give a clear and direct answer.
3. If the context does not contain sufficient information to answer, \
   respond with exactly: \
   "I don't have enough information in my sources to answer that."
4. Never invent course names, requirements, schedules, instructor names, \
   or student opinions that are not present in the context.
5. Do not list or number sources in your answer — \
   sources are displayed separately to the user.\
6. When given results for course difficulty out of 5, interpret 4-5 as "hard", 3 as "medium", and 1-2 as "easy".\
"""


def _build_user_message(query: str, chunks: list[dict]) -> str:
    context_blocks = []
    for i, chunk in enumerate(chunks, 1):
        context_blocks.append(f"[{i}]\n{chunk['text']}")
    context = "\n\n".join(context_blocks)
    return f"CONTEXT:\n{context}\n\nQUESTION: {query}"


# ---------------------------------------------------------------------------
# Source attribution  (programmatic — not left to the LLM)
# ---------------------------------------------------------------------------

def _build_source_list(chunks: list[dict]) -> list[str]:
    """Deduplicate and count chunks per source, return a sorted source list."""
    counts: dict[str, int] = {}
    for chunk in chunks:
        counts[chunk["source"]] = counts.get(chunk["source"], 0) + 1

    sources = []
    for source, count in sorted(counts.items()):
        label = f"{source}  ({count} passage{'s' if count > 1 else ''} retrieved)"
        sources.append(label)
    return sources


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def answer(query: str) -> dict:
    """Retrieve relevant chunks, call the LLM, and return a structured result.

    Returns a dict with:
        answer  — the LLM's grounded response string
        sources — list of source attribution strings (built from retrieved chunks,
                  not from LLM output — always present regardless of LLM behaviour)
        chunks  — the raw retrieved chunks (for debugging / display)
    """
    chunks = retrieve(query)

    user_message = _build_user_message(query, chunks)
    client = _get_client()

    completion = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
    )

    answer_text = completion.choices[0].message.content.strip()
    sources     = _build_source_list(chunks)

    return {
        "answer":  answer_text,
        "sources": sources,
        "chunks":  chunks,
    }


# ---------------------------------------------------------------------------
# CLI test runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate.py \"<your question>\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"\nQuery: {query}\n{'─' * 60}")

    result = answer(query)

    print("\nAnswer:")
    print(result["answer"])

    print("\nSources:")
    for s in result["sources"]:
        print(f"  • {s}")
