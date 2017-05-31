#!/bin/bash

set -ex

# Скрипт ищет торретнты которые старше 30 дней 
# и удаляет торрент и файл.

REMOTE=$(cat settings.json | jq -re '.transmission_remote')
USERNAME=$(cat settings.json | jq -re '.transmission_remote_username')
PASSWORD=$(cat settings.json | jq -re '.transmission_remote_password')
TTL=$(cat settings.json | jq -re '.ttl')

listing() {
    $("$REMOTE" -n "$USERNAME:$PASSWORD" -l | awk '{print $1}' | grep -v 'ID' | grep -v 'Sum:')
}
bt_search() {
    $("$REMOTE" -n "$USERNAME:$PASSWORD" -t "$NAME" -i | grep 'Seeding Time' | awk '{print $3}')
}
remove() {
    $("$REMOTE" -n "$USERNAME:$PASSWORD" -t "$NAME" --remove-and-delete 2>&1 > /dev/null)
}

for NAME in $(listing); do
    BT_TTL=$(bt_search)
    if [[ "$BT_TTL" -gt "$TTL" ]]; then
        remove
    fi
done
