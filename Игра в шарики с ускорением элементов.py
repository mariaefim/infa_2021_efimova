from tkinter import *
from random import randrange as rnd, choice
import time

root = Tk()
root.geometry('800x600')
canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)
colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

class Ball(object):
    # Класс цветных шариков.
        # X, y - координаты, r - радиус
        # Color - цвет
        #vel_x, vel_y - проекции скорости на x и на y соответственно

        def __init__(self, x, y, r, color, vel_x=3, vel_y=3):
            self.color = color
            self.x = x
            self.y = y
            self.r = r
            self.vel_x = vel_x
            self.vel_y = vel_y


balls = []
for i in range(10):
    balls.append(Ball(rnd(100, 700), rnd(100, 500), rnd(30, 50), choice(colors)))


def new_ball():
    global Ball1
    # Создает новые шары раз в 1 секунду, вызывая саму себя.
    # x, y - координаты (случайные в промежутке 100-700, 100-500
    # r - радиус
    canv.delete(ALL)
    for i in range(10):
        canv.create_oval(balls[i].x - balls[i].r, balls[i].y - balls[i].r, balls[i].x + balls[i].r, balls[i].y + balls[i].r, fill=balls[i].color, width=0)
    root.after(1000, balls_movements)

def balls_movements():
    for i in range(10):
        balls[i].y += balls[i].vel_y
        balls[i].x += balls[i].vel_x
        if balls[i].x > 800 - balls[i].r or balls[i].x < 0 + balls[i].r:
            balls[i].vel_x *= -1
        if balls[i].y > 600 - balls[i].r or balls[i].y < 0 + balls[i].r:
            balls[i].vel_y *= -1
    canv.delete(ALL)
    for i in range(10):
        canv.create_oval(balls[i].x - balls[i].r, balls[i].y - balls[i].r, balls[i].x + balls[i].r, balls[i].y + balls[i].r, fill=balls[i].color,
                     width=0)
    canv.create_text(100, 100, text='your score: ' + str(point),
                              justify=CENTER, font="Verdana 14")
    root.after(10, balls_movements)

def click(event):
    global point
    scores = canv.create_text(100, 100, text="",
                      justify=CENTER, font="Verdana 14")
    for i in range(10):
        if ((event.x - balls[i].x)**2 + (event.y - balls[i].y)** 2) ** 0.5 <= balls[i].r:
            canv.create_rectangle(35, 90, 170, 110, fill='white', outline='white')
            point += 1
            scores = canv.create_text(100, 100, text='your score: ' + str(point),
                      justify=CENTER, font="Verdana 14")
            balls[i].vel_x += point
            balls[i].vel_y += point
            if balls[i].vel_x > 20:
                balls[i].r = 0



point = 0
new_ball()
canv.bind('<Button-1>', click)
mainloop()
