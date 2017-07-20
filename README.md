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
3. Add your bot on Telegram and follow the instructions it sends you

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
|url|Public URL of the service (just used for instructions)|
