#!/bin/bash
mkdir -p  /home/ub/red/zip/$1/
cd /home/ub/cvat/utils/cli/
python cli.py --auth red:red --server-host 172.16.16.88 ls > ./tmp/lp_task.csv
cd tmp/
python id_name.py --keyword $1 > lp_id.txt
cd ..
filename='tmp/lp_id.txt'
while read line; do
python cli.py --auth red:red --server-host 172.16.16.88 dump --format "YOLO 1.1" ${line%%,*} /home/ub/red/zip/$1/${line##*,}.zip
done < $filename
