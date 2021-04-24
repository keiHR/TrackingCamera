import cv2
import numpy as np

from BlobAnalysis import BlobAnalysis
from Camera import Camera


def main():

    # 動画を取得
    capture = cv2.VideoCapture(0)
    # 幅
    W = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    # 高さ
    H = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # 中心座標
    center = (W/2, H/2)

    while True:
        ret, frame = capture.read()

        # マスク画像の取得
        mask = Camera(frame).color_detector()

        # マスク画像がある（赤色が含まれる）時はブロブ解析を行う
        if np.max(mask) != 0:
            # マスク画像のブロブ解析
            target = BlobAnalysis(mask).analysis()

            # フレームに面積最大ブロブの中心周囲を円で描く
            # 面積最大ブロブの中心座標を取得
            center_x = int(target["center"][0])
            center_y = int(target["center"][1])
            # 円で描く
            # cv2.circle(frame, (center_x, center_y), 30, (0, 200, 0), thickness=3, lineType=cv2.LINE_AA)

            # フレームに面積最大ブロブの周囲を四角で囲む
            upper_left = target["upper_left"]
            lower_right = (upper_left[0] + target["width"], upper_left[1] + target["height"])
            cv2.rectangle(frame, upper_left, lower_right, (0, 200, 0), thickness=3, lineType=cv2.LINE_AA)

        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
