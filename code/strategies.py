import numpy as np
import nashpy as nash


class NashStrategy:
    @staticmethod
    def get_action(game: nash.Game, playerI: int) -> np.ndarray:

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

        return actions[playerI];