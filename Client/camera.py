import cv2


def save_photo(save_route):
    # cap = cv2.VideoCapture(0)  # Jetson Nano接入的摄像头
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 笔记本接入的摄像头
    if cap.isOpened():
        ret_val, img = cap.read()
        cv2.imwrite(save_route, img)
        # print('Picture Get!')
        cap.release()
    
    else:
        print("Unable to open camera")
