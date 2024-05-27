import unittest
import requests
from dotenv import dotenv_values
import time

config = dotenv_values(".env")
ENDPOINT = 'http://192.144.12.8:5000'
HEADERS = {"Authorization": f"Bearer {config['APP_TOKEN']}"}


class TestApi(unittest.TestCase):
    def test_home(self):
        t = time.time()
        resp = requests.get(ENDPOINT)
        self.assertIn('Housing price service', resp.text)
        print('test_home',time.time() - t)

    def test_api(self):
        t = time.time()
        data = {'total_meters': 44,
                'rooms_count': 1,
                'floor': 1,
                'floors_count': 1,
                'county_short': "ЦАО",
                'object_type': "Новостройка"}
        resp = requests.post(ENDPOINT +'/predict',
                             json=data,
                             headers=HEADERS)
        self.assertIn('price', resp.text)
        print('test api',time.time()-t)


if __name__ == '__main__':
    unittest.main()