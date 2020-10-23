import os
import cv2
import numpy as np


def data_aug_translation(img_folder_path):
    img_paths = os.listdir(img_folder_path)
    num = len(img_paths) + 1
    for img_path in img_paths:
        img = cv2.imread(img_folder_path+'/'+img_path)
        img_size = img.shape[0]
        r1, r2 = np.random.rand(1,2)[0] - 0.5
        move1 = np.array([[1, 0, img_size*r1], [0, 1, img_size*r2]], dtype=np.float32)

def data_aug_rotation(img_folder_path, list_angle):
    imgs = os.listdir(img_folder_path)
    for img in imgs:
        img_name = img
        img = cv2.imread(os.path.join(img_folder_path, img))
        rows, cols = img.shape[:2]
        for angle in list_angle:
            move = cv2.getRotationMatrix2D((cols/2,rows/2), angle, 1)
            img_change = cv2.warpAffine(img, move, (cols,rows))
            cv2.imwrite(os.path.join(img_folder_path, img_name.replace('.', 'augment.')), img_change)


# '/home/Desktop/out/train/yashang'
if __name__ == '__main__':
    data_aug_rotation('out/train/yise', [90])
    # data_aug_rotation('/home/qiangde/PycharmProjects/utils/out/train/yise')
























