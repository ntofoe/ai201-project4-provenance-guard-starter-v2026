"""
Capstone (Shape B): run one signal so it can't take down the request.

run_signal() calls a signal on a worker thread and waits at most
config.SIGNAL_TIMEOUT_SECONDS. It never raises. It returns:

    (score, None, elapsed_ms)      on success: a finite score in [0, 1]
    (None, failure, elapsed_ms)    on failure: failure is a dict with
                                   signal, kind ("error" | "timeout" | "bad_value"),
                                   error (short message), ms

Limitation (declared out of scope): on timeout we stop WAITING; the signal
keeps running in the background and holds a worker until it finishes.
"""
import concurrent.futures as cf
import math
import time

import config

_pool = cf.ThreadPoolExecutor(max_workers=config.SIGNAL_WORKERS,
                              thread_name_prefix="signal")

FAULTS = {"model_error", "model_slow", "style_error", "style_slow"}


def _inject(name, fn, fault):
    """Swap in a broken or slow version of the signal, only if fault injection is on."""
    if not (config.FAULT_INJECTION_ENABLED and fault):
        return fn
    if fault == f"{name}_error":
        def broken(text):
            raise RuntimeError(f"injected fault: {name} signal failed")
        return broken
    if fault == f"{name}_slow":
        def slow(text):
            time.sleep(config.FAULT_SLOW_SECONDS)
            return fn(text)
        return slow
    return fn


def _ms(t0):
    return round((time.perf_counter() - t0) * 1000, 1)


def run_signal(name, fn, text, fault=None):
    call = _inject(name, fn, fault)
    t0 = time.perf_counter()
    future = _pool.submit(call, text)
    try:
        raw = future.result(timeout=config.SIGNAL_TIMEOUT_SECONDS)
    except cf.TimeoutError:
        ms = _ms(t0)
        return None, {"signal": name, "kind": "timeout",
                      "error": f"no result after {config.SIGNAL_TIMEOUT_SECONDS}s",
                      "ms": ms}, ms
    except Exception as e:  # any error inside the signal
        ms = _ms(t0)
        return None, {"signal": name, "kind": "error",
                      "error": f"{type(e).__name__}: {e}"[:200], "ms": ms}, ms

    ms = _ms(t0)
    try:
        score = float(raw)
    except (TypeError, ValueError):
        return None, {"signal": name, "kind": "bad_value",
                      "error": f"not a number: {raw!r}"[:200], "ms": ms}, ms
    if not math.isfinite(score) or not 0.0 <= score <= 1.0:
        return None, {"signal": name, "kind": "bad_value",
                      "error": f"out of range: {score!r}", "ms": ms}, ms
    return score, None, ms


if __name__ == "__main__":
    # Terminal test: run both signals normally, then under each fault.
    import detector
    import stylometry

    config.FAULT_INJECTION_ENABLED = True   # for this test only
    text = ("Artificial intelligence is transforming the way we live and work. "
            "It offers many benefits, including increased efficiency and improved "
            "decision-making. However, it also raises important ethical questions "
            "that society must address.")

    print("warming up the model...")
    detector.model_signal(text)

    for fault in [None, "model_error", "style_error", "model_slow", "style_slow"]:
        m = run_signal("model", detector.model_signal, text, fault)
        s = run_signal("style", stylometry.style_signal, text, fault)
        print(f"\nfault={fault}")
        print(f"  model: score={m[0]}  failure={m[1]}  ms={m[2]}")
        print(f"  style: score={s[0]}  failure={s[1]}  ms={s[2]}")
