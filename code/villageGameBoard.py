import numpy as np;

class VillageGameBoard:
    def __init__(self, harvest_factor = 1.1,
                raid_factor = 0.8,
                trade_factor = 0.5) -> None:
        
        self.harvest_factor = harvest_factor;
        self.raid_factor = raid_factor;
        self.trade_factor = trade_factor;

    def get_board_states(self, resources) -> list[np.ndarray]:
        board_states = [np.zeros((3, 3)),np.zeros((3, 3))] # Create 2 3x3 arrays as game board states
        
        # Fill the board state with the predicted outcomes
        harvest_harvest = self.harvest_harvest(resources)
        harvest_raid = self.harvest_raid(resources)
        harvest_trade = self.harvest_trade(resources)

        raid_harvest = self.raid_harvest(resources)
        raid_raid = self.raid_raid(resources)
        raid_trade = self.raid_trade(resources)

        trade_harvest = self.trade_harvest(resources)
        trade_raid = self.trade_raid(resources)
        trade_trade = self.trade_trade(resources)
        
        board_states[0][0,:] = np.array([harvest_harvest[0], harvest_raid[0], harvest_trade[0]])
        board_states[0][1,:] = np.array([raid_harvest[0], raid_raid[0], raid_trade[0]])
        board_states[0][2,:] = np.array([trade_harvest[0], trade_raid[0], trade_trade[0]])

        board_states[1][0,:] = np.array([harvest_harvest[1], harvest_raid[1], harvest_trade[1]])
        board_states[1][1,:] = np.array([raid_harvest[1], raid_raid[1], raid_trade[1]])
        board_states[1][2,:] = np.array([trade_harvest[1], trade_raid[1], trade_trade[1]])

        return board_states

    def harvest_harvest(self, resources: np.ndarray) -> np.ndarray:
        out = np.array([0,0]);

        out[0] = resources[0]*self.harvest_factor;
        out[1] = resources[1]*self.harvest_factor;

        return out;

    def harvest_raid(self, resources) -> np.ndarray:
        out = np.array([0,0]);

        raid_value = resources[0] * self.raid_factor;

        out[0] = -raid_value;
        out[1] = raid_value;

        return out;

    def raid_harvest(self, resources) -> np.ndarray:
        return self.harvest_raid(resources[::-1])[::-1];

    def harvest_trade(self, resources) -> np.ndarray:
        out = np.array([0,0]);

        trade_value =  0;

        out[0] = resources[0]*self.harvest_factor;
        out[1] = trade_value;

        return out;

    def raid_raid(self, resources) -> np.ndarray:
        out = np.array([0,0]);

        out[0] = -resources[0] * self.raid_factor + resources[1] * self.raid_factor;
        out[1] = -resources[1] * self.raid_factor + resources[0] * self.raid_factor;

        return out;

    def raid_trade(self, resources) -> np.ndarray:
        out = np.array([0,0]);

        raid_value = resources[1] * self.raid_factor;

        out[0] = raid_value;
        out[1] = -raid_value;

        return out;

    def trade_raid(self, resources) -> np.ndarray:
        return self.raid_trade(resources[::-1])[::-1];

    def trade_harvest(self, resources) -> np.ndarray:
        return self.harvest_trade(resources[::-1])[::-1];

    def trade_trade(self, resources) -> np.ndarray:
        out = np.array([0,0]);

        out[0] = resources[1]*self.trade_factor;
        out[1] = resources[0]*self.trade_factor;

        return out