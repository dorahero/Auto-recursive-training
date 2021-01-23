from os import name
import yaml
import argparse

def write_template(nc:int, names:list, saved_path:str, template_path="./yolov5_training/templates") -> None:    
    coco128_yaml = yaml.load(open(f"{template_path}/coco128.yaml"))    
    yolov5s = yaml.load(open(f"{template_path}/yolov5s.yaml"))
    yolov5m =  yaml.load(open(f"{template_path}/yolov5m.yaml"))
    yolov5l =  yaml.load(open(f"{template_path}/yolov5l.yaml"))
    yolov5x = yaml.load(open(f"{template_path}/yolov5x.yaml"))
    
    #coco
    coco128_yaml['nc']=nc
    coco128_yaml['names']=names
    #s
    yolov5s['nc']=nc
    #m
    yolov5m['nc']=nc
    #l
    yolov5l['nc']=nc
    #x
    yolov5x['nc']=nc
    with open(f'{saved_path}/data.yaml', 'w') as f:    
        data = yaml.dump(coco128_yaml, f)    
    with open(f'{saved_path}/yolov5s.yaml', 'w') as f:
        yaml.dump(yolov5s,f)
    with open(f'{saved_path}/yolov5m.yaml', 'w') as f:
        yaml.dump(yolov5m,f )
    with open(f'{saved_path}/yolov5l.yaml', 'w') as f:
        yaml.dump(yolov5l,f )
    with open(f'{saved_path}/yolov5x.yaml', 'w') as f:
        yaml.dump(yolov5x,f)

     


def load_obj_names(tmp_path="./yolov5_training/tmp") -> tuple:
    with open(f"{tmp_path}/obj.names") as f:
        names = [_.replace("\n", "") for _ in f.readlines()]
    return len(names), names


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_path', type=str, help='coco128.yaml saved path')
    
    opt = parser.parse_args()
    opt_dict = vars(opt)

    if opt.save_path:
        # check args
        # error_val = ['save_path']
        # for key ,value in opt_dict.items():
        #     if value=='' or value==None or value=="None":
        #         opt_dict[key]=HYP_SCRATCH_DICT[key]             

        nc , names= load_obj_names()
        write_template(nc=nc, names=names, saved_path=opt.save_path)
