import pytest

from .string_data_manipulators import *


@pytest.mark.string_manipulators
@pytest.mark.parametrize("data_dict, date_today, result", [
    (
            {'sunday': ['3:00-4:00'], 'tuesday': ['3:00-4:00']},
            datetime.today().replace(year=2023, month=7, day=5, hour=1, minute=50, second=0, microsecond=0),
            datetime.today().replace(year=2023, month=7, day=9, hour=3, minute=0, second=0, microsecond=0),

    ),
])
def test_get_nearest_lesson(data_dict: dict, date_today: datetime, result: datetime):
    assert get_nearest_lesson(data_dict, datetime_today=date_today) == result
