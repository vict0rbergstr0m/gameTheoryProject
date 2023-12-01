import nashpy as nash
import nashpy.repeated_games as create_repeated_games
import numpy as np

#prisoners dilemma
A = np.array([[3, 0], [5, 1]])
B = np.array([[3, 5], [0, 1]])

#matching pennies
A = np.array([[1, -1], [-1, 1]])

#rock paper scissors
A = np.array([[0,-1, 1], [1, 0, -1], [-1, 1, 0]])

#bayesian game example
A = np.array([[2, 1, 1, 0], [0.8, 1, 0.4, 0.6], [1.5, 0.5, 1.7, 0.7], [0.3, 0.5, 1.1, 1.3]])
B = np.array([[1, 0.7, 1.2, 0.9], [0.2, 1.1, 1, 1.9], [1.4, 1.1, 0.4, 0.1], [0.6, 1.5, 0.2, 1.1]])

#hawk-dove
A = np.array([[-2, 6], [0, 3]])
B = np.array([[-2, 0], [6, 3]])

#create a game ith payoff matrices
my_game = nash.Game(A, B)
#if constant sum, you cn create it just with once matrix
my_game = nash.Game(A)

#check for best response
sigma_r = np.array([0, 1])
sigma_c = np.array([1, 0])
print(my_game.is_best_response(sigma_r, sigma_c))

#compute all Nash equilibria with support enumeration
equilibria = my_game.support_enumeration()
for eq in equilibria:
    print(eq)
    
#if constant sum, you can use the linear program feature
my_game.linear_program()

#create a repeated version of the game
repeated_game = create_repeated_games.obtain_repeated_game(game=my_game, repetitions=2) #bug: i>1 repetitions corresponds to i+1 repetitions.
#get corresponding strategies
strategies = create_repeated_games.obtain_strategy_space(A=A, repetitions=2) #bug: i>1 repetitions corresponds to i+1 repetitions.

#replicator dynamics
y0 = np.array([0.05, 0.95])#initial population
timepoints = np.linspace(0, 10, 1500)
population_1, population_2 = my_game.replicator_dynamics(y0=y0, timepoints=timepoints).T