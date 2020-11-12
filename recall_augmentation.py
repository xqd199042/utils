import json


class Box:
    # xy是左上角坐标
    def __init__(self, x, y, w, h, category=None):
        self.category = category
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        if category is None:
            self.boxes = []

    def get_area(self):
        return self.w * self.h

def calculate_inter_area(b1: Box, b2: Box):
    left_x, left_y = max([b1.x, b2.x]), max([b1.y, b2.y])
    right_x, right_y = min([b1.x+b1.w, b2.x+b2.w]), min([b1.y+b1.h, b2.y+b2.h])
    height = right_y - left_y
    width = right_x - left_x
    area = height * width if height>0 and width>0 else 0
    return area

def objs_to_boxes(json_file_path: str):
    instance = None
    boxes = []
    with open(json_file_path, 'r', encoding='utf-8') as f:
        instance = json.load(f)
    objs = instance['shapes']
    for obj in objs:
        points = obj['points']






























