from __future__ import annotations
import json, sys, os, click
from tabulate import tabulate
from rich.console import Console
from .config import load_config
from .scanners.base import normalize
from .scanners.nessus import NessusScanner
from .scanners.qualys import QualysScanner
from .scanners.tenable import TenableScanner
from .patch.strategies import plan_waves
from .metrics import exposure_reduction, estimate_mttr_improvement, sla_compliance, count_criticals

console = Console()

@click.group()
@click.version_option()
def main():
    "Vulnerability Scanning & Patch Management Optimization CLI"

@main.command()
@click.option("--source", type=click.Choice(["nessus","qualys","tenable"]), default="nessus")
@click.option("--input", "input_path", type=click.Path(exists=True), help="Path to sample/raw findings JSON.")
@click.option("--out", "out_path", type=click.Path(), default="out/normalized.json")
def scan(source, input_path, out_path):
    "Fetch and normalize scanner findings."
    os.environ["VPO_SAMPLE"] = input_path or os.environ.get("VPO_SAMPLE","data/sample_assets.json")
    if source == "nessus":
        raw = NessusScanner().fetch_findings()
    elif source == "qualys":
        raw = QualysScanner().fetch_findings()
    else:
        raw = TenableScanner().fetch_findings()
    norm = normalize(raw)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(norm, f, indent=2)
    console.print(f"[bold green]Normalized[/bold green] {len(norm)} findings -> {out_path}")

@main.command()
@click.option("--input", "normalized_path", type=click.Path(exists=True), required=True, help="Normalized findings JSON.")
@click.option("--policy", type=click.Choice(["aggressive","balanced","conservative"]), default="balanced")
@click.option("--waves", type=int, default=3)
@click.option("--sla-days", type=int, default=14)
@click.option("--out", "plan_path", type=click.Path(), default="out/plan.json")
def plan(normalized_path, policy, waves, sla_days, plan_path):
    "Create a patch plan (waves) according to a policy."
    with open(normalized_path, "r", encoding="utf-8") as f:
        norm = json.load(f)
    waves_list = plan_waves(norm, waves=waves, policy=policy)
    os.makedirs(os.path.dirname(plan_path), exist_ok=True)
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(waves_list, f, indent=2)
    console.print(f"[bold cyan]Planned[/bold cyan] {len(waves_list)} waves -> {plan_path}")
    # Pretty print
    sizes = [len(w) for w in waves_list]
    table = [[i+1, sizes[i]] for i in range(len(sizes))]
    console.print(tabulate(table, headers=["Wave","Assets"], tablefmt="github"))

@main.command()
@click.option("--normalized", type=click.Path(exists=True), required=True)
@click.option("--plan", "plan_path", type=click.Path(exists=True), required=True)
@click.option("--baseline-days", type=int, default=30)
def metrics(normalized, plan_path, baseline_days):
    "Compute exposure reduction, MTTR improvement, and SLA compliance."
    import json
    with open(normalized, "r", encoding="utf-8") as f:
        norm = json.load(f)
    with open(plan_path, "r", encoding="utf-8") as f:
        waves = json.load(f)
    baseline_crit = count_criticals(norm)
    post_first = count_criticals(waves[0])
    red = exposure_reduction(baseline_crit, post_first)
    mttr_imp = estimate_mttr_improvement(baseline_days, len(waves))
    sla = sla_compliance(norm, 14, waves)
    table = [
        ["Criticals (baseline)", baseline_crit],
        ["Criticals (after wave 1)", post_first],
        ["Exposure reduction (%)", f"{red:.1f}"],
        ["MTTR improvement (%)", f"{mttr_imp:.1f}"],
        ["SLA compliance (%)", f"{sla:.1f}"],
    ]
    console.print(tabulate(table, headers=["Metric","Value"], tablefmt="github"))

if __name__ == "__main__":
    main()
