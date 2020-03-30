#==================================================================================================
#                       Covid19-Simulation
#                       Author: T.K.
#                       Date: 28.03.2020
#==================================================================================================

from citizen import Citizen
import turtle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def init_board():
    screen = turtle.Screen()
    screen.setup(width=800, height=800)
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

def move_citizens(cit_s, cit_h, cit_r, pos_s, pos_h, pos_r):
    # Re-Initialize Lists of heathy and sick citizens and their positions. These are taken as start-input for the next step
    fin_cit_s, fin_cit_h, fin_cit_r, fin_pos_s, fin_pos_h, fin_pos_r = [],[],[],[],[],[]

    for person in cit_h:
        # This function moves the citizen and returns the coordinates after the step
        x_temp, y_temp, status = person.move_pos()

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
        x_temp, y_temp, status = person.move_pos()

        if status == "sick":
            fin_pos_s.append([x_temp, y_temp])
            fin_cit_s.append(person)
        elif status == "recovered":
            fin_pos_r.append([x_temp, y_temp])
            fin_cit_r.append(person)
        else:
            pass

    for person in cit_r:
        # This function moves the citizen and returns the coordinates after the step
        x_temp, y_temp, status = person.move_pos()
        fin_cit_r.append(person)
        fin_pos_r.append([x_temp, y_temp])

    #print(len(fin_cit_s), len(fin_cit_h), len(fin_cit_r))

    return fin_cit_s, fin_cit_h, fin_cit_r, fin_pos_s, fin_pos_h, fin_pos_r

def evaluate_data(count, inf_nrs, rec_nrs):
    # Create datasets to plot
    const = [100] * count
    recovered = np.asarray(inf_nrs) + np.asarray(rec_nrs)
    
    # Create and Show Plot
    plt.plot(range(0,count), const, color="green")
    plt.fill_between(range(0,count), const, color="green")

    plt.plot(range(0,count), recovered, color="grey")
    plt.fill_between(range(0,count), recovered, color="grey")

    plt.plot(range(0,count), inf_nrs, color="red")
    plt.fill_between(range(0,count), inf_nrs, color="red")
    
    #plt.show()
    fig.canvas.draw()

#==================================================================================================

if __name__ == "__main__":
    board = init_board()
    citizens, positions = init_citizens()
    
    citizens_s, citizens_h, citizens_r = citizens[:2], citizens[1:], []
    position_s, position_h, position_r = positions[:2], positions[1:], []
    
    counter, infection_nrs, recovered_nrs = 0, [], []
    run = True
    
    fig = plt.gcf()
    plt.ylabel('Number of Infections')
    plt.xlabel('Simulation Steps')
    fig.show()
    fig.canvas.draw()

    # Plot once at the End of Simulation
    while run == True:
        counter+=1
        board.update()
        citizens_s, citizens_h, citizens_r, position_s, position_h, position_r = move_citizens(citizens_s, citizens_h, citizens_r, position_s, position_h, position_r)
        
        # Record Data for Evaluation
        infection_nrs.append(len(citizens_s))
        recovered_nrs.append(len(citizens_r))

        # Determine steps in which plot is refreshed
        if counter % 50 == 0:
            evaluate_data(counter, infection_nrs, recovered_nrs)
        
        if len(citizens_s) == 0:
            run=False
    
    plt.show()
    #board.mainloop()