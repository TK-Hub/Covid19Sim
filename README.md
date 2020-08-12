# Covid19Sim
This is a simulation of how infectious deseases can spread and how social distancing measures can influence the maximum number of people being sick at particular point in time. Once you run this script, a menu will appear in the console asking to input "1" or "2" in the console for the following options:

 1: "Ball Simulation":
    This is a simulation of object moving around in a confined space. Once two points get close together, and one of them is infected, there is a certain probability to transfer the desease. This is computationally more demanding than option 2 (which does a similar calculation, but without rendering a space of moving objects) and the population should be kept around 100.

 2: "Mathematical Simulation":
    This is a similar simulation, but only as mathematical calculation. Therefore, this allows for simulating a larger population (I recommend around 10,000). If this option is selected, another similar input is asked:
    
2.1: "1 set, 2D": 
    This does the calculation for one set of parameters and outputs one 2D-graph (the maxiumum of which representing the peak of sick people at a time).
    
2.2: "Value range, 3D": 
    Expand this analysis to a range of values. This takes a range of daily contacts and infection probabilities and shows the change in the maximum number of sick people. It creates a surface map, where every point represents the maximum of the graph created in 2.1.

The parameters for this Simulation can be set in "parameters.json".