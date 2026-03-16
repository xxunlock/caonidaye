"""Application settings and configuration loader."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class Settings:
    """Global settings object loaded from YAML."""

    def __init__(self, data: dict[str, Any]):
        self.data = data

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Settings":
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(data)

    def get(self, dotted_key: str, default: Any = None) -> Any:
        node: Any = self.data
        for key in dotted_key.split('.'):
            if not isinstance(node, dict):
                return default
            node = node.get(key, default)
        return node
