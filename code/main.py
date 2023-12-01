from villageGameBoard import VillageGameBoard;
import numpy as np;
import nashpy as nash
from enum import Enum

class Moves(Enum):
    harvest = 0;
    raid = 1;
    trade = 2;


#TODO: raiding is way to strong when the resources are low, make the max raid reward some multiplier of your own resources

n_rounds = 100;

harvest_factor = 0.1;
raid_factor = 0.8;
trade_factor = 0.2;

start_res_1 = 1000;
start_res_2 = 1000;

resources = np.array([start_res_1, start_res_2]);
gameBoard = VillageGameBoard(harvest_factor, raid_factor, trade_factor);

def get_game(resources) -> nash.Game:
    state = gameBoard.get_board_states(resources);
    game = nash.Game(state[0], state[1]);
    print(game);
    return game


for i in range(n_rounds):
    print("Round " + str(i+1) + str(resources));
    game = get_game(resources);

    actions = [np.random.randint(3), np.random.randint(3)]; # 0 = harvest, 1 = raid, 2 = trade
    utility = np.array([game.payoff_matrices[0][actions[0],actions[1]],game.payoff_matrices[1][actions[0],actions[1]]]);
    resources = resources + utility;

    print("player 1 played: " + str(actions[0]));
    print("player 2 played: " + str(actions[1]));

    if resources[0] < 0:
        print("player 1 lost");
        break;
    if resources[1] < 0:
        print("player 2 lost");
        break;
    pass
print("Final resources: " + str(resources))