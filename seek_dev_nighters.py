import requests
import json
import pytz
from datetime import datetime


def load_single_page(page_number):
    url = 'http://devman.org/api/challenges/solution_attempts/'
    result_dict = None

    payloads = {'page': page_number}

    req = requests.get(url, params=payloads)

    try:
        if req.status_code == requests.codes.ok:
            result_dict = json.loads(req.text)['records']
        return result_dict
    except ValueError:
        return None


def load_attempts():
    pages = 10
    for page in range(1, pages):
        single_page_dict = load_single_page(page)

        if not single_page_dict:
            yield None

        for user_record in single_page_dict:
            yield {
                'username': user_record['username'],
                'timestamp': user_record['timestamp'],
                'timezone': user_record['timezone'],
            }


def get_midnighters(single_record, morning_hour):
    midnighters_hours = {hour for hour in range(morning_hour)}
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
    morning_hour = 5
    for page_load_attempt in load_attempts():
        if page_load_attempt:
            midnighter = get_midnighters(page_load_attempt, morning_hour)
            if midnighter:
                print(midnighter)
