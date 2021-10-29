from random import randrange as rnd, choice
from tkinter import *
import math
import time

# print (dir(math))

root = Tk()
fr = Frame(root)
root.geometry('800x600')
canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)
x_borders = 800
y_borders = 600
points = 0

class ball():
    def __init__(self, x=40, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.vy_list = [0 for i in range(10)]
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.gravit = -3
        self.t = 1
        self.friction = 0.3
        self.stop = False
        self.energy_loss = 0.8
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill=self.color
        )
        self.live = 30

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        if not (self.stop):
            self.y -= self.vy + self.gravit / 2
        else:
            self.vx *= self.friction
            self.t += 1
            if self.t > 30:
                self.r = 0
        self.vy += self.gravit
        if self.x > x_borders - self.r or self.x < 0 + self.r:
            self.vx *= -1
        if self.y < 0 + self.r:
            self.vy = -abs(self.vy)
        if self.y > y_borders - self.r:
            self.vy = abs(self.vy) * self.energy_loss
            if abs(self.vy) <= 2:
                self.stop = True
        self.set_coords()

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:e
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        if ((self.x - obj.x) ** 2 + (self.y - obj.y) ** 2) ** 0.5 < obj.r + self.r:
            return True
        else:
            return False


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width=7)  # FIXME: don't know how to set it...

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y - new_ball.y) / (event.x - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.y - 450) / (event.x - 20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target():
    def __init__(self):
        self.live = 1
        self.vx = rnd(0, 6) / 2
        self.vy = rnd(-3, 3) / 2
        # FIXME: doesn't work!!! How to call this functions when object is created?
        self.id = canv.create_oval(0, 0, 0, 0)
        self.id_points = canv.create_text(30, 30, text=points, font='28')
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(10, 50)
        color = self.color = 'red'
        canv.coords(self.id, x - r, y - r, x + r, y + r)
        canv.itemconfig(self.id, fill=color)

    def hit(self):
        """Попадание шарика в цель."""
        global points
        canv.coords(self.id, -10, -10, -10, -10)
        points += 1

    def move(self):
        if self.live:
            self.x += self.vx
            self.y += self.vy
            if self.x > x_borders - self.r or self.x < 0 + self.r:
                self.vx *= -1
            if self.y < 0 + self.r or self.y > 600 - self.r:
                self.vy *= -1
            self.set_coords()

    def set_coords(self):
        canv.coords(
            self.id,
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r
        )

def new_game(event=''):
    global gun, t1, screen1, balls, bullet
    canv.create_rectangle(0, 0, x_borders, y_borders, fill='white')
    t1 = target()
    t2 = target()
    balls = []
    screen1 = canv.create_text(400, 300, text='', font='28')
    g1 = gun()
    t1.new_target()
    t2.new_target()
    bullet = 0
    game_stopped = False
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    while (t1.live or t2.live or balls) and not game_stopped:
        t1.move()
        t2.move()
        for b in balls:
            b.move()
            if b.hittest(t1) and t1.live:
                t1.live = False
                t1.hit()
                canv.itemconfig(t1.id_points, text=points)
                canv.itemconfig(t2.id_points, text=points)
            if b.hittest(t2) and t2.live:
                t2.live = False
                t2.hit()
                canv.itemconfig(t1.id_points, text=points)
                canv.itemconfig(t2.id_points, text=points)
            if not t2.live and not t1.live:
                canv.bind('<Button-1>', '')
                canv.bind('<ButtonRelease-1>', '')
                canv.itemconfig(screen1, text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
                canv.update()
                game_stopped = True
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    time.sleep(0.6)
    print('here')
    canv.itemconfig(screen1, text='')
    canv.delete(gun)
    canv.update()
    new_game()


new_game()

mainloop()