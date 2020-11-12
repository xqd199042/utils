import os
import cv2


# 原图裁减成detect需要的size
def original_crop(img_file: str, target_folder_path='crop_imgs', crop_size=768, overlap=0.5):
    file_name = img_file[img_file.rindex(os.sep)+1:]
    img = cv2.imread(img_file)
    x_offset, y_offset = 0, 0
    img_height, img_width = img.shape[0], img.shape[1]
    v, h = int(img_height/(crop_size*overlap)), int(img_width/(crop_size*overlap))
    print(v, ' ', h)
    for i in range(v):
        if i == v-1:
            y_offset = img_height - crop_size
        for j in range(h):
            if j == h-1:
                x_offset = img_width - crop_size
            img_new = img[y_offset:y_offset+crop_size, x_offset:x_offset+crop_size]
            img_name = file_name.replace('.jpg', '_%d_%d.jpg'%(y_offset, x_offset))
            cv2.imwrite(os.path.join(target_folder_path, img_name), img_new)
            print(img_name, ' is cropped.')
            x_offset += int(crop_size * overlap)
        y_offset += int(crop_size * overlap)
        x_offset = 0









if __name__ == '__main__':
    original_crop('/home/qiangde/Data/huawei/black/side/0897-0004-03.jpg', '/home/qiangde/Data/huawei/black/side/test')

































