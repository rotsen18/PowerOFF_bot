from datetime import time, datetime, timedelta
from enum import Enum


class PowerOFF:
    class PowerAvailability(Enum):
        OFF = 'Нема'
        MAYBE_OFF = 'Можливо'
        ON = 'Є'

    SCHEDULE_GROUP_1 = {
        0: {
            (0, 9, 10, 11, 12, 21, 22, 23): PowerAvailability.MAYBE_OFF,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.OFF,
            (5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.ON
        },
        1: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.OFF,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.ON,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.MAYBE_OFF
        },
        2: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.ON,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.MAYBE_OFF,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.OFF
        },
        3: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.MAYBE_OFF,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.OFF,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.ON
        },
        4: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.OFF,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.ON,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.MAYBE_OFF
        },
        5: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.ON,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.MAYBE_OFF,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.OFF
        },
        6: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.MAYBE_OFF,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.OFF,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.ON
        },
    }
    SCHEDULE_GROUP_2 = {
        0: {
            (0, 9, 10, 11, 12, 21, 22, 23): PowerAvailability.OFF,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.ON,
            (5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.MAYBE_OFF
        },
        1: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.ON,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.MAYBE_OFF,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.OFF
        },
        2: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.MAYBE_OFF,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.OFF,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.ON
        },
        3: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.OFF,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.ON,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.MAYBE_OFF
        },
        4: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.ON,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.MAYBE_OFF,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.OFF
        },
        5: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.MAYBE_OFF,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.OFF,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.ON
        },
        6: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.OFF,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.ON,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.MAYBE_OFF
        },
    }
    SCHEDULE_GROUP_3 = {
        0: {
            (0, 9, 10, 11, 12, 21, 22, 23): PowerAvailability.ON,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.MAYBE_OFF,
            (5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.OFF
        },
        1: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.MAYBE_OFF,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.OFF,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.ON
        },
        2: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.OFF,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.ON,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.MAYBE_OFF
        },
        3: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.ON,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.MAYBE_OFF,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.OFF
        },
        4: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.MAYBE_OFF,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.OFF,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.ON
        },
        5: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.OFF,
            (1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.ON,
            (0, 5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.MAYBE_OFF
        },
        6: {
            (9, 10, 11, 12, 21, 22, 23): PowerAvailability.ON,
            (0, 1, 2, 3, 4, 13, 14, 15, 16): PowerAvailability.MAYBE_OFF,
            (5, 6, 7, 8, 17, 18, 19, 20): PowerAvailability.OFF
        },
    }

    @classmethod
    def day_data(cls, group_id: int, weekday: int) -> list:
        schedule = cls._get_schedule(group_id)
        day_schedule = schedule.get(weekday)
        day_schedule_list = []
        for hours, status in day_schedule.items():
            day_schedule_list.extend([[time(hour), status.value] for hour in hours])
        return day_schedule_list

    @staticmethod
    def format_day_schedule(schedule: list, day: int) -> list:
        hours_list = schedule.copy()
        hours_list.sort()
        new_list = [hours_list[0]]
        for current_item in hours_list[1:]:
            previous_item = new_list[-1]
            if not current_item[1] == previous_item[1]:
                prev_time = current_item[0]
                last_item = [time(prev_time.hour - 1, 59), previous_item[1]]
                new_list.append(last_item)
            new_list.append(current_item)
        last_item = new_list[-1]
        last_time = last_item[0]
        last_corrected_item = [time(last_time.hour, 59), last_item[1]]
        new_list.append(last_corrected_item)
        now = datetime.now()
        if day == now.weekday():
            new_list.append([now.time(), 'ЗАРАЗ'])
        new_list.sort()
        result_list = []
        for item in new_list:
            time_value = item[0].strftime('%H:%M')
            status_value = item[1]
            icons = {
                PowerOFF.PowerAvailability.ON.value: '🟢',
                PowerOFF.PowerAvailability.OFF.value: '🔴',
                PowerOFF.PowerAvailability.MAYBE_OFF.value: '⚪',
                'ЗАРАЗ': '  ➡️',
            }
            icon = icons.get(status_value)
            row = f'{icon} {time_value} - {status_value}'
            if status_value == 'ЗАРАЗ':
                row = f'<b>{row}</b>'
            result_list.append(row)
        return result_list

    @classmethod
    def _get_schedule(cls, group_id: int) -> dict:
        return getattr(cls, f'SCHEDULE_GROUP_{group_id}')
