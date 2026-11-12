"""Capstone criterion 4: capture the final Unit 8 version's healthy response
to the standard sample, so capstone responses can be compared against it."""
import json, urllib.request
import scenarios

BODY = {"text": scenarios.MY_WRITING[0], "creator_id": "baseline_unit8"}
req = urllib.request.Request("http://127.0.0.1:5000/submit", data=json.dumps(BODY).encode(),
                             headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req) as r:
    status, data = r.status, json.loads(r.read())

baseline = {"source_commit": "6ab06cf (final Unit 8)", "http_status": status}
for k in ("model_score", "style_score", "combined_score", "confidence", "guess", "label"):
    baseline[k] = data.get(k)

with open("results/unit8_baseline.json", "w") as f:
    json.dump(baseline, f, indent=2)
print(json.dumps(baseline, indent=2))
