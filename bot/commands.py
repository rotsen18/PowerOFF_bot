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
        formatted_date = date.strftime('%d %B %Y')
        schedule.insert(1, formatted_date)
        schedule.insert(2, '-' * 15 + '\n')
        return '\n'.join(schedule)

    @staticmethod
    def _get_date_from_weekday(weekday: int):
        today = datetime.today()
        week_dates = {}
        for day_shift in range(7):
            actual = today + timedelta(days=day_shift)
            actual_weekday = actual.weekday()
            week_dates[actual_weekday] = actual
        return week_dates.get(weekday)

    @staticmethod
    def another_group_statuses(group_id: int):
        message = PowerOFF.another_groups_status(group_id)
        return message

    @staticmethod
    def update():
        with open('ver.txt') as f:
            version = f.read()
            version = str(version).strip()
        return f'We have new release {version}, check update'
