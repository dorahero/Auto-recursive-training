# YOLOv5 recursive-training
- [x] Python
- [x] [YOLOv5](https://github.com/ultralytics/yolov5)
- [x] Pytorch
- [x] [cvat-cli](https://github.com/openvinotoolkit/cvat/tree/develop/utils/cli)
- [x] docker

# Installation:
- Put `cvat` floder in `cvat/util/cli`  
- Put others in your `yolov5` floder
- check all the path is your path

# Step 1:
- export data which be labeled on cvat
```shell
export.sh $TASK_KEYWORD
```  

# Step 2:
- unzip these zip files
```shell
init_unzip_n.sh $TASK_KEYWORD
```  

# Step 3:
- start recursive yolov5 training
```shell
r_train.sh $TASK_KEYWORD
```  