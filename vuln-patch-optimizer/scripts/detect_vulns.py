# Demo script that reads a normalized file and prints top criticals
import json, sys
path = sys.argv[1] if len(sys.argv) > 1 else "out/normalized.json"
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
crit = [x for x in data if x.get("severity",0) >= 4]
print(f"Critical findings: {len(crit)}")
top = sorted(crit, key=lambda x: x["cvss"], reverse=True)[:10]
for t in top:
    print(f"- {t['asset_id']} {t['vuln_id']} (sev {t['severity']} cvss {t['cvss']})")
