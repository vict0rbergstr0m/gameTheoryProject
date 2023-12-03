from villageGameBoard import VillageGameBoard
import numpy as np
import nashpy as nash
from strategies import *

class Game:
    def __init__(self, harvest_factor, raid_factor, max_raid_value, raid_cost, trade_factor, start_res_1, start_res_2, strategies: list = [NashStrategy(), NashStrategy()]):
        self.harvest_factor = harvest_factor
        self.raid_factor = raid_factor
        self.max_raid_value = max_raid_value
        self.raid_cost = raid_cost
        self.trade_factor = trade_factor
        self.start_res_1 = start_res_1
        self.start_res_2 = start_res_2
        self.resources = np.array([start_res_1, start_res_2])
        self.gameBoard = VillageGameBoard(harvest_factor, raid_factor, max_raid_value, raid_cost, trade_factor)
        self.strategies = strategies;
        self.prev_actions = np.array([-1,-1])
        self.resources_history: np.ndarray = np.array([0,0]);

    def get_round(self) -> tuple[nash.Game, np.ndarray]:
        return (self.get_game(self.resources), self.resources)

    def run(self, game) -> list[np.ndarray]:
        actions = [self.strategies[0].get_action(game, 0,self.prev_actions),
                    self.strategies[1].get_action(game, 1,self.prev_actions)];

        utility = np.array([game.payoff_matrices[0][actions[0],actions[1]],game.payoff_matrices[1][actions[0],actions[1]]]);

        self.resources_history = np.vstack((self.resources_history, self.resources.copy()));

        self.resources = self.resources + utility

        print("\nplayer 1 played: " + str(actions[0]));
        print("player 2 played: " + str(actions[1]));
        print("\n\n\n");

        self.prev_actions = actions.copy()
        return actions;

    def get_game(self, resources) -> nash.Game:
        print("resources: " + str(resources))
        state = self.gameBoard.get_board_states(resources)
        game = nash.Game(state[0], state[1])
        print(game)
        return game

if __name__ == "__main__":
    n_rounds = 10;

    harvest_factor = 0.5;
    raid_factor = 0.8;
    raid_cost = 0.1;
    max_raid_value = 2;
    trade_factor = 0.2;

    start_res_1 = 100;
    start_res_2 = 100;

    game = Game(harvest_factor, raid_factor, max_raid_value, raid_cost, trade_factor, start_res_1, start_res_2);
    for i in range(n_rounds):
        (round,_) = game.get_round();
        game.run(round)
