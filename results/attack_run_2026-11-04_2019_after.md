# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 20:19
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `e1eba6f5-f142-4886-9eb2-4c3e9c6d8dc1` | unsure | 0.137 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `ace757d5-5595-4f84-b51b-85b78e5cd9d4` | human | 0.353 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `317e8c85-dfa2-4444-b881-598d3f9b4469` | unsure | 0.019 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `bb14a7b1-456a-4672-952f-0335d9b299fd` | unsure | 0.311 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `7dae2294-3943-462b-b329-b26c34ff092d` | human | 0.470 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `03b1bccd-5755-44fb-b3f0-09817ed02e4d` | unsure | 0.127 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `b5d3240d-b070-4073-9b18-7f3db5f18396` | unsure | 0.214 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `29ec150d-11b3-4f0c-93d9-9de1775e7f30` | unsure | 0.000 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `d9ab3814-81b1-49b8-b6f0-ddacfb7563ca` | unsure | 0.137 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `67c14f62-a5cc-4ad1-aec2-5edc73a43bfd` | ai | 0.785 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `47b089d4-dee9-409e-8c87-1fbbe38a26be` | unsure | 0.060 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `bdb1ee93-08cf-4e02-b35e-6002a669b92c` | unsure | 0.435 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `b75aacb2-6a81-4aca-bd0d-7f84560e6162` | unsure | 0.377 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `d54f5880-b93f-465b-8692-225878b4ba15` | unsure | 0.366 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `00ce0a04-86d0-49d5-998d-3d624255834f` | unsure | 0.633 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `2c9ccd8e-9ac7-4e58-a628-2812fdbad117` | unsure | 0.315 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `86c15315-e47f-4ba0-9551-00ee95fc3b1b` | unsure | 0.482 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `55607c06-fb16-4a20-af02-ea291f0c2004` | unsure | 0.000 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c6ae93de-8254-4e65-81ee-52bf25d63e1b` | unsure | 0.237 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `57ac1f0d-9e88-47a0-b727-2513d6424ebf` | human | 0.662 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `1a2ed65f-a637-4f82-8965-3fc58c3cd9d2` | unsure | 0.149 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `e50598fe-8958-4f1b-8f7f-a7bce6a9afc1` | unsure | 0.291 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `bd21d785-3b39-43a5-b511-cbc47254bb70` | unsure | 0.231 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `b2be7e4d-9e21-4d99-a22a-2fcb303b8e8f` | unsure | 0.013 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 200 | `3a7bdc1c-c3a7-4f58-b5cb-8ae1b0b74e59` | unsure | 0.000 |  |
| MF03 | malformed | text is control characters | 200 | `89dc4619-5551-480e-a206-1345e018c2e5` | unsure | 0.000 |  |
| MF04 | malformed | text is only punctuation | 200 | `9440edbb-3ed2-467d-aa19-b844e8e1ab95` | unsure | 0.000 |  |
| MF05 | malformed | text is a very long single word | 200 | `77d01225-c52a-4e82-8d70-435c059c4d6a` | unsure | 0.000 |  |
| MF06 | malformed | text is emoji only | 200 | `dd2cb6b4-1176-4120-9484-a967b9887972` | unsure | 0.000 |  |
| MF07 | malformed | text is right-to-left script | 200 | `b39e7cb3-b939-4e16-af5c-9177b2f428ac` | unsure | 0.000 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bd8611d9-5900-42eb-b057-426ae3163215` | unsure | 0.000 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `197775ea-07ab-4a34-aa11-23baf2150067` | unsure | 0.000 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `71c5422b-a50a-4c41-acf4-f2e817daec40` | unsure | 0.000 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8449f843-049d-4e5a-8361-bce21f4f34f7` | unsure | 0.000 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c3fa15ed-d7a4-450a-a01e-3903242ebb92` | unsure | 0.000 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e5395a8c-b8f1-4a8c-b8aa-aaf445f7b4fd` | unsure | 0.000 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `640d8ad2-57d5-46ca-bbe1-1adc4925270f` | unsure | 0.000 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ab3506cc-ce65-4ea0-85a8-b53f9823e057` | unsure | 0.000 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cd0b123d-bd57-402c-9b85-fac3d0d90b17` | unsure | 0.000 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `764f1858-e0d3-477b-b111-e3746498c8c8` | unsure | 0.000 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
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
  "content_id": "e1eba6f5-f142-4886-9eb2-4c3e9c6d8dc1",
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
  "content_id": "ace757d5-5595-4f84-b51b-85b78e5cd9d4",
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
  "content_id": "317e8c85-dfa2-4444-b881-598d3f9b4469",
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
  "content_id": "bb14a7b1-456a-4672-952f-0335d9b299fd",
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
  "content_id": "7dae2294-3943-462b-b329-b26c34ff092d",
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
  "content_id": "03b1bccd-5755-44fb-b3f0-09817ed02e4d",
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
  "content_id": "b5d3240d-b070-4073-9b18-7f3db5f18396",
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
  "content_id": "29ec150d-11b3-4f0c-93d9-9de1775e7f30",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "d9ab3814-81b1-49b8-b6f0-ddacfb7563ca",
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
  "content_id": "67c14f62-a5cc-4ad1-aec2-5edc73a43bfd",
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
  "content_id": "47b089d4-dee9-409e-8c87-1fbbe38a26be",
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
  "content_id": "bdb1ee93-08cf-4e02-b35e-6002a669b92c",
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
  "content_id": "b75aacb2-6a81-4aca-bd0d-7f84560e6162",
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
  "content_id": "d54f5880-b93f-465b-8692-225878b4ba15",
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
  "content_id": "00ce0a04-86d0-49d5-998d-3d624255834f",
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
  "content_id": "2c9ccd8e-9ac7-4e58-a628-2812fdbad117",
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
  "content_id": "86c15315-e47f-4ba0-9551-00ee95fc3b1b",
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
  "content_id": "55607c06-fb16-4a20-af02-ea291f0c2004",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "c6ae93de-8254-4e65-81ee-52bf25d63e1b",
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
  "content_id": "57ac1f0d-9e88-47a0-b727-2513d6424ebf",
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
  "content_id": "1a2ed65f-a637-4f82-8965-3fc58c3cd9d2",
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
  "content_id": "e50598fe-8958-4f1b-8f7f-a7bce6a9afc1",
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
  "content_id": "bd21d785-3b39-43a5-b511-cbc47254bb70",
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
  "content_id": "b2be7e4d-9e21-4d99-a22a-2fcb303b8e8f",
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
  "status": 200,
  "content_id": "3a7bdc1c-c3a7-4f58-b5cb-8ae1b0b74e59",
  "creator_id": "attacker_MF02",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
  "label": "Our automated check couldn't tell whether this was written by a person or with help from AI. That's common: careful, formal, or short writing often lands here, and it is not a judgment about you or your work. Nothing happens to your submission because of this result. If you'd like a person to look at it, you can request a review.",
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "89dc4619-5551-480e-a206-1345e018c2e5",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "9440edbb-3ed2-467d-aa19-b844e8e1ab95",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "77d01225-c52a-4e82-8d70-435c059c4d6a",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "dd2cb6b4-1176-4120-9484-a967b9887972",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "b39e7cb3-b939-4e16-af5c-9177b2f428ac",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "bd8611d9-5900-42eb-b057-426ae3163215",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "197775ea-07ab-4a34-aa11-23baf2150067",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "71c5422b-a50a-4c41-acf4-f2e817daec40",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "8449f843-049d-4e5a-8361-bce21f4f34f7",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "c3fa15ed-d7a4-450a-a01e-3903242ebb92",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "e5395a8c-b8f1-4a8c-b8aa-aaf445f7b4fd",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "640d8ad2-57d5-46ca-bbe1-1adc4925270f",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "ab3506cc-ce65-4ea0-85a8-b53f9823e057",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "cd0b123d-bd57-402c-9b85-fac3d0d90b17",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
  "content_id": "764f1858-e0d3-477b-b111-e3746498c8c8",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0,
  "model_score": null,
  "style_score": null,
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
