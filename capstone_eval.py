"""
Capstone trials: tests criteria.md "Capstone criteria" exactly as written.

  --mode on   service started with AI201_FAULTS=1  -> criteria 1, 2, 3, 4
  --mode off  service started with AI201_FAULTS unset -> criterion 5

Three trials, one request at a time, fresh creator_id each time, 15 s wait
after every slow-fault response. Raw results go to results/.
"""
import argparse, json, time, urllib.request, uuid
import scenarios, scoring

BASE = "http://127.0.0.1:5000"
TEXT = scenarios.MY_WRITING[0]
BASELINE = json.load(open("results/unit8_baseline.json"))
FIELDS = ("model_score", "style_score", "combined_score", "confidence", "guess", "label")

def submit(fault=None):
    headers = {"Content-Type": "application/json"}
    if fault:
        headers["X-Fault"] = fault
    body = {"text": TEXT, "creator_id": f"cap_eval_{uuid.uuid4().hex[:8]}"}
    req = urllib.request.Request(BASE + "/submit", data=json.dumps(body).encode(), headers=headers)
    t0 = time.perf_counter()
    with urllib.request.urlopen(req) as r:
        status, data = r.status, json.loads(r.read())
    return status, data, round(time.perf_counter() - t0, 3)

def decision_records(cid):
    with urllib.request.urlopen(f"{BASE}/log?limit=2000") as r:
        entries = json.loads(r.read())["entries"]
    return [e for e in entries if e.get("content_id") == cid and "event" not in e]

def unsure_ok(status, data):
    return status == 200 and bool(data.get("content_id")) and data.get("guess") == "unsure" \
        and data.get("label") == scoring.LABEL_UNSURE

def matches_baseline(status, data):
    return status == 200 and all(data.get(k) == BASELINE[k] for k in FIELDS)

def healthy_record_ok(cid, need_fault_null=False):
    recs = decision_records(cid)
    if len(recs) != 1:
        return False
    r = recs[0]
    ok = r.get("degraded") is False and r.get("failures") == []
    return ok and (r.get("fault_injected") is None if need_fault_null else True)

def failure_record_ok(cid, fault, kind):
    recs = decision_records(cid)
    if len(recs) != 1:
        return False
    r = recs[0]
    fails = [f for f in r.get("failures", []) if f.get("signal") == "model"]
    return (r.get("degraded") is True and (r.get("duration_ms") or 0) > 0
            and r.get("fault_injected") == fault and len(fails) == 1
            and bool(fails[0].get("error")) and isinstance(fails[0].get("ms"), (int, float))
            and fails[0].get("kind") == kind)

def run_on(trial, raw):
    res = {}
    faulted = []
    c1 = []
    for _ in range(3):
        s, d, t = submit("model_error")
        c1.append(unsure_ok(s, d)); faulted.append((d.get("content_id"), "model_error", "error"))
        raw.append({"trial": trial, "criterion": 1, "status": s, "secs": t, "resp": d})
    c2 = []
    for _ in range(3):
        s, d, t = submit("model_slow")
        c2.append(unsure_ok(s, d) and t <= 6.0); faulted.append((d.get("content_id"), "model_slow", "timeout"))
        raw.append({"trial": trial, "criterion": 2, "status": s, "secs": t, "resp": d})
        time.sleep(15)
    c4 = []
    for _ in range(3):
        s, d, t = submit()
        c4.append(matches_baseline(s, d) and healthy_record_ok(d.get("content_id")))
        raw.append({"trial": trial, "criterion": 4, "status": s, "secs": t, "resp": d})
    c3 = [failure_record_ok(cid, f, k) for cid, f, k in faulted]
    res[1], res[2], res[3], res[4] = (sum(c1), 3), (sum(c2), 3), (sum(c3), 6), (sum(c4), 3)
    return res

def run_off(trial, raw):
    c5 = []
    for fault in ("model_error", "model_slow"):
        s, d, t = submit(fault)
        c5.append(matches_baseline(s, d) and healthy_record_ok(d.get("content_id"), need_fault_null=True))
        raw.append({"trial": trial, "criterion": 5, "header": fault, "status": s, "secs": t, "resp": d})
    return {5: (sum(c5), 2)}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["on", "off"], required=True)
    ap.add_argument("--label", default="before")
    a = ap.parse_args()
    raw, table = [], {}
    for trial in (1, 2, 3):
        res = run_on(trial, raw) if a.mode == "on" else run_off(trial, raw)
        for c, (got, of) in res.items():
            table.setdefault(c, []).append(f"{got}/{of}")
        print(f"trial {trial}: " + "  ".join(f"C{c} {g}/{o}" for c, (g, o) in res.items()))
    out = f"results/capstone_{a.label}_faults_{a.mode}.json"
    json.dump({"table": table, "raw": raw}, open(out, "w"), indent=2)
    print("\n| Criterion | Run 1 | Run 2 | Run 3 |")
    for c, runs in table.items():
        print(f"| {c} | " + " | ".join(runs) + " |")
    slow = [x["secs"] for x in raw if x["criterion"] == 2]
    if slow:
        print(f"\ncriterion 2 elapsed seconds: {slow}")
    print(f"\nwrote {out}")
