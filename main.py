import requests
import json

from config import url, rules
from sms import send_sms
from datetime import datetime
from khayyam import JalaliDatetime

def get_rates():
    """
    send a get requests to the fixer.io api and get live rates
    :return: request.Response instance
    """
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    return None


def archive(filename, rates):
    """
    get filename and rates, save them to the specific directory
    :param filename:
    :param rates:
    :return: None
    """
    with open(f'data/{filename}.json', 'w') as f:
        f.write(json.dumps(rates))

def send_sms(timestamp, rates):
    """
    get timestamp and rates, check if there is preferred rates and
    then send sms
    :param timestamp:
    :param rates:
    :return:
    """
    now = JalaliDatetime(datetime.now()).strftime('%y-%B-%d  %A  %H:%M')
    msg = f"{timestamp} - {now} - rates"

    if rules['sms']['preferred'] is not None:
        tmp = dict()
        for exc in rules['sms']['preferred']:
            tmp[exc] = rates[exc]
        rates = tmp

    text = json.dumps(rates)
    msg = f"{timestamp} - {now} - rates \n {text}"

    send_sms(msg)


def check_notify_rules(rates):
    """
    Check if user defined notify rules and if rates reached to the defined
    rules, then generate proper msg to send.
    :param rates:
    :return: msg (str)
    """
    preferred = rules['notification']['preferred']
    msg = ''
    for exc in preferred.keys():
        if rates[exc] <= preferred[exc]['min']:
            msg += f'{exc} reached min: {rates[exc]} \n'
        if rates[exc] >= preferred[exc]['max']:
            msg += f'{exc} reached max: {rates[exc]} \n'

    return msg


def send_notification(msg):
    now = JalaliDatetime(datetime.now()).strftime('%y-%B-%d  %A  %H:%M')
    msg += now
    send_sms(msg)


if __name__ == "__main__":
    res = get_rates()

    if rules['archive']:
        archive(res['timestamp'], res['rates'])

    if rules['sms']['enable']:
        send_sms(res['timestamp'], res['rates'])

    if rules['notification']['enable']:
        notification_msg = check_notify_rules(res['rates'])
        if notification_msg:
            send_notification(notification_msg)
