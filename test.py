import os

import cv2


class Test:

    def __init__(self):
        self.age = 0
    def get_age(self):
        self.calculate_age()
        return self.age

    def calculate_age(self):
        pass

if __name__ == '__main__':
    path = '/home/qiangde/Data/huawei/black/side'
    result = {}
    files = os.listdir(path)
    for file in files:
        if not file.endswith('.jpg'): continue
        img = cv2.imread(os.path.join(path, file))
        size = (img.shape[0], img.shape[1])
        if size not in result:
            result[size] = [file]
        else:
            result[size].append(file)
    for size in result:
        print(size, '\n', result[size])


