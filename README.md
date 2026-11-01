# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

Provenance Guard is a small web service a writing site could plug into. It estimates whether a piece of writing may have been produced with AI help. It returns a probabilistic guess, never proof, plus a plain-English label and a way for the writer to appeal.

The path a submission takes:

1. **Arrives at `POST /submit`** as JSON with `text` and `creator_id`.
2. **Validation** (`app.py::submit`): a missing or non-string `text` returns 400 `INVALID_TEXT`; empty text returns 400 `EMPTY_TEXT`; a missing `creator_id` returns 400 `INVALID_CREATOR`; over 10,000 words returns 413 `TEXT_TOO_LONG`. Bad input never reaches the model.
3. **A `content_id` is created** (UUID4). The appeal path depends on it.
4. **Signal one** (`detector.py::model_signal`): GPT-2, running locally, scores how predictable the text is, from 0 to 1 (higher means more likely AI).
5. **Signal two** (`stylometry.py::style_signal`): scores the shape of the text (sentence-length spread, vocabulary variety, expressive punctuation), from 0 to 1 (higher means more likely AI).
6. **Combine and label** (`scoring.py::combine_signals`, `scoring.py::score_to_label`): an equal-weight average becomes one score, which maps to one of three labels. Text under 25 words is always labeled "unsure," because it is too short to judge.
7. **Log and respond**: every decision is appended to `logs/audit.jsonl` via `audit.log_decision`, and the writer gets back the `content_id`, guess, confidence, label, and both signal scores.

If the writer disagrees, `POST /appeal` with the `content_id` and their `reasoning` records the appeal next to the original decision (it never overwrites it) and moves the item to `under_review`.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to GPT-2. The model reads the text one token at a time, scores how likely each next word was, and averages that into perplexity. Low perplexity (few surprises) maps to a higher AI score.

**Why that might differ between human and AI writing:** Language models generate text by choosing high-probability next words, so AI writing tends to be exactly what another model expects. Human writing has odd word choices, personal details, slang, and mistakes that surprise the model.

**What it can't see:** Who actually wrote the text. It only sees predictability. Plain, careful, or formal human writing (for example, from a non-native English speaker or in a formal report) is predictable and can be wrongly flagged as AI. That is the false positive this system most needs to avoid. In the other direction, AI text with typos, rare synonyms, or a "casual" rewrite becomes less predictable and can pass as human. On very short text, a single unusual word swings the score, so the result is unreliable. It also only reads the first ~400 tokens (about 300 words, `config.py::DETECTOR_MAX_TOKENS`), so anything after that is never scored.

### Signal two — the style signal

**What it measures:** The shape of the text, not its meaning. Three features: how much sentence lengths vary (spread), the ratio of unique words to total words (vocabulary variety), and how much punctuation is used per word. These are combined into one 0–1 score where higher means more likely AI.

**Why that might differ between human and AI writing:** AI writing tends to be uniform: sentences of similar length, safe repeated vocabulary, and steady, conventional punctuation. Human writing is burstier. It mixes short and long sentences, uses more varied or unusual words, and has irregular punctuation (dashes, ellipses, fragments).

**What it can't see:** Meaning or authorship. Any human who writes in an even, disciplined style (formal essays, technical writing, a careful non-native speaker) looks "AI-like" on these numbers. And AI text can be made to look human just by varying sentence length or adding punctuation, without changing a word of substance. It is also unreliable on short text: a two-line poem has too few sentences to measure spread at all. Two things I measured: vocabulary variety is nearly useless on short text (any 30-word passage has mostly unique words, so it always reads "human"), and a short, simple poem reads AI-like (the two-line test poem scored 0.76 on style).

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** An equal-weight average of the two signals. Because an average can never be more extreme than its inputs, the "high-confidence AI" label requires *both* signals to be high. One signal alone can't accuse anyone. I chose a strict AI threshold on purpose: I would rather let AI text through as "unsure" than accuse a real writer. Separately, any text under 25 words is always labeled "unsure."

**The numbers:** (all in `config.py`)
- `WEIGHT_MODEL_SIGNAL = 0.5`, `WEIGHT_STYLE_SIGNAL = 0.5`
- `HUMAN_THRESHOLD = 0.35`: scores of 0.35 and below get "high-confidence human"
- `AI_THRESHOLD = 0.85`: scores of 0.85 and above get "high-confidence AI"
- Anything in between gets "unsure"
- `confidence` in the response is `abs(combined - 0.5) * 2`, meaning how far the score is from a coin flip. It is **not** "probability of AI." It is set to 0.0 when the under-25-word rule applies.

**Where it lives:** `scoring.py::combine_signals` (the average) and `scoring.py::score_to_label` (the thresholds and label text). The under-25-word rule is in `app.py::submit`.

**Why 0.85 — the calibration that decided it** (`calibrate.py`, run before choosing):

| Sample | Model | Style | Combined |
|---|---|---|---|
| Clearly AI | 0.908 | 0.700 | 0.804 |
| Clearly human (casual) | 0.227 | 0.000 | 0.114 |
| **Formal human: my own grad school statement of purpose** | 0.893 | 0.636 | **0.765** |
| Lightly edited AI | 0.655 | 0.679 | 0.667 |

My own honest writing scored only 0.04 below clearly AI text, and *higher* than lightly edited AI. Both signals fail the same way on polished, formal prose, so combining them does not cancel the error. At the slides' default of 0.78, I would be one small difference away from being accused on my own application. A threshold of 0.85 keeps my writing in "unsure" with a real margin. The cost: ordinary AI text like sample 1 also lands in "unsure." Only very bland, repetitive AI text reached the AI label in my tests (0.93).

**A case where my two signals split, and what my rule does with it:** The test poem "To be or not to be. Alas a bird in a tree." scored **0.298 on the model signal** (the odd phrasing surprised GPT-2, which reads as human) but **0.76 on style** (two short sentences of equal length with no expressive punctuation, which reads as AI). The average is 0.53, so the result is "unsure." The under-25-word rule would force "unsure" anyway (12 words). I think that's the right outcome: two methods disagreeing is uncertainty, and the system should say so rather than pick a side.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | "Our automated check found that this writing reads like it was written by a person. No action is needed." |
| unsure | above 0.35 and below 0.85, **or any text under 25 words** | "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review." |
| high-confidence AI | 0.85 – 1.00 | "Our automated check thinks this writing was likely produced with help from AI. Automated checks can be wrong, and this is not a final decision. If you wrote this yourself, you can request a human review and tell us how you wrote it." |

Ranges come from `scoring.label_ranges()`. Boundaries are inclusive: 0.35 is "human" and 0.85 is "AI." All three labels were reached by real submissions (see the audit log): a casual message scored 0.11 (human), a two-line poem was labeled unsure, and a bland, repetitive AI paragraph scored 0.93 (AI).

**Why I worded the "unsure" one this way:** With my strict threshold, "unsure" is the label most writers will see, including honest formal writers like me (my own statement of purpose lands here). So it has to read as neutral and normal, not as a softer accusation. It says a *system* couldn't tell, not that the writer did anything. It explains in plain words why careful or short writing often lands there. It says outright that it is not a judgment about the writer, promises nothing happens because of it, and offers a human review instead of demanding one. It uses no numbers and no technical words, because the writer reading it has never heard of a threshold.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission** (a short poem, labeled "unsure" because it is under 25 words)

```bash
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d '{"text": "To be or not to be. Alas a bird in a tree.", "creator_id": "poet1"}'
```

```json
{
  "combined_score": 0.5291,
  "confidence": 0.0,
  "content_id": "01fd4fc3-4116-4bc4-bdc8-0c68888d70bb",
  "guess": "unsure",
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "model_score": 0.2981,
  "status": "decided",
  "style_score": 0.76
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" -d '{"content_id": "01fd4fc3-4116-4bc4-bdc8-0c68888d70bb", "reasoning": "I wrote this poem myself for a workshop. It is short on purpose."}'
```

```json
{
  "content_id": "01fd4fc3-4116-4bc4-bdc8-0c68888d70bb",
  "message": "Thanks. Your appeal has been recorded and this submission is now waiting for review by a person. The original result stays on file next to your explanation; nothing is changed automatically.",
  "status": "under_review"
}
```

An appeal with an unknown id returns 404 and changes nothing:

```json
{
  "error": "NOT_FOUND",
  "message": "We couldn't find a submission with that ID. Please check it and try again."
}
```

**What the log shows afterwards** (the original decision is untouched; the appeal is appended after it)

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.52905,
      "content_id": "01fd4fc3-4116-4bc4-bdc8-0c68888d70bb",
      "creator_id": "poet1",
      "guess": "unsure",
      "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
      "model_score": 0.2981,
      "status": "decided",
      "style_score": 0.76,
      "timestamp": "2026-11-01T21:50:31+00:00",
      "word_count": 12
    },
    {
      "content_id": "01fd4fc3-4116-4bc4-bdc8-0c68888d70bb",
      "creator_id": "poet1",
      "event": "appeal",
      "reasoning": "I wrote this poem myself for a workshop. It is short on purpose.",
      "status": "under_review",
      "timestamp": "2026-11-01T21:53:15+00:00"
    }
  ]
}
```
---

## How I Used AI

**Moment 1: checking whether my acceptance criteria were testable**

- *What I asked for:* I brought five proposed criteria to Claude and asked it to check whether a stranger could verify each one without asking me what I meant (the check the assignment recommends).
- *What came back:* It flagged that criterion 1 didn't say *which* 10 samples, that the score-spread criterion had no sample size, and, most importantly, that my 100-word minimum would refuse most poems on a writing site *and* would break the requirement that every submission gets one of the three labels.
- *What I changed:* I chose a 25-word minimum where short text gets the "unsure" label instead of being refused, required at least 3 of my 10 human samples to be formal or plain writing, and added sample sizes and a 404 rule for unknown appeal ids.

**Moment 2: choosing the AI threshold after calibration**

- *What I asked for:* After running my four calibration samples, I asked Claude to explain the trade-offs between a strict threshold (0.85), a tight one (0.80), and an agreement rule.
- *What came back:* It pointed out that my own statement of purpose scored 0.765, only 0.04 below clearly AI text, so no threshold cleanly separates them. A 0.80 threshold would pass my writing by a fragile margin, and an agreement rule would just be tuning to two data points. It recommended the strict option as the only one consistent with my 0-false-positive criterion.
- *What I changed:* I chose 0.85 (strict) instead of the slides' default of 0.78, and I wrote the cost into my README honestly: ordinary AI text now lands in "unsure."

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
