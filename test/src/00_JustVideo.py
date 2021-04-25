import cv2

# VideoCapture オブジェクトを取得します
capture = cv2.VideoCapture(1)

# フレームサイズの取得
# width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

# フレームサイズの変更
# ret, frame = capture.read()
# capture = cv2.resize(frame, size)


while(True):
    ret, frame = capture.read()
    # resize the window
    size = (800, 600)
    frame = cv2.resize(frame, size)

    cv2.imshow('title', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


capture.release()
cv2.destroyAllWindows()
