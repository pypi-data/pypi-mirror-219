import cv2
import math
import numpy as np
import os, shutil
from matplotlib import pyplot as plt

def addnoisy(image, n=10000):
    """
    :param image: 原始图像
    :param n: 添加椒盐的次数,默认为10000
    :return: 返回被椒盐处理后的图像
    """
    result = image.copy()
    w, h = image.shape[:2]
    for i in range(n):
        # 分别在宽和高的范围内生成一个随机值，用以代表x, y坐标
        x = np.random.randint(0, w)
        y = np.random.randint(0, h)
        if np.random.randint(0, 2) == 0:   #产生0，1的随机数
            # 生成白色噪声（盐噪声）
            result[x, y] = 0
        else:
            # 生成黑色噪声（椒噪声）
            result[x, y] = 255
    return result

def getContours(img, cThr=(100, 100), showCanny=False, minArea=1000, filter=0, draw=True):
    """
    :param img: 输入图像
    :param cThr: 阈值
    :param showCanny:展示经过处理后的边缘,默认Fales
    :param minArea: 更改大小
    :param filter: 过滤
    :param draw: 绘制边缘
    :return: 返回图像轮廓
    """
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=3)
    imgThre = cv2.erode(imgDial, kernel, iterations=2)
    if showCanny: cv2.imshow('Canny', imgThre)
    contours, hiearchy = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finalCountours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalCountours.append([len(approx), area, approx, bbox, i])
            else:
                finalCountours.append([len(approx), area, approx, bbox, i])
    finalCountours = sorted(finalCountours, key=lambda x: x[1], reverse=True)
    if draw:
        for con in finalCountours:
            cv2.drawContours(img, con[4], -1, (0, 0, 255), 3)
    return img, finalCountours


def empty(a):
    pass

