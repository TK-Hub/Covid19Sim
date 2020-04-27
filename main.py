#==================================================================================================
#                       Covid19-Simulation
#                       Author: T.K.
#                       Date: 28.03.2020
#==================================================================================================

from citizen import Citizen, Covid_Pool
import turtle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

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
    sim_type = input("Please select the type of simulation to run. \n 1: Ball Simulation \n 2: Mathematical Simulation \n")
    
    if sim_type == "1":
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
        
        #plt.show()
        board.mainloop()
    
    if sim_type == "2":
        #==========================================================================================
        # 2D-Plot
        """nr_people, contagion_prob, daily_contacts, healing_days = 9999, 0.3, 3, 7
        covid_pool = Covid_Pool(nr_people, contagion_prob, daily_contacts, healing_days)
        x, y1, y2, y3 = [], [], [], []


        #fig = plt.figure()
        #ax1 = fig.add_subplot(1,1,1)

        while len(covid_pool.citizen_list_healed) < (nr_people-500):
        #def animate(i):
            covid_pool.a_day_in_the_city()
            x.append(covid_pool.sim_days)
            # Const. total nr.
            y1.append(len(covid_pool.citizen_list_healthy) + len(covid_pool.citizen_list_sick) + len(covid_pool.citizen_list_healed))
            # Sick + recovered people to distinct recovered people
            y2.append(len(covid_pool.citizen_list_healed) + len(covid_pool.citizen_list_sick))
            # Nr. of sick people
            y3.append(len(covid_pool.citizen_list_sick))

        #print(x, y1, y2, y3)
        plt.plot(x, y1, color="blue")
        plt.fill_between(x, y1, color="blue")
        
        plt.plot(x, y2, color="green")
        plt.fill_between(x, y2, color="green")
        
        plt.plot(x, y3, color="red")
        plt.fill_between(x, y3, color="red")
        plt.ylabel('Number of Citizens')
        plt.xlabel('Number of Past Days')
        
        
        #ani = animation.FuncAnimation(fig, animate, interval=100)
        plt.show()"""

        #==========================================================================================
        # 3D-Plot
        range_prob = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7]
        range_contacts = [3, 4, 5, 6, 7]
        range_healing = []
        result_data = []
        #result_data = [(0.3, 3, 29), (0.3, 4, 29), (0.3, 5, 23), (0.3, 6, 22), (0.3, 7, 21), (0.35, 3, 25), (0.35, 4, 24), (0.35, 5, 22), (0.35, 6, 21), (0.35, 7, 19), (0.4, 3, 25), (0.4, 4, 23), (0.4, 5, 21), (0.4, 6, 21), (0.4, 7, 19), (0.45, 3, 25), (0.45, 4, 21), (0.45, 5, 20), (0.45, 6, 19), (0.45, 7, 19), (0.5, 3, 22), (0.5, 4, 21), (0.5, 5, 20), (0.5, 6, 19), (0.5, 7, 18), (0.55, 3, 22), (0.55, 4, 20), (0.55, 5, 20), (0.55, 6, 19), (0.55, 7, 18), (0.6, 3, 22), (0.6, 4, 20), (0.6, 5, 19), (0.6, 6, 18), (0.6, 7, 18), (0.65, 3, 20), (0.65, 4, 19), (0.65, 5, 19), (0.65, 6, 18), (0.65, 7, 17), (0.7, 3, 20), (0.7, 4, 19), (0.7, 5, 19), (0.7, 6, 18), (0.7, 7, 17)]
        
        for i in range_prob:
            for j in range_contacts:
                nr_people, contagion_prob, daily_contacts, healing_days = 9999, i, j, 7
                covid_pool = Covid_Pool(nr_people, contagion_prob, daily_contacts, healing_days)
                x, y1, y2, y3 = [], [], [], []

                while len(covid_pool.citizen_list_healed) < (nr_people-500):
                    covid_pool.a_day_in_the_city()
                    x.append(covid_pool.sim_days)
                    # Const. total nr.
                    y1.append(len(covid_pool.citizen_list_healthy) + len(covid_pool.citizen_list_sick) + len(covid_pool.citizen_list_healed))
                    # Sick + recovered people to distinct recovered people
                    y2.append(len(covid_pool.citizen_list_healed) + len(covid_pool.citizen_list_sick))
                    # Nr. of sick people
                    y3.append(len(covid_pool.citizen_list_sick))
                
                result_data.append((i, j, max(y3)))
        
        print(result_data)
        
        # Prepare Data Tuples for Plotting
        x, y, z = zip(*result_data)
        grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]
        grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')

        # 3D-Plot Data
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_surface(grid_x, grid_y, grid_z, cmap=plt.cm.Spectral)
        ax.set_xlabel('Infection Probability')
        ax.set_ylabel('Average Number of Daily Contacts')
        ax.set_zlabel('Max. Nr. Sick People')
        plt.show()