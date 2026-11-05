"""Read a run_eval report and print status codes, combined scores, and medians.
Reads the report file only; sends nothing to the service."""
import json, re, statistics, sys

path = sys.argv[1]
text = open(path).read()
medians = {}

for section in re.split(r"^### ", text, flags=re.M)[1:]:
    name = section.splitlines()[0].strip()
    trials = re.findall(r"\*\*Trial (\d)\*\*\s*```json\n(.*?)```", section, re.S)
    for t, block in trials:
        rows = json.loads(block)
        statuses = [r.get("status") for r in rows]
        combined = [round((r["model_score"] + r["style_score"]) / 2, 3)
                    if r.get("model_score") is not None else None for r in rows]
        print(f"{name:<16} trial {t}  status {statuses}")
        if any(c is not None for c in combined):
            print(f"{'':<16}          combined {combined}")
        scored = [c for c in combined if c is not None]
        if scored:
            medians.setdefault(name, []).append(statistics.median(scored))
    print()

for name, ms in medians.items():
    print(f"median combined, {name:<16}: {ms}")
if "spread_ai" in medians and "spread_human" in medians:
    gaps = [round(a - h, 3) for a, h in zip(medians["spread_ai"], medians["spread_human"])]
    print(f"\nmedian gap (AI - human) per trial: {gaps}   target: >= 0.30")
