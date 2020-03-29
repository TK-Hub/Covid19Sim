#==================================================================================================
#                       Covid19-Simulation
#                       Author: Tim Kolb
#                       Date: 28.03.2020
#==================================================================================================

from citizen import Citizen
import turtle
import numpy as np
import matplotlib.pyplot as plt

def init_board():
    screen = turtle.Screen()
    screen.setup(width=1000, height=1000)
    screen.bgcolor("black")
    screen.title("Covid19-Simulation")
    screen.tracer(0)
    return screen

def init_citizens():
    citizens=[]
    initial_positions=[]
    for j in range(100):
        citizen = Citizen()
        initial_x, initial_y = citizen.init_pos()
        citizens.append(citizen)
        initial_positions.append([initial_x, initial_y])
    return citizens, initial_positions

def move_citizens(cit_s, cit_h, pos_s, pos_h):
    # Re-Initialize Lists of heathy and sick citizens and their positions. These are taken as start-input for the next step
    fin_cit_s, fin_cit_h, fin_pos_s, fin_pos_h = [],[],[],[]

    for person in cit_h:
        # This function moves the citizen and returns the coordinates after the step
        x_temp, y_temp = person.move_pos()

        # Calculate distances and health status, returns the status as string
        status = person.sim_infection([x_temp, y_temp], pos_s)

        if status == "healthy":
            fin_pos_h.append([x_temp, y_temp])
            fin_cit_h.append(person)
        elif status == "sick":
            fin_pos_s.append([x_temp, y_temp])
            fin_cit_s.append(person)
        else:
            pass

    for person in cit_s:
        # This function moves the citizen and returns the coordinates after the step
        x_temp, y_temp = person.move_pos()
        fin_cit_s.append(person)
        fin_pos_s.append([x_temp, y_temp])

    #print(len(fin_cit_s), len(fin_cit_h))
    return fin_cit_s, fin_cit_h, fin_pos_s, fin_pos_h

def evaluate_data(count, inf_nrs):
    plt.plot(range(0,count), inf_nrs)
    plt.ylabel('Number of Infections')
    plt.xlabel('Simulation Steps')
    plt.show()

#==================================================================================================

if __name__ == "__main__":
    board = init_board()
    citizens, positions = init_citizens()
    citizens_s, citizens_h = citizens[:1], citizens[1:]
    position_s, position_h = positions[:1], positions[1:]

    run = True
    counter, infection_nrs = 0, []
    while run == True:
        counter+=1
        board.update()
        citizens_s, citizens_h, position_s, position_h = move_citizens(citizens_s, citizens_h, position_s, position_s)
        infection_nrs.append(len(citizens_s))
        if len(citizens_s)>99:
            run=False
    #board.mainloop()
    evaluate_data(counter, infection_nrs)