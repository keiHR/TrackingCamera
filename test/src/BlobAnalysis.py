import cv2
import numpy as np


class BlobAnalysis:

    def __init__(self, binary_img):
        self.binary_img = binary_img

    def analysis(self):
        nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(self.binary_img)
        # 2値画像のラベリング処理
        """
        nlabels:ラベルの数
        labels:画像のラベリング結果を保持している二次元配列。配列の要素は、各ピクセルのラベル番号となっている。
        stats:オブジェクトのバウンディングボックス（開始点の x 座標、y 座標、幅、高さ）とオブジェクトのサイズ。
       　　　　 左上の x 座標, 左上の y 座標, 幅, 高さ, 面積 の順で格納
        centroids:オブジェクトの重心
        """
        nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(self.binary_img)

        # 面積最大ブロブの情報格納用
        maxblob = {}

        # ブロブ情報を項目別に抽出
        # nはラベルの数で、画像の背景が０とラベリングされているので、−１することで実際のオブジェクトの数を返す
        n = nlabels - 1

        # 背景画像の情報を削除
        data = np.delete(stats, 0, 0)
        center = np.delete(centroids, 0, 0)

        # ブロブ面積最大のインデックス
        max_index = np.argmax(data[:, 4])

        # 面積最大ブロブの各種情報を取得
        maxblob["upper_left"] = (data[:, 0][max_index], data[:, 1][max_index])  # 左上座標
        maxblob["width"] = data[:, 2][max_index]  # 幅
        maxblob["height"] = data[:, 3][max_index]  # 高さ
        maxblob["area"] = data[:, 4][max_index]  # 面積
        maxblob["center"] = center[max_index]  # 中心座標

        return maxblob

