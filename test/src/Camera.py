"""
画面上にカメラの取得動画を表示する
また、赤色のマスク動画も表示する
ブロブ解析→画像をラベリング処理し、ラベル付けされた領域の特徴を解析すること
参考URL:https://algorithm.joho.info/programming/python/opencv-color-tracking-py/
"""

import cv2
import numpy as np


class Camera:

    def __init__(self, frame):
        self.frame = frame

    def color_detector(self):
        # HSVに変換
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

        # 赤色のHSVの値域1
        hsv_min = np.array([0, 127, 0])
        hsv_max = np.array([30, 255, 255])
        mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

        # 赤色のHSVの値域2
        hsv_min = np.array([150, 127, 0])
        hsv_max = np.array([179, 255, 255])
        mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

        return mask1 + mask2

