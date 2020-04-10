import numpy as np
import random

########## initialization (Data/constants) of the problem:  optimal objective fun - 36834.28641887699 #################
# NUM_USERS, NUM_SERVERS = 20, 3
# NUM_USERS, NUM_SERVERS = 1000, 7
NUM_USERS, NUM_SERVERS = 10000, 100

# some constants needed to initialize USER_MEMORY_USAGE, SERVER_ENERGY_CONSUMPTION, SERVER_RAM_CAPACITY below
min_energy_per_mb   = 1.63 / 8192 # 1.63W for a 8GB DDR4 RAM
max_energy_per_mb   = 6 / 4096 #6W per 4GB DDR1
min_memory_usage    = 128 #in MB
max_memory_usage    = 4192
min_memory_capacity = 32*1024 #In MB
max_memory_capacity = 256*1024 
step                = 8*1024 #RAM can only add up by 8GB
possible_memories   = [memory for memory in range(min_memory_capacity, max_memory_capacity+1024, step)]

np.random.seed(1)

USER_MEMORY_USAGE = np.random.randint(min_memory_usage, max_memory_usage, NUM_USERS)
SERVER_ENERGY_CONSUMPTION = (max_energy_per_mb - min_energy_per_mb) * np.random.rand(NUM_SERVERS ) + min_energy_per_mb
SERVER_RAM_CAPACITY = np.random.choice(possible_memories, NUM_SERVERS)
###########################################################################################################################


# Genetic Algorithm hyperparameters:
if NUM_USERS == 20 and NUM_SERVERS == 3:
    POPULATION_SIZE         = 100
    P_CROSSOVER             = 0.9 
    P_MUTATION              = 0.2 
    TOURNAMENT_SIZE         = 3
    IND_PB                  = .01
    HALL_OF_FAME_SIZE       = 20
    HARD_CONSTRAINT_PENALTY = 1000
    SOFT_CONSTRAINT_PENALTY = 100
    MAX_GENERATIONS         = 50
elif NUM_USERS == 1000 and NUM_SERVERS == 7:
    POPULATION_SIZE         = 500
    P_CROSSOVER             = 0.9
    P_MUTATION              = 0.2
    TOURNAMENT_SIZE         = 3
    IND_PB                  = .01
    HALL_OF_FAME_SIZE       = 30
    HARD_CONSTRAINT_PENALTY = 10000
    SOFT_CONSTRAINT_PENALTY = 1000
    MAX_GENERATIONS         = 100
elif NUM_USERS == 10000 and NUM_SERVERS == 100:
    POPULATION_SIZE         = 500
    P_CROSSOVER             = 0.9
    P_MUTATION              = 0.5
    TOURNAMENT_SIZE         = 3
    IND_PB                  = .01
    HALL_OF_FAME_SIZE       = 30
    HARD_CONSTRAINT_PENALTY = 10000
    SOFT_CONSTRAINT_PENALTY = 1000
    MAX_GENERATIONS         = 100

