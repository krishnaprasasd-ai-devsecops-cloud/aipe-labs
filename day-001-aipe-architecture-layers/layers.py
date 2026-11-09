"""Day 1 lab: one request travelling through the AIPE layers (stdlib only).
Run:  python layers.py
Break/fix: set FAIL_LAYER=retrieval  (Windows: $env:FAIL_LAYER="retrieval") and watch which layer reports the failure."""
import os, time, logging, json

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("aipe")

def layer(name):
    def deco(fn):
        def wrap(ctx):
            t = time.perf_counter()
            if os.getenv("FAIL_LAYER") == name:
                raise RuntimeError(f"{name} layer failed (injected)")
            out = fn(ctx)
            ms = (time.perf_counter() - t) * 1000
            ctx["trace"].append({"layer": name, "ms": round(ms, 2)})
            log.info("layer=%s ms=%.2f", name, ms)
            return out
        return wrap
    return deco

@layer("gateway")
def gateway(ctx):  ctx["user"] = "krishna"; return ctx            # auth, rate limit
@layer("retrieval")
def retrieval(ctx): ctx["docs"] = ["AIPE = build + run AI systems"]; return ctx   # RAG stub
@layer("model")
def model(ctx):    ctx["answer"] = f"Answer using {len(ctx['docs'])} doc(s)"; return ctx  # LLM stub
@layer("guardrails")
def guardrails(ctx): ctx["safe"] = "password" not in ctx["answer"].lower(); return ctx

def handle(question):
    ctx = {"q": question, "trace": []}
    try:
        for step in (gateway, retrieval, model, guardrails):
            ctx = step(ctx)
    except RuntimeError as e:
        log.error("request failed: %s", e); ctx["error"] = str(e)
    return ctx

if __name__ == "__main__":
    print(json.dumps(handle("What is an AI Platform Engineer?"), indent=2))
