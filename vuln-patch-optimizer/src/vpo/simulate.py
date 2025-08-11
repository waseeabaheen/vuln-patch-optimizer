from __future__ import annotations
import random
def generate_sample(n_assets: int = 50, seed: int = 42):
    random.seed(seed)
    items = []
    for i in range(n_assets):
        items.append({
            "asset_id": f"asset-{i:03d}",
            "severity": random.choices([1,2,3,4,5], weights=[5,10,25,30,30])[0],
            "vuln": f"CVE-20{random.randint(19,25)}-{random.randint(1000,9999)}",
            "cvss": round(random.uniform(4.0, 10.0), 1),
            "title": "Sample Vulnerability"
        })
    return items
