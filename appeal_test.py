"""Criterion 4: 5 of 5 appeals with a real content_id set status to under_review
and are logged; an unknown content_id returns 404. Three trials."""
import json, urllib.request, urllib.error

BASE = "http://127.0.0.1:5000"
TEXT = ("I finished the reading for class this week and I have a few questions "
        "about the second chapter, especially the part about how the model handles "
        "short inputs and what happens when two signals disagree with each other.")

def post(path, body):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")

def log_for(cid):
    with urllib.request.urlopen(f"{BASE}/log?limit=500") as r:
        return [e for e in json.loads(r.read())["entries"] if e.get("content_id") == cid]

for trial in (1, 2, 3):
    passed = 0
    for i in range(1, 6):
        _, sub = post("/submit", {"text": TEXT, "creator_id": f"eval_appeal_t{trial}_{i}"})
        cid = sub["content_id"]
        status, ap = post("/appeal", {"content_id": cid, "reasoning": f"I wrote this myself (trial {trial}, #{i})."})
        logged = any(e.get("event") == "appeal" and e.get("status") == "under_review" for e in log_for(cid))
        ok = status == 200 and ap.get("status") == "under_review" and logged
        passed += ok
        print(f"trial {trial} appeal {i}: http {status}, status {ap.get('status')}, logged {logged} -> {'PASS' if ok else 'FAIL'}")
    s404, _ = post("/appeal", {"content_id": f"does-not-exist-{trial}", "reasoning": "test"})
    print(f"trial {trial}: {passed}/5 appeals recorded; unknown id -> http {s404}\n")
