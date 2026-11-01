# Acceptance Criteria — Provenance Guard

Scores run from 0 to 1; higher means more likely AI.
Written before any combined scores were seen.

## 1. False positives: 0 of 10 human samples labeled "high-confidence AI"
**Target:** I submit 10 human-written samples (at least 3 of them formal or plain-style writing). None receives the high-confidence AI label.
**Why:** That label is an accusation against a real writer. One failure means investigating the thresholds, not that the whole system is broken. Passing 10 samples does not prove a reliable false-positive rate, but any accusation of honest work is the costliest mistake this system can make. This target commits me to a high AI threshold, with borderline text going to "unsure."

## 2. Score spread: median gap of at least 0.30
**Target:** Across at least 5 clearly-AI and 5 clearly-human samples, the median combined score of the AI group is at least 0.30 higher than the median of the human group.
**Why:** If the two groups score close together, the labels are mostly noise. 0.30 is an initial engineering target, not a scientific cutoff. I will also check for overlap, since a median gap alone can hide individual errors.

## 3. Bad input: predictable responses, never a crash
**Target:** In 5 of 5 attempts for each case below, the service returns the listed response and never an HTTP 500:
- Missing, null, or non-string `text` → HTTP 400, `INVALID_TEXT`
- Empty or whitespace-only `text` → HTTP 400, `EMPTY_TEXT`
- Fewer than 25 words → HTTP 200 with the "unsure" label (no accusation possible)
- More than 10,000 words → HTTP 413, `TEXT_TOO_LONG`, with the limit explained

**Why:** A crash looks like an outage and leaves no audit trail. Short text cannot be judged reliably, but this is a writing site where poems are often short, so short work gets "unsure" rather than being refused or accused. Long text is never silently truncated.

## 4. Appeal path: 5 of 5 valid appeals recorded
**Target:** 5 of 5 appeals with a real `content_id` set the item's status to `under_review` and create an audit log entry with the content_id, timestamp, and reasoning. An unknown `content_id` returns HTTP 404 and changes nothing.
**Why:** This is deterministic code, so anything below 100% is a bug. The appeal is the only protection a wrongly accused writer has. It triggers review; it does not automatically reverse the decision.

## 5. Label coverage: all three labels reachable
**Target:** Calling `score_to_label` with scores just below, at, and just above each threshold in `config.py` produces the expected label every time, and real submissions produce each of the three labels (human, unsure, AI) at least once.
**Why:** A label that can never appear means a gap in my ranges. Seeing each label once proves it is reachable, not that it is accurate.
