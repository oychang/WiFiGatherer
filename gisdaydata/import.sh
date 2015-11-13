#!/bin/bash
./adb -d shell 'run-as com.oychang.wifigatherer cat /data/data/com.oychang.wifigatherer/databases/LocationData.db > /sdcard/Location.sqlite'
./adb pull /sdcard/Location.sqlite .

sqlite3 Location.sqlite <<EOF
.headers on
.mode csv
.output out.csv
select * from Readings;
EOF
