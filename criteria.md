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


---

## Capstone criteria

*Written for Unit 9 (Shape B: harden against failure), before any capstone test results.*

Run each criterion in three trials. Use the same valid 225-word statement-of-purpose sample from `measure_cost.py` for every `POST /submit` request, with a fresh `creator_id` each time. Wait for startup warm-up to finish and send requests one at a time. After an injected timeout, wait 15 seconds from the response before sending another request so the timed-out worker can finish. A criterion is MET if it meets its target in all three trials.

### 1. A signal error returns an unsure result
**Target:** With `AI201_FAULTS=1`, submit the sample three times per trial with the `model_error` fault. All 3 of 3 responses must return HTTP 200, include a `content_id`, and return `guess: "unsure"` with the full unsure label.
**Why:** A signal can fail on any submission. Even one 500 leaves a writer without a result or an ID they can use to appeal. Returning a different label would give the writer a classification based on an incomplete score.

### 2. A slow signal returns an unsure result within six seconds
**Target:** With fault injection enabled, submit the sample three times per trial using the fault that makes the model signal run for about 15 seconds. Measure elapsed time from sending the local request to receiving the full response. All 3 of 3 requests must return HTTP 200 with `guess: "unsure"` and the full unsure label within 6.0 seconds each.
**Why:** The model gets five seconds before the service stops waiting. A six-second limit gives the service one more second to finish scoring, write the audit entry, and send the response. A request that waits for the full 15-second fault misses the target.

### 3. Every failed signal leaves a matching audit record
**Target:** For the six faulted requests in each trial *(the three from criterion 1 and the three from criterion 2)*, use each returned `content_id` to find its decision record in `logs/audit.jsonl`. All 6 of 6 requests must have exactly one matching decision record *(an entry with that `content_id` and no `event` field)* with `degraded: true`, a positive `duration_ms`, the injected fault recorded in `fault_injected`, and a failure entry naming the `model` signal. The entry must include a nonempty error message and elapsed `ms`, with `kind: "error"` for the three error requests and `kind: "timeout"` for the three slow requests.
**Why:** The writer sees the same unsure label in both cases. The audit record is how a reviewer or developer tells a model error from a timeout. A missing or duplicate record makes that submission harder to investigate.

### 4. Healthy requests preserve Unit 8 scoring
**Target:** On the same machine, submit the sample once to the final Unit 8 version to capture its model, style, and combined scores, confidence, guess, and label. In each capstone trial, submit the sample three times with fault injection enabled and no fault header. All 3 of 3 responses must return HTTP 200 and match the Unit 8 values at the precision returned by the API. Each matching audit record must show `degraded: false` and an empty `failures` list.
**Why:** The capstone adds failure handling around the existing signals. A change in a healthy request's score or label would change what a writer sees even though both signals completed. The same input and model on the same machine give a direct comparison.

### 5. Fault headers have no effect when fault injection is off
**Target:** Start the capstone with `AI201_FAULTS` unset. In each trial, submit the sample once with the `model_error` header value and once with the slow-model fault header value. Both requests must return HTTP 200 and match the healthy response from criterion 4 on scores, confidence, guess, and label. Both matching audit records must show `degraded: false`, `fault_injected: null`, and an empty `failures` list.
**Why:** Fault headers are for testing. Either header affecting even one ordinary request would let a caller change how a submission is scored when the service is running with fault injection off.

*Italicized phrases in criterion 3 are clarifications added during review (which six requests; how a decision record is identified). They define terms; they don't change the target.*
