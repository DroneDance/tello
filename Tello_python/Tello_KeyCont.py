#
# Tello Python3 Control Demo 
#
# http://www.ryzerobotics.com/
#
# 1/1/2018

import threading 
import socket
import sys
import time
import cv2

host = ''
port = 9000
locaddr = (host,port) 


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_address = ('192.168.10.1', 8889)

sock.bind(locaddr)

def recv():
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break


print ('\r\n\r\nTello Python3 Demo.\r\n')

print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

print ('end -- quit demo.\r\n')


#recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()

tello_img = cv2.imread("./tello.jpg")
msg = None
speed = input("Speed=")

sock.sendto(b"command", tello_address)

while True: 

    try:
        cv2.imshow("Tello Control!", tello_img)
        
        k = cv2.waitKey(1)
        if k == ord('q'):
            sock.sendto(b"land", tello_address)
            sock.close()
            break  
        if k == ord('t'):
            msg = "takeoff"
            print("Takeoff!")
        elif k == ord('l'):
            msg = "land"
            print("Land!")
        elif k == ord('a'):
            msg = "left " + speed
        elif k == ord('d'):
            msg = "right " + speed
        elif k == ord('w'):
            msg = "forward " + speed
        elif k == ord('s'):
            msg = "back " + speed
        if msg == None:
            continue
        # Send data
        #msg = msg.decode(encoding="utf-8")
        msg = msg.encode(encoding="utf-8") 
        sent = sock.sendto(msg, tello_address)
        msg = None
    
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()  
        break


