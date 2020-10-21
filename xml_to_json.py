import os

from pypinyin import pinyin, NORMAL
from xml.etree import ElementTree as ET


def word_to_pinyin(word: str):
    s = ''
    for i in pinyin(word, style=NORMAL):
        s += ''.join(i)
    return s

def xml_to_labelme_json(xml_path: str, img_folder_path):
    img_name = xml_path[xml_path.rindex(os.sep)+1:xml_path.rindex('.xml')]
    json_path = os.path.join(img_folder_path, img_name+'.json')
    root = ET.parse(xml_path).getroot()
    json_out = {'version': '1.0', 'imageData': None, 'imageWidth': root[4][0].text, 'imageHeight': root[4][1].text, 'imageDepth': root[4][2].text, 'imagePath': img_name+'.jpg'}
    





if __name__ == '__main__':
    print(os.sep)





















