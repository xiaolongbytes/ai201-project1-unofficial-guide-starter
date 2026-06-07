"""app.py

Gradio web interface for the OSU CS Unofficial Guide.

Run with:
    python app.py
"""

import gradio as gr

from generate import answer

# ---------------------------------------------------------------------------
# Response formatter
# ---------------------------------------------------------------------------

def _format_response(result: dict) -> tuple[str, str]:
    """Return (answer_md, retrieved_chunks_md) as separate strings."""
    # --- Answer + source list ---
    sources_md = "\n".join(f"- {s}" for s in result["sources"])
    answer_md = (
        f"### Answer\n\n"
        f"{result['answer']}\n\n"
        f"---\n\n"
        f"### Sources\n\n"
        f"{sources_md}"
    )

    # --- Retrieved chunks (full text, no truncation) ---
    chunk_blocks = []
    for i, chunk in enumerate(result["chunks"], 1):
        block = (
            f"**[{i}] {chunk['source']}** — chunk {chunk['chunk_index']} "
            f"(score: {chunk['score']:.4f})\n\n"
            f"```\n{chunk['text']}\n```"
        )
        chunk_blocks.append(block)
    chunks_md = "\n\n---\n\n".join(chunk_blocks)

    return answer_md, chunks_md


# ---------------------------------------------------------------------------
# Gradio handler
# ---------------------------------------------------------------------------

def handle_query(query: str) -> tuple[str, str]:
    query = query.strip()
    if not query:
        return "Please enter a question.", ""
    try:
        result = answer(query)
        return _format_response(result)
    except RuntimeError as e:
        return f"⚠️ Configuration error: {e}", ""
    except Exception as e:
        return f"⚠️ Something went wrong: {e}", ""


# ---------------------------------------------------------------------------
# UI layout
# ---------------------------------------------------------------------------

EXAMPLE_QUESTIONS = [
    "how hard is cs 493 cloud application development?",
    "How many hours a week does cs 261 data structures take?",
    "What is cs 499 vertically integrated projects?",
    "Which classes will help me get a job?",
    "What advice do students have for cs 261 data structures?",
    "Is cs 432 Intro to Machine Learning worth it?",
]

with gr.Blocks(title="OSU CS Unofficial Guide") as demo:
    gr.Markdown(
        """
        # 📚 OSU CS Post-Bacc — Unofficial Guide
        Ask questions about courses, workload, and student experiences in the
        Oregon State University online Computer Science program.
        Answers are grounded in student reviews and Reddit discussions.
        Get the inside scoop.
        """
    )

    query_box = gr.Textbox(
        label="Your Question",
        placeholder="e.g. What classes should I take first semester?",
        lines=2,
    )
    submit_btn = gr.Button("Ask", variant="primary")
    answer_box = gr.Markdown(label="Response")
    chunks_box = gr.Markdown(label="Retrieved Chunks")

    # gr.Examples is the correct Gradio primitive for clickable example inputs.
    # Clicking a row populates query_box; it does not auto-submit.
    gr.Examples(
        examples=EXAMPLE_QUESTIONS,
        inputs=query_box,
        label="Example Questions",
    )

    submit_btn.click(fn=handle_query, inputs=query_box, outputs=[answer_box, chunks_box])
    query_box.submit(fn=handle_query, inputs=query_box, outputs=[answer_box, chunks_box])


if __name__ == "__main__":
    demo.queue()   # explicitly initialise asyncio queue locks (required on Python 3.14+)
    demo.launch()
