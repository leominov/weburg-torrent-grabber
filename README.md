# Weburg Torrent Grabber

Works fine only for Planeta users.

## Requirements

Python 2.7.X 

jq

## Default settings

```json
{
    "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0",
    "torrents_directory": "./torrents/",
    "debug": true,
    "use_transmission": true,
    "transmission_show": "/usr/bin/transmission-show",
    "transmission_remote": "/usr/bin/transmission-remote",
    "transmission_remote_username": "user",
    "transmission_remote_password": "password",
    "ttl": "30"
}
```

## Usage

```shell
$ mkdir torrents
$ ./weburg.py
```

## Deleting old torrents and files

Скрипт ищет торретнты которые старше 30 дней и удаляет торрент и файл.

Конфиге сторочки `transmission_remote_username`, `transmission_remote_password` внужно поменять на свои, `ttl` определяет торренты старше скольких дней удалять.

### Usage

```shell
$ ./del_old_bt.sh
```
