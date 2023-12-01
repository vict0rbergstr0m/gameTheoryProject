from villageGameBoard import VillageGameBoard;
import numpy as np;
import nashpy as nash
from enum import Enum

class Moves(Enum):
    harvest = 0;
    raid = 1;
    trade = 2;


#TODO: problem, both players slowly trickle down into nothing....

n_rounds = 1000;

harvest_factor = 0.1;
raid_factor = 0.8;
raid_cost = 0.1;
max_raid_value = 2;
trade_factor = 0.2;

start_res_1 = 100;
start_res_2 = 100;

resources = np.array([start_res_1, start_res_2]);
gameBoard = VillageGameBoard(harvest_factor, raid_factor, max_raid_value, raid_cost, trade_factor);

def get_game(resources) -> nash.Game:
    state = gameBoard.get_board_states(resources);
    game = nash.Game(state[0], state[1]);
    print(game);
    return game

print("\n\n===========Start============")
for i in range(n_rounds):
    print("\n\n-------Round " + str(i+1) + " " + str(resources) + "--------\n");

    game = get_game(resources);

    print("\nnash equilibria:");
    equilibria = game.support_enumeration();
    eq_sum = np.array([[1/10,1/10,1/10],[1/10,1/10,1/10]])
    for eq in equilibria:
        print(eq);
        eq_sum[0] = eq_sum[0] + eq[0];
        eq_sum[1] = eq_sum[1] + eq[1];
    eq_sum[0] = eq_sum[0]/(eq_sum[0][0]+eq_sum[0][1]+eq_sum[0][2]);
    eq_sum[1] = eq_sum[1]/(eq_sum[1][0]+eq_sum[1][1]+eq_sum[1][2]);

    available_actions = [0, 1, 2]
    actions = [np.random.choice(available_actions, p=eq_sum[0]), 
                np.random.choice(available_actions, p=eq_sum[1])]; # 0 = harvest, 1 = raid, 2 = trade
    
    
    utility = np.array([game.payoff_matrices[0][actions[0],actions[1]],game.payoff_matrices[1][actions[0],actions[1]]]);
    resources = resources + utility;

    print("\nplayer 1 played: " + str(actions[0]));
    print("player 2 played: " + str(actions[1]));

    if resources[0] == resources[1] and resources[0] == 1:
        print("\nbot players lost");
        break;

    if resources[0] <= 1:
        print("\nplayer 1 lost");
        break;
    if resources[1] <= 1:
        print("\nplayer 2 lost");
        break;
    pass
print("Final resources: " + str(resources))