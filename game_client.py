from graphics import *
import random, threading
import keyboard
import time
import socket
gold = 0
gld2 = 0
size = 500
win=GraphWin("test", size, size)
win.setBackground("black")
posX = random.randint(1, int(size / 50)) * 50 - 25
posY = random.randint(1, int(size / 50)) * 50 - 25
oldX, oldY = posX, posY
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(('92.63.104.186', 5051))
oldX2=0
oldY2=0

x1, y1 = 0, 0
x2, y2 = 50, 50
for i in range(round(size/50)):
    for g in range(round(size/50)):
        cr = Rectangle(Point(x1, y1), Point(x2, y2))
        cr.setOutline("black")
        cr.setFill("green")
        cr.draw(win)
        x1 += 50
        x2 += 50
    x1=0
    x2=50
    y1+=50
    y2+=50
# gx = random.randint(1, size / 50) * 50 - 25
# gy = random.randint(1, size / 50) * 50 - 25
golddata=["25", "25"]
gore = Circle(Point(25, 25), 20)
gore.setFill("gold")
gore.draw(win)

pers = Circle(Point(posX, posY), 15)
txt = Text(Point(posX, posY), gold)
txt2 = Text(Point(0, 0), gld2)
pers.setFill("red")
pers.draw(win)
txt.draw(win)
txt2.draw(win)
running = True
pers2 = Circle(Point(0,0), 15)
pers2.setFill("blue")
pers2.draw(win)

gdata=['0','0']

def main():
    global pers
    global txt
    global win
    global oldX, oldY, posX, posY, gx, gy, gold, gore
    global sock
    global pers2
    global oldX2, oldY2, gdata, sock, golddata, txt2, gld2
    gx = golddata[0]
    gy = golddata[1]
    gore.undraw()
    gore = Circle(Point(gx, gy), 20)
    gore.setFill("yellow")
    gore.draw(win)
    #print(posX, posY, gx, gy)
    if posX == int(gx) and posY == int(gy):
        golddata = [str(random.randint(25, 250)*-1), str(random.randint(25, 250)*-1)]
        sock.send(("GG").encode('utf-8'))
        #print("sent")
        gore.undraw()
        gx = golddata[0]
        gy = golddata[1]
        gold += 1
        sock.send(('{0}+G'.format(gold)).encode('utf-8'))
        txt.setText(gold)
        gore = Circle(Point(gx, gy), 20)
        gore.setFill("yellow")
        gore.draw(win)
        print(str(gold)+'g')

    #print(gdata)
    if posX != oldX:
        pers.move(posX-oldX, 0)
        txt.move(posX - oldX, 0)
        oldX = posX
        sock.send(('{0}+X'.format(posX)).encode('utf-8'))
        time.sleep(0.1)
    if posY != oldY:
        pers.move(0, posY - oldY)
        txt.move(0, posY - oldY)
        oldY = posY
        sock.send(('{0}+Y'.format(posY)).encode('utf-8'))
        time.sleep(0.1)
    if gdata[1] == "Y":
        pers2.undraw()
        txt2.undraw()
        pers2 = Circle(Point(oldX2, gdata[0]), 15)
        oldY2 = gdata[0]
        pers2.setFill("blue")
        pers2.draw(win)
        txt2 = Text(Point(oldX2, gdata[0]), gld2)
        txt2.setText(gld2)
        txt2.draw(win)
        gdata[1] = "0"
    if gdata[1] == "X":
        pers2.undraw()
        txt2.undraw()
        pers2 = Circle(Point(gdata[0], oldY2), 15)
        oldX2 = gdata[0]
        pers2.setFill("blue")
        pers2.draw(win)
        txt2 = Text(Point(gdata[0], oldY2), gld2)
        txt2.setText(gld2)
        txt2.draw(win)
        gdata[1] = "0"


def proc_input():
    global pers, posX, posY
    if keyboard.is_pressed('w'):
        posY = posY - 50
    if keyboard.is_pressed('s'):
        posY = posY + 50
    if keyboard.is_pressed('a'):
        posX = posX - 50
    if keyboard.is_pressed('d'):
        posX = posX + 50

def multiplayer():
    global sock, oldX2, oldY2, pers2, gdata, golddata, gld2, txt2
    sock.send(('{0}+Y'.format(posY)).encode('utf-8'))
    sock.send(('{0}+X'.format(posX)).encode('utf-8'))
    while True:
        data = sock.recv(1024)
        #print(data)
        data2 = data.decode('utf-8').split("$")
        data = data2[0].split("+")
        golddata = data2[1].split(":")
        #print(golddata, data2[1])
        gdata=data
        print(gdata)
        if gdata[1] == "G":
            gld2=gdata[0]


b=threading.Thread(target=multiplayer, args=())
b.start()
while running:
    main()
    proc_input()
