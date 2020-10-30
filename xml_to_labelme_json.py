import os
import json
from pypinyin import pinyin, NORMAL
from xml.etree import ElementTree as ET


def word_to_pinyin(word: str):
    s = ''
    for i in pinyin(word, style=NORMAL):
        s += ''.join(i)
    return s

# 单个xml文件对应一张图片，转为json文件放在图片目录下
def xml_to_labelme_json(xml_path: str, img_folder_path):
    img_name = xml_path[xml_path.rindex(os.sep)+1:xml_path.rindex('.xml')]
    json_path = os.path.join(img_folder_path, img_name+'.json')
    root = ET.parse(xml_path).getroot()
    # 'shapes' is used to store points like [[x1,y1],[x2,y2],...]
    json_out = {'version': '1.0', 'shapes': [], 'imageData': None, 'imageWidth': int(root[4][0].text), 'imageHeight': int(root[4][1].text), 'imageDepth': int(root[4][2].text), 'imagePath': img_name+'.jpg'}
    items = root[1][0]
    for item in items:
        instance = {'label': word_to_pinyin(item[0].text), 'points': []}
        axiss = item[2]
        if len(axiss) <=4:
            x1, y1, x2, y2 = float(axiss[0].text), float(axiss[1].text), float(axiss[2].text), float(axiss[3].text)
            x_min, y_min, x_max, y_max = min([x1, x2]), min([y1, y2]), max([x1, x2]), max([y1, y2])
            instance['points'].extend([[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]])
        else:
            for i, axis in enumerate(axiss):
                if i%2 == 1: instance['points'].append([float(axiss[i-1].text), float(axiss[i].text)])
        json_out['shapes'].append(instance)
    print('Json created: ', json_out)
    with open(json_path, 'w', encoding='utf-8') as f:
        content = json.dumps(json_out, ensure_ascii=False)
        f.write(content)
        f.close()

# json文件需要和imgs在同一目录下
def delete_json(img_folder_path: str):
    for file in os.listdir(img_folder_path):
        if file.endswith('.json'):
            os.remove(os.path.join(img_folder_path, file))

if __name__ == '__main__':
    # xml folder path
    pre = '/home/qiangde/Data/side/outputs'
    xml_files = os.listdir(pre)
    for xml_file in xml_files:
        xml_to_labelme_json(os.path.join(pre, xml_file), '/home/qiangde/Data/side') # image folder path
    # delete_json('/home/qiangde/Data/side')




















