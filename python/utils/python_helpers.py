from typing import Any


def try_pars_int(value: Any) -> int | None:
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def try_pars_float(value: Any) -> float | None:
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def format_numbers(value: Any) -> str | None:
    return format(value, '3_d').replace("_", " ")