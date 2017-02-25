from collections import namedtuple

import requests

from bottle import HTTPResponse, request, route, run

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

# parse config
config = ConfigParser()
# init config
config.add_section('Server')
config.set('Server', 'host', 'localhost')
config.set('Server', 'port', '9987')

config.read('config.ini')

access_token = config.get('Telegram', 'access_token')
api_base = 'https://api.telegram.org/bot{}'.format(access_token)
webhook_url = 'https://urotel.crapwa.re/uptimerobot'

Alert = namedtuple('Alert', [
    'type', 'name', 'details', 'contacts', 'datetime'])
Monitor = namedtuple('Monitor', ['id', 'name', 'url', 'alert'])


def send_telegram_message(chatid, message):
    data = {
        'chat_id': chatid,
        'parse_mode': 'Markdown',
        'text': message
    }
    requests.post(api_base + '/sendMessage', json=data)


@route('/uptimerobot', method='POST')
def uptimerobot_webhook():
    # parse query-data into named tuple's
    query = request.query
    alert = Alert(
        query.alertType, query.alertTypeFriendlyName, query.alertDetails,
        query.monitorAlertContacts, query.alertDateTime
    )
    monitor = Monitor(
        query.monitorID, query.monitorFriendlyName, query.monitorURL, alert
    )
    # send notification
    send_telegram_message(
        query.chatid,
        '{monitor} ({url}) is {event} ({reason})'.format(
            monitor=monitor.name, url=monitor.url,
            event=monitor.alert.name, reason=monitor.alert.details
        )
    )
    return HTTPResponse(status=204)


@route('/telegram', method='POST')
def telegram_webhook():
    if request.json:
        chatid = request.json.get('message', {}).get('chat', {}).get('id')
        message = request.json.get('message', {}).get('text')
        if not chatid or not message:
            return HTTPResponse('204')
        if message == '/start':
            send_telegram_message(chatid, '\n'.join([
                'Hello there, now create a UptimeRobot-alert:',
                'Alert Contact Type: `Web-Hook`',
                'Friendly Name: `Telegram`',
                'URL to Notify: `{webhook}?chatid={chatid}&`'.format(
                    chatid=chatid, webhook=webhook_url)
            ]))

    return HTTPResponse(status=204)


if __name__ == '__main__':
    run(
        host=config.get('Server', 'host'),
        port=config.getint('Server', 'port')
    )
