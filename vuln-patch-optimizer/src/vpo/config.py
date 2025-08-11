from __future__ import annotations
import os, yaml
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class Config:
    policy: str = "balanced"
    waves: int = 3
    sla_days: int = 14

def load_config(path: str | None) -> Config:
    if not path:
        return Config()
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return Config(
        policy=data.get("policy", "balanced"),
        waves=int(data.get("waves", 3)),
        sla_days=int(data.get("sla_days", 14)),
    )
