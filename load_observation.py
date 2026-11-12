"""Capstone load observation (not a criterion): 4 slow faults sent at once,
then 3 healthy requests 0.5 s later, all concurrent. Do healthy requests
come back falsely degraded because the worker pool is full?"""
import json, threading, time, urllib.request, uuid, sys
import scenarios

BASE = "http://127.0.0.1:5000"
TEXT = scenarios.MY_WRITING[0]
label = sys.argv[1] if len(sys.argv) > 1 else "before"
results, lock = [], threading.Lock()

def send(kind, fault=None):
    headers = {"Content-Type": "application/json"}
    if fault:
        headers["X-Fault"] = fault
    body = {"text": TEXT, "creator_id": f"load_{uuid.uuid4().hex[:8]}"}
    req = urllib.request.Request(BASE + "/submit", data=json.dumps(body).encode(), headers=headers)
    t0 = time.perf_counter()
    with urllib.request.urlopen(req) as r:
        d = json.loads(r.read())
    with lock:
        results.append({"kind": kind, "secs": round(time.perf_counter() - t0, 2),
                        "degraded": d.get("degraded"), "failures": d.get("failures"),
                        "guess": d.get("guess")})

threads = [threading.Thread(target=send, args=("slow", "model_slow")) for _ in range(4)]
for t in threads: t.start()
time.sleep(0.5)
healthy = [threading.Thread(target=send, args=("healthy",)) for _ in range(3)]
for t in healthy: t.start()
for t in threads + healthy: t.join()

for r in sorted(results, key=lambda r: r["kind"]):
    print(json.dumps(r))
h = [r for r in results if r["kind"] == "healthy"]
print(f"\nhealthy requests degraded: {sum(1 for r in h if r['degraded'])} of {len(h)}")
json.dump(results, open(f"results/load_observation_{label}.json", "w"), indent=2)
