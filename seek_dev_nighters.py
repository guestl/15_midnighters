import requests
import json
import pytz
from datetime import datetime


def load_single_page(page_number):
    url = 'http://devman.org/api/challenges/solution_attempts/'
    result = None

    payloads = {'page': page_number}

    req = requests.get(url, params=payloads)

    try:
        if req.status_code == requests.codes.ok:
            result = json.loads(req.text)['records']
        return result
    except ValueError:
        exit("Error with content of the page {}".format(req.url))


def load_attempts():
    pages = 10
    for page in range(1, pages):
        single_page_dict = load_single_page(page)

        if not single_page_dict:
            exit('Error with load page {}'.format(page))

        for item in single_page_dict:
            yield {
                'username': item['username'],
                'timestamp': item['timestamp'],
                'timezone': item['timezone'],
            }


def get_midnighters(single_record, morning_hour):
    midnighters_hours = {hour for hour in range(morning_hour)}
    result = None

    if single_record['timestamp'] and single_record['timezone']:
        user_tz = pytz.timezone(single_record['timezone'])
        user_utc_time = single_record['timestamp']

        user_local_time = pytz.utc.localize(datetime.utcfromtimestamp(
            user_utc_time), is_dst=None).astimezone(user_tz)

        if user_local_time.hour in midnighters_hours:
            result = single_record['username']

    return result


if __name__ == '__main__':
    morning_hour = 5
    for item in load_attempts():
        midnighter = get_midnighters(item, morning_hour)
        if midnighter:
            print(midnighter)
