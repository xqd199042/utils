import json
import os
import numpy as np


def default_anno_strategy(anno: str):
    return anno

class Labelme2Coco:
    # target_folder_path要绝对路径
    # 通常labelme json文件和图片在一个folder目录
    def __init__(self, classname_to_id: dict, target_folder_path: str, anno_strategy=default_anno_strategy):
        self.images = []
        self.annotations = []
        self.categories = []
        self.img_id = 0
        self.anno_id = 0
        self.classname_to_id = classname_to_id
        self._init_categories(classname_to_id)
        self._init_imgs_and_annos(target_folder_path, anno_strategy)
        print('coco initialized.')

    def save_coco_json(self, save_path='coco_format.json'):
        instance = {'info': 'spytensor created',
                    'license': 'license',
                    'images': self.images,
                    'annotations': self.annotations,
                    'categories': self.categories}
        json.dump(instance, open(save_path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2) # indent=2 is better

    def _init_categories(self, classname_to_id: dict):
        for k in classname_to_id:
            category = {}
            category['id'] = classname_to_id[k]
            category['name'] = k
            self.categories.append(category)

    def _init_imgs_and_annos(self, target_folder_path: str, anno_strategy):
        files = os.listdir(target_folder_path)
        for file in files:
            if not file.endswith('.json'): continue
            instance = None
            json_file_path = os.path.join(target_folder_path, file)
            with open(json_file_path, 'r', encoding='utf-8') as f:
                instance = json.load(f)
            image = {'id': self.img_id}
            image['width'], image['height'] = instance['imageWidth'], instance['imageHeight']
            image['file_name'] = json_file_path.replace('.json', '.jpg')
            self.images.append(image)
            for obj in instance['shapes']:
                self._init_annos(obj, anno_strategy)
            self.img_id += 1

    def _init_annos(self, obj, anno_strategy):
        annotation = {'id': self.anno_id, 'image_id': self.img_id, 'category_id': self.classname_to_id[anno_strategy(obj['label'])], 'iscrowd': 0, 'area': 1.0}
        points = obj['points']
        annotation['segmentation'] = [np.asarray(points).flatten().tolist()]
        annotation['bbox'] = self._bbox_to_coco_bbox(points)
        self.annotations.append(annotation)
        self.anno_id += 1

    def _bbox_to_coco_bbox(self, points):
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        min_x, min_y = min(xs), min(ys)
        max_x, max_y = max(xs), max(ys)
        return [min_x, min_y, max_x-min_x, max_y-min_y]

# classname_to_id = {'baomo':1, 'cashang':2, 'huashang':3, 'pengshang':4, 'yashang':5, 'yise':6}
if __name__ == '__main__':
    classname_to_id = {'baomo': 1, 'cashang': 2, 'huashang': 3, 'pengshang': 4, 'yashang': 5, 'yise': 6}
    def anno_strategy(anno: str):
        if anno in ('usbbaomo', 'USBbaomo', 'anjianbaomo', 'kongbaomo'):
            anno = 'baomo'
        if anno.endswith('pengshang'):
            anno = 'pengshang'
        return anno
    obj = Labelme2Coco(classname_to_id, 'D:\\Data\\huawei\\black\\side', anno_strategy)
    obj.save_coco_json()

























