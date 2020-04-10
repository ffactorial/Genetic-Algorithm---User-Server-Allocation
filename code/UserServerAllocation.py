import numpy as np


class ResourceAllocationProblem:

    def __init__(self, numUsers, numServers, userMemoryUsage, serverEnergyConsumption, serverRAMCapacity, softConstraintPenalty, hardConstraintPenalty):
        self.users = ["user_"+str(i) for i in range(numUsers)]
        self.servers = ["server_"+str(i) for i in range(numServers)]
        self.userMemoryUsage = userMemoryUsage
        self.serverEnergyConsumption = serverEnergyConsumption
        self.serverRAMCapacity = serverRAMCapacity
        self.softConstraintPenalty = softConstraintPenalty
        self.hardConstraintPenalty = hardConstraintPenalty

        # eqn 1.1 - objective function value
        self.objective = None

        # number of eqn 1.3 violations
        self.NumberOfServerRAMCapacityViolations = None


    def __len__(self):
        return len(self.users)

    # we will maximize eqn (1.1) - hardConstraintPenalty*constraint_violation(eqn 1.3) - softConstrainedPenalty*users_not_allocated_any_server
    # so if there is no vilation of eqn (1.3) then there would be o penalty & we'll get max (eqn 1.1)
    def getHybridObjectiveFunction(self, individual):
        if len(individual) != self.__len__():
            raise ValueError("size of serverAllocation list should be equal to ", self.__len__())


        # objective function (eqn 1.1)
        self.objective = self.getObjectiveFunction(individual)

        # get various Hard constraint violations violations:
        self.NumberOfServerRAMCapacityViolations, totalServerCapacityViolation = self.countNumberOfServerRAMCapacityViolations(individual)


        # get various Soft constraint violations violations e.g. not necessary to hold but good if satisfied (allocate to worst server in worst case)
        user_not_allocated_any_server = []
        for i in range(len(self.users)):
            if individual[i] == len(self.servers):
                user_not_allocated_any_server.append(i+1)
        userNotAllocatedPenalty = len(user_not_allocated_any_server)

        # so our hybrid objective finally becomes eqn(1.1) - penalty*constraint_violation eqn(1.3) - 
        hybrid_objective = self.objective - self.hardConstraintPenalty*totalServerCapacityViolation - self.softConstraintPenalty*userNotAllocatedPenalty

        return hybrid_objective


    # eqn 1.1
    def getObjectiveFunction(self, individual):
        maxEnergy = max(self.serverEnergyConsumption)
        maxUsage = max(self.userMemoryUsage)
        objective = 0
        for i in range(len(self.users)):
            if individual[i] < len(self.servers):
                x_ij = 1
                server = individual[i]
                objective += (maxEnergy-self.serverEnergyConsumption[server]+1)*(maxUsage-self.userMemoryUsage[i]+1)*x_ij
            else:
                x_ij = 0
                # objective += 0

        return objective

    # eqn 1.3. 
    def countNumberOfServerRAMCapacityViolations(self, individual):
        number_violations = 0
        total_violation = 0

        for i in range(len(self.servers)):
            server_capacity = self.serverRAMCapacity[i]
            # users who were assigned to server i
            user_list = np.where(individual == i)[0].tolist()

            server_memory_usage = []
            for user in user_list:
                server_memory_usage.append(self.userMemoryUsage[user])

            total_server_memory_usage = sum (server_memory_usage)

            if total_server_memory_usage > server_capacity:
                number_violations += 1
                total_violation = (total_server_memory_usage - server_capacity)

        return number_violations, total_violation



    def printserverAllocationInfo(self, individual):

        # incase there are any soft constraints violations e.g. unallocated users then:
        user_not_allocated_any_server = []
        for i in range(len(self.users)):
            # remembr the last server means the user wasn't allocated to any server
            if individual[i] == len(self.servers):
                user_not_allocated_any_server.append(i+1)
                # print ("User: %d Not Allocated to Any Server" %(i))
            # if individual[i] < len(self.servers):
                # print ("User: %d -> Allocated to Server: %d" %(i, individual[i]))
        print()


        if self.NumberOfServerRAMCapacityViolations == 0 and len(user_not_allocated_any_server) == 0:
            print("HURRAY !!!!!!!!!!!!!!!!!!")
            print("Optimal objective function found & No Constraint Violation")
            # print("Optimal Objective Value:", self.objective)
        print()
        
        print("Optimal Objective Function Value (Eqn 1.1) = ", self.objective)
        print()

        print("Number Of Soft Constraint Violations (eqn 1.2 - Users allocation limit) =", len(user_not_allocated_any_server))
        print()

        print("Number Of Hard Constraint Violations (eqn 1.3 - Server Capacity) =", self.NumberOfServerRAMCapacityViolations)
        print() 



        # incase there are any soft constraints violations e.g. unallocated users then:
        if len(user_not_allocated_any_server) > 0:
            print("Users not allocated any servers are:")
            print(user_not_allocated_any_server)
            print()











