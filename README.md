UroTel
======
Send UptimeRobot-notifications to Telegram

Installation
============
* Install requirements `pip install -r requirements.txt`

Usage
=====
1. Create a [config](#Configuration) at `config.ini`
2. Run `python server.py`
3. Add a new alert contact to your UptimeRobot-account


### Alert Contact Information
* **Type**: Web-hook
* **URL to notify**: Url to your UroTel-instance
* **POST Value (JSON Format)**
```json
{
    "secret": "secret set in your config",
    "monitor": {
        "id": "*monitorID*",
        "url": "*monitorURL*",
        "name": "*monitorFriendlyName*"
    },
    "alert": {
        "type": "*alertType*",
        "name": "*alertTypeFriendlyName*",
        "details": "*alertDetails*",
        "contacts": "*monitorAlertContacts*"
    }
}
```
* Check `Send as JSON (application/json). If not selected, the data will be sent as a standard POST (application/x-www-form-urlencoded).`

Configuration
=============
### `[Telegram]`
|Key|Description|
|-|-|
|access_token|Access token for your setup Telegram-bot|

### `[Server]`
|Key|Description|
|-|-|
|host|Host of the UroTel-server|
|port|Port of the UroTel-server|
|secret|Secret used to ensure validity of Webhook-calls|
