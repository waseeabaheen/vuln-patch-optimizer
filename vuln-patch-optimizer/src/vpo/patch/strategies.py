from __future__ import annotations
from typing import List, Dict, Any
import math

def plan_waves(normalized: List[Dict[str, Any]], waves: int = 3, policy: str = "balanced") -> List[List[Dict[str, Any]]]:
    # Simple policy logic:
    # - aggressive: prioritize by severity then cvss (desc)
    # - conservative: prioritize by severity then cvss (desc) but smaller first wave
    # - balanced: even split by severity bands
    items = sorted(normalized, key=lambda x: (x["severity"], x["cvss"]), reverse=True)

    if policy == "aggressive":
        chunk = math.ceil(len(items)/waves)
        return [items[i:i+chunk] for i in range(0, len(items), chunk)]

    if policy == "conservative":
        sizes = [max(1, math.floor(len(items)*0.2))] + [0]*(waves-1)
        remaining = len(items) - sizes[0]
        tail_chunk = math.ceil(remaining/(waves-1)) if waves>1 else remaining
        for i in range(1, waves):
            sizes[i] = tail_chunk
        out, idx = [], 0
        for s in sizes:
            out.append(items[idx:idx+s])
            idx += s
        return out

    # balanced
    # Split by severity buckets first
    buckets = {5:[],4:[],3:[],2:[],1:[]}
    for it in items:
        buckets[it["severity"]].append(it)
    # round-robin fill waves
    out = [[] for _ in range(waves)]
    w = 0
    for sev in [5,4,3,2,1]:
        for it in buckets[sev]:
            out[w % waves].append(it)
            w += 1
    return out
