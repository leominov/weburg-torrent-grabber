#!/bin/bash

# Скрипт ищет торретнты которые старше 30 дней 
# и удаляет торрент и файл.

REMOTE=$(cat settings.json | jq -r '.transmission_remote')
LOGIN=$(cat settings.json | jq -r '.login')
PASSWD=$(cat settings.json | jq -r '.passwd')
TTL=$(cat settings.json | jq -r '.ttl')

listing(){
$REMOTE -n ''$LOGIN:$PASSWD'' -l | awk '{print $1}' | grep -v 'ID' | grep -v 'Sum:'
}
bt_search(){
$REMOTE -n ''$LOGIN:$PASSWD'' -t $NAME -i | grep 'Seeding Time' | awk '{print $3}'
}
remove(){
$REMOTE -n ''$LOGIN:$PASSWD'' -t $NAME --remove-and-delete 2>&1 > /dev/null
}

for NAME in $(listing); do
	BT_TTL=$(bt_search)
	if [[ "$BT_TTL" -gt "$TTL" ]]; then
		remove
	fi
done
