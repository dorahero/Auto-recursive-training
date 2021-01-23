#!/bin/bash
d=$(date "+%Y%m%d")
mkdir -p /home/ub/cvat_backup/${d}/csv/
cd /home/ub/cvat/utils/cli/
python cli.py --auth red:red --server-host 172.16.16.88 ls > /home/ub/cvat_backup/${d}/csv/task.csv
python cli.py --auth red:red --server-host 172.16.16.88 ls > ./tmp2/lp_task.csv
cd tmp2/
python id_name.py --keyword "" > lp_id.txt
cd ..
filename='tmp2/lp_id.txt'
while read line; do
python cli.py --auth red:red --server-host 172.16.16.88 dump --format "YOLO 1.1" ${line%%,*} /home/ub/cvat_backup/${d}/${line##*,}.zip
done < $filename
