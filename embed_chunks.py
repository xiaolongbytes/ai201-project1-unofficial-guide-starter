"""embed_chunks.py

Loads every chunk JSON from chunks/, embeds with all-MiniLM-L6-v2, and stores
the vectors + metadata in a persistent ChromaDB collection.

Run once (or with --reset to rebuild from scratch):
    python embed_chunks.py
    python embed_chunks.py --reset
"""

import argparse
import json
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
CHUNKS_DIR   = Path(__file__).resolve().parent / "chunks"
CHROMA_DIR   = Path(__file__).resolve().parent / "chroma_db"
COLLECTION   = "osu_cs_guide"
EMBED_MODEL  = "all-MiniLM-L6-v2"
BATCH_SIZE   = 64   # chunks per embedding + insertion batch
# ---------------------------------------------------------------------------


def load_chunks(chunks_dir: Path) -> list[dict]:
    """Load all chunk records from every per-source JSON file in chunks_dir."""
    records: list[dict] = []
    for json_path in sorted(chunks_dir.glob("*.json")):
        if json_path.name.startswith("_"):   # skip _summary.json
            continue
        batch = json.loads(json_path.read_text(encoding="utf-8"))
        records.extend(batch)
    return records


def build_collection(reset: bool = False) -> None:
    print(f"Loading chunks from {CHUNKS_DIR} …")
    chunks = load_chunks(CHUNKS_DIR)
    if not chunks:
        sys.exit("No chunks found. Run chunk_documents.py first.")
    print(f"  {len(chunks)} chunks loaded from {len(list(CHUNKS_DIR.glob('*.json'))) - 1} sources")

    # -- ChromaDB setup -------------------------------------------------------
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    if reset:
        try:
            client.delete_collection(COLLECTION)
            print(f"Deleted existing collection '{COLLECTION}'")
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"},   # cosine similarity for sentence embeddings
    )

    # Skip chunks already stored (allows incremental updates without --reset)
    existing_ids = set(collection.get(include=[])["ids"])
    new_chunks = [c for c in chunks if c["chunk_id"] not in existing_ids]
    if not new_chunks:
        print("All chunks already embedded. Use --reset to rebuild.")
        return
    print(f"  {len(new_chunks)} new chunks to embed ({len(existing_ids)} already stored)")

    # -- Embedding ------------------------------------------------------------
    print(f"\nLoading embedding model '{EMBED_MODEL}' …")
    model = SentenceTransformer(EMBED_MODEL)

    print(f"Embedding {len(new_chunks)} chunks in batches of {BATCH_SIZE} …")
    for batch_start in range(0, len(new_chunks), BATCH_SIZE):
        batch = new_chunks[batch_start : batch_start + BATCH_SIZE]

        texts      = [c["text"]        for c in batch]
        ids        = [c["chunk_id"]    for c in batch]
        metadatas  = [
            {
                "source":      c["source"],
                "chunk_index": c["chunk_index"],
                "char_length": c["char_length"],
            }
            for c in batch
        ]

        embeddings = model.encode(texts, show_progress_bar=False).tolist()

        collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        done = min(batch_start + BATCH_SIZE, len(new_chunks))
        print(f"  [{done}/{len(new_chunks)}] stored", end="\r")

    print(f"\nDone. Collection '{COLLECTION}' now contains {collection.count()} chunks.")
    print(f"ChromaDB persisted at: {CHROMA_DIR}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Embed chunks into ChromaDB.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete and rebuild the collection from scratch.",
    )
    args = parser.parse_args()
    build_collection(reset=args.reset)
