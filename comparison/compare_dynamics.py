from dataclasses import dataclass


CORRECT = "correct"
TOO_SOFT = "too_soft"
TOO_LOUD = "too_loud"
UNKNOWN = "unknown"


DYNAMIC_LEVELS = {
    "pp": 1,
    "p": 2,
    "mp": 3,
    "mf": 4,
    "f": 5,
    "ff": 6,
}


@dataclass
class DynamicComparison:
    result: str
    difference: int|None

def compare_dynamic(expected_dynamic: str|None,played_dynamic: str|None,) -> DynamicComparison:

    if (
        expected_dynamic is None
        or played_dynamic is None
    ):
        return DynamicComparison(result=UNKNOWN,difference=None,)

    if (
        expected_dynamic not in DYNAMIC_LEVELS
        or played_dynamic not in DYNAMIC_LEVELS
    ):
        return DynamicComparison(result=UNKNOWN,difference=None,)

    difference = (DYNAMIC_LEVELS[played_dynamic] - DYNAMIC_LEVELS[expected_dynamic])

    if difference==0:
        return DynamicComparison(result=CORRECT,difference=0,)

    if difference>0:
        return DynamicComparison(result=TOO_LOUD,difference=difference,)

    return DynamicComparison(result=TOO_SOFT,difference=difference,)