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


def easily_readable_time(dt):
    # Make sure we have an instance of arrow
    if not isinstance(dt, arrow.Arrow):
        dt = arrow.get(dt)

    # Capitalizing AM/PM forces TTS to say "am" as "A M"
    dt_format = 'h mm A'
    # Remove 00 if minutes are 0
    if dt.format('mm') == '00':
        dt_format = 'h A'

    return dt.format(dt_format)
