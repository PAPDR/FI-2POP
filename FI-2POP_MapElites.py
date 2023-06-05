# -*- coding: utf-8 -*-
"""
Created on Mon May  1 21:00:34 2023

@author: pipos
"""

import random
import numpy as np
import matplotlib.pyplot as plt



# Define the Simulation class
class Simulation:
    def __init__(self, bounds):
        self.score = 0
        self.x = random.randint(bounds[0][0], bounds[0][1])
        self.y = random.randint(bounds[1][0], bounds[1][1])
        self.path = []
        self.path.append(self.score)

    def is_feasible(self):
        #True if not negative
        return self.score > 0
    
    def mutate(self):
        #20% chance of becoming negative
        if (random.randint(1, 10) <= 2):
            self.score = -self.score
            
    def simulate(self):
        #For 10 steps, add a value between -x and y.
        #At every step, mutate
        for i in range(10):
            self.score = self.score + random.randint(-self.x,self.y)
            self.mutate()
            self.path.append(self.score)
    
    def fitness(self):
        #Return the "fitness"
        return self.score
        
def map_elites(num_bins=[11,11], bounds = [(0,10),(0,10)], num_generations = 10000):
    
    #bounds is the dimensions of the search space
    #num_bins is the number of bins in each section of the map.
   
    
    #Here we want to create 2 maps. One for feasible and one for infeasible
    map_elites_infeasible = {}
    map_elites_feasible = {}
    for i in range(num_bins[0]):
        for j in range(num_bins[1]):
            map_elites_feasible[(i, j)] = {'solution': None, 'fitness': -np.inf}
            map_elites_infeasible[(i, j)] = {'solution': None, 'fitness': -np.inf}
    
    #For number of generations, create a new simulation
    for i in range(num_generations):
        
        #Create simulation
        simulate = Simulation(bounds)
        
        #Simulate
        simulate.simulate()
        
        #Use the simulate x and y as placing points for the bins
        bin_index = (simulate.x, simulate.y)

        #If feasible put in one map-elites
        if simulate.is_feasible():
            #If better score, replace
            if simulate.fitness() > map_elites_feasible[bin_index]['fitness']:
                #Solution is the new simulation
                map_elites_feasible[bin_index]['solution'] = simulate
                #fitness is the new score
                map_elites_feasible[bin_index]['fitness'] = simulate.fitness()
        #If not feasible do the same in the non_feasible map_elites
        else:
            if simulate.fitness() > map_elites_infeasible[bin_index]['fitness']:
                #Solution is the new simulation
                map_elites_infeasible[bin_index]['solution'] = simulate
                #fitness is the new score
                map_elites_infeasible[bin_index]['fitness'] = simulate.fitness()
                
    return (map_elites_feasible, map_elites_infeasible)
    
    
def map_elites_to_heatmap(map_elite_dict, num_bins=[11,11],  bounds = [(0,10),(0,10)]):
    
    # Create an empty 2D array to represent the heatmap
    heatmap = np.zeros((num_bins[0], num_bins[1]))
    
    # Populate the heatmap with the fitness values from the map elites
    for i in range(num_bins[0]):
        for j in range(num_bins[1]):
            heatmap[i, j] = map_elite_dict[(i, j)]['fitness']
    
    # Create the heatmap plot
    plt.imshow(heatmap.T, origin='lower', extent=[bounds[0][0], bounds[0][1], bounds[1][0], bounds[1][1]])
    plt.colorbar()
    
    # Label the axes
    plt.xlabel('X')
    plt.ylabel('Y')
    
    # Show the plot
    plt.show()

def main():
    ME = map_elites()
    map_elites_to_heatmap(ME[0])
    map_elites_to_heatmap(ME[1])
    #print(ME[1])
    pass




if __name__ == "__main__":
    main()