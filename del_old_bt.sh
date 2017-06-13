#!/bin/bash
# Скрипт ищет и удаляет торренты старше
# заданного количества дней.

set -e

CONFIG=$1

if [[ $1 == "-h" ]]; then
    echo -e "$ ./del_old_bt.sh /path_you_dir/settings.json" >&2 
    exit 0
fi

if [[ -z $CONFIG ]]; then
    echo -e "No config file, using -h for more info" >&2 
    exit 1
fi

REMOTE=$(cat $CONFIG | jq -re '.transmission_remote')
USERNAME=$(cat $CONFIG | jq -re '.transmission_remote_username')
PASSWORD=$(cat $CONFIG | jq -re '.transmission_remote_password')
TTL=$(cat $CONFIG | jq -re '.ttl')
LOGFILE=$(cat $CONFIG | jq -re '.logfile_del')
DATE=$(date +%F_%T)
TXT_DEL="deleting torrent #"


listing() {
    $REMOTE -n $USERNAME:$PASSWORD -l | awk '{print $1}' | grep -v 'ID' | grep -v 'Sum:' | sed 's/[^0-9]//g'
}
bt_id() {
    $REMOTE -n $USERNAME:$PASSWORD -t $1 -i | grep 'Seeding Time' | awk '{print $3}'
}
bt_name() {
    $REMOTE -n $USERNAME:$PASSWORD -t $1 -i | grep 'Name:' | awk '{print $2}'
}
remove() {
    $REMOTE -n $USERNAME:$PASSWORD -t $1 --remove-and-delete 2>&1 > /dev/null
}
loging() {
    echo -e $DATE $* >> $LOGFILE
}

for ID in $(listing); do
    BT_TTL=$(bt_id $ID)
    if [[ "$BT_TTL" -gt "$TTL" ]]; then
        NAME=$(bt_name $ID)
        remove $ID
        loging $TXT_DEL $ID $NAME
    fi
done
