from typing import Dict, Any, Optional


def merge_dicts(*dicts: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for d in dicts:
        result.update(d or {})
    return result
