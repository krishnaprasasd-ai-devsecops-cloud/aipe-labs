# Day 1 Lab: AIPE architecture layers

**Goal:** see one request pass through the layers of an AI platform and find which layer broke.

## Steps
1. `python layers.py` - a request goes gateway -> retrieval -> model -> guardrails; each layer logs its latency.
2. Break it: `FAIL_LAYER=retrieval python layers.py` (PowerShell: `$env:FAIL_LAYER="retrieval"; python layers.py`).
3. Read the log: the error names the failing layer, and the trace stops there. That is why layers + tracing matter.
4. Extend: add a `cache` layer before `model` and compare the trace.

## Cleanup
Nothing to clean up (stdlib only, no cloud resources).

Blog post: see `03-website-blog/drafts/day-001-aipe-architecture-layers.md`
