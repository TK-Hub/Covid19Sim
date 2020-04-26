#==================================================================================================
#                       Class Definitions for Covid19-Simulation
#                       Author: T.K.
#                       Date: 28.03.2020
#==================================================================================================
import random
import turtle
import time
import numpy as np

class Citizen:
    def __init__(self):

        # Initialize basic properties of single citizen
        self.pos_x = random.randint(-400,400)
        self.pos_y = random.randint(-400,400)
        self.status = "healthy"
        self.sickdays = 0


    def init_pos(self):
        self.man = turtle.Turtle()
        self.man.shape("circle")
        self.man.color("green")
        self.man.penup()
        self.man.goto(self.pos_x, self.pos_y)
        self.man.dx=random.randint(-4,4)
        self.man.dy=random.randint(-4,4)
        return self.pos_x, self.pos_y

    def move_pos(self):
        
        # Concentrate on central spot
        """prob = random.random()
        print(prob)

        if prob < 0.002:
            self.man.goto(0,0)
        else:
            self.man.setx(self.man.xcor() + self.man.dx)
            self.man.sety(self.man.ycor() + self.man.dy)"""

        # Random Walk
        self.man.setx(self.man.xcor() + self.man.dx)
        self.man.sety(self.man.ycor() + self.man.dy)

        if self.man.xcor() > 400:
            self.man.dx *= -1
        if self.man.xcor() < -400:
            self.man.dx *= -1
        if self.man.ycor() > 400:
            self.man.dy *= -1
        if self.man.ycor() < -400:
            self.man.dy *= -1
        
        if 1 <= self.sickdays < 250:
            self.sickdays+=1
        if self.sickdays == 250:
            self.man.color("grey")
            self.sickdays+=1
            self.status="recovered"

        return self.man.xcor(), self.man.ycor(), self.status

    def sim_infection(self, coo_temp, comp_pos):
        for i in comp_pos:
            dist = np.sqrt(np.sum((np.asarray(i) - np.asarray(coo_temp)) ** 2))
            if (dist < 15) and (random.random()<0.7):
                self.status="sick"
                self.man.color("red")
                self.sickdays+=1
                break
            else:
                self.status="healthy"
        return self.status


class Pool_Citizen:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = "healthy"

class Covid_Pool:
    def __init__(self, size):
        # Initialize basic properties of single citizen
        self.size = size
        self.citizen_list_healthy = [Pool_Citizen(0, 0) for i in range(self.size)]
        self.citizen_list_sick, self.citizen_list_healed, self.citizen_list_dead = [], [], []
        self.prob_sick = 0
        self.sim_days = 0

    def calculate_probabilities(self):
        self.prob_sick = len(self.citizen_list_sick) / (self.citizen_list_healthy)
        return self.prob_sick

    def a_day_in_the_city(self):
        calculate_probabilities()
        for citizen in self.citizen_list_healthy:
            if random.random() < self.prob_sick:
                citizen.status = "sick"
                
        self.sim_days += 1