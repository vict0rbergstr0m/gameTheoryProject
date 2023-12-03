import numpy as np
import nashpy as nash

class AbstractStrategy:
    def get_action(self, game: nash.Game, prev_action: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class NashStrategy(AbstractStrategy):
    def get_action(self, game: nash.Game, prev_action: np.ndarray) -> np.ndarray:
        equilibria = game.support_enumeration();
        eq_sum = np.array([[1/100,1/100,1/100],[1/100,1/100,1/100]]) #default probabilities, 0 will give error....
        for eq in equilibria:
            eq_sum[0] = eq_sum[0] + eq[0]; #sum all nash equilibria
            eq_sum[1] = eq_sum[1] + eq[1];
        eq_sum[0] = eq_sum[0]/(eq_sum[0][0]+eq_sum[0][1]+eq_sum[0][2]);
        eq_sum[1] = eq_sum[1]/(eq_sum[1][0]+eq_sum[1][1]+eq_sum[1][2]);

        available_actions = [0, 1, 2]
        actions = [np.random.choice(available_actions, p=eq_sum[0]),  #choose action based on probabilities of sum of nash equilibria
                    np.random.choice(available_actions, p=eq_sum[1])]; # 0 = harvest, 1 = raid, 2 = trade

        print(prev_action)
        return actions[0];

class HarvestStrategy(AbstractStrategy):
    def get_action(self, game: nash.Game, prev_action: np.ndarray) -> np.ndarray:
        actions = np.array([0,0]);
        return actions[0];

class RaidStrategy(AbstractStrategy):
    def get_action(self, game: nash.Game, prev_action: np.ndarray) -> np.ndarray:
        actions = np.array([1,0]);
        return actions[0];

class TradeStrategy(AbstractStrategy):
    def get_action(self, game: nash.Game, prev_action: np.ndarray) -> np.ndarray:
        actions = np.array([2,0]);
        return actions[0];

class PacifistStrategy(AbstractStrategy):
    def get_action(self, game: nash.Game, prev_action: np.ndarray) -> np.ndarray:
        equilibria = game.support_enumeration();
        eq_sum = np.array([[1/100,1/100,1/100],[1/100,1/100,1/100]]) #default probabilities, 0 will give error....
        for eq in equilibria:
            eq_sum[0] = eq_sum[0] + eq[0]; #sum all nash equilibria
            eq_sum[1] = eq_sum[1] + eq[1];
        
        eq_sum[0][1] = 0; #remove raid before normalizing
        eq_sum[1][1] = 0;

        eq_sum[0] = eq_sum[0]/(eq_sum[0][0]+eq_sum[0][1]+eq_sum[0][2]);
        eq_sum[1] = eq_sum[1]/(eq_sum[1][0]+eq_sum[1][1]+eq_sum[1][2]);

        available_actions = [0, 0, 2]
        actions = [np.random.choice(available_actions, p=eq_sum[0]),  #choose action based on probabilities of sum of nash equilibria
                    0]; # 0 = harvest, 1 = raid, 2 = trade

        print(prev_action)
        return actions[0];