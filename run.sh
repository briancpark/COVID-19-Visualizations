#! /bin/bash

RUNAT="06:00"

while [ 1 ]
do
    DATE=`/bin/date +%H:%M`
    if [ $DATE. = $RUNAT. ]
    then
        python3 main.py
    fi

    sleep 3600
done