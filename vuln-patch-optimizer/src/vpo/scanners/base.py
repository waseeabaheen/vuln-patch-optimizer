from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class Scanner(ABC):
    @abstractmethod
    def fetch_findings(self) -> List[Dict[str, Any]]:
        ...

def normalize(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    # Expected normalized keys: asset_id, severity (1-5), vuln_id, cvss, title
    out = []
    for f in findings:
        item = {
            "asset_id": f.get("asset_id") or f.get("host") or f.get("ip"),
            "severity": int(f.get("severity", f.get("risk", 3))),
            "vuln_id": f.get("plugin_id") or f.get("qid") or f.get("vuln", "unknown"),
            "cvss": float(f.get("cvss", 7.0)),
            "title": f.get("title", "Untitled"),
        }
        out.append(item)
    return out
