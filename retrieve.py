"""retrieve.py

Retrieval module for the OSU CS Unofficial Guide.

Importable:
    from retrieve import retrieve
    results = retrieve("Should I take CS 373?")

Or run directly to test queries interactively:
    python retrieve.py
    python retrieve.py "Should I take CS 373?"
"""

from pathlib import Path
from typing import Optional

import chromadb
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CHROMA_DIR  = Path(__file__).resolve().parent / "chroma_db"
COLLECTION  = "osu_cs_guide"
EMBED_MODEL = "all-MiniLM-L6-v2"
TOP_K       = 5     # default number of chunks to return per query
# ---------------------------------------------------------------------------

# Module-level singletons — initialised once on first call to retrieve()
_model:      Optional[SentenceTransformer] = None
_collection: Optional[chromadb.Collection] = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def _get_collection() -> chromadb.Collection:
    global _collection
    if _collection is None:
        if not CHROMA_DIR.exists():
            raise RuntimeError(
                f"ChromaDB not found at {CHROMA_DIR}. "
                "Run embed_chunks.py first."
            )
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _collection = client.get_collection(COLLECTION)
    return _collection


def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """Return the top-k most relevant chunks for *query*.

    Each returned dict contains:
        text        — the chunk text
        source      — source document name
        chunk_index — position of this chunk within its source
        score       — cosine distance (0.0 = identical, 1.0 = unrelated)
    """
    model      = _get_model()
    collection = _get_collection()

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    chunks: list[dict] = []
    for text, meta, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({
            "text":        text,
            "source":      meta["source"],
            "chunk_index": meta["chunk_index"],
            "score":       round(distance, 4),
        })

    return chunks


# ---------------------------------------------------------------------------
# Interactive test runner
# ---------------------------------------------------------------------------

def _print_results(query: str, results: list[dict]) -> None:
    print(f"\n{'='*70}")
    print(f"Query: {query!r}")
    print(f"{'='*70}")
    for i, r in enumerate(results, 1):
        print(f"\n[{i}] score={r['score']:.4f}  source={r['source']}")
        print(f"    chunk_index={r['chunk_index']}")
        print("-" * 50)
        # Print up to 400 chars of the chunk text for readability
        preview = r["text"][:]
        print(preview)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Query passed as a command-line argument
        q = " ".join(sys.argv[1:])
        _print_results(q, retrieve(q))
    else:
        # Interactive mode
        print(f"OSU CS Guide — Retrieval Test  (model={EMBED_MODEL}, top_k={TOP_K})")
        print("Type a question and press Enter. Ctrl-C to quit.\n")
        try:
            while True:
                q = input("Query> ").strip()
                if not q:
                    continue
                _print_results(q, retrieve(q))
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
