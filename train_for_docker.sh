#!/bin/bash
rm -rf /home/ub/red/yolo_data
mkdir -p /home/ub/red/yolo_data
cd /home/ub/red
python data_random.py --rename
python modify_yaml.py --save_path yolo_data
cd /home/ub/red/yolo_new/
cp /home/ub/red/yolo_new/yolov5s.pt tmp/best.pt
d=$(date +%Y%m%d)
# --hyp data/hyp.car288.yaml 
python stop_train.py --cfg ../yolo_data/yolov5s.yaml --weights tmp/best.pt --data ../yolo_data/data.yaml --hyp data/hyp.car288.yaml  --batch-size 8 --multi-scale --epoch 10000 --name "${d}_${a}" --project runs/$d --exist-ok
python stop_detect.py --weights runs/$d/$1/weights/best.pt --source ../yolo_data/valid/images/
echo true > tmp/ok.txt
echo true > tmp/really_ok.txt
echo 3 > tmp/val_loss.txt
tmp=$(<tmp/ok.txt)
temp=$(<tmp/really_ok.txt)
n=0
while $temp
do
    testnum=$(find ../data_original/*/ -type f | wc -l)
    while $tmp
    do
        python stop_train.py --cfg ../yolo_data/yolov5s.yaml --weights tmp/best.pt --data ../yolo_data/data.yaml --hyp data/hyp.car288.yaml --batch-size 8 --multi-scale --epoch 10000 --name $1 --project runs/$d --exist-ok
        python stop_detect.py --weights runs/$d/$1/weights/last.pt
        value=$(<tmp/ok.txt)
        tmp=$value
        n=$((n+1))
        if [ $n == 5 ]; then
            cd /home/ub/red/
            python data_random.py
            n=0
            cd /home/ub/red/yolo_new/
        fi
    done
    if [ $testnum -le 10 ]; then
        break
    fi
    mAP=$(<tmp/mAP.txt)
    if [ $(echo "$mAP > 0.95" | bc) -eq 1 ]; then
        cd /home/ub/red/
        python data_random.py --notrain --test-data --class-size 200
        cd /home/ub/red/yolo_new/
        python stop_test.py --weights runs/$d/$1/weights/last.pt
        break
    elif [ $(echo "$mAP > 0.9" | bc) -eq 1 ]; then
        cd /home/ub/red/
        python data_random.py --notrain --test-data --class-size 100
        cd /home/ub/red/yolo_new/
        python stop_test.py --weights runs/$d/$1/weights/last.pt
    elif [ $(echo "$mAP > 0.85" | bc) -eq 1 ]; then
        cd /home/ub/red/
        python data_random.py --notrain --test-data --class-size 50
        cd /home/ub/red/yolo_new/
        python stop_test.py --weights runs/$d/$1/weights/last.pt
    elif [ $(echo "$mAP > 0.65" | bc) -eq 1 ]; then
        cd /home/ub/red/
        python data_random.py --notrain --test-data --class-size 20
        cd /home/ub/red/yolo_new/
        python stop_test.py --weights runs/$d/$1/weights/last.pt
    else
        cd /home/ub/red/
        python data_random.py --notrain --test-data
        cd /home/ub/red/yolo_new/
        python stop_test.py --weights runs/$d/$1/weights/last.pt
    fi
    temp=$(<tmp/really_ok.txt)
done