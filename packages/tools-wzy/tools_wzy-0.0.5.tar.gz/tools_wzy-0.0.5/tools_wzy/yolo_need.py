# coding:utf-8

import os
import random
import xml.etree.ElementTree as ET


# xml_to_yolo把文件夹下所有xml转换为yolo格式的label，
# split_train_val，获取所有xml文件路径，然后将其按照一定比例划分为train, val, test

def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def xml_to_yolo(xml_folder, xml_name, labels_folder, class_list=None):
    if class_list is None:
        class_list = ["person"]
    in_file = open(xml_folder + '/' + xml_name, encoding='UTF-8')
    out_file = open(labels_folder + '/' + xml_name[:-3] + 'txt', 'w')  # 这边写txt是要写到label这个文件夹中的。
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        # difficult = obj.find('Difficult').text
        cls = obj.find('name').text
        if cls not in class_list or int(difficult) == 1:
            continue
        cls_id = class_list.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        b1, b2, b3, b4 = b
        # 标注越界修正
        if b2 > w:
            b2 = w
        if b4 > h:
            b4 = h
        b = (b1, b2, b3, b4)
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


def xmls_to_yolo(xmls_folder, class_list=None):
    if class_list is None:
        class_list = ['person']
    # 创建label文件夹
    up_folder = os.path.dirname(xmls_folder)
    labels_folder = up_folder + '/labels'
    os.makedirs(labels_folder, exist_ok=True)

    # 对xml_folder下所有文件进行转换
    xml_names = [f.name for f in os.scandir(xmls_folder) if f.is_file()]
    for xml_name in xml_names:
        xml_to_yolo(xmls_folder, xml_name, labels_folder, class_list)
    print("xml文件转换成功：" + labels_folder)
    return labels_folder


def split_train_val(xmls_folder, trainval_proportion=0.9, train_proportion=0.8):
    # trainval_proportion: 训练集和验证集占总体的比例，剩下的是测试集
    # train_proportion: 训练集占train_val比例，可自己进行调整

    # 创建label文件夹
    up_folder = os.path.dirname(xmls_folder)
    split_folder = up_folder + '/dataSet_path'
    images_folder = up_folder + '/images'
    os.makedirs(split_folder, exist_ok=True)

    # 读取所有xml文件名，拼接到
    xmls_names = [os.path.join(images_folder, f.name[:-4]+'.jpg') for f in os.scandir(xmls_folder) if f.is_file()]
    # 随机划分
    num = len(xmls_names)
    list_index = range(num)
    tv = int(num * trainval_proportion)
    tr = int(tv * train_proportion)
    trainval = random.sample(list_index, tv)
    train = random.sample(trainval, tr)

    # 写入四个文件
    file_trainval = open(split_folder + '/trainval.txt', 'w')
    file_test = open(split_folder + '/test.txt', 'w')
    file_train = open(split_folder + '/train.txt', 'w')
    file_val = open(split_folder + '/val.txt', 'w')

    for i in list_index:
        name = xmls_names[i][:-4] + '.jpg\n'
        if i in trainval:
            file_trainval.write(name)
            if i in train:
                file_train.write(name)
            else:
                file_val.write(name)
        else:
            file_test.write(name)

    file_trainval.close()
    file_train.close()
    file_val.close()
    file_test.close()
    print("数据集划分成功：" + split_folder)
    return split_folder


def gen_yaml(dataSet_folder, class_list, yaml_name = 'dataset.yaml'):
    import yaml

    # 数据集配置参数
    params = {
        'path': dataSet_folder,
        'train': dataSet_folder + '/train.txt',
        'val': dataSet_folder + '/val.txt',
        'test': dataSet_folder + '/test.txt',
        'nc': len(class_list),
        'names': {i: category for i, category in enumerate(class_list)}
    }


    # 将数据集配置参数写入 YAML 文件
    yaml_path = os.path.dirname(dataSet_folder) + '/' + yaml_name
    yaml.Dumper.ignore_aliases = lambda *args: True # 设置默认流参数以保留键值对的顺序
    with open(yaml_path, 'w') as f:
        yaml.dump(params, f, sort_keys=False)
    print("data yaml文件生成成功：" + yaml_path)
    return yaml_path

if __name__ == '__main__':
    xmls_folder = r'F:\Zhiyuan\pic_annotations_data\Annotations'
    class_list = ["person"]
    labels_folder = xmls_to_yolo(xmls_folder, class_list)
    dataSet_folder = split_train_val(xmls_folder, 0.5, 0.5)
    yaml_path = gen_yaml(dataSet_folder, class_list, 'test.yaml')



