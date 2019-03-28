# coding: UTF-8
"""
User: 五根弦的吉他
function：simple knn识别简单验证码（纯数字、无扭曲、无遮挡、排列整齐）
"""
import numpy as np
import math
from scipy.misc import imread
import os


def knn(k, pure_data, labels, test_data):
    """
    :param k:
    :param pure_data:
    :param labels:
    :param test_data:  一个batch的数组
    :return:
    """
    predict_labels = []
    if type(test_data) is not list:
        test_data = list(test_data)
    for each in test_data:
        res = np.tile(each, (pure_data.shape[0], 1)) - pure_data
        #math.sqrt(np.sum(res**2, axis=1))
        distance = np.sum(res ** 2, axis=1)**0.5

        sorted_index = distance.argsort()  # 返回从小到大排序后的数据的在原数组中的下标
        count_dict = {}
        """
        # 这样写会出错，why？？？数目对应不起来
        count_dict = {labels[sorted_index[i]]: count_dict.get(labels[sorted_index[i]], 0) + 1 for i in range(k)}
        onesort = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
        """

        for i in range(k):
            count_dict[label[sorted_index[i]]] = count_dict.get(labels[sorted_index[i]], 0) + 1
        onesort = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)

        
        print("count_dict:\n", onesort)
        #print("sortedclascount:\n", sortedClassCount)
        print("{}的类别是：{}".format(test_data_path, onesort[0][0]))
        predict_labels.append(onesort[0][1])

    return predict_labels


def chg_img2data(img_path):
    """
    对单张图片进行处理
    :param img_path:
    :return:
    """
    m = imread(img_path, mode='L')
    # 取5个数字的像素矩阵并reshape成行向量
    d1 = m[4:18, 4:14].reshape(1, 140)   # 单写一个数的话，默认行是1
    d2 = m[4:18, 13:23].reshape(1, 140)
    d3 = m[4:18, 22:32].reshape(1, 140)
    d4 = m[4:18, 31:41].reshape(1, 140)
    d5 = m[4:18, 40:50].reshape(1, 140)
    # 将5个行向量垂直堆叠在一起, 传入元组

    return np.vstack((d1, d2, d3, d4, d5))


def change_all_img(folderpath):
    # 对文件夹下所有图片进行处理
    label_list = []
    for filename in os.listdir(folderpath):
        print(filename)
        label_list.extend(filename[0:5])
        yield {
            'each_vstack': chg_img2data(os.path.join(folderpath, filename)),
            'label_list': label_list
        }

"""
# 这样直接拼接起来也会出错，虽不报错，但最后得到的数据是错的
def concat(generator):
    for index, item in enumerate(generator):
        if index==0:
            new_vstack = item['each_vstack']
            print("vstack:\n", item['each_vstack'])
            continue
        print("v_stack:\n", item['each_vstack'])
        new_vstack = np.vstack((item['each_vstack'], new_vstack))
        label_list = item['label_list']
    print('new_vstack:\n', new_vstack)
    print('shape of new_vstack:', new_vstack.shape)
    print('label_list:\n', label_list)
    label = np.array(label_list)
    print("label:\n", label)
    return new_vstack, label
"""


def concat(generator):
    datax = []
    for index, item in enumerate(generator):
        datax.extend(item['each_vstack'])
        label = item['label_list']
    print("label_list:\n", label)
    np.savez('data.npz', dataimg=datax, label=label)


if __name__ == '__main__':
    data_folder = './data'
 
    test_data_path = './test/test3.aspx'
    #data, label = concat(change_all_img(data_folder))
    concat(change_all_img(data_folder))
    DATA = np.load('data.npz')
    data = DATA['dataimg']
    label = DATA['label']
    knn(k=5, pure_data=data, labels=label, test_data=chg_img2data(test_data_path))

