# the codes were run with python 3.6

# Install some import python libraries first
pip install pandas
pip install numpy
pip install deap
pip install matplotlib
pip install openpyxl
pip install xlrd

# how to run the code:Go to code folder 
python main.py

# code explanation
- configuration_servers_users.py [ initializes the problem instance & genetic algorithm parameters]
- elitism.py [ used in main.py by the genetic algorithm function]
- main.py [ executes GA & saves the figure & csv file in output folder]

# Solution explanation (about chromosome representation)
- Individual Chromosome is a list of length NUM_USERS where the element at index i means which server was allocated to user i
e.g. suppose there are 5 users (0-5) & 3 servers (0-2) then a sample individual is [2,0,1,2,3] which means that assign
--- user 0 to server 2
--- user 1 to server 0
--- user 2 to server 1
--- user 3 to server 2
--- user 4 to NO SERVER (we have server number 0-2 only so server 3 is just a placeholder that it's not existent)

# Solution explanation (hybrid optimization)
--- idea is that at optimality there would be no constraint violation so there wont be any penalty & we will get max (eqn 1.1)
--- the constraint in eqn 1.2 (user allocation limit) is automatically satiesfied because for each user we assigned only one server with individualCreator
--- constraint in eqn (1.3) is Hard constraints e.g. we don't want any violation
--- we introudce an additional Soft constraint - in the pdf below eqn 1.1 on the line 'The ”+1” in both terms means that allocating the user with most usage to the worst server is still better that not allocating him at all, since the objective is also to maximize the number of users allocated.' this means that we want all users to be allocated but its not necessary. Some cane be unallocated also, but we prefer if all users get allocated
--- hybrid_objective =  objective_function (eqn 1.1) - hardConstraintPenalty*violation(eqn 1.3) - softConstraintPenalty*num_users_not_allocated_to_any_server
