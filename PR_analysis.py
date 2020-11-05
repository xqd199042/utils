import os


class Box:
    # xy是左上角坐标
    def __init__(self, category, x, y, w, h):
        self.category = category
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_area(self):
        return self.w * self.h

    def get_iou(self, box):
        total_area = self.get_area() + box.get_area()
        inter_area = calculate_inter_area(self, box)
        iou = inter_area*1.0/(total_area-inter_area)
        return iou

    def matches(self, box, threshold=0.5):
        result = False
        if self.category == box.category and self.get_iou(box)>=threshold: result = True
        return result

def calculate_inter_area(b1: Box, b2: Box):
    left_x, left_y = max([b1.x, b2.x]), max([b1.y, b2.y])
    right_x, right_y = min([b1.x+b1.w, b2.x+b2.w]), min([b1.y+b1.h, b2.y+b2.h])
    height = right_y - left_y
    width = right_x - left_x
    area = height * width if height>0 and width>0 else 0
    return area

# precision and recall analysis
def pr_analysis(gt_boxes: list, infer_boxes: list):
    correct_list = []
    recall_list = []
    for gt_box in gt_boxes:
        # 如果infer_boxes里面有匹配该gt_box的box,放入correct_list
        # 如果infer_boxes里面无匹配该gt_box的box,则放入recall_list
        # 最后infer_boxes里剩下的是过杀
        for infer_box in infer_boxes:
            pass

# 返回两个list,输入的是两个绝对路径
# [{'filename':xxx, 'boxes':[box1, box2, ...]}...{}]
def txts_to_boxes(gt_txt_folder_path: str, infer_txt_folder_path: str, img_size):
    infer_txts = os.listdir(infer_txt_folder_path)
    infer_boxes, gt_boxes = [], []
    for infer_txt in infer_txts:
        # 一个infer_txt对应一张img，每张原图有N个缺陷，就有N个boxes
        filename = os.path.join(infer_txt_folder_path, infer_txt)
        instance = {'filename': filename, 'boxes': []}
        with open(filename, 'r', encoding='utf-8') as f:
            txt_to_box(f, instance, img_size)
        infer_boxes.append(instance)
        gt_txt = os.path.join(gt_txt_folder_path, infer_txt)
    return gt_boxes, infer_boxes

# 单个txt文件f转为box对象
def txt_to_box(f, instance, img_size):
    for line in f.readlines():
        line = line.strip('\n')
        object = line.split(' ')
        category = int(object[1])
        x = (float(object[2]) - float(object[4]) / 2) * img_size[0]
        y = (float(object[3]) - float(object[5]) / 2) * img_size[1]
        w, h = float(object[4]) * img_size[0], float(object[5]) * img_size[1]
        instance['boxes'].append(Box(category, int(x), int(y), int(w), int(h)))






if __name__ == '__main__':
    test = ' 0 3 4 5'
    print(test.split(' '))


















