# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

"Should I take X course? Is the course good? Is it worth it?"

This sort of information is passed down via word of mouth, student to student. However, if a student is new or not well connected, they're missing out on these insights. They also might not be aware of subreddits, chat groups, and other student built online resources.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Student built course survey | Google sheet of informal course survey results | https://docs.google.com/spreadsheets/d/1MFBGJbOXVjtThgj5b6K0rv9xdsC1M2GQ0pJVB-8YCeU/edit?gid=2042942971#gid=2042942971 |
| ~~2~~ | ~~OSU Requirements~~ | ~~Lists all required courses~~ | ~~https://catalog.oregonstate.edu/college-departments/engineering/school-electrical-engineering-computer-science/computer-science-applied-bs-hbs/#requirementstext~~ |
| ~~3~~ | ~~OSU CS Course Schedule~~ | ~~Lists every course and when it's offered in the coming year (I filtered out results prior to 2021)~~ | ~~https://ecampus.oregonstate.edu/soc/ecatalog/ecourselist.htm?termcode=all&subject=CS~~ |
| 4 | OSU subreddit | Thread showing a free alternative for CS290 | https://www.reddit.com/r/OSUOnlineCS/comments/1s2bsn9/everyone_should_be_taking_full_stack_open/ |
| 5 | OSU subreddit | Thread with class advice for new student | https://www.reddit.com/r/OSUOnlineCS/comments/1nscw8b/finally_accepted_winter_2026_start/ |
| 6 | OSU subreddit | Thread about CS 373 | https://www.reddit.com/r/OSUOnlineCS/comments/1lo19nj/cs_373_what_in_the_actual_f/ |
| 7 | OSU subreddit | Thread about CS 332 | https://www.reddit.com/r/OSUOnlineCS/comments/1mhx9ss/cs_332_intro_to_applied_ds/ |
| 8 | OSU subreddit | Thread about CS 499 | https://www.reddit.com/r/OSUOnlineCS/comments/1mxmr0k/cs_499_vertically_integrated_projects/ |
| 9 | OSU subreddit | Thread about what courses help you find a job | https://www.reddit.com/r/OSUOnlineCS/comments/1tlqxo9/what_classes_will_help_you_get_a_job/ |
| 10 | OSU subreddit | Thread about CS 332 and CS 432 | https://www.reddit.com/r/OSUOnlineCS/comments/1si34b9/cs332_intro_to_data_science_and_cs432_intro_to/ |
| 11 | OSU subreddit | Thread about CS 372 | https://www.reddit.com/r/OSUOnlineCS/comments/1qyz9qb/did_they_revamp_cs_372_introduction_to_computer/ |
| 12 | OSU subreddit | Thread about AI531, CS 370, CS 427, CS 464, CS 492, CS 493 | https://www.reddit.com/r/OSUOnlineCS/comments/1pdjhdf/ai531_agents_search_reasoning_cs370_into_to/ |
| 13 | OSU subreddit | Thread about CS 467 | https://old.reddit.com/r/OSUOnlineCS/comments/1m7cr4l/cs_467_thougts/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

1000 characters

**Overlap:**

100 characters

**Why these choices fit your documents:**

Some of the most valueable comments and reviews were quite long and when split into smaller chunks, hard to decipher which course they corresponded to. The larger chunk size was required to ingest the full reviews and which course it applied to. Minimal overlap did not seem to negatively impact the results as much as a smaller chunk size did, so I kept it small to maximize the amount of unique information in each chunk.

**Preprocessing steps:**
For CSVs, I prefixed every data value with its column header to give the LLM more context about the data's meaning. It also sanitized the data so commas and newlines wouldn't mess up data processing.

For the reddit threads, I downloaded the old.reddit.com thread page as HTML and extracted the text content. I also preserved comment context by prefixing each comment with what it was responding to, so the LLM could better understand the overall conversation.

I also had to create custom chunking logic for the student reviews to prevent chunks from happening mid-review or bundling separate course reviews together.

**Final chunk count:**
607 chunks

### Sample Chunks

```json
     {
    "chunk_id": "Course Reviews (Responses) - Form Responses 1__156",
    "source": "Course Reviews (Responses) - Form Responses 1",
    "chunk_index": 156,
    "text": "Timestamp 6/13/2023 1:19:06\nWhat Course Did You Take? CS 325 - Analysis of Algorithms\nHow hard was this class? 5\nHow much time did you spend on average (per week) for this class? 13-18 hours\nWhat tips would you give students taking this course? Focus on activities for the exam. Look up and prep with deriving recurrence formulas, P = NP proofs (lightly touch on), and graph algorithms (Prims, TSP, MST).\nWhen did you take this course? SP 2023",
    "char_length": 443
  }

  {
    "chunk_id": "Finally accepted! Winter 2026 start : OSUOnlineCS__2",
    "source": "Finally accepted! Winter 2026 start : OSUOnlineCS",
    "chunk_index": 2,
    "text": "[In reply to: \"Finally accepted! Winter 2026 start\"]\n\nI had my quarters all planned out my first quarter.\nAnd that plan changed every single quarter.\nSee how you feel about CS 161+225 and calibrate from there. 225 (discrete math) is one of the hardest and time consuming classes in the program. 271, 261, 374 also tend to be harder.\nThe advisors can usually tell you which classes are challenging. Also check out the course analytics/review links and discord in the side bar.\nMacs are great for cs.",
    "char_length": 498
  }

  {
    "chunk_id": "What Classes will help you get a Job ? : OSUOnlineCS__2",
    "source": "What Classes will help you get a Job ? : OSUOnlineCS",
    "chunk_index": 2,
    "text": "[In reply to: \"What Classes will help you get a Job ?\"]\n\nYour capstone.\n90% of the courses in this program are mediocre at best. Take what you get from them, do your own learning, and then bake that knowledge into a project.\nThen when the next course comes around bake the knowledge you get into the same project as before. Now you got a stew going.\nThen bring all of that cumulative knowledge from that project into a new project - your capstone.\nThis is the way.",
    "char_length": 464
  }

  {
    "chunk_id": "CS332 Intro to Data Science and CS432 Intro to Machine Learning - Good Classes, heavy heavy workload__5",
    "source": "CS332 Intro to Data Science and CS432 Intro to Machine Learning - Good Classes, heavy heavy workload",
    "chunk_index": 5,
    "text": "[In reply to: \"CS332 Intro to Data Science and CS432 Intro to Machine Learning - Good Classes, heavy heavy workload\"]\n\nThis was pretty much my experience as well. IMO neural networks was less work than the other 2 (and very interesting too). I’m fine with a big workload, but the problem was how lopsided it would be week to week. At least Dr. Gates opens the whole class up day 1 so you can work ahead if possible. I liked each class more than the previous one, didn’t care much for data science but LOVED neural networks",
    "char_length": 522
  }

  {
    "chunk_id": "CS 499 Vertically Integrated Projects : OSUOnlineCS__2",
    "source": "CS 499 Vertically Integrated Projects : OSUOnlineCS",
    "chunk_index": 2,
    "text": "[In reply to: \"CS 499 Vertically Integrated Projects\"]\n\nI can comment on this as I completed it. In my opinion it is a great alternative to the capstone requirement. It is a more flexible and longer term way to get some hands on skills. However, the competition is fierce as not everyone is selected. This is key, only a few people were allowed to do this and it involved showing that you can code well and have enough courses under your belt. What helped my application was the successful completion of CS 406 Projects. Day to day, for my section, a sub part of the larger team we built out modules for a web application. At the time, we had no database and nothing was reactified so we were all creating this stuff blind. The second term things were redactores into React so we didn't need to use a separate project to demo our progress and we had a database too. During my final time, I was reimplementing what I already did without the database to align with the database. Although I didn't finis",
    "char_length": 1000
  }
```

### Retrieval Test Results

Sources 2, 3, and 5 were directly relevant as it correctly found CS 261 reviews with tips for future students. The other 2 results mentioned data structures but didn't have direct advice.

```bash
======================================================================
Query: 'What advice do people have for cs 261 data structures?'
======================================================================

[1] score=0.3922  source=CS 467 - Thougts : OSUOnlineCS
    chunk_index=15
--------------------------------------------------
[In reply to: "Jesus. I just started the program and this doesn’t bode well. I’m already annoyed with having to take stupid classes like ENGR 310, which is a waste of my time and money. Data Structures better not have discussion posts."]

if you're taking ENGR 103 (not 310), then you aren't doing the post-bacc which requires CS467.  You'll instead be doing a Senior Design project which runs over 3 quarters instead of just 1.

[2] score=0.4167  source=Course Reviews (Responses) - Form Responses 1
    chunk_index=135
--------------------------------------------------
Timestamp 5/20/2023 19:32:41
What Course Did You Take? CS 261 - Data Structures
How hard was this class? 3
How much time did you spend on average (per week) for this class? 18+ hours
What tips would you give students taking this course? Learn how to get really good at using your debugger and start on the assignments early. Read the requirements carefully and take the time to plan and map out your approach before coding. It will help limit rework and debugging later on. Make sure you’re fully grasping the content from each module, especially the early ones as complexity ramps up and everything builds in itself.
When did you take this course? SP 2023

[3] score=0.4398  source=CS 467 - Thougts : OSUOnlineCS
    chunk_index=14
--------------------------------------------------
[In reply to: "CS 467 - Thougts"]

Jesus. I just started the program and this doesn’t bode well. I’m already annoyed with having to take stupid classes like ENGR 310, which is a waste of my time and money. Data Structures better not have discussion posts.

[4] score=0.4481  source=Course Reviews (Responses) - Form Responses 1
    chunk_index=217
--------------------------------------------------
Timestamp 8/21/2023 11:53:35
What Course Did You Take? CS 261 - Data Structures
How hard was this class? 2
How much time did you spend on average (per week) for this class? 6-12 hours
What tips would you give students taking this course? Not too hard at all. You go over the basic data structures and implement them from scratch starting with a static array to hashmaps. However, they provide starter code and the assignment document is very detailed and well written. Tests were fair and as long as you do the explorations you should be fine.
When did you take this course? SU 2024

[5] score=0.4538  source=Course Reviews (Responses) - Form Responses 1
    chunk_index=425
--------------------------------------------------
Timestamp 6/16/2025 12:46:08
What Course Did You Take? CS 261 - Data Structures
How hard was this class? 4
How much time did you spend on average (per week) for this class? 13-18 hours
What tips would you give students taking this course? Class is not easy, but definitely doable. Biggest advice is to start assignments early. Make sure to utilize your free days (not using them doesn't benefit you). There are two unproctored exams (midterm and final). Don't go too slow on the exams, otherwise you will run out of time. If you are struggling with the material, check out Abdul Bari on Youtube/Udemy. Supplementing 261 with his course can be very effective.
When did you take this course? Spring 2025
```

All five sources were from a reddit thread specifically discussing CS 432 and their evaluations of the course. Highly relevant and high value for the query.

```bash
======================================================================
Query: 'is cs 432 intro to machine learning worth it?'
======================================================================

[1] score=0.3235  source=CS332 Intro to Data Science and CS432 Intro to Machine Learning - Good Classes, heavy heavy workload
    chunk_index=4
--------------------------------------------------
[In reply to: "CS332 Intro to Data Science and CS432 Intro to Machine Learning - Good Classes, heavy heavyworkload"]

That sounds very frustrating. I do find that in the core classes I’ve taken so far, discussion posts are often just as intense as assignments so that doesn’t surprise me.
As for the comments about not wanting to use AI, I’m not a fan of it either but if you want to work in this field you are better off getting used to using it. It has becoming a requirement in more and more companies. I work for a company that is nowhere near “the cutting-edge” and very old fashioned in everything we doand even we are all expected to use it.

[2] score=0.3330  source=CS332 Intro to Data Science and CS432 Intro to Machine Learning - Good Classes, heavy heavy workload
    chunk_index=0
--------------------------------------------------
CS332 Intro to Data Science and CS432 Intro to Machine Learning - Good Classes, heavy heavy workload

[3] score=0.3379  source=CS332 Intro to Data Science and CS432 Intro to Machine Learning - Good Classes, heavy heavy workload
    chunk_index=15
--------------------------------------------------
[In reply to: "CS332 Intro to Data Science and CS432 Intro to Machine Learning - Good Classes, heavy heavyworkload"]

My experience was very different. I found the workload extremely lite compared to most other courses in mydegree. In fact, I would say that there is a lot of overlapping material that feels a bit redundant and nearly all of the code is handed to you. I still found a lot of enjoyment out of this series of classes, but there was a good amount of documentation. Still, it tool me very little time to breeze through the explorations, maybe an hour on the discussion post, and then the assignment that is due every other week is extremely manageable if paced.

[4] score=0.3699  source=CS332 Intro to Data Science and CS432 Intro to Machine Learning - Good Classes, heavy heavy workload
    chunk_index=5
--------------------------------------------------
[In reply to: "CS332 Intro to Data Science and CS432 Intro to Machine Learning - Good Classes, heavy heavyworkload"]

This was pretty much my experience as well. IMO neural networks was less work than the other 2 (and very interesting too). I’m fine with a big workload, but the problem was how lopsided it would be week to week. At least Dr. Gates opens the whole class up day 1 so you can work ahead if possible. I liked each class morethan the previous one, didn’t care much for data science but LOVED neural networks

[5] score=0.3882  source=CS332 Intro to Data Science and CS432 Intro to Machine Learning - Good Classes, heavy heavy workload
    chunk_index=10
--------------------------------------------------
[In reply to: "CS332 Intro to Data Science and CS432 Intro to Machine Learning - Good Classes, heavy heavyworkload"]

I enjoyed all the classes so far.
Yes, 332 was a lot of documenting/writing but I understood the why. I believe the Professor was trying to get students to understand the “why” behind data science, because it’s not just about cleaning data and running models. The hard part is telling the story, choosing the best model and interpreting the results, thenhow to improve. People in this field typically have doctorate level degrees which means years of studying,researching and understanding.
ML was much lighter and DL has long explorations but that makes sense because the subject is more complex.
I appreciated Dr. Gates’s way of presenting the information. To me, it gave a great overview and examples/break down topics that can be extremely complex that takes people years to study and understand. She may link her site, but it’s because her site has all the same information
```

```bash
======================================================================
Query: 'how hard is cs 493 cloud application development?'
======================================================================

[1] score=0.3854  source=Course Reviews (Responses) - Form Responses 1
    chunk_index=450
--------------------------------------------------
Timestamp 12/10/2025 11:06:07
What Course Did You Take? CS 493 - Cloud Application Development
How hard was this class? 2
How much time did you spend on average (per week) for this class? 6-12 hours
What tips would you give students taking this course? Start assignments early, especially with the last project. Google and the docs are your best friends. Amazing if you want to be a full stack/backend cloud application developer. Very relevant to my job and very helpful to have for any cloud capstone projects. No APIdocumentation writing and minimal Postman test writing mentioned in previous reviews. Maybe the course hasbeen modified since then.
When did you take this course? FA 2025

[2] score=0.4024  source=Course Reviews (Responses) - Form Responses 1
    chunk_index=194
--------------------------------------------------
Timestamp 6/20/2023 16:28:53
What Course Did You Take? CS 493 - Cloud Application Development
How hard was this class? 2
How much time did you spend on average (per week) for this class? 6-12 hours
What tips would you give students taking this course? Give yourself plenty of time to complete the assignments, but if you are good at following instructions and utilizing external resources to research topics, it's an easy A.
When did you take this course? SP2023

[3] score=0.4762  source=AI531 Agents, Search, Reasoning; CS370 Into to Security; CS427 Cryptography; CS464 Open Source; CS49
    chunk_index=6
--------------------------------------------------
[In reply to: "AI531 Agents, Search, Reasoning; CS370 Into to Security; CS427 Cryptography; CS464 Open Source; CS492/493 Mobile/Cloud Development"]

Looking back, cloud was a very useful course for my career.

[4] score=0.4833  source=CS 499 Vertically Integrated Projects : OSUOnlineCS
    chunk_index=0
--------------------------------------------------
CS 499 Vertically Integrated Projects

[5] score=0.5008  source=AI531 Agents, Search, Reasoning; CS370 Into to Security; CS427 Cryptography; CS464 Open Source; CS49
    chunk_index=7
--------------------------------------------------
[In reply to: "AI531 Agents, Search, Reasoning; CS370 Into to Security; CS427 Cryptography; CS464 Open Source; CS492/493 Mobile/Cloud Development"]

Mobile was a few small Android apps, primarily using Google's tutorials for me a few years back. I'm surprised you got dark arts before intro to security, since I did into before dark arts. Anyway, dark arts is a whole lot of BS, as you know. Intro was less of that, but you could totally be bitten by your program not decoding/cracking in time if you're the type to do everything last-minute. Cloud was a lot like mobile in that you're going to be friends with Google's tutorials. I found it hard to get used to the cloud console, but once it clicked, it got easier.
```

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

all-MiniLM-L6-v2 via sentence-transformers, as this is what we have access to for this project. It runs locally with no API key, no rate limits, and is free to use. 

**Production tradeoff reflection:**

For real users and if cost wasn't a constraint, the tradeoffs that would impact embedding model choices would mainly be balancing result accuracy vs. latency/speed. A more powerful embedding model that is better at grabbing the most relevant information might generate better responses. However if it is meaningfully slower, the user might lose patience and leave the tool, rendering the added accuracy useless. 

Due to the content sources of this use case being relatively short and independent, I don't expect context length being a major limiting factor that would impact the model choice.

Due to the audience of this tool (students attending or considering Oregon State University CS), features like multi-lingual support would also likely not be a major factor in the model choice, since all classes are taught in English. Therefore fluency in English should be a safe assumption for our user base.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

```
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
```

**How source attribution is surfaced in the response:**

Sources were deterministically tracked and outputted in `generate.py`. It, separate from the LLM response, tracks the sources in the chunks and summarizes them into a compact format that is displayed with the LLM response. This way we can guarantee that the sources will be shown and are accurately displayed from the sources used by the LLM without worrying about LLM determinism/hallucinations.

---

## Query Interface

I used the Gradio skeleton code as a starter. The UI has a question input, an "ask" button to submit the query, and a place where answers and source chunks are reported, as well as a few example questions as buttons to quick ask to try it out. 

```
Your Question: "What is CS 499 vertically integrated projects?"

Answer: "CS 499 Vertically Integrated Projects is a course that can serve as an alternative to the capstone requirement, offering a more flexible and longer-term way to gain hands-on skills. It involves working on projects, potentially in teams, and requires a selection process where students must demonstrate their coding abilities and completion of relevant courses, such as CS 406 Projects. The course can be taken for 1-2 credits per quarter, and with 4 credits, it can substitute for CS 467 Capstone."

Sources:

- CS 332 Intro to Applied DS : OSUOnlineCS (1 passage retrieved)
- CS 499 Vertically Integrated Projects : OSUOnlineCS (3 passages retrieved)
- Did they revamp CS 372 (Introduction to Computer Networks)? : OSUOnlineCS (1 passage retrieved)

[1] CS 499 Vertically Integrated Projects : OSUOnlineCS — chunk 0 (score: 0.0670)

`CS 499 Vertically Integrated Projects`

[2] CS 499 Vertically Integrated Projects : OSUOnlineCS — chunk 2 (score: 0.4318)

`[In reply to: "CS 499 Vertically Integrated Projects"]

I can comment on this as I completed it. In my opinion it is a great alternative to the capstone requirement. It is a more flexible and longer term way to get some hands on skills. However, the competition is fierce as not everyone is selected. This is key, only a few people were allowed to do this and it involved showing that you can code well and have enough courses under your belt. What helped my application was the successful completion of CS 406 Projects. Day to day, for my section, a sub part of the larger team we built out modules for a web application. At the time, we had no database and nothing was reactified so we were all creating this stuff blind. The second term things were redactores into React so we didn't need to use a separate project to demo our progress and we had a database too. During my final time, I was reimplementing what I already did without the database to align with the database. Although I didn't finis`

[3] CS 499 Vertically Integrated Projects : OSUOnlineCS — chunk 1 (score: 0.5043)

`I recently learned about CS 499 VIP program which you can take 1-2 credits per quarter. If you have 4 credits, it can substitute for CS 467 Capstone. I haven't found any reviews about this VIP pilot program. Can someone who have taken it share feedbacks? What does a typical workload/assignment and grading  look like? Is it individual or team work? Do you enjoy the class? TIA`

[4] Did they revamp CS 372 (Introduction to Computer Networks)? : OSUOnlineCS — chunk 0 (score: 0.5331)

`Did they revamp CS 372 (Introduction to Computer Networks)?`

[5] CS 332 Intro to Applied DS : OSUOnlineCS — chunk 0 (score: 0.5410)

`CS 332 Intro to Applied DS`
```

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | "How many hours a week does cs 261 data structures take?" | "Based on student reviews, CS 261 takes around 10-15 hours a week. | "The time spent on CS 261 - Data Structures varies. Some students reported spending 6-12 hours per week, while others spent 13-18 hours per week. Sources: • Course Reviews (Responses) - Form Responses 1  (5 passages retrieved)" | Relevant | Accurate |
| 2 | "How hard is cs 493 cloud application development?" | "Based on student reviews, CS 493 is considered a easy course, with a difficulty rating of around 2 out of 5. | "CS 493 - Cloud Application Development is considered easy, with a difficulty rating of 2 out of 5. Sources: • AI531 Agents, Search, Reasoning; CS370 Into to Security; CS427 Cryptography; CS464 Open Source; CS49  (2 passages retrieved) • CS 499 Vertically Integrated Projects : OSUOnlineCS  (1 passage retrieved) • Course Reviews (Responses) - Form Responses 1  (2 passages retrieved)" | Relevant | Accurate |
| 3 | "Should I take CS 373 defense against the dark arts as one of my elective choices?" | "Student sentiment is negative based on reviews, so probably not." | "I don't have enough information in my sources to answer that. Sources: • AI531 Agents, Search, Reasoning; CS370 Into to Security; CS427 Cryptography; CS464 Open Source; CS49  (2 passages retrieved) • CS 332 Intro to Applied DS : OSUOnlineCS  (1 passage retrieved) • CS 373 WHAT IN THE ACTUAL F.... : OSUOnlineCS  (1 passage retrieved) • Course Reviews (Responses) - Form Responses 1  (1 passage retrieved)" | Off-target  | Inaccurate (even though one of the sources specifically centers around CS 373 complaints, the retrieval failed to pull that information. I think it's because there actually wasn't enough in the data source to flag to the LLM that it was relevant, as the thread never mentioned the course name, and CS 373 wasn't enough for the relevancy score.) |
| 4 | "As a new student, which courses should I take?" | "As a new student, you should consider taking CS 161 and CS 225." | "I don't have enough information in my sources to answer that. Sources: • CS 332 Intro to Applied DS : OSUOnlineCS  (1 passage retrieved) • Course Reviews (Responses) - Form Responses 1  (1 passage retrieved) • What Classes will help you get a Job ? : OSUOnlineCS  (3 passages retrieved)" | Off-target  | Inaccurate, even though one of the sources specifically centers around a new student asking for course advice. I think the retrieval failed for similar reasons to question 3, where there isn't enough similarity between the question asked and the content of the thread for the retriever to flag it as relevant. |
| 5 | "Is CS 332 intro to data sciences worth it?" | "Student sentiment is mixed based on reviews, so you might want to consider your interests and career goals." | "Opinions about CS 332 Intro to Data Science are mixed. Some students found the workload to be extremely light and enjoyed the class, despite feeling that there was a lot of overlapping material and redundant work. Others had a negative experience, feeling that the professor did not contribute much original content, and that the class was not well-structured. Additionally, some students found the assignments to be repetitive and felt that they were not getting a realistic view of what data science is like in a real-world setting. Therefore, whether CS 332 is worth it depends on individual preferences and expectations. Sources: • CS332 Intro to Data Science and CS432 Intro to Machine Learning - Good Classes, heavy heavy workload  (5 passages retrieved)" | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
As a new student, which courses should I take?

**What the system returned:**
I don't have enough information in my sources to answer that

**Root cause (tied to a specific pipeline stage):**
Retrieval failure.

Even though one of the sources specifically centers around a new student asking for course advice. I think the retrieval failed for similar reasons to question 3, where there isn't enough similarity between the question asked and the content of the thread for the retriever to flag it as relevant. It could have also been due to the other results from the top k retrieval all being poor fits, which could have caused the overall relevance score to be too low for the LLM to consider the retrieved chunks as useful context.

**What you would change to fix it:**
Perhaps I could at the embedding stage tried to have embedded which course or main topic (e.g. new student) each chunk was about as metadata so it was present during the retrieval stage, so that even if the chunk contents itself didn't refer to the topic, the chunk meta data would, to add resiliency. However, this would complicate the embedding portion of this pipeline.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
Since I knew what the step after the current in-progress step needed, I never had to re-do the engineering work once I reached the next step. I had a concrete goal that I knew would prepare me and move me towards the final goal. 

**One way your implementation diverged from the spec, and why:**
I did not realize how much pre-processing/customization/optimization of my chunking strategy I ended up having to do to the documents in order to preserve relevant context so the retrieval step could find 

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* An csv file and a html file that needed to be sanitized, as well as any specific issues or guidances I knew needed to be addressed (like commas inside of strings for the csv and html tags in the html files)
- *What it produced:* `csv_to_clean_text.py` and `html_to_clean_text.py`
- *What I changed or overrode:* I did have to iterate a few times as the first few passes revealed issues I had not identified earlier, such as quirks with how new reddit vs old reddit rendered html and realizing each cell of the csv needed to be tied back to its column title, otherwise all context was lost.

**Instance 2**

- *What I gave the AI:* `see the retrieval approach section of the planning.md. Generate the embedding and retrieval code. See the architecture diagram and implement the embedding step  (loading chunks from your ingestion pipeline, embedding with all-MiniLM-L6-v2 , storing in
ChromaDB with source metadata) and a retrieval function`
- *What it produced:* `embed_chunks.py` and `retrieve.py`
- *What I changed or overrode:* I experimented with changing the top k limit (increasing it to 7), but found that increasing the results tended to pollute the retrieved information pool with less relevant results.
