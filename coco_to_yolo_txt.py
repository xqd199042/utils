import shutil
import os
from collections import defaultdict
import random
import json


# coco json文件就一个，整个instance作为输入
def coco_to_txt(instance):
    name_box_id = defaultdict(list)
    imgs = instance['images']
    width, height = imgs[0]['width'], imgs[0]['height']
    annos = instance['annotations']
    for anno in annos:
        id = anno['image_id']
        # 这里的file_name已经是绝对路径
        name = imgs[id]['file_name']
        category = anno['category_id']
        name_box_id[name].append([anno['bbox'], category])
    for name in name_box_id:
        file = name.replace('.jpg', '.txt')
        with open(file, 'w') as f:
            boxes = name_box_id[name]
            for box in boxes:
                x_center = (box[0][0] + box[0][2]/2)/width
                y_center = (box[0][1] + box[0][3]/2)/height
                w = box[0][2]/width
                h = box[0][3]/height
                box_info = " %d %.03f %.03f %.03f %.03f" % (box[1], x_center, y_center, w, h)
                f.write(box_info)
                f.write('\n')

def split_train_val_test(data_folder_path: str, datasets_name: str, test_ratio=0.1, val_ratio=0.5):
    base_path = os.path.join(data_folder_path[:data_folder_path.rindex(os.sep)], datasets_name)
    make_folders(base_path)
    total_txt = [txt for txt in os.listdir(data_folder_path) if txt.endswith('.txt')]
    test_txt = random.sample(total_txt, int(len(total_txt)*test_ratio))
    val_txt = random.sample(test_txt, int(len(test_txt)*val_ratio))
    for txt in total_txt:
        if txt in test_txt:
            if txt in val_txt:
                copy(os.path.join(data_folder_path, txt), os.path.join(os.path.join(base_path, 'labels/val'), txt))
            else:
                copy(os.path.join(data_folder_path, txt), os.path.join(os.path.join(base_path, 'labels/test'), txt))
        else:
            copy(os.path.join(data_folder_path, txt), os.path.join(os.path.join(base_path, 'labels/train'), txt))

def copy(src_txt_path, dst_txt_path):
    shutil.copy(src_txt_path, dst_txt_path)
    shutil.copy(src_txt_path.replace('.txt', '.jpg'), dst_txt_path.replace('labels', 'images').replace('.txt', '.jpg'))

def make_folders(base_path):
    folders = ('images/train', 'images/val', 'images/test', 'labels/train', 'labels/val', 'labels/test')
    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

if __name__ == '__main__':
    # instance = None
    # with open('coco_format.json', 'r', encoding='utf-8') as f:
    #     instance = json.load(f)
    # coco_to_txt(instance)
    split_train_val_test('/home/qiangde/Desktop/double_check', 'HUAWEI')






































