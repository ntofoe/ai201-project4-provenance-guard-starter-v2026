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
| "Clearly human" (casual) **(AI-written; see note)** | 0.227 | 0.000 | 0.114 |
| **Formal human: my own grad school statement of purpose** | 0.893 | 0.636 | **0.765** |
| Lightly edited AI | 0.655 | 0.679 | 0.667 |

*Correction (Unit 8): the casual "clearly human" sample was written by Claude in a casual style, not by a person. It shows the human label is reachable, but it is not evidence about real human writing. In Unit 8, criterion 2's human group uses only my own writing.*

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

**Unit 8, Moment 3: diagnosing the crash**

- *What I asked for:* After the attack run, I asked Claude why MF02 (a single character) returned a 500.
- *What came back:* Its first guess was that the detector malfunctioned. The traceback I pulled from the service showed something more specific: the detector raised `ValueError` *on purpose* for too-short text, and the real fault was that my route called it before checking length.
- *What I changed:* I wrote the diagnosis as a route-stage problem, not a detector bug, and moved the short-text check ahead of the signals as my one improvement.

**Unit 8, Moment 4: choosing the improvement**

- *What I asked for:* Before choosing between fixing the crash and reweighting the signals, I asked to see the per-signal numbers rather than take a recommendation.
- *What came back:* A weight sweep on my own data. The median gap stayed between 0.213 and 0.232 at every weight, and higher model weight pushed my own writing closer to being accused.
- *What I changed:* I chose input validation, and put criterion 2 in What's Still Broken as a signal-level limit.

Claude also wrote the helper scripts (`summarize_eval.py`, `appeal_test.py`, `calibrate.py`), the five AI samples in `scenarios.py`, and first drafts of the Unit 8 README sections. The ten human samples in `scenarios.py` are my own writing. Claude flagged that its earlier "clearly human" ramen sample was AI-written, which led to the correction above.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 100 per day, on `POST /submit` (`config.py::RATE_LIMIT_PER_MINUTE` and `RATE_LIMIT_PER_DAY`, applied by the `@limiter.limit` decorator on `app.py::submit`).

**Why those numbers and not others:** A real writer submits their own work a few times an hour, and maybe up to ten times in a burst while revising and resubmitting. 10 per minute leaves that comfortable. 100 per day is far more than any real writer needs. A script trying to map exactly where my 0.85 AI threshold sits needs hundreds or thousands of probes, so it hits the daily wall quickly. A lower per-minute limit (say 3) would block an honest writer fixing typos. A higher one (say 60) would let a script probe dozens of variations a minute.

**What a caller counts as:** The `creator_id` in the request body, falling back to the IP address only when there is no usable `creator_id` (`app.py::rate_limit_key`). The upside: one writer can't be locked out by someone else on the same network, like a shared household or campus Wi-Fi. **The weakness:** `creator_id` is whatever the caller types. A script that sends a new made-up `creator_id` on every request is never limited at all. That is exactly what the main attack file does (every row has its own `creator_id`), and it's why only the `flood_same_creator` rows were stopped. My limiter stops a careless flood, not a determined one. Real protection would need authenticated accounts, or a second limit per IP address on top of the per-creator one.

The limiter's counts are kept in memory (`config.py::RATE_LIMIT_STORAGE = "memory://"`), so restarting the service resets them.

**The run of status codes when I pushed past it:**

```
$ python run_attacks.py --flood 15
15 submissions as 'flood_tester' against http://127.0.0.1:5000

200 200 200 200 200 200 200 200 200 200 429 429 429 429 429

5 of 15 were rate limited.
Wrote results/flood_2026-11-04_1926.md
```

Rejected requests are logged. The 429 handler writes an entry, so a flood doesn't show up as silence:

```json
{
  "creator_id": "flood_tester",
  "event": "rejected",
  "limit": "10 per 1 minute",
  "reason": "rate_limited",
  "status": "rejected",
  "timestamp": "2026-11-05T00:26:19+00:00"
}
```

---

## Attack Run — Before

Full report: `results/attack_run_2026-11-04_1935_before.md` (produced by `run_attacks.py::main`). Audit log for the run: `results/audit_extract.json`.

**How I marked HELD or BROKE:** each attack names what it was going for. A false-positive attack is BROKE if human writing got the "high-confidence AI" label. A malformed attack is BROKE if the service crashed (5xx). An evasion or injection attack is BROKE only if AI text received the **"human"** label, because only that label tells a reader the text is human-written. Seven evasions ended "unsure," and I mark those HELD. That is **not** a detection success: under my strict 0.85 threshold, ordinary AI text lands in "unsure" with no evasion at all (my plain ChatGPT-style sample scored 0.804). By the attack set's own goal, avoiding the AI label, those seven succeeded. The stage is the label mapping, and it is the trade I chose on purpose in Unit 7.

**Result: 52 HELD, 4 BROKE.**

| ID | Family | Targeting | Status | Guess | Verdict |
|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | **human** | **BROKE** |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | **human** | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure | HELD |
| EV08 | evasion | signal one: text below the token window | 200 | unsure | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | unsure | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | unsure | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | unsure | HELD (closest call: combined 0.816) |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | **human** | **BROKE** |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | HELD (labels are fixed strings) |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | HELD (log stores no submitted text) |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | HELD |
| MF02 | malformed | text is a single character | **500** | — | **BROKE** |
| MF03 | malformed | text is control characters | 200 | unsure | HELD |
| MF04 | malformed | text is only punctuation | 200 | unsure | HELD |
| MF05 | malformed | text is a very long single word | 200 | unsure | HELD |
| MF06 | malformed | text is emoji only | 200 | unsure | HELD |
| MF07 | malformed | text is right-to-left script | 200 | unsure | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | — | HELD |
| RQ01 | malformed | no text field at all | 400 | — | HELD |
| RQ02 | malformed | no creator_id | 400 | — | HELD |
| RQ03 | malformed | text is a number | 400 | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | HELD |
| RQ05 | malformed | text is null | 400 | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | HELD |
| FL01_01 to FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 (x10) | unsure | HELD |
| FL01_11, FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 (x2) | — | HELD (limit hit at request 11) |

**Ten audit log entries from the run** (from `results/audit_extract.json`)

The three breaks that got the "human" label, the closest false-positive call, a careful non-native writer, the one AI catch, the log-injection attempt, garbage text that was scored anyway, and two rejections:

```json
[
  {"combined_score": 0.3235, "content_id": "7d9c990f-0cba-414c-8222-f2019f181218", "creator_id": "attacker_EV02", "guess": "human", "label": "Our automated check found that this writing reads like it was written by a person. No action is needed.", "model_score": 0.5943, "status": "decided", "style_score": 0.0527, "timestamp": "2026-11-05T00:35:50+00:00", "word_count": 93},
  {"combined_score": 0.26485, "content_id": "93d5107a-1303-4236-abe7-0b0704693e82", "creator_id": "attacker_EV05", "guess": "human", "label": "Our automated check found that this writing reads like it was written by a person. No action is needed.", "model_score": 0.3212, "status": "decided", "style_score": 0.2085, "timestamp": "2026-11-05T00:35:51+00:00", "word_count": 81},
  {"combined_score": 0.16885, "content_id": "02f91c45-fb43-4187-ba8d-30157903dc95", "creator_id": "attacker_PI02", "guess": "human", "label": "Our automated check found that this writing reads like it was written by a person. No action is needed.", "model_score": 0.2044, "status": "decided", "style_score": 0.1333, "timestamp": "2026-11-05T00:35:54+00:00", "word_count": 42},
  {"combined_score": 0.8164, "content_id": "ce669c3d-cd2b-427e-b3b2-a563b1f10f15", "creator_id": "attacker_FP05", "guess": "unsure", "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.", "model_score": 0.8005, "status": "decided", "style_score": 0.8323, "timestamp": "2026-11-05T00:35:53+00:00", "word_count": 70},
  {"combined_score": 0.68845, "content_id": "a3415e8e-d70f-4235-ae94-c80337aa2b5e", "creator_id": "attacker_FP03", "guess": "unsure", "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.", "model_score": 0.8051, "status": "decided", "style_score": 0.5718, "timestamp": "2026-11-05T00:35:53+00:00", "word_count": 83},
  {"combined_score": 0.8926499999999999, "content_id": "c115a420-55d6-4c5d-8349-1e65319874f0", "creator_id": "attacker_EV10", "guess": "ai", "label": "Our automated check thinks this writing was likely produced with help from AI. Automated checks can be wrong, and this is not a final decision. If you wrote this yourself, you can request a human review and tell us how you wrote it.", "model_score": 0.9792, "status": "decided", "style_score": 0.8061, "timestamp": "2026-11-05T00:35:52+00:00", "word_count": 78},
  {"combined_score": 0.38434999999999997, "content_id": "970d01a5-8e71-4cc2-8c97-804d29a3f330", "creator_id": "attacker_PI05", "guess": "unsure", "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.", "model_score": 0.6401, "status": "decided", "style_score": 0.1286, "timestamp": "2026-11-05T00:35:54+00:00", "word_count": 28},
  {"combined_score": 0.25, "content_id": "02fcac72-ae32-4bde-b26b-84dcfaf6e85e", "creator_id": "attacker_MF03", "guess": "unsure", "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.", "model_score": 0.0, "status": "decided", "style_score": 0.5, "timestamp": "2026-11-05T00:35:55+00:00", "word_count": 3},
  {"creator_id": "attacker_MF01", "event": "rejected", "http_status": 400, "reason": "EMPTY_TEXT", "status": "rejected", "timestamp": "2026-11-05T00:35:54+00:00"},
  {"creator_id": "attacker_flood", "event": "rejected", "limit": "10 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-05T00:35:57+00:00"}
]
```

What is **not** in the log is just as telling. MF02, the crash, left **no entry at all**: counting entries with `creator_id == "attacker_MF02"` returns **0**. The exception happened before `audit.log_decision` ran. Without the attack runner's own record, that attack would have been invisible.

**The single worst outcome:** **MF02.** A writer who submits something very short (a one-word title, a "thanks," a one-line poem) gets an HTTP 500 and, because the service runs in debug mode, a Werkzeug debugger page showing my stack trace. Worse, the crash happened before a `content_id` was created or anything was logged. So that writer has **no id to appeal with, and the system has no record they were ever there.** Every other failure in this run at least left an appealable, logged decision. This one left the writer with nothing.

---

## Run Log and Verdicts

Produced by `run_eval.py::main` (scenarios in `scenarios.py`). Criterion 4 was tested by `appeal_test.py` because it needs a submission and then an appeal against the returned id. Reports: `results/run_2026-11-04_2007_before.md`, `results/appeal_test_before.txt`. Combined scores and medians were recomputed from the report by `summarize_eval.py`.

All three trials of every criterion were identical. Neither signal is random, so that's expected. It means each verdict holds, rather than turning up once.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labeled "high-confidence AI" | 0 of 10 | 0/10 | 0/10 | 0/10 | **MET** |
| 2. Median combined score, AI minus human | ≥ 0.30 | 0.219 | 0.219 | 0.219 | **MISSED** |
| 3. Bad input gets the listed response, 5 of 5 per case | 4 of 4 cases | 3 of 4 | 3 of 4 | 3 of 4 | **MISSED** |
| 4. Appeals set `under_review` and are logged; unknown id → 404 | 5 of 5 | 5/5 | 5/5 | 5/5 | **MET** |
| 5. All three labels reached by real submissions | 3 of 3 | 3/3 | 3/3 | 3/3 | **MET** |

**How I decided each verdict:**
1. **MET.** All 10 of my pieces got "unsure" in every trial, so none was accused. The margin is thin, though: my two diversity-statement halves scored 0.774 and 0.769, and my statement of purpose 0.765, all within 0.09 of the 0.85 line. And none of my writing was ever labeled "human" either. The system protects me by never deciding about my writing at all.
2. **MISSED.** The AI median was 0.801 and the human median 0.582, a gap of 0.219, short of 0.30 in all three trials. The groups also **overlap**: the lowest AI text (0.734) scored below three of my human pieces. The human group was my own formal writing (samples 1–5), the hardest comparison, and that's stated here rather than hidden. The criterion didn't specify casual writing, so the verdict stands.
3. **MISSED.** Invalid, empty, and too-long bodies got 400, 400, and 413, five of five each, in every trial. Under-25-word text got the promised 200 with "unsure" in only **3 of 5**: `"a"` and `"Hello"` crashed. Any case below 5 of 5 is a miss, so the criterion is missed.
4. **MET.** 15 of 15 appeals across three trials returned `under_review` and appeared in the log, and the unknown id returned 404 every time.
5. **MET.** A casual message got "human" (0.114), ChatGPT-style text got "unsure" (0.804), and bland repetitive AI text got "ai" (0.932), in every trial. One honesty note: the "human" text here was written by Claude in a casual style. That's fine for *reachability*, which is what this criterion tests, but it is not evidence about human writing.

**Real output from one trial** (trial 1, `results/run_2026-11-04_2007_before.md`, produced by `run_eval.py::main` calling `app.py::submit`; long `label`/`error` strings shortened with "..."):

```json
{
  "criterion_1_my_own_writing (2 of 10)": [
    {"status": 200, "guess": "unsure", "confidence": 0.5295, "model_score": 0.8931, "style_score": 0.6364, "label": "Our automated check couldn't tell whether this was written b...", "sent": "During my undergraduate studies in Mathematics, I developed a solid fo"},
    {"status": 200, "guess": "unsure", "confidence": 0.2991, "model_score": 0.7442, "style_score": 0.5549, "label": "Our automated check couldn't tell whether this was written b...", "sent": "Advancing my Mathematics studies has been a big delight for me in rece"}
  ],
  "criterion_2_spread_ai (1 of 5)": [
    {"status": 200, "guess": "unsure", "confidence": 0.6083, "model_score": 0.9083, "style_score": 0.7, "label": "Our automated check couldn't tell whether this was written b...", "sent": "Artificial intelligence is transforming the way we live and work. It o"}
  ],
  "criterion_2_spread_human (1 of 5)": [
    {"status": 200, "guess": "unsure", "confidence": 0.5295, "model_score": 0.8931, "style_score": 0.6364, "label": "Our automated check couldn't tell whether this was written b...", "sent": "During my undergraduate studies in Mathematics, I developed a solid fo"}
  ],
  "criterion_3_bad_invalid (1 of 5)": [
    {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "{\"creator_id\": \"eval_inv_missing\"}"}
  ],
  "criterion_3_bad_empty (1 of 5)": [
    {"status": 400, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "(empty text)"}
  ],
  "criterion_3_bad_short (3 of 5, including both failures)": [
    {"status": null, "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)...", "sent": "a"},
    {"status": null, "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)...", "sent": "Hello"},
    {"status": 200, "guess": "unsure", "confidence": 0.0, "model_score": 0.4937, "style_score": 0.5, "label": "Our automated check couldn't tell whether this was written b...", "sent": "Thanks for the help today."}
  ],
  "criterion_3_bad_toolong (1 of 5)": [
    {"status": 413, "guess": null, "confidence": null, "model_score": null, "style_score": null, "label": null, "sent": "word word word word word word word word word word word word word word "}
  ],
  "criterion_5_label_coverage (3 of 3)": [
    {"status": 200, "guess": "human", "confidence": 0.773, "model_score": 0.227, "style_score": 0.0, "label": "Our automated check found that this writing reads like it wa...", "sent": "ok so I tried the new ramen place last night. honestly? overrated. the"},
    {"status": 200, "guess": "unsure", "confidence": 0.6083, "model_score": 0.9083, "style_score": 0.7, "label": "Our automated check couldn't tell whether this was written b...", "sent": "Artificial intelligence is transforming the way we live and work. It o"},
    {"status": 200, "guess": "ai", "confidence": 0.8649, "model_score": 0.9337, "style_score": 0.9312, "label": "Our automated check thinks this writing was likely produced ...", "sent": "Technology is an important part of modern life. It helps people to wor"}
  ]
}
```

Criterion 4, from `results/appeal_test_before.txt` (produced by `appeal_test.py`):

```
trial 1: 5/5 appeals recorded; unknown id -> http 404
trial 2: 5/5 appeals recorded; unknown id -> http 404
trial 3: 5/5 appeals recorded; unknown id -> http 404
```

**Diagnoses**

*Criterion 3 miss and attack MF02: stage, the route; mechanism, the signals were called before short text was handled.* `detector.py::perplexity` deliberately raises `ValueError("Text is too short to score")` when there are too few tokens to predict. `app.py::submit` called the detector without checking length first and without catching the error, so the exception became a 500. My under-25-word rule existed, but it ran *after* both signals, so it protected the label, not the code. Because the service runs in debug mode, the 500 was an HTML debugger page, which is why `run_eval.py` saw `JSONDecodeError` and status `null`. The crash happened before `audit.log_decision`, so it left no log entry. "Thanks for the help today." (5 words) did *not* crash, so the detector's cutoff is a token count, not my 25-word count.

*Criterion 2 miss: stage, both signals; mechanism, neither separates formal human writing from AI, so no combining rule can.* Signal one rates polished prose as predictable: my writing scored 0.53–0.89, AI scored 0.77–0.93. Signal two **saturates at 0.700** on evenly paced text. Sentence spread and punctuation both max out at "AI-like," and type-token ratio contributes nothing on paragraphs this short, so three AI texts and two of my pieces all scored exactly 0.700. I swept the model weight from 0.0 to 1.0 on the same data: the gap never exceeded 0.232, and the higher the model weight, the closer my own writing got to the AI line (my statement of purpose reaches 0.893 at weight 1.0). This is a limit of what the signals measure, not of the weights.

*Attacks EV02, EV05, PI02: stage, signal two (EV02) or both signals (EV05, PI02); mechanism, deliberate surface irregularity reads as human.*
- **EV02** (broken-up sentences): `style_score` **0.053**. Chopped sentences maximize length spread, which my style signal reads as human. Signal one still leaned AI (0.594), but the equal-weight average dragged the result down to 0.324, which is "human."
- **EV05** (heavy human editing pass): model 0.321, style 0.209. Both signals read it as human. That may be partly *correct*: if a person rewrote most of the text, it is arguably human writing now. I count it as broken because the attack set does, but the line between "edited AI" and "human" is genuinely unclear.
- **PI02** (instruction disguised as a system message): model 0.204, style 0.133. The instruction itself did nothing; neither signal reads instructions. The *formatting* did it. Markup like "SYSTEM:" is unusual text for GPT-2, which pushes perplexity up, and my style signal counts colons and brackets as "expressive punctuation." So injection syntax looks like human irregularity to both.

**The pattern:** both of my signals measure **surface regularity** as a stand-in for "AI." So the system fails in mirror image. Deliberate irregularity makes AI look human (EV02, EV05, PI02), and natural formality makes humans look like AI (criterion 2, and FP05 at 0.816, where the style signal, 0.832, was the higher of the two). That's one problem, not four. MF02 and criterion 3 are a separate, simpler problem: the order of operations in the route.

---

## The Improvement

**What I changed:** One thing, in `app.py::submit`. Text under 25 words is now decided **before** either signal runs: it gets the "unsure" label with confidence 0.0 and `null` signal scores, and is logged like any other decision. Before, both signals ran on all text and the under-25-word rule only overrode the label afterwards. Nothing else changed: weights, thresholds, label text, and every 25+ word path are identical. The change is its own commit ("Unit 8 improvement: decide short text (<25 words) before the signals run").

**Which diagnosis pointed at it:** Criterion 3's miss and attack MF02. Both had the same stage and mechanism: the route called `detector.model_signal` on 1-token text, the detector raised `ValueError`, and the route turned it into a 500 with no audit entry. I considered reweighting the signals instead, to address criterion 2, but a weight sweep on my own data showed the median gap never exceeds 0.232 at any weight (see Run Log). So that diagnosis points at the signals themselves, not something one setting can fix.

### Attack Run — After

Report: `results/attack_run_2026-11-04_2019_after.md`. Same 56 attacks, same marking rule. The service was restarted first so the rate limiter started fresh, as in the before-run.

**Result: before 52 HELD / 4 BROKE → after 53 HELD / 3 BROKE.** Only MF02 changed.

| ID | Targeting | Before | After | Change |
|---|---|---|---|---|
| EV01 | signal two: typos raise word variety | 200 unsure, HELD | 200 unsure, HELD | — |
| EV02 | signal two: broken-up sentences raise length spread | 200 **human, BROKE** | 200 **human, BROKE** | — |
| EV03 | signal two: a pasted quotation changes the shape | 200 unsure, HELD | 200 unsure, HELD | — |
| EV04 | signal one: unusual words raise perplexity | 200 unsure, HELD | 200 unsure, HELD | — |
| EV05 | both signals: heavy human editing pass | 200 **human, BROKE** | 200 **human, BROKE** | — |
| EV06 | signal two: one very long sentence and one very short | 200 unsure, HELD | 200 unsure, HELD | — |
| EV07 | signal two: padding with punctuation | 200 unsure, HELD | 200 unsure, HELD | — |
| EV08 | signal one: text below the token window | 200 unsure, HELD | 200 unsure, HELD | — |
| EV09 | both: AI text with a human opening paragraph bolted on | 200 unsure, HELD | 200 unsure, HELD | — |
| EV10 | signal two: repeated stanza structure | 200 ai, HELD | 200 ai, HELD | — |
| FP01–FP08 | false-positive attacks (8 rows) | 200 unsure, HELD (all 8) | 200 unsure, HELD (all 8) | — |
| PI01, PI03–PI06 | prompt injection (5 rows) | 200 unsure, HELD (all 5) | 200 unsure, HELD (all 5) | — |
| PI02 | instruction disguised as a system message | 200 **human, BROKE** | 200 **human, BROKE** | — |
| MF01 | text is only whitespace | 400, HELD | 400, HELD | — |
| **MF02** | **text is a single character** | **500, BROKE** | **200 unsure, HELD** | **fixed** |
| MF03–MF07 | control chars, punctuation, long word, emoji, RTL script | 200 unsure, HELD (all 5) | 200 unsure, HELD (all 5) | scores now `null` |
| MF08 | text is 60,000 characters | 413, HELD | 413, HELD | — |
| RQ01–RQ12 | malformed requests (12 rows) | 400, HELD (all 12) | 400, HELD (all 12) | — |
| FL01_01–10 | 20 rapid submissions from one creator | 200, HELD | 200, HELD | — |
| FL01_11–12 | 20 rapid submissions from one creator | 429, HELD | 429, HELD | — |

### Run Log — After

Report: `results/run_2026-11-04_2020_after.md`, `results/appeal_test_after.txt`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Before | After |
|---|---|---|---|---|---|---|
| 1. My own writing labeled AI | 0 of 10 | 0/10 | 0/10 | 0/10 | MET | **MET** |
| 2. Median gap, AI minus human | ≥ 0.30 | 0.219 | 0.219 | 0.219 | MISSED | **MISSED** |
| 3. Bad input, 5 of 5 per case | 4 of 4 cases | 4 of 4 | 4 of 4 | 4 of 4 | MISSED | **MET** |
| 4. Appeals recorded; unknown id → 404 | 5 of 5 | 5/5 | 5/5 | 5/5 | MET | **MET** |
| 5. All three labels reachable | 3 of 3 | 3/3 | 3/3 | 3/3 | MET | **MET** |

`bad_short`, the only scenario that changed, after the fix, from `summarize_eval.py`:

```
bad_short        trial 1  status [200, 200, 200, 200, 200]
bad_short        trial 2  status [200, 200, 200, 200, 200]
bad_short        trial 3  status [200, 200, 200, 200, 200]
```

Every other number in the after-run matches the before-run exactly, including the 0.219 median gap. That's how I know nothing else moved.

**Did it help, and how do I know:** Yes, for exactly what it targeted. The short-text crash is gone (MF02: 500 → 200; criterion 3: missed → met), short submissions now get an `content_id` they can appeal with, and they now leave an audit entry (before, MF02 left zero). It did nothing for the signal-level failures (criterion 2, EV02, EV05, PI02), which is expected, since they were never input problems.

**What it cost:** short submissions now carry no signal scores at all. If a reviewer asks "what did the detector make of this 10-word poem?", the log can't say. And any AI text under 25 words is now *guaranteed* "unsure," without the signals even looking. That's an evasion route I opened deliberately (it's EV08's idea, "text below the token window," taken to its limit). I accept it, because a signal reading on 10 words was noise anyway, and the alternative was crashing on real writers.

---

## What's Still Broken

**Attacks still getting through**

- **EV02 (broken-up sentences labeled human).** *What I'd do:* stop treating sentence-length spread as evidence of a human. It's the cheapest thing to fake. I'd either cap its contribution or replace it with something harder to game, like variation in sentence *structure* rather than length. *Why I stopped:* that's a redesign of signal two, and this unit allows one change. I spent mine on the crash.
- **EV05 (heavily edited AI labeled human).** *What I'd do:* probably nothing at the detector level. If a person rewrote most of the text, calling it human may be closer to right than wrong. A platform that cares about this needs a policy on AI-assisted writing, not a better threshold. *Why I stopped:* I don't think it's a detector problem.
- **PI02 (fake system message labeled human).** *What I'd do:* strip markup-like tokens ("SYSTEM:", brackets, role tags) before scoring, so formatting can't masquerade as human irregularity, and stop counting colons and brackets as "expressive" punctuation in `stylometry.py`. *Why I stopped:* it's a change to signal two plus preprocessing, two changes beyond my one.
- **The seven evasions that landed in "unsure."** These are HELD under my marking rule, but by the attack set's goal they succeeded. *What I'd do:* nothing with the threshold. Lowering 0.85 to catch them would start accusing my own writing (0.774 at worst). *Why I stopped:* it's the trade I chose on purpose; see below.

**Criteria still missed**

- **Criterion 2 (median gap 0.219, target 0.30).** *What I'd do:* add a third signal that measures something other than surface regularity, for example comparing the text against a second, different language model, or measuring how the text's predictability *varies* across sentences rather than its average. Reweighting can't fix it: my sweep showed the gap stays between 0.213 and 0.232 at every weight. *Why I stopped:* a new signal is a stretch feature and more than one change. I'm not revising the criterion either, because it was measurable and I simply missed it.

**Other weaknesses I found along the way**

- **The rate limit is easy to dodge.** It keys on `creator_id`, which the caller makes up, so a script that changes it every request is never limited. *Fix:* add a per-IP limit alongside the per-creator one, or require authenticated accounts.
- **Debug mode leaks internals.** Before the fix, the crash returned a Werkzeug debugger page with my stack trace. *Fix:* run with `DEBUG = False` and a production server (gunicorn is already in `requirements.txt`) anywhere outside my laptop.
- **The log doesn't store the submitted text.** That made the log-injection attack (PI05) harmless, but it also means a reviewer handling an appeal can't reread what was submitted from the log alone. *Fix:* store a hash of the text in the log and the text itself in a separate store with access controls.
- **Signal one reads only the first ~300 words** (`DETECTOR_MAX_TOKENS = 400`). AI text placed after 300 human words is never scored by it.

**The trade I'd make if this ran for real:**

I would keep the strict threshold and let more AI text through as "unsure," because a false accusation lands on one real person, while a missed detection is spread thinly across the platform. The people who pay for that choice are honest writers competing against undetected AI-assisted work, and readers who trust a "human" label that can be gamed. I'd rather they pay than the writer whose own statement of purpose scored 0.765.

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

## Capstone

**What This Extends**

Provenance Guard, the AI-writing detector service from Units 7–8 (same repository). What's new is a failure-handling layer around the two signals. Before this unit, if `detector.model_signal` or `stylometry.style_signal` raised an error or hung, `/submit` returned a 500 or stalled, and the failure left no audit entry. The only bad path that was protected was text under 25 words, which Unit 8 fixed by checking length first.

**The Shape**

Shape B: harden against failure. Every signal call in `app.py::submit` now goes through one wrapper, `run_signal`, that runs the signal with a time limit and catches any error. If a signal fails or runs past its limit, `/submit` still returns HTTP 200 with the "unsure" label (no accusation is possible on a result the system couldn't compute), and the audit log records which signal failed, how it failed, and how long the request took. Failures can be triggered on purpose through a setting in `config.py`, so the bad path is testable.

Out of scope, decided before building:
- No new signal, and no changes to weights, thresholds, or label text. The scoring that Unit 8 measured stays exactly as it was.
- No hosting. The service loads GPT-2 locally (~550 MB), which won't fit a 512 MB free host, so it runs locally (Path B).
- No rate-limit changes, even though Unit 8 found the limiter can be dodged by changing `creator_id`.
- The time limit stops *waiting* for a slow signal; it doesn't kill the computation. Stopping a running PyTorch call cleanly is out of scope.


**Running It**

Path B: local with logs. The service loads GPT-2 locally (about 548 MB), which won't fit a 512 MB free host. The start command, setup, and environment are in [`RUNNING.md`](RUNNING.md) (start with `python app.py`, or `AI201_FAULTS=1 python app.py` to enable fault injection for testing).

I tested `RUNNING.md` by cloning the repo into a fresh folder and following it exactly. **The first attempt found a gap:** pip installed NumPy 2.5.4, which torch 2.2.2 (the last build for Intel Macs, compiled against NumPy 1.x) warns may crash. I pinned `numpy<2` in `requirements.txt`, and the second clean-clone test passed `test.py` with no warning (9 of 9 checks; "all 8 import cleanly"). The same test also measured a cold-start model warm-up of 10,417 ms, which is now documented in `RUNNING.md`. Caveat: GPT-2 was already in my Hugging Face cache, so the clean test did not re-download it.

**Instrumentation**

Every request to `/submit` writes one JSON record to `logs/audit.jsonl` (via `audit.log_decision` or `audit.log_rejection`, called from `app.py::submit` and `app.py::_reject`). Each decision record holds:

- **When:** `timestamp`
- **What came in:** `creator_id`, `word_count`, `char_count`, `text_sha256` (first 16 hex characters of a SHA-256 of the text), `text_preview` (first 80 characters)
- **What came out:** `content_id`, `guess`, `label`, `model_score`, `style_score`, `combined_score`, `status`
- **How long it took:** `duration_ms` (whole request, timed from a `before_request` hook), `model_ms`, `style_ms`
- **What went wrong (new this unit):** `degraded` (true if either signal failed), `failures` (for each failed signal: `signal`, `kind` of `error`/`timeout`/`bad_value`, the error message, and its `ms`), and `fault_injected` (the test fault, if one was forced)

Rejected requests (400/413) are logged with `reason`, `http_status`, and `duration_ms`. Known gap: rate-limit rejections (429) are logged by the starter's handler, but Flask-Limiter runs before my timer starts, so they carry no `duration_ms`.

One change in what the log holds: Unit 7–8's log stored no submitted text at all (which is why the Unit 8 log-injection attack PI05 held). This unit adds an 80-character `text_preview` so a record shows what came in. It's still written as escaped JSON, so text in it can't break or forge a record.

Thirteen entries from the log. The `label` field is omitted from each to keep this readable; it's the full label text shown in Label Variants. The first two are **failed runs**: a *real* cold-start timeout (the model was still loading from disk when the first request arrived, before I added the startup warm-up) and an *injected* error. The third is a rejected input. The last ten are the cost-measurement runs.

```json
{"char_count": 230, "combined_score": null, "content_id": "14df7d07-85db-4ecd-98b1-91239956f73a", "creator_id": "cap_test_1", "degraded": true, "duration_ms": 5008.3, "failures": [{"error": "no result after 5.0s", "kind": "timeout", "ms": 5003.3, "signal": "model"}], "fault_injected": null, "guess": "unsure", "model_ms": 5003.3, "model_score": null, "status": "decided", "style_ms": 4.1, "style_score": 0.7, "text_preview": "Artificial intelligence is transforming the way we live and work. It offers many", "text_sha256": "3504872697a56490", "timestamp": "2026-11-11T23:50:19+00:00", "word_count": 31}
{"char_count": 230, "combined_score": null, "content_id": "0d73d63d-4672-4bcb-91a4-cde9150551ef", "creator_id": "cap_test_2", "degraded": true, "duration_ms": 0.9, "failures": [{"error": "RuntimeError: injected fault: model signal failed", "kind": "error", "ms": 0.1, "signal": "model"}], "fault_injected": "model_error", "guess": "unsure", "model_ms": 0.1, "model_score": null, "status": "decided", "style_ms": 0.2, "style_score": 0.7, "text_preview": "Artificial intelligence is transforming the way we live and work. It offers many", "text_sha256": "3504872697a56490", "timestamp": "2026-11-11T23:50:19+00:00", "word_count": 31}
{"creator_id": "cap_test_4", "duration_ms": 0.4, "event": "rejected", "http_status": 400, "reason": "EMPTY_TEXT", "status": "rejected", "timestamp": "2026-11-11T23:55:38+00:00"}
{"char_count": 1622, "combined_score": 0.76475, "content_id": "fb21729e-5086-4680-8e15-b7013b3020f8", "creator_id": "cost_run_1", "degraded": false, "duration_ms": 399.6, "failures": [], "fault_injected": null, "guess": "unsure", "model_ms": 396.8, "model_score": 0.8931, "status": "decided", "style_ms": 1.4, "style_score": 0.6364, "text_preview": "During my undergraduate studies in Mathematics, I developed a solid foundation i", "text_sha256": "9c79590daf2bcad8", "timestamp": "2026-11-12T00:12:55+00:00", "word_count": 225}
{"char_count": 1622, "combined_score": 0.76475, "content_id": "439c9a47-fe38-4ffe-9578-bbca849ca767", "creator_id": "cost_run_2", "degraded": false, "duration_ms": 405.1, "failures": [], "fault_injected": null, "guess": "unsure", "model_ms": 402.9, "model_score": 0.8931, "status": "decided", "style_ms": 1.5, "style_score": 0.6364, "text_preview": "During my undergraduate studies in Mathematics, I developed a solid foundation i", "text_sha256": "9c79590daf2bcad8", "timestamp": "2026-11-12T00:12:55+00:00", "word_count": 225}
{"char_count": 1622, "combined_score": 0.76475, "content_id": "6d7e593c-1785-4ab6-91d9-6717a4945bbb", "creator_id": "cost_run_3", "degraded": false, "duration_ms": 407.8, "failures": [], "fault_injected": null, "guess": "unsure", "model_ms": 406.1, "model_score": 0.8931, "status": "decided", "style_ms": 1.2, "style_score": 0.6364, "text_preview": "During my undergraduate studies in Mathematics, I developed a solid foundation i", "text_sha256": "9c79590daf2bcad8", "timestamp": "2026-11-12T00:12:55+00:00", "word_count": 225}
{"char_count": 1622, "combined_score": 0.76475, "content_id": "bdc0e414-e680-4e2b-b8a8-00c8c2255674", "creator_id": "cost_run_4", "degraded": false, "duration_ms": 459.7, "failures": [], "fault_injected": null, "guess": "unsure", "model_ms": 457.9, "model_score": 0.8931, "status": "decided", "style_ms": 1.0, "style_score": 0.6364, "text_preview": "During my undergraduate studies in Mathematics, I developed a solid foundation i", "text_sha256": "9c79590daf2bcad8", "timestamp": "2026-11-12T00:12:56+00:00", "word_count": 225}
{"char_count": 1622, "combined_score": 0.76475, "content_id": "b45552c9-7880-433d-bcb9-350ba2424797", "creator_id": "cost_run_5", "degraded": false, "duration_ms": 375.7, "failures": [], "fault_injected": null, "guess": "unsure", "model_ms": 373.8, "model_score": 0.8931, "status": "decided", "style_ms": 1.3, "style_score": 0.6364, "text_preview": "During my undergraduate studies in Mathematics, I developed a solid foundation i", "text_sha256": "9c79590daf2bcad8", "timestamp": "2026-11-12T00:12:56+00:00", "word_count": 225}
{"char_count": 1622, "combined_score": 0.76475, "content_id": "8f89f949-76cd-45e1-a1ab-e6a6cacb4450", "creator_id": "cost_run_6", "degraded": false, "duration_ms": 383.8, "failures": [], "fault_injected": null, "guess": "unsure", "model_ms": 382.2, "model_score": 0.8931, "status": "decided", "style_ms": 1.1, "style_score": 0.6364, "text_preview": "During my undergraduate studies in Mathematics, I developed a solid foundation i", "text_sha256": "9c79590daf2bcad8", "timestamp": "2026-11-12T00:12:57+00:00", "word_count": 225}
{"char_count": 1622, "combined_score": 0.76475, "content_id": "bd8d7781-7633-4832-948d-d16dbb76de80", "creator_id": "cost_run_7", "degraded": false, "duration_ms": 371.0, "failures": [], "fault_injected": null, "guess": "unsure", "model_ms": 369.6, "model_score": 0.8931, "status": "decided", "style_ms": 0.9, "style_score": 0.6364, "text_preview": "During my undergraduate studies in Mathematics, I developed a solid foundation i", "text_sha256": "9c79590daf2bcad8", "timestamp": "2026-11-12T00:12:57+00:00", "word_count": 225}
{"char_count": 1622, "combined_score": 0.76475, "content_id": "f64f70a9-11a2-4dce-83f9-29e7918400c5", "creator_id": "cost_run_8", "degraded": false, "duration_ms": 372.2, "failures": [], "fault_injected": null, "guess": "unsure", "model_ms": 370.7, "model_score": 0.8931, "status": "decided", "style_ms": 1.0, "style_score": 0.6364, "text_preview": "During my undergraduate studies in Mathematics, I developed a solid foundation i", "text_sha256": "9c79590daf2bcad8", "timestamp": "2026-11-12T00:12:57+00:00", "word_count": 225}
{"char_count": 1622, "combined_score": 0.76475, "content_id": "179c3c9b-dc2b-4b7b-baff-fbd4503eb80b", "creator_id": "cost_run_9", "degraded": false, "duration_ms": 369.7, "failures": [], "fault_injected": null, "guess": "unsure", "model_ms": 368.1, "model_score": 0.8931, "status": "decided", "style_ms": 1.1, "style_score": 0.6364, "text_preview": "During my undergraduate studies in Mathematics, I developed a solid foundation i", "text_sha256": "9c79590daf2bcad8", "timestamp": "2026-11-12T00:12:58+00:00", "word_count": 225}
{"char_count": 1622, "combined_score": 0.76475, "content_id": "2e55529c-6900-4a0d-a5ce-fa87e7fd7875", "creator_id": "cost_run_10", "degraded": false, "duration_ms": 379.2, "failures": [], "fault_injected": null, "guess": "unsure", "model_ms": 377.6, "model_score": 0.8931, "status": "decided", "style_ms": 1.1, "style_score": 0.6364, "text_preview": "During my undergraduate studies in Mathematics, I developed a solid foundation i", "text_sha256": "9c79590daf2bcad8", "timestamp": "2026-11-12T00:12:58+00:00", "word_count": 225}
```

**What It Costs**

This system calls no paid API, so its real cost is **seconds of compute.** I measured it with `measure_cost.py`: 10 identical submissions of a realistic 225-word piece (my statement of purpose), then the server-side `duration_ms` of each read back from the audit log. That's the service's own timing, not an estimate. Output: `results/cost_measurement.txt`.

- **Mean: 392.4 ms per run** (median 381.5, min 369.7, max 459.7). No run was degraded.
- **Where the time goes:** the model signal averaged 390.6 ms (99.5% of the run); the style signal averaged 1.2 ms; validation, logging, and the response took the remaining ~2 ms.
- **Cost depends on length, up to a cap:** a 31-word submission took 69 ms; this 225-word one takes about 390 ms. Signal one stops reading at ~400 tokens (about 300 words), so cost should level off for anything longer.
- **Startup is a separate, one-time cost:** about 10.4 s to load GPT-2 (cold start, measured from a clean clone).

**A hundred people a day:** 100 runs × 0.392 s = **39.2 seconds of compute per day.** If each person submitted ten times, that's 1,000 × 0.392 s = 392 s, about 6.5 minutes a day. At this scale compute isn't the constraint; the model's ~550 MB memory footprint is, which is what ruled out the free host.

**Run Log and Verdicts**

Criteria: `criteria.md` → "Capstone criteria" (committed in `add capstone criteria`, before any results). Tests: `capstone_eval.py` (`--mode on` for criteria 1–4, `--mode off` for criterion 5), which follows the protocol in `criteria.md` exactly: one request at a time, a fresh `creator_id` each time, a 15-second wait after each slow fault. Baseline for criterion 4: `results/unit8_baseline.json`, captured by `capture_baseline.py` from the final Unit 8 code (commit `6ab06cf`, run from a separate git worktree). Results: `results/capstone_before_faults_on.json` and `results/capstone_before_faults_off.json` (committed as `first capstone results`).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. A signal error returns an unsure result | 3 of 3 | 3/3 | 3/3 | 3/3 | **MET** |
| 2. A slow signal returns an unsure result within 6.0 s | 3 of 3 | 3/3 | 3/3 | 3/3 | **MET** |
| 3. Every failed signal leaves a matching audit record | 6 of 6 | 6/6 | 6/6 | 6/6 | **MET** |
| 4. Healthy requests preserve Unit 8 scoring | 3 of 3 | 3/3 | 3/3 | 3/3 | **MET** |
| 5. Fault headers have no effect when fault injection is off | 2 of 2 | 2/2 | 2/2 | 2/2 | **MET** |

**How I decided each verdict:** each target had to hold in every trial, and it did. Criterion 2's nine slow requests took 5.005–5.010 s (all under 6.0). Criterion 4's healthy responses matched the Unit 8 baseline exactly (model 0.8931, style 0.6364, combined 0.7648, confidence 0.5295, "unsure"). Criterion 5's `model_error` and `model_slow` headers produced that same healthy response with `fault_injected: null`.

**Real output from trial 1** (`capstone_eval.py` calling `app.py::submit`; long `label` strings shortened with "..."):

```json
{
  "criterion_1": {"http_status": 200, "client_secs": 0.017, "response": {"combined_score": null, "confidence": 0.0, "content_id": "3937e7a2-d1d1-4308-922d-02daf738cfcb", "degraded": true, "failures": [{"kind": "error", "signal": "model"}], "guess": "unsure", "label": "Our automated check couldn't tell whether this was written b...", "model_score": null, "status": "decided", "style_score": 0.6364}},
  "criterion_2": {"http_status": 200, "client_secs": 5.005, "response": {"combined_score": null, "confidence": 0.0, "content_id": "8858fce6-0084-4693-9d2c-35a5cfc909b5", "degraded": true, "failures": [{"kind": "timeout", "signal": "model"}], "guess": "unsure", "label": "Our automated check couldn't tell whether this was written b...", "model_score": null, "status": "decided", "style_score": 0.6364}},
  "criterion_4": {"http_status": 200, "client_secs": 0.516, "response": {"combined_score": 0.7648, "confidence": 0.5295, "content_id": "1113dbd4-aa10-42be-91e6-f66e89fa289e", "degraded": false, "failures": [], "guess": "unsure", "label": "Our automated check couldn't tell whether this was written b...", "model_score": 0.8931, "status": "decided", "style_score": 0.6364}},
  "criterion_5": {"header": "model_error", "http_status": 200, "response": {"combined_score": 0.7648, "confidence": 0.5295, "content_id": "d60d912b-870e-4156-8f26-593102a3a736", "degraded": false, "failures": [], "guess": "unsure", "label": "Our automated check couldn't tell whether this was written b...", "model_score": 0.8931, "status": "decided", "style_score": 0.6364}}
}
```

Criterion 3: the audit records (from `logs/audit.jsonl`, written by `app.py::submit` via `audit.log_decision`) for the criterion 1 and criterion 2 requests above. The writer saw the same response for both; the log tells them apart:

```json
{"char_count": 1622, "combined_score": null, "content_id": "3937e7a2-d1d1-4308-922d-02daf738cfcb", "creator_id": "cap_eval_139b1193", "degraded": true, "duration_ms": 2.5, "failures": [{"error": "RuntimeError: injected fault: model signal failed", "kind": "error", "ms": 0.2, "signal": "model"}], "fault_injected": "model_error", "guess": "unsure", "model_ms": 0.2, "model_score": null, "status": "decided", "style_ms": 1.4, "style_score": 0.6364, "text_preview": "During my undergraduate studies in Mathematics, I developed a solid foundation i", "text_sha256": "9c79590daf2bcad8", "timestamp": "2026-11-12T00:31:17+00:00", "word_count": 225}
{"char_count": 1622, "combined_score": null, "content_id": "8858fce6-0084-4693-9d2c-35a5cfc909b5", "creator_id": "cap_eval_d0151a68", "degraded": true, "duration_ms": 5002.6, "failures": [{"error": "no result after 5.0s", "kind": "timeout", "ms": 5000.2, "signal": "model"}], "fault_injected": "model_slow", "guess": "unsure", "model_ms": 5000.2, "model_score": null, "status": "decided", "style_ms": 2.0, "style_score": 0.6364, "text_preview": "During my undergraduate studies in Mathematics, I developed a solid foundation i", "text_sha256": "9c79590daf2bcad8", "timestamp": "2026-11-12T00:31:22+00:00", "word_count": 225}
```

**All five met, so were my targets too low? Yes.** All five criteria test one request at a time. When I reviewed them before running anything, the honest answer to "what would have to happen for this to fail?" was the same for every one: a bug I hadn't seen. Criterion 2 is the clearest case of a loose target: the measured range was 5.005–5.010 s against a 6.0 s limit. If I tightened one target, it would be **criterion 2, to 5.1 s**, which still allows for logging and response time but would catch any added delay after the timeout. The real gap is that **no criterion tested concurrent requests**, so I ran a load observation (below) to look where my criteria didn't.

**Load observation (not a criterion): what my criteria missed.** `load_observation.py` sends 4 slow-fault requests at once, then 3 healthy requests 0.5 s later, all concurrent. Before the improvement (`results/load_observation_before.txt`):

```
{"kind": "healthy", "secs": 10.01, "degraded": true, "failures": [{"kind": "timeout", "signal": "model"}, {"kind": "timeout", "signal": "style"}], "guess": "unsure"}
{"kind": "healthy", "secs": 10.01, "degraded": true, "failures": [{"kind": "timeout", "signal": "model"}, {"kind": "timeout", "signal": "style"}], "guess": "unsure"}
{"kind": "healthy", "secs": 10.01, "degraded": true, "failures": [{"kind": "timeout", "signal": "model"}, {"kind": "timeout", "signal": "style"}], "guess": "unsure"}
{"kind": "slow", "secs": 10.03, "degraded": true, "failures": [{"kind": "timeout", "signal": "model"}, {"kind": "timeout", "signal": "style"}], "guess": "unsure"}
(three more slow rows, identical)
healthy requests degraded: 3 of 3
```

**Diagnosis.** *Stage:* `guard.run_signal`, specifically its shared pool of 4 worker threads. *Mechanism, in three parts:* (1) a timed-out signal keeps its worker for the full 15-second fault, because the wrapper stops waiting but can't stop the thread; (2) the 5-second clock starts when a job is **queued**, so time spent waiting for a free worker counts against the limit; (3) the two signals go through the pool one after the other, so with the pool full, the model job times out at 5 s and the style job (normally about 1 ms) then waits behind the same busy workers and times out at 10 s. Four slow requests filled the pool, and every healthy request behind them was reported as failed, even though nothing was wrong with it. Under concurrency, criterion 2's own target would also fail (10.03 s, not under 6.0 s).


**The Improvement**

*What I changed:* one thing, in `guard.py::run_signal`. Each signal call now runs on **its own thread** (`guard.py::_run_own_thread`) instead of a shared pool of 4 workers. The time limit, error catching, return values, and `app.py` are all unchanged. Committed on its own: `Capstone improvement: run each signal on its own thread instead of a shared 4-worker pool` (between the `first capstone results` commit and the after-runs commit).

*Why this change:* the diagnosis said a stuck signal holds a **shared** resource, so one slow signal can starve every other request. A thread per call removes the sharing: a stuck signal now only ever holds its own thread. I considered two alternatives. Running the style signal outside the pool would have fixed the 10-second double timeout but left healthy requests' model signal falsely timing out. Raising the pool from 4 to 16 would have passed this load test but only moved the threshold: 16 concurrent slow requests would reproduce the same failure.

**Run Log — After** (`results/capstone_after_faults_on.json`, `results/capstone_after_faults_off.json`, same protocol and script)

| Criterion | Target | Run 1 | Run 2 | Run 3 | Before | After |
|---|---|---|---|---|---|---|
| 1. A signal error returns an unsure result | 3 of 3 | 3/3 | 3/3 | 3/3 | MET | **MET** |
| 2. A slow signal returns an unsure result within 6.0 s | 3 of 3 | 3/3 | 3/3 | 3/3 | MET | **MET** |
| 3. Every failed signal leaves a matching audit record | 6 of 6 | 6/6 | 6/6 | 6/6 | MET | **MET** |
| 4. Healthy requests preserve Unit 8 scoring | 3 of 3 | 3/3 | 3/3 | 3/3 | MET | **MET** |
| 5. Fault headers have no effect when fault injection is off | 2 of 2 | 2/2 | 2/2 | 2/2 | MET | **MET** |

Criterion 2 elapsed times after: 5.005–5.010 s, the same as before. No regressions: everything the criteria measured still holds.

**Load observation — before and after** (`results/load_observation_before.txt`, `results/load_observation_after.txt`)

| | Before | After |
|---|---|---|
| Healthy requests falsely degraded | **3 of 3** | **0 of 3** |
| Healthy request time | 10.01 s (both signals timed out) | **1.03 s**, scored correctly |
| Slow-fault request time | 10.03 s (model *and* style timed out) | **5.02–5.03 s** (only the model timed out, as injected) |

After:

```
{"kind": "healthy", "secs": 1.03, "degraded": false, "failures": [], "guess": "unsure"}
{"kind": "healthy", "secs": 1.03, "degraded": false, "failures": [], "guess": "unsure"}
{"kind": "healthy", "secs": 1.03, "degraded": false, "failures": [], "guess": "unsure"}
{"kind": "slow", "secs": 5.02, "degraded": true, "failures": [{"kind": "timeout", "signal": "model"}], "guess": "unsure"}
{"kind": "slow", "secs": 5.03, "degraded": true, "failures": [{"kind": "timeout", "signal": "model"}], "guess": "unsure"}
{"kind": "slow", "secs": 5.03, "degraded": true, "failures": [{"kind": "timeout", "signal": "model"}], "guess": "unsure"}
{"kind": "slow", "secs": 5.03, "degraded": true, "failures": [{"kind": "timeout", "signal": "model"}], "guess": "unsure"}
healthy requests degraded: 0 of 3
```

*Did it help?* Yes, for exactly the failure it targeted. Under concurrent load, healthy requests went from 3 of 3 falsely degraded to 0 of 3, and slow requests now fail in ~5 s as designed instead of 10. My five criteria can't show this, since they were met before and after. Their after-run shows the change broke nothing. The load observation is the evidence that it helped.

*What it cost:* threads are no longer capped. Each stuck call keeps its own thread alive until the signal finishes on its own (15 s for an injected slow fault), so a burst of N slow requests now means N live threads instead of a ceiling of 4. And healthy requests now share the CPU when they overlap: three concurrent GPT-2 calls took 1.03 s each, about 2.6 times the 392 ms sequential average. That's well under the 5 s limit here, but enough concurrent healthy requests would eventually push past it. The failure moved from "a full worker queue" to "a busy CPU," and it now takes more load to trigger it.

**What's Still Broken**

All five criteria were met before and after, so by the spec's rule this section names the target I'd tighten, then what my criteria never tested.

*The target I'd tighten:* criterion 2, from 6.0 s to **5.1 s**. Measured slow-fault responses took 5.005–5.010 s in every trial, before and after. A 6.0 s limit would let nearly a full second of extra delay after the timeout go unnoticed; 5.1 s still covers logging and the response but would catch it.

*What's still broken, or untested:*

- **Concurrent healthy load is now the limit.** Three overlapping GPT-2 calls took 1.03 s each, 2.6 times the sequential average. I never measured where concurrent healthy requests start crossing the 5 s limit and get falsely degraded again. *What I'd do:* run the load observation at increasing concurrency (3, 6, 12, 24 healthy requests) to find that point, then decide between a longer limit and a cap. *Why I stopped:* this unit allows one improvement, and I spent it on the worker-pool failure that I'd actually observed.
- **Threads are uncapped.** Since the improvement, each stuck signal holds its own thread until it finishes, so a burst of slow requests creates that many live threads. *What I'd do:* add a cap (a semaphore) that returns a degraded "unsure" immediately, with `kind: "overloaded"`, when too many signal threads are alive, so overload fails fast and visibly instead of piling up. *Why I stopped:* it's a second change, and a cap reintroduces a limit, so it would need its own before/after test.
- **A timed-out signal keeps computing.** The wrapper stops waiting at 5 s, but the GPT-2 call (or the injected sleep) runs to completion in the background. *Why I stopped:* declared out of scope in The Shape; stopping a running PyTorch call cleanly isn't something Python threads support.
- **My criteria never tested concurrency.** All five ran one request at a time, which is why they couldn't catch the failure the load observation found. Next time, at least one criterion would name a concurrent load and a target for it.
- **The fault header is an attack surface if misconfigured.** With `AI201_FAULTS=1`, anyone who sends `X-Fault` can force "unsure" on their own submission. Criterion 5 shows the header is inert when injection is off, but nothing stops someone starting a real deployment with it on. *What I'd do:* refuse to start with fault injection on unless debug mode is also on.
- **Unchanged from Unit 8:** the rate limit can still be dodged by rotating `creator_id`, and the service still runs Flask's debug server, which isn't meant for production.

*The one thing I'd do first with another unit:* find the concurrency point where healthy requests start getting falsely degraded again, and write a criterion for it. It's the only failure mode this unit actually observed, and my improvement moved it rather than removed it, so it's the place where a real writer would most likely be told "unsure" for no reason.

**How I Used AI**

*Moment 1: reviewing my criteria before committing them*

- *What I asked for:* I pasted my five capstone criteria into Claude and asked it to apply the spec's three self-check questions to each one (testable from the sentence alone? would two people score it the same way? what would have to happen for it to fail?) without rewriting them.
- *What came back:* Criterion 3 had two gaps a stranger would need to ask about: which six requests it meant, and how to tell a decision record from an appeal record. More importantly, for every criterion, the honest answer to "what would make this fail?" was the same: a bug I hadn't seen. All five ran one request at a time, so none tested concurrency. Claude first said my protocol excluded the stressors I'd measured, then corrected itself: the startup warm-up already prevents cold-start timeouts, and sequential requests can never exhaust four workers, so the real untested risk was concurrency.
- *What I changed:* I added the two clarifications to criterion 3, marked in italics in `criteria.md` as clarifications, not target changes. I kept all five criteria as written, and I decided to test concurrency separately as a load observation instead of changing a criterion.

*Moment 2: choosing the improvement*

- *What I asked for:* After all five criteria came back MET, I asked Claude to predict what concurrent load would do before I ran it, then, after the run, to explain the trade-offs of three possible fixes before I chose one.
- *What came back:* It predicted healthy requests would be falsely degraded because the shared pool would be full. That held (3 of 3, 10.01 s each). But it missed that the slow-fault requests themselves would also take 10 s, because their style signal queued behind the same busy workers. It laid out three options with predicted outcomes and costs, and recommended a thread per signal call.
- *What I changed:* I asked for a fuller explanation before deciding, then chose the thread-per-call change. I kept the write-up of its cost (uncapped threads, CPU sharing under load) rather than presenting the improvement as a clean win.

*What else came from Claude:* recommending Provenance Guard and Shape B (my choice to accept), the code in `guard.py`, the timing and logging additions in `app.py`, the test scripts (`capstone_eval.py`, `capture_baseline.py`, `load_observation.py`, `measure_cost.py`), and first drafts of these README sections, which I reviewed. Claude initially assumed a warm GPT-2 call took a second or two; measurement showed ~75 ms for a short paragraph and ~390 ms for 225 words.

I wrote the five criteria myself.

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
