import arrow
from . import words_to_numbers


def date_shift(numbers, unit, now=None):
    if now is None:
        now = arrow.utcnow()

    if unit[-1] != 's':
        unit = unit + 's'

    kwargs = {
        unit: words_to_numbers.text2int(numbers)
    }

    after_shift = now.replace(**kwargs)

    return after_shift
