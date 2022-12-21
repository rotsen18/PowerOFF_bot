import urllib.parse

import requests


class Zakaz:
    DOMAIN = 'https://stores-api.zakaz.ua'

    @staticmethod
    def get(url: str) -> dict:
        response = requests.get(url)
        return response.json()

    @classmethod
    def get_all_stores(cls):
        url = urllib.parse.urljoin(cls.DOMAIN, 'stores')
        data = cls.get(url)
        stores = {}
        for store in data:
            city = store.get('city')
            stores[city] = stores.get(city, []) + [store]
        return stores

    @classmethod
    def get_city_stores(cls, city: str) -> dict:
        stores = cls.get_all_stores()
        return stores.get(city)

    @classmethod
    def get_store_info(cls, store_id: int) -> dict:
        url = urllib.parse.urljoin(cls.DOMAIN, f'stores/{store_id}')
        data = cls.get(url)
        return data

    @classmethod
    def get_delivery_schedule(cls, store_id):
        url = urllib.parse.urljoin(cls.DOMAIN, f'stores/{store_id}/delivery_schedule/plan/')
        data = cls.get(url)
        return data

    @classmethod
    def format_delivery_schedule(cls, schedule):
        delivery_prices = []
        for day in schedule:
            for delivery in day['items']:
                price = (delivery['price'] - delivery['available_discount']) / 100
                message = f"[{delivery['date']} {delivery['time_range']}] - {price} UAH"
                delivery_prices.append(message)
            delivery_prices.append('\n')
        return delivery_prices
