import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

from SG90servo_ver2 import SG90servo
from Camera.BlobAnalysis import BlobAnalysis
from Camera.Camera import Camera


def main():

    """カメラ設定"""
    # 動画を取得
    capture = cv2.VideoCapture(0)
    # 幅
    W = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    # 高さ
    H = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # 中心座標
    center = (W/2, H/2)
    
    """サーボモータ設定"""
    sg90 = SG90servo(12)
    # 角度を0度に設定する
    deg = 0
    sg90.servo_deg(deg)
    time.sleep(3)


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
            
            # サーボモータの制御
            if center[0] < center_x and abs(center[0] - center_x) > 50:
                deg -= 3
                if deg < -90:
                    deg = -90
                sg90.servo_deg(deg)
                time.sleep(0.1)
                sg90.stop()
        
            elif center[0] > center_x and abs(center[0] - center_x) > 50:
                deg += 3
                if deg > 90:
                    deg = 90
                sg90.servo_deg(deg)
                time.sleep(0.1)
                sg90.stop()

        cv2.imshow("Frame", frame)
        # cv2.imshow("Mask", mask)
        
        
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()
    sg90.servo_deg(0)
    time.sleep(1)
    GPIO.cleanup()
    print("---END---")


if __name__ == '__main__':
    main()
