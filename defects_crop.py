import os
import cv2
import json


# 从分割坐标中得到左上右下坐标
def polygon_to_crop_axis(list_axis):
    list_x, list_y = [], []
    for i, axis in enumerate(list_axis):
        if i%2==0: list_x.append(axis)
        else: list_y.append(axis)
    min_x, min_y = min(list_x), min(list_y)
    max_x, max_y = max(list_x), max(list_y)
    return (min_x, min_y), (max_x, max_y)

# 从放labelme的json文件的文件夹中获得img_infos, 必须是绝对路径
def json_crop_infos(json_folder_path: str):
    json_files = os.listdir(json_folder_path)
    crop_infos = []
    for json_file in json_files:
        if not json_file.endswith('.json'): continue
        crop_info = {'imagePath': os.path.join(json_folder_path, json_file.replace('.json', '.jpg')), 'objects':[]}
        instance = None
        with open(os.path.join(json_folder_path, json_file), 'r', encoding='utf-8') as f:
            instance = json.load(f)
        for crop_area in instance['shapes']:
            obj = {'label': crop_area['label']}
            obj['axis'] = polygon_to_crop_axis([e for point in crop_area['points'] for e in point])
            crop_info['objects'].append(obj)
        crop_infos.append(crop_info)
    return crop_infos

# img_infos should be [{'imagePath': 'xxx', 'defects':[{'label': 'xx', 'axis': [...]}]}, ...]
# 截出路径在当前目录out/train下面
def defects_crop(img_infos: list, crop_size=128):
    current_path = os.path.join(os.getcwd(), 'out/train')
    result = {}
    for img_info in img_infos:
        img_path = img_info['imagePath']
        img_name = img_path[img_path.rindex(os.sep)+1: img_path.rindex('.')]
        img = cv2.imread(img_path)
        limit_x, limit_y = img.shape[1], img.shape[0]
        for obj in img_info['objects']:
            label, axis = obj['label'], obj['axis']
            if label not in result:
                result[label] = 0
                os.makedirs(os.path.join(current_path, label))
            result[label] += 1
            min_x, min_y = axis[0]
            max_x, max_y = axis[1]
            center_x, center_y = (min_x + max_x)//2, (min_y + max_y)//2
            img_crop_path = os.path.join(os.path.join(current_path, label), img_name+'_'+str(result[label])+'.jpg')
            crop_min_y, crop_max_y, crop_min_x, crop_max_x = center_y - crop_size // 2, center_y + crop_size // 2, center_x - crop_size // 2, center_x + crop_size // 2
            if center_y - crop_size // 2 <= 0: crop_min_y, crop_max_y = 0, crop_size
            if center_y + crop_size // 2 >= limit_y: crop_min_y, crop_max_y = limit_y - crop_size, limit_y
            if center_x - crop_size // 2 <= 0: crop_min_x, crop_max_x = 0, crop_size
            if center_x + crop_size // 2 >= limit_x: crop_min_x, crop_max_x = limit_x - crop_size, limit_x
            img_new = img[int(crop_min_y):int(crop_max_y), int(crop_min_x):int(crop_max_x)]
            cv2.imwrite(img_crop_path, img_new)
            print('%s %d is cropped' % (label, result[label]))


if __name__ == '__main__':
    # defects_crop('/home/qiangde/Data/huawei/black/side/outputs', '/home/qiangde/Data/huawei/black/side')
    img_infos = json_crop_infos('D:\\Data\\huawei\\black\\side')
    defects_crop(img_infos, crop_size=64)





















