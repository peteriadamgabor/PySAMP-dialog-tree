from typing import Any


def try_pars_int(value: Any):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def try_pars_float(value: Any):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None
