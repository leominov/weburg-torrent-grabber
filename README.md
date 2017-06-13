# Weburg Torrent Grabber

Works fine only for Planeta users.

## Requirements

* Python 2.7.X
* jq

## Default settings

```javascript
{
    "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0",
    "torrents_directory": "./torrents/",
    "debug": true,
    "use_transmission": true,
    "transmission_show": "/usr/bin/transmission-show",
    "transmission_remote": "/usr/bin/transmission-remote",
    "transmission_remote_username": "user",
    "transmission_remote_password": "password",
    "ttl": "30",
    "logfile_del": "/opt/weburg-torrent-grabber/bt_del.log"
}
```

## Usage

```shell
$ mkdir torrents
$ ./weburg.py
```

## Deleting old torrents and files

Скрипт ищет торренты которые старше 30 дней, затем удаляет торренты и их файлы.

В файле `settings.json` значения `transmission_remote_username` и `transmission_remote_password` нужно заменить на свои, значение параметра `ttl` задается в днях и определяет, какие торренты будут удалены.

### Usage

```shell
$ ./del_old_bt.sh /opt/weburg-torrent-grabber/settings.json
```
