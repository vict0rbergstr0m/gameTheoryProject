from villageGameBoard import VillageGameBoard;
import numpy as np;

harvest_factor = 0.1;
raid_factor = 0.8;
trade_factor = 0.2;

start_res_1 = 1000;
start_res_2 = 1000;

resources = np.array([start_res_1, start_res_2]);
gameBoard = VillageGameBoard(harvest_factor, raid_factor, trade_factor);

state = gameBoard.get_board_states(resources);
print(state[0]);
print(state[1]);