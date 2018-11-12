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

data = None
font = cv2.FONT_HERSHEY_SIMPLEX

def recv():
    global data
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            #print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break

def forward_land():

    sock.sendto(b"takeoff", tello_address)
    time.sleep(5)
    sock.sendto(b"forward 150", tello_address)
    time.sleep(5)
    sock.sendto(b"land", tello_address)

def display_status():
    global data,tello_img
    try:
        battery = data.decode(encoding="utf-8")
        battery = battery[:2] 
        cv2.putText(tello_img, battery + "%", (330, 240), font, 1, (0,255,0), thickness=4)
        cv2.rectangle(tello_img, (310,250),(310 + int(battery),270),(0,0,255),thickness=-1)
        cv2.rectangle(tello_img, (310,250),(410,270),(255,255,0),thickness=2)    
    except TypeError:
        pass
    except AttributeError:
        pass
    except ValueError:
        pass

print ('\r\n\r\nTello Python3 Demo.\r\n')

print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

print ('end -- quit demo.\r\n')


#recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()

tello_img = None
msg = None
speed = input("Speed=")

sock.sendto(b"command", tello_address)

while True: 
    tello_img = cv2.imread("./tello.jpg")
    try:
        sock.sendto(b"battery?",tello_address)
        display_status()
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
        elif k == ord('f'):
            forward_land()
        if msg == None:
            continue
        # Send data
        #msg = msg.decode(encoding="utf-8")
        msg = msg.encode(encoding="utf-8") 
        send = sock.sendto(msg, tello_address)
        msg = None
    
    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()  
        break


