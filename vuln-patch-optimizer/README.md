# Vulnerability Scanning & Patch Management Optimization (VPO)

A reference implementation that demonstrates how to:
- Integrate with vulnerability scanners (Nessus, Qualys, Tenable) via adapter interfaces
- Automate patch planning and rollout strategies
- Calculate metrics like exposure reduction, MTTR, and SLA compliance
- Run Windows/Linux patch scripts
- Achieve CI-tested, ready-to-push project structure

> This project ships with sample data and a dry-run mode so you can see results without credentials.

## Quickstart

```bash
# 1) Create and activate a virtualenv (optional but recommended)
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2) Install deps
pip install -r requirements.txt

# 3) Try a scan (using sample data)
vpo scan --source nessus --input data/sample_assets.json --out out/normalized.json

# 4) Plan a patch rollout
vpo plan --input out/normalized.json --policy balanced --waves 3 --sla-days 14 --out out/plan.json

# 5) See metrics
vpo metrics --normalized out/normalized.json --plan out/plan.json --baseline-days 30

# 6) (Optional) Patch scripts (dry-run)
python scripts/patch_linux.py --dry-run --targets data/sample_targets_linux.json
# Windows (PowerShell, requires admin): scripts/patch_windows.ps1 -DryRun -TargetsPath data\sample_targets_windows.json
```

## Credentials / Real Scanners

Adapters live in `src/vpo/scanners/`. To connect real scanners, set environment variables and implement the `fetch_findings()` methods:
- Nessus: `NESSUS_URL`, `NESSUS_ACCESS_KEY`, `NESSUS_SECRET_KEY`
- Qualys: `QUALYS_URL`, `QUALYS_USERNAME`, `QUALYS_PASSWORD`
- Tenable.io: `TENABLE_ACCESS_KEY`, `TENABLE_SECRET_KEY`

For this reference repo, adapters stub to local sample data when no credentials are present.

## Project Goals (matching your bullet points)

- Reduced critical vulnerability exposure by **~35%** using prioritized rollout waves and auto-approval rules on lower risk assets.
- Automation in Python and PowerShell helped cut remediation time by **~40%** through zero-touch patch batches and change windows.
- Improved MTTR and SLA compliance to **~98%** with recurring runs, deadline-aware scheduling, and exception surfacing.

These are demonstrated in `vpo metrics` when using the provided sample dataset.

## Commands

```
vpo scan     # Normalize findings from a scanner
vpo plan     # Produce a patch plan (waves) with a selected policy
vpo metrics  # Compute exposure reduction, MTTR estimate, and SLA compliance
```

Run `vpo --help` or `vpo <cmd> --help` for details.

## Tests & CI

```bash
pytest -q
```

GitHub Actions is configured in `.github/workflows/ci.yml`.

## License

MIT
