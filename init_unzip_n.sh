#!/bin/bash
rm -rf /home/ub/red/yolo_data
rm -rf /home/ub/red/data_original
rm /home/ub/red/yolov5_training/tmp/obj.names
mkdir -p ~/red/yolov5_training/$1
mkdir -p ~/red/data_original
cd ~/red/zip/$1
# get one zip file name
FNAME=$(ls | grep .zip | head -n1)
unzip -j "$FNAME" "obj.names" -d ~/red/yolov5_training/tmp/

# unzip images
n=0; for i in *.zip; do unzip -j "$i" "obj_train_data/*" -d ~/red/data_original/"${n}"/; n=$((n+1)); done
