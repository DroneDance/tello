import cv2

tello_add = "udp://192.168.10.1:6038?overrun_nonfatal=1&fifo_size=50000000"
cap = cv2.VideoCapture(tello_add)

while True:
    ret, frame = cap.read()
    cv2.imshow("show image!", frame)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
