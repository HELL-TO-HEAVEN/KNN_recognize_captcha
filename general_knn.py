# coding: UTF-8
import numpy as np
import math


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

        sorted_index = distance.argsort()
        count_dict = {}
        count_dict = {labels[i]: count_dict.get(labels[i], default=0) + 1 for i in range(k)}
        sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
        print("{}的类别是：", count_dict[0])
        predict_labels.append(count_dict[0])

    return predict_labels




