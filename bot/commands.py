from datetime import datetime, timedelta

from services.zakaz import Zakaz
from services.power import PowerOFF
import settings


class Command:
    @staticmethod
    def zakaz_shedule() -> str:
        data = Zakaz.get_delivery_schedule(settings.HOME_STORE_ID)
        deliveries = Zakaz.format_delivery_schedule(data)
        return '\n'.join(deliveries)

    @classmethod
    def day_power_off_schedule(cls, group_id: int, day: int):
        data = PowerOFF.day_data(group_id, day)
        schedule = PowerOFF.format_day_schedule(data, day)
        schedule.insert(0, f'Група {group_id}')
        date = cls._get_date_from_weekday(day)
        formatted_date = date.strftime('%a %d %m %Y')
        schedule.insert(1, formatted_date)
        schedule.insert(2, '-' * 15 + '\n')
        return '\n'.join(schedule)

    @staticmethod
    def _get_date_from_weekday(weekday: int):
        today = datetime.today()
        day_shift = today.weekday() % 7
        monday = today - timedelta(days=day_shift)
        week_dates = {
            day_num: monday + timedelta(days=day_num)
            for day_num in range(7)
        }
        return week_dates.get(weekday)

    @staticmethod
    def another_group_statuses(group_id: int):
        message = PowerOFF.another_groups_status(group_id)
        return message
