# Weburg Torrent Grabber

Работает только для абонентов сети "Планета".

## Программные требования

* Python 2.7.X
* jq


## Установка

```shell
$ mkdir /opt/weburg-torrent-grabber/
$ cd /opt/weburg-torrent-grabber/
$ git clone https://github.com/leominov/weburg-torrent-grabber .
$ mkdir torrents
```

## Настройка

Пример настроек можно найти в файле `settings.json`.

## Запуск

```shell
$ ./weburg.py
```

## Удаление старых торрентов

Скрипт `del_old_bt.sh` ищет и удаляет торренты старше заданного количества дней, скаченные файлы так же будут удалены.

### Настройка

В файле `settings.json` значения `transmission_remote_username` и `transmission_remote_password` нужно заменить на свои реквизиты Transmission Remote; значение параметра `ttl` задается в днях и определяет, какие торренты будут удалены. Параметр `logfile_del` определяет путь к лог-файлу.

### Запуск

```shell
$ ./del_old_bt.sh /opt/weburg-torrent-grabber/settings.json
```
