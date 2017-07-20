from collections import namedtuple

import requests
from bottle import Bottle, HTTPResponse, request

app = Bottle()
app.config.load_config('config.ini')

api_base = 'https://api.telegram.org/bot{}'.format(
    app.config['telegram.access_token']
)
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


@app.route('/uptimerobot', method='POST')
def uptimerobot_webhook():
    # parse query-data into named tuple's
    query = request.query
    if query.secret != app.config['server.secret']:
        return HTTPResponse(status=401)
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


@app.route('/telegram', method='POST')
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


@app.route('/')
def index():
    return 'UroTel (Uptimerobot Telegram notifier)'


if __name__ == '__main__':
    app.run(
        host=app.config.get('server.host', '127.0.0.1'),
        port=int(app.config.get('server.port', 8080))
    )
