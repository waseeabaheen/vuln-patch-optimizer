from __future__ import annotations
import os, json
from typing import List, Dict, Any
from .base import Scanner

class QualysScanner(Scanner):
    def fetch_findings(self) -> List[Dict[str, Any]]:
        sample_path = os.environ.get("VPO_SAMPLE", "data/sample_assets.json")
        with open(sample_path, "r", encoding="utf-8") as f:
            return json.load(f)
