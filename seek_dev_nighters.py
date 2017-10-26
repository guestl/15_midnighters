import requests
import pytz
from datetime import datetime


def get_pages_amount(url):
    req = requests.get(url)

    try:
        if req.ok:
            return req.json()['number_of_pages']
    except ValueError:
        return None


def load_single_page(page_number, url):
    result_dict = None

    payloads = {'page': page_number}

    req = requests.get(url, params=payloads)

    try:
        if req.ok:
            result_dict = req.json()['records']
        return result_dict
    except ValueError:
        return None


def load_attempts(url, pages_amount):
    for page in range(1, pages_amount):
        single_page_dict = load_single_page(page, url)

        if not single_page_dict:
            yield

        for user_record in single_page_dict:
            yield {
                'username': user_record['username'],
                'timestamp': user_record['timestamp'],
                'timezone': user_record['timezone'],
            }


def get_midnighters(single_record, hour_of_night_stop):
    midnighters_hours = set(range(hour_of_night_stop))
    result_username = None

    if single_record['timestamp'] and single_record['timezone']:
        user_tz = pytz.timezone(single_record['timezone'])
        user_utc_time = single_record['timestamp']

        user_local_time = pytz.utc.localize(datetime.utcfromtimestamp(
            user_utc_time), is_dst=None).astimezone(user_tz)

        if user_local_time.hour in midnighters_hours:
            result_username = single_record['username']

    return result_username


if __name__ == '__main__':
    url = 'http://devman.org/api/challenges/solution_attempts/'
    hour_of_night_stop = 5
    pages_amount = get_pages_amount(url)

    if pages_amount is None:
        exit("Error while loading a page")

    for page_load_attempt in load_attempts(url, pages_amount):
        if page_load_attempt:
            midnighter = get_midnighters(page_load_attempt, hour_of_night_stop)
            if midnighter:
                print(midnighter)
