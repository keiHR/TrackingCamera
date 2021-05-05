import RPi.GPIO as GPIO
import main

class SG90servo():
    def __init__(self,motorport=2):
        self.port = motorport
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.port, GPIO.OUT)
        self.servo = GPIO.PWM(self.port, 50)

        self.servo.start(0.0) # set duty cicle to 0-100
        self.minlim = -90
        self.maxlim = 90

    # サーボモータを動かす関数
    def servo_deg(self,deg):

        if deg > self.maxlim:
            print("Exceed max degree!")
            return
        elif deg < self.minlim:
            print("Exceed min degree!")
            return
        
        cycle = 7.25+4.75*deg/90.0
        self.servo.ChangeDutyCycle(cycle)
        
        
    #トラッキング用の関数
    def tracking(self, type, deg, center, bin, target, step):
        
        # 最大回転角度
        max = 90
        # 最小回転角度 typeが0：水平回転　typeが1：垂直回転
        if type == 0:
            min = -90
        else:
            min = -30
        
        # 回転するか否かを判定する閾値　カメラの中心と対象物の距離が閾値よりも大きいとトラッキングするようにする
        threshold = center / bin
        
        # モータの回転制御
        if center < target and abs(center - target) > threshold:
            deg -= step
            if deg < min:
                deg = min
        elif center > target and abs(center - target) > threshold:
            deg += step
            if deg > max:
                deg = max
        self.servo_deg(deg)
        

    def stop(self):
        self.servo.start(0.0)
