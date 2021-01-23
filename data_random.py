import os
import random
import glob
import shutil
from pathlib import Path
from tqdm.auto import tqdm
import argparse
if not os.path.exists('yolo_data'):
    os.mkdir('yolo_data')
if not os.path.exists('yolo_data/test'):
    os.mkdir('yolo_data/test')
    os.mkdir('yolo_data/test/images')
    os.mkdir('yolo_data/test/labels')
if not os.path.exists('yolo_data/train'):
    os.mkdir('yolo_data/train')
    os.mkdir('yolo_data/train/images')
    os.mkdir('yolo_data/train/labels')
if not os.path.exists('yolo_data/valid'):
    os.mkdir('yolo_data/valid')
    os.mkdir('yolo_data/valid/images')
    os.mkdir('yolo_data/valid/labels')
count = 0

name_list = ['.jpg', '.JPG', '.PNG', '.png']

file_list = glob.glob('./data_original/*/*')

for file_name in file_list:
    file_name_f = file_name
    for n in name_list:
        file_name = file_name.replace(n, '.jpg')
    os.rename(file_name_f, file_name)
    
def batch_rename(path):
    random_list = [x for x in range(0, len(path))]
    random.shuffle(random_list)
    for j, fname in enumerate(path):
        new_jname = str(random_list[j]) + '.jpg'
        new_tname = str(random_list[j]) + '.txt'
        # print(os.path.dirname(fname)+'/'+new_jname)
        os.rename(fname, os.path.dirname(fname)+'/'+new_jname)
        os.rename('.' + fname.split('.')[1] + '.txt', os.path.dirname(fname)+'/'+new_tname)
        # print(fname.split('.')[1])
        
def data_label(path=[], class_size=10, train=True, test=False, test_size=100):
    class_dict = {}
    tmp_dict = {}
    for p in path:
        _ = os.path.dirname(p)
        class_dict[_.split('/')[-1]] = []
        tmp_dict[_.split('/')[-1]] = []
    for i, p in tqdm(enumerate(path)):
        _ = os.path.dirname(p)
        train_size = 0
        if train:
            train_size = class_size
        if len(class_dict[_.split('/')[-1]]) < train_size:
            class_dict[_.split('/')[-1]].append(p)
        elif len(tmp_dict[_.split('/')[-1]]) < class_size:
            tmp_dict[_.split('/')[-1]].append(p)
    for c in class_dict:
        for i, x in enumerate(class_dict[c]):
            if train:
                if i < len(class_dict[c])*0.9:
                    shutil.move(x, './yolo_data/train/images')
                    shutil.move('.' + x.split('.')[1] + '.txt', './yolo_data/train/labels')
                elif i < len(class_dict[c]):
                    shutil.move(x, './yolo_data/valid/images')
                    shutil.move('.' + x.split('.')[1] + '.txt', './yolo_data/valid/labels')
    if test:
        for tmp in tmp_dict:
            for t in tmp_dict[tmp]:
                shutil.move(t, './yolo_data/test/images')
                shutil.move('.' + t.split('.')[1] + '.txt', './yolo_data/test/labels')
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--rename', action='store_true', default=False)
    parser.add_argument('--class-size', default=10)
    parser.add_argument('--notrain', action='store_false', default=True)
    parser.add_argument('--test-data', action='store_true', default=False)
    parser.add_argument('--test-size', default=100)
    args = parser.parse_args()
    test = glob.glob('./data_original/*/*.txt')
    for t in test:
        with open(t, 'r', encoding='utf-8') as f:
            cont = f.read()
        if len(cont) == 0:
            print(t)
            os.remove(t)
            os.remove('.' + t.split('.')[1] + '.jpg')

    all_list = glob.glob('./data_original/*/*.jpg')

    if args.rename:
        batch_rename(all_list)
    # with open('./logcount.txt', 'w', encoding='utf-8') as f:
    #     f.write(str(count))
    all_list = glob.glob('./data_original/*/*.jpg')

    random.shuffle(all_list)
    # print(all_list)
    # print(len(all_list)//5)
    data_label(path=all_list, class_size=int(args.class_size), train=args.notrain, test=args.test_data, test_size=int(args.test_size))

