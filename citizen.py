#==================================================================================================
#                       Class Definitions for Covid19-Simulation
#                       Author: Tim Kolb
#                       Date: 28.03.2020
#==================================================================================================
import random
import turtle
import time
import numpy as np

class Citizen:
    def __init__(self):

        # Initialize basic properties of single citizen
        self.pos_x = random.randint(-500,500)
        self.pos_y = random.randint(-500,500)
        self.status = "healthy"
        self.sickdays = 0


    def init_pos(self):
        self.man = turtle.Turtle()
        self.man.shape("circle")
        self.man.color("green")
        self.man.penup()
        self.man.goto(self.pos_x, self.pos_y)
        self.man.dx=random.randint(-3,3)
        self.man.dy=random.randint(-3,3)
        return self.pos_x, self.pos_y

    def move_pos(self):
        self.man.setx(self.man.xcor() + self.man.dx)
        self.man.sety(self.man.ycor() + self.man.dy)

        if self.man.xcor() > 500:
            self.man.dx *= -1
        if self.man.xcor() < -500:
            self.man.dx *= -1
        if self.man.ycor() > 500:
            self.man.dy *= -1
        if self.man.ycor() < -500:
            self.man.dy *= -1
        
        if 1 <= self.sickdays < 300:
            self.sickdays+=1
        if self.sickdays == 300:
            self.man.color("grey")
            self.sickdays+=1
            self.status="recovered"

        return self.man.xcor(), self.man.ycor(), self.status

    def sim_infection(self, coo_temp, comp_pos):
        for i in comp_pos:
            dist = np.sqrt(np.sum((np.asarray(i) - np.asarray(coo_temp)) ** 2))
            if dist < 15:
                self.status="sick"
                self.man.color("red")
                self.sickdays+=1
                break
            else:
                self.status="healthy"
        return self.status
