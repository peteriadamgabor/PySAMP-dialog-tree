from typing import Any


def try_pars_int(value: Any):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None
