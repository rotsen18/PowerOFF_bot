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

    @staticmethod
    def day_power_off_schedule(group_id: int, day: int):
        data = PowerOFF.day_data(group_id, day)
        schedule = PowerOFF.format_day_schedule(data, day)
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        schedule.insert(0, f'Група {group_id}')
        if today.weekday() == day:
            schedule.insert(1, str(today.date()))
        elif tomorrow.weekday() == day:
            schedule.insert(1, str(tomorrow.date()))
        schedule.insert(2, '-' * 15 + '\n')
        return '\n'.join(schedule)
