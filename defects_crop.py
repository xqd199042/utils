from xml.dom.minidom import parse, Element
from xml_to_labelme_json import word_to_pinyin
import os
import cv2


# convert segmentation axis to detection axis
def polygon_to_line(list_axis):
    list_x, list_y = [], []
    for i, axis in enumerate(list_axis):
        if i%2==0: list_x.append(axis)
        else: list_y.append(axis)
    min_x, min_y = min(list_x), min(list_y)
    max_x, max_y = max(list_x), max(list_y)
    return (min_x, min_y), (max_x, max_y)

# given a xml path, return a list [...] containing {defect_name: defect_axis}
def xml_info_out(anno_path):
    result = []
    root = parse(anno_path).documentElement
    items = root.getElementsByTagName('item')
    for item in items:
        name = item.getElementsByTagName('name')[0].childNodes[0].data
        dic = {'name': name}
        lines = item.getElementsByTagName('line')
        if len(lines)>0:
            line = lines[0]
            list_axis = [int(node.childNodes[0].data) for node in line.childNodes if type(node)==Element]
            dic['axis'] = polygon_to_line(list_axis)
        else:
            try:
                polygon = item.getElementsByTagName('polygon')[0]
            except:
                continue
            list_axis = [int(node.childNodes[0].data) for node in polygon.childNodes if type(node)==Element]
            dic['axis'] = polygon_to_line(list_axis)
        result.append(dic)
    return result

def defects_crop(xml_folder_path: str, img_folder_path: str, crop_size=64):
    current_path = os.path.join(os.getcwd(), 'out/train')
    result = {}
    xml_files = os.listdir(xml_folder_path)
    for xml_file in xml_files:
        xml_path = os.path.join(xml_folder_path, xml_file)
        infos = xml_info_out(xml_path)
        for info in infos:
            name, axis = word_to_pinyin(info['name']), info['axis']
            if name not in result:
                result[name] = 0
                os.makedirs(os.path.join(current_path, name))
            result[name] += 1
            min_x, min_y = axis[0]
            max_x, max_y = axis[1]
            center_x, center_y = (min_x + max_x) // 2, (min_y + max_y) // 2
            width, height = max_x - min_x + 1, max_y - min_y + 1
            img_crop_path = os.path.join(os.path.join(current_path, name), str(result[name])+'.jpg')
            img_path = os.path.join(img_folder_path, xml_file.replace('.xml', '.jpg'))
            img = cv2.imread(img_path)
            limit_x, limit_y = img.shape[1], img.shape[0]
            crop_min_y, crop_max_y, crop_min_x, crop_max_x = center_y - crop_size // 2, center_y + crop_size // 2, center_x - crop_size // 2, center_x + crop_size // 2
            if center_y - crop_size // 2 <= 0: crop_min_y, crop_max_y = 0, crop_size
            if center_y + crop_size // 2 >= limit_y: crop_min_y, crop_max_y = limit_y - crop_size, limit_y
            if center_x - crop_size // 2 <= 0: crop_min_x, crop_max_x = 0, crop_size
            if center_x + crop_size // 2 >= limit_x: crop_min_x, crop_max_x = limit_x - crop_size, limit_x
            img_new = img[crop_min_y:crop_max_y, crop_min_x:crop_max_x]
            cv2.imwrite(img_crop_path, img_new)
            print('%s %d is cropped'%(name, result[name]))

if __name__ == '__main__':
    defects_crop('/home/qiangde/Data/huawei/black/side/outputs', '/home/qiangde/Data/huawei/black/side')





















