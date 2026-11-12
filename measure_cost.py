"""Capstone: measure the cost of one run as seconds of compute.
Sends 10 identical realistic submissions, then reads each one's server-side
duration_ms, model_ms and style_ms back from the audit log."""
import json, statistics, time, urllib.request
import scenarios

BASE = "http://127.0.0.1:5000"
TEXT = scenarios.MY_WRITING[0]          # ~250-word statement of purpose
N = 10

def post(body):
    req = urllib.request.Request(BASE + "/submit", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.perf_counter()
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
    return data, round((time.perf_counter() - t0) * 1000, 1)

ids, client_ms = [], []
for i in range(1, N + 1):
    data, ms = post({"text": TEXT, "creator_id": f"cost_run_{i}"})
    ids.append(data["content_id"]); client_ms.append(ms)

with urllib.request.urlopen(f"{BASE}/log?limit=200") as r:
    entries = {e.get("content_id"): e for e in json.loads(r.read())["entries"]}

rows = [entries[c] for c in ids]
server = [e["duration_ms"] for e in rows]
model = [e["model_ms"] for e in rows]
style = [e["style_ms"] for e in rows]

print(f"{N} runs, {rows[0]['word_count']} words each, degraded in {sum(e['degraded'] for e in rows)} of {N}")
for i, (s, m, st, c) in enumerate(zip(server, model, style, client_ms), 1):
    print(f"  run {i:>2}: server {s:>7} ms   model {m:>7} ms   style {st:>5} ms   client {c:>7} ms")
print(f"\nserver duration_ms: mean {statistics.mean(server):.1f}, median {statistics.median(server):.1f}, min {min(server)}, max {max(server)}")
print(f"model_ms mean {statistics.mean(model):.1f}  |  style_ms mean {statistics.mean(style):.2f}")
print(f"client round trip mean {statistics.mean(client_ms):.1f} ms")
