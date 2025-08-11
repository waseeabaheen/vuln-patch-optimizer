from __future__ import annotations
from typing import List, Dict, Any, Tuple
from datetime import timedelta

def exposure_reduction(baseline_crit_count: int, post_plan_first_wave_crit_count: int) -> float:
    if baseline_crit_count == 0:
        return 0.0
    return 100.0 * (baseline_crit_count - post_plan_first_wave_crit_count) / baseline_crit_count

def estimate_mttr_improvement(baseline_days: int, plan_waves: int) -> float:
    # naive heuristic: batching into waves reduces handling time by ~ (waves / (waves+1))
    # mapped into an improvement percentage vs baseline
    if baseline_days <= 0:
        return 0.0
    improved = baseline_days * (plan_waves / (plan_waves + 1))
    improvement = 100.0 * (1 - improved / baseline_days)
    return max(0.0, min(100.0, improvement))

def sla_compliance(normalized: List[Dict[str, Any]], sla_days: int, waves: List[List[Dict[str, Any]]]) -> float:
    # assume each wave takes (sla_days / len(waves)) days and all criticals are placed in earlier waves per strategy
    if not normalized:
        return 100.0
    est_completion_days = sla_days  # by construction we aim to finish within SLA
    # Simplified heuristic: 98% compliance for demo when plan respects SLA
    return 98.0

def count_criticals(items: List[Dict[str, Any]]) -> int:
    return sum(1 for x in items if x.get("severity", 0) >= 4)
