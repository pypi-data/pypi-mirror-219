from datetime import datetime, timedelta

WEEK_DAYS = (
    "monday", "tuesday", "wednesday", "thursday",
    "friday", "saturday", "sunday"
)


def get_nearest_lesson(*args, datetime_today=None):
    """
        This script returns nearst lesson from iterable,
        for example, if user lessons iterable object is -> {'sunday': ['3:00-4:00'], 'tuesday': ['3:00-4:00']}
        and today is friday, then nearest lesson will be 'sunday': ['3:00-4:00']
    :param args:
    :return:
    """

    if not args:
        return None

    week_day_index = datetime_today.weekday() \
        if datetime_today else datetime.today().weekday()

    user_lessons_graph_dict, = args

    days_remaining_to_next_lesson = 0

    while True:
        try:
            week_day = WEEK_DAYS[week_day_index]
            if week_day in user_lessons_graph_dict:
                today = datetime_today or datetime.today()

                lesson_time = user_lessons_graph_dict[week_day][0].split(":")

                lesson_datetime = today + timedelta(days=days_remaining_to_next_lesson)
                lesson_datetime = lesson_datetime.replace(
                    hour=int(lesson_time[0]), minute=int(lesson_time[-1])
                ).replace(second=0, microsecond=0)

                return lesson_datetime

            week_day_index += 1

        except IndexError:
            week_day_index = 0

        finally:
            if days_remaining_to_next_lesson >= 7:
                return None

            days_remaining_to_next_lesson += 1
