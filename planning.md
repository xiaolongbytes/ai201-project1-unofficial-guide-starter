# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

"Should I take X course? Is the course good? Is it worth it?"

This sort of information is passed down via word of mouth, student to student. However, if a student is new or not well connected, they're missing out on these insights. They also might not be aware of subreddits, chat groups, and other student built online resources.
It's also very difficult when planning to know if the course you're planning to take is offered in the term you are planning to take it.
Includes supplemental course opportunities outside of the curriculum.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Student built course survey | Google sheet of informal course survey results | https://docs.google.com/spreadsheets/d/1MFBGJbOXVjtThgj5b6K0rv9xdsC1M2GQ0pJVB-8YCeU/edit?gid=2042942971#gid=2042942971 |
| 2 | OSU Requirements | Lists all required courses | https://catalog.oregonstate.edu/college-departments/engineering/school-electrical-engineering-computer-science/computer-science-applied-bs-hbs/#requirementstext |
| 3 | OSU CS Course Schedule | Lists every course and when it's offered in the coming year | https://ecampus.oregonstate.edu/soc/ecatalog/ecourselist.htm?termcode=all&subject=CS |
| 4 | OSU subreddit | Thread showing a free alternative for CS290 | https://www.reddit.com/r/OSUOnlineCS/comments/1s2bsn9/everyone_should_be_taking_full_stack_open/ |
| 5 | OSU subreddit | Thread with class advice for new student | https://www.reddit.com/r/OSUOnlineCS/comments/1nscw8b/finally_accepted_winter_2026_start/ |
| 6 | OSU subreddit | Thread about CS 373 | https://www.reddit.com/r/OSUOnlineCS/comments/1lo19nj/cs_373_what_in_the_actual_f/ |
| 7 | OSU subreddit | Thread about CS 467 | https://www.reddit.com/r/OSUOnlineCS/comments/1m7cr4l/cs_467_thougts/ |
| 8 | OSU subreddit | Thread about CS 332 | https://www.reddit.com/r/OSUOnlineCS/comments/1mhx9ss/cs_332_intro_to_applied_ds/ |
| 9 | OSU subreddit | Thread about CS 499 | https://www.reddit.com/r/OSUOnlineCS/comments/1mxmr0k/cs_499_vertically_integrated_projects/ |
| 10 | OSU subreddit | Thread about what courses help you find a job | https://www.reddit.com/r/OSUOnlineCS/comments/1tlqxo9/what_classes_will_help_you_get_a_job/ |
| 11 | OSU subreddit | Thread about CS 332 and CS 432 | https://www.reddit.com/r/OSUOnlineCS/comments/1si34b9/cs332_intro_to_data_science_and_cs432_intro_to/ |
| 12 | OSU subreddit | Thread about CS 372 | https://www.reddit.com/r/OSUOnlineCS/comments/1qyz9qb/did_they_revamp_cs_372_introduction_to_computer/ |
| 13 | OSU subreddit | Thread about AI531, CS 370, CS 427, CS 464, CS 492, CS 493 | https://www.reddit.com/r/OSUOnlineCS/comments/1pdjhdf/ai531_agents_search_reasoning_cs370_into_to/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
