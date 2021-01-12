#! /bin/bash

RUNAT1="06:00"
RUNAT2="18:00"

while [ 1 ]
do
    DATE=`/bin/date +%H:%M`
    if [ $DATE. = $RUNAT1. ]
    then
        git pull
        ipython main.py
    fi  
    
    if [ $DATE. = $RUNAT2. ]
    then
        git pull
        ipython main.py
    fi

    sleep 3600
done