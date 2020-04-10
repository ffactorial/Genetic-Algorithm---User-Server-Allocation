'''
Many parts of below code is borrowed from the book "Hands-On-Genetic-ALgorithms" prpoblem with modifications for our problem.

The codes are MIT Licensed by book author, so can be used without restrictions

https://github.com/PacktPublishing/Hands-On-Genetic-Algorithms-with-Python/blob/master/Chapter10/01-solve-mountain-car.py
'''

# import DEAP library for GA related setup
from deap import base
from deap import creator
from deap import tools

# some other general imports
import random, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# needed for Hall Of Fame e.g. some best solutions from past generation who won't undergo crossover
import elitism


# use the resource allocation class which has all the objective function & constraint logic
import UserServerAllocation

# choose one of the problem configurations
from configuration_users_servers import *


# set the random seed for the deap's GA related initialization:
random.seed(5)

toolbox = base.Toolbox()

# create the resource allocation problem instance to be used:
rap = UserServerAllocation.ResourceAllocationProblem(NUM_USERS, NUM_SERVERS, USER_MEMORY_USAGE, SERVER_ENERGY_CONSUMPTION, 
    SERVER_RAM_CAPACITY, SOFT_CONSTRAINT_PENALTY, HARD_CONSTRAINT_PENALTY)

# define a single objective, maximizing fitness strategy:
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# create the Individual Chromosome class based on list:
# Individual is a list of length NUM_USERS where the element at index i means which server was allocated to user i
creator.create("Individual", list, fitness=creator.FitnessMax)

# create an operator that randomly returns 0 to NUM_SERVERS.
toolbox.register("assignServers", random.randint, 0, NUM_SERVERS)

# create the individual operator to fill up an Individual instance:
# - Individual Chromosome is a list of length NUM_USERS where the element at index i means which server was allocated to user i
# e.g. suppose there are 5 users (0-4) & 3 servers (0,1,2) then a sample individual is [2,0,1,2,3] which means that assign
# --- user 0 to server 2
# --- user 1 to server 0
# --- user 2 to server 1
# --- user 3 to server 2
# --- user 4 to NO SERVER (we have server number 0-2 only so server 3 is just a placeholder which means this user wasn't assigned any)
toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.assignServers, len(rap))

# create the population operator to generate a list of individuals:
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)


# hybrid_objective =  onjective_function (eqn 1.1) - penalty*server_capacity_constraint(eqn 1.3) 
# the constraint in eqn 1.2 (user allocation limit) is automatically satiesfied because for each user we assigned only one server with individualCreator
# the idea is that at optimality there would be no constraint violation so there won't be any penalty & we'd have max (eqn 1.1)
def getHybridObjectiveFunction(individual):
    return rap.getHybridObjectiveFunction(individual),  # return a tuple


toolbox.register("evaluate", getHybridObjectiveFunction)

# genetic operators (selection, crossover & mutation):
toolbox.register("select", tools.selTournament, tournsize=TOURNAMENT_SIZE)  # selection
toolbox.register("mate", tools.cxTwoPoint) # crossover
toolbox.register("mutate", tools.mutUniformInt, low=0, up=NUM_SERVERS, indpb=1.0/len(rap)) # mutation


# Genetic Algorithm flow:
def main():

    # create initial population (generation 0):
    population = toolbox.populationCreator(n=POPULATION_SIZE)

    # prepare the statistics object for hybrid_objective function:
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("hybrid_objective_max", np.max)
    stats.register("hybrid_objective_avg", np.mean)

    # define the hall-of-fame object:
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    # perform the Genetic Algorithm flow with hof feature added:
    population, logbook = elitism.eaSimpleWithElitism(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                              ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

    # print best solution found:
    best = hof.items[0]

    print()
    print("============= Summary - Problem/Solution ===============\n")
    print("Number Of Users (%d), Number Of Servers (%d)" %(NUM_USERS, NUM_SERVERS))
    rap.printserverAllocationInfo(best)

    if not os.path.exists('../output/'+str(NUM_USERS)+'Users_'+str(NUM_SERVERS)+'Servers/'):
        os.makedirs('../output/'+str(NUM_USERS)+'Users_'+str(NUM_SERVERS)+'Servers/')
    output_dir = '../output/'+str(NUM_USERS)+'Users_'+str(NUM_SERVERS)+'Servers/'

    import warnings
    warnings.filterwarnings("ignore")

    print("Saving Server To User Allocation Scheme to Folder %s \n"%(output_dir))
    output_filename = 'Server_to_UserList'
    allocation_df = pd.DataFrame(data = [], columns = ["Server", "Allocated Users"])
    for i in range(NUM_SERVERS):
        assigned_users = np.where(np.array(best) == i)[0].tolist()
        allocation_df.loc[i,"Server"] = i
        allocation_df.loc[i, "Allocated Users"] = assigned_users
    allocation_df.to_csv(output_dir + output_filename + '.csv', index=False)
    allocation_df.to_excel(output_dir + output_filename + '.xlsx', index=False)


    print("Saving User To Server Allocation Scheme to Folder %s \n"%(output_dir))
    output_filename = 'User_to_Server'
    allocation_df = pd.DataFrame(data = [], columns = ["User", "Allocated Server"])
    for i in range(NUM_USERS):
        allocation_df.loc[i,"User"] = i
        allocation_df.loc[i,"Allocated Server"] = best[i]
    allocation_df.to_csv(output_dir + output_filename + '.csv', index=False)
    allocation_df.to_excel(output_dir + output_filename + '.xlsx', index=False)
    
    print("============= End Summary ==================")

    # plot statistics:
    # extract statistics:
    maxHybridFitnessValues, meanHybridFitnessValues = logbook.select("hybrid_objective_max", "hybrid_objective_avg")    
    
    plt.plot(maxHybridFitnessValues, color='red')
    plt.plot(meanHybridFitnessValues, color='green')
    plt.xlabel('Generation')
    plt.ylabel('Max / Average Hybrid Objective Function Value')
    plt.title('Max and Average Hybrid Objective Function over Generations')
    plt.savefig(output_dir + 'GA_Convergence.png')
    # plt.show()


if __name__ == "__main__":
    main()

