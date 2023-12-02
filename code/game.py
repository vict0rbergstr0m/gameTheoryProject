from villageGameBoard import VillageGameBoard
import numpy as np
import nashpy as nash

class Game:
    def __init__(self, harvest_factor, raid_factor, max_raid_value, raid_cost, trade_factor, start_res_1, start_res_2):
        self.harvest_factor = harvest_factor
        self.raid_factor = raid_factor
        self.max_raid_value = max_raid_value
        self.raid_cost = raid_cost
        self.trade_factor = trade_factor
        self.start_res_1 = start_res_1
        self.start_res_2 = start_res_2
        self.resources = np.array([start_res_1, start_res_2])
        self.gameBoard = VillageGameBoard(harvest_factor, raid_factor, max_raid_value, raid_cost, trade_factor)


    def get_round(self) -> tuple[nash.Game, np.ndarray]:
        return (self.get_game(self.resources), self.resources)

    def run(self, game) -> list[np.ndarray]:
        #game = self.get_game(self.resources)

        equilibria = game.support_enumeration();
        eq_sum = np.array([[1/10,1/10,1/10],[1/10,1/10,1/10]]) #default probabilities, 0 will give error....
        for eq in equilibria:
            eq_sum[0] = eq_sum[0] + eq[0]; #sum all nash equilibria
            eq_sum[1] = eq_sum[1] + eq[1];
        eq_sum[0] = eq_sum[0]/(eq_sum[0][0]+eq_sum[0][1]+eq_sum[0][2]);
        eq_sum[1] = eq_sum[1]/(eq_sum[1][0]+eq_sum[1][1]+eq_sum[1][2]);

        available_actions = [0, 1, 2]
        actions = [np.random.choice(available_actions, p=eq_sum[0]),  #choose action based on probabilities of sum of nash equilibria
                    np.random.choice(available_actions, p=eq_sum[1])]; # 0 = harvest, 1 = raid, 2 = trade
        
        
        utility = np.array([game.payoff_matrices[0][actions[0],actions[1]],game.payoff_matrices[1][actions[0],actions[1]]]);
        self.resources = self.resources + utility

        print("\nplayer 1 played: " + str(actions[0]));
        print("player 2 played: " + str(actions[1]));
        print("\n\n\n");

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
