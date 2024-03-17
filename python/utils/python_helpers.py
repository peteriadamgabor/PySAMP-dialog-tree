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


# Print iterations progress
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='=', printEnd="\n"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}%% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
