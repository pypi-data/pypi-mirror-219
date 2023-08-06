import inspect
from typing import Any

from docstring_parser import parse


def parse_description(o: Any):
    try:
        s = inspect.getdoc(o)
    except Exception:
        return ""
    p = parse(s)
    des = " ".join([(p.short_description or ""), (p.long_description or "")])
    return des.strip()
