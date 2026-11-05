# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 19:35
- Auto-marked BROKE (5xx, crash, no response): **1**
- Left for you to judge: **55**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `74d10607-375c-4a80-ba46-f1698550bb90` | unsure | 0.137 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `7d9c990f-0cba-414c-8222-f2019f181218` | human | 0.353 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `97da0084-710f-4c68-9f38-8aa53400b13b` | unsure | 0.019 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `8cbbdf40-0c5a-45de-9211-0f1dd5ac3a0e` | unsure | 0.311 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `93d5107a-1303-4236-abe7-0b0704693e82` | human | 0.470 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `85901ca9-b6cf-4d85-9ff5-13f9d5e56231` | unsure | 0.127 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `d4e4b1b6-d807-4678-be44-e2e48f4a02a2` | unsure | 0.214 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `6e1fb93d-d748-4818-b557-a1185fcd9a33` | unsure | 0.000 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `b86dede5-c9d7-4896-871a-3fb7e1367149` | unsure | 0.137 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c115a420-55d6-4c5d-8349-1e65319874f0` | ai | 0.785 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `0ad97866-aec0-4645-b6a4-5a4d0cee8b20` | unsure | 0.060 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `9d262dd8-1eec-4de4-b1f0-2460341760eb` | unsure | 0.435 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `a3415e8e-d70f-4235-ae94-c80337aa2b5e` | unsure | 0.377 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `537827d7-cacc-4ab2-a602-5a9b2da1e3a0` | unsure | 0.366 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `ce669c3d-cd2b-427e-b3b2-a563b1f10f15` | unsure | 0.633 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `85dc973a-8558-4fce-9f87-47cefa6c5e58` | unsure | 0.315 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `4681c26c-d695-4f09-94b9-53a4818a7ffb` | unsure | 0.482 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `8c3cc21a-6119-49e3-84f7-4dbf9d11385a` | unsure | 0.000 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `1b221b86-5375-4988-89cb-d3efd2c302ff` | unsure | 0.237 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `02f91c45-fb43-4187-ba8d-30157903dc95` | human | 0.662 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `037f1795-c80f-44d3-8d8c-58ff986c1255` | unsure | 0.149 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `e3bec112-9c4b-4f50-bf8b-496f0b40d855` | unsure | 0.291 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `970d01a5-8e71-4cc2-8c97-804d29a3f330` | unsure | 0.231 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `e598ecf2-14b6-40c0-8c50-d8a4932eca01` | unsure | 0.013 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `02fcac72-ae32-4bde-b26b-84dcfaf6e85e` | unsure | 0.000 |  |
| MF04 | malformed | text is only punctuation | 200 | `030baedd-0b27-4f9b-af4c-6bdb5e47ec8e` | unsure | 0.000 |  |
| MF05 | malformed | text is a very long single word | 200 | `c059a9ba-d2a2-468c-b4e1-7e4f7505a06b` | unsure | 0.000 |  |
| MF06 | malformed | text is emoji only | 200 | `b9309e2d-9a73-4a19-9f65-5b98d846b139` | unsure | 0.000 |  |
| MF07 | malformed | text is right-to-left script | 200 | `abb2a0a1-8eca-4aaf-b8d6-cbc46938532b` | unsure | 0.000 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `846fb0bf-d50c-4a5f-8c75-418c1924c6d8` | unsure | 0.000 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e79f5885-5e6d-4080-bbd2-2fedcbec97dd` | unsure | 0.000 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `007e138d-f8e0-4c4a-ab1f-72f60737f0f2` | unsure | 0.000 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `48c2c11c-09c6-42b6-8cf5-12aabd2cd594` | unsure | 0.000 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `969fb25c-b5f8-4541-8072-b9f1535a9413` | unsure | 0.000 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b5fc0ba1-e816-4e3a-98a3-36753f5ed204` | unsure | 0.000 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `841fb7b7-0cdf-4a75-93b9-5e219cadd6bd` | unsure | 0.000 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5a25be2b-372c-45e4-81d1-281714cc60ff` | unsure | 0.000 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `62cfe1a0-d700-46b7-8c63-e1fa6ab44b1f` | unsure | 0.000 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a151b152-0f97-4114-b18f-1c1ab66335cc` | unsure | 0.000 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 1 | 19 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "74d10607-375c-4a80-ba46-f1698550bb90",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.1365,
  "model_score": 0.1635,
  "style_score": 0.7,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "7d9c990f-0cba-414c-8222-f2019f181218",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.353,
  "model_score": 0.5943,
  "style_score": 0.0527,
  "label": "Our automated check found that this writing reads like it was written by a person. No action is needed.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "97da0084-710f-4c68-9f38-8aa53400b13b",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.0187,
  "model_score": 0.6662,
  "style_score": 0.3151,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "8cbbdf40-0c5a-45de-9211-0f1dd5ac3a0e",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.3114,
  "model_score": 0.6114,
  "style_score": 0.7,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "93d5107a-1303-4236-abe7-0b0704693e82",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.4703,
  "model_score": 0.3212,
  "style_score": 0.2085,
  "label": "Our automated check found that this writing reads like it was written by a person. No action is needed.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "85901ca9-b6cf-4d85-9ff5-13f9d5e56231",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.1273,
  "model_score": 0.5727,
  "style_score": 0.3,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "d4e4b1b6-d807-4678-be44-e2e48f4a02a2",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.2138,
  "model_score": 0.5862,
  "style_score": 0.2,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "6e1fb93d-d748-4818-b557-a1185fcd9a33",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.2452,
  "style_score": 0.6172,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "b86dede5-c9d7-4896-871a-3fb7e1367149",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.1367,
  "model_score": 0.7042,
  "style_score": 0.4325,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "c115a420-55d6-4c5d-8349-1e65319874f0",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.7853,
  "model_score": 0.9792,
  "style_score": 0.8061,
  "label": "Our automated check thinks this writing was likely produced with help from AI. Automated checks can be wrong, and this is not a final decision. If you wrote this yourself, you can request a human review and tell us how you wrote it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "0ad97866-aec0-4645-b6a4-5a4d0cee8b20",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.06,
  "model_score": 0.6175,
  "style_score": 0.4425,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "9d262dd8-1eec-4de4-b1f0-2460341760eb",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.4348,
  "model_score": 0.7387,
  "style_score": 0.6961,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "a3415e8e-d70f-4235-ae94-c80337aa2b5e",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.3769,
  "model_score": 0.8051,
  "style_score": 0.5718,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "537827d7-cacc-4ab2-a602-5a9b2da1e3a0",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.3662,
  "model_score": 0.8329,
  "style_score": 0.5333,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "ce669c3d-cd2b-427e-b3b2-a563b1f10f15",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6328,
  "model_score": 0.8005,
  "style_score": 0.8323,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "85dc973a-8558-4fce-9f87-47cefa6c5e58",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.315,
  "model_score": 0.8814,
  "style_score": 0.4336,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "4681c26c-d695-4f09-94b9-53a4818a7ffb",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.4816,
  "model_score": 0.8816,
  "style_score": 0.6,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "8c3cc21a-6119-49e3-84f7-4dbf9d11385a",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.3223,
  "style_score": 0.467,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "1b221b86-5375-4988-89cb-d3efd2c302ff",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.2375,
  "model_score": 0.4625,
  "style_score": 0.3,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "02f91c45-fb43-4187-ba8d-30157903dc95",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.6623,
  "model_score": 0.2044,
  "style_score": 0.1333,
  "label": "Our automated check found that this writing reads like it was written by a person. No action is needed.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "037f1795-c80f-44d3-8d8c-58ff986c1255",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.1488,
  "model_score": 0.5943,
  "style_score": 0.2569,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "e3bec112-9c4b-4f50-bf8b-496f0b40d855",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.291,
  "model_score": 0.4998,
  "style_score": 0.2092,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "970d01a5-8e71-4cc2-8c97-804d29a3f330",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.2313,
  "model_score": 0.6401,
  "style_score": 0.1286,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "e598ecf2-14b6-40c0-8c50-d8a4932eca01",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.0129,
  "model_score": 0.5583,
  "style_score": 0.4546,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "02fcac72-ae32-4bde-b26b-84dcfaf6e85e",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "030baedd-0b27-4f9b-af4c-6bdb5e47ec8e",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "c059a9ba-d2a2-468c-b4e1-7e4f7505a06b",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "b9309e2d-9a73-4a19-9f65-5b98d846b139",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.9969,
  "style_score": 0.8,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "abb2a0a1-8eca-4aaf-b8d6-cbc46938532b",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.9064,
  "style_score": 0.8,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "846fb0bf-d50c-4a5f-8c75-418c1924c6d8",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "e79f5885-5e6d-4080-bbd2-2fedcbec97dd",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "007e138d-f8e0-4c4a-ab1f-72f60737f0f2",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "48c2c11c-09c6-42b6-8cf5-12aabd2cd594",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "969fb25c-b5f8-4541-8072-b9f1535a9413",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "b5fc0ba1-e816-4e3a-98a3-36753f5ed204",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "841fb7b7-0cdf-4a75-93b9-5e219cadd6bd",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "5a25be2b-372c-45e4-81d1-281714cc60ff",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "62cfe1a0-d700-46b7-8c63-e1fa6ab44b1f",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "a151b152-0f97-4114-b18f-1c1ab66335cc",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
