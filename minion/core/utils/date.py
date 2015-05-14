import arrow
from . import words_to_numbers


def date_shift(numbers, unit, now=None):
    if now is None:
        now = arrow.utcnow()

    # Arrow expects the unit to be plural for it to shift
    if unit[-1] != 's':
        unit = unit + 's'

    # Let it raise IllegalWordException if words aren't valid numbers
    kwargs = {
        unit: words_to_numbers.text2int(numbers)
    }

    after_shift = now.replace(**kwargs)

    return after_shift
