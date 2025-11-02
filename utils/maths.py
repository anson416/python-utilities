from pydantic import validate_call


@validate_call
def clamp(num: float, a: float, b: float) -> float:
    if a > b:
        raise ValueError("`a` must be smaller than or equal to `b`")
    return max(a, min(num, b))
