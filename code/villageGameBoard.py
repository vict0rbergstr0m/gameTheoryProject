import numpy as np;

class VillageGameBoard:
    """
    This class contains the rules of the game,
    it can be reused for getting the rewards of different players.
    You will only need different GameBoards if e.g. some regions of the "map"
    should give a higher harvest yield for example...
    """

    #todo: write a general, get_raid_value function, that takes resources as input
    def __init__(self, harvest_factor = 0.1,
                raid_factor = 0.8,
                max_raid_value = 2,
                raid_cost = 0.1,
                trade_factor = 0.2) -> None:
        
        self.harvest_factor = harvest_factor;
        self.raid_factor = raid_factor;
        self.max_raid_value = max_raid_value;
        self.raid_cost = raid_cost;
        self.trade_factor = trade_factor;
        self.max_harvest = 1000;

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

        out[0] = min(self.max_harvest,max(1,resources[0]*self.harvest_factor));
        out[1] = min(self.max_harvest,max(1,resources[1]*self.harvest_factor));

        return out;

    def harvest_raid(self, resources) -> np.ndarray:
        out = np.array([0,0]);

        max_raid_value = self.max_raid_value * resources[1];
        raid_value = resources[0] * self.raid_factor;
        raid_value = __smooth_Max__(raid_value, max_raid_value);

        raid_cost = max(-self.raid_cost * resources[1], -0.5*resources[0]); #you use some of your_resources to raid, but max cost is half of opponent_resources

        #raid_value = raid_value + raid_cost;

        out[0] = -raid_value;
        out[1] = raid_value + raid_cost;

        return out;

    def raid_harvest(self, resources) -> np.ndarray:
        return self.harvest_raid(resources[::-1])[::-1];

    def harvest_trade(self, resources) -> np.ndarray:
        out = np.array([0,0]);

        trade_value =  0;

        out[0] = min(self.max_harvest,max(1,resources[0]*self.harvest_factor));
        out[1] = trade_value;

        return out;

    def raid_raid(self, resources) -> np.ndarray:
        out = np.array([0,0]);

        max_raid_value = [self.max_raid_value * resources[0], # you cant gain more than max_raid_value*your_resources
                            self.max_raid_value * resources[1]];
        
        raid_gain = [resources[1] * self.raid_factor, #you gain the opponent_resources*raid_factor 
                        resources[0] * self.raid_factor];

        raid_gain = np.array([__smooth_Max__(raid_gain[0], max_raid_value[0]), #the gain is clamped to max_raid_value*your_resources
                        __smooth_Max__(raid_gain[1], max_raid_value[1])]);

        raid_loss = np.array([-raid_gain[1], #you lose what the opponent gains
                        -raid_gain[0]]);

        raid_cost = np.array([max(-self.raid_cost * resources[0], -0.5*resources[1]), #you use some of your_resources to raid, but max cost is half of opponent_resources
                                max(-self.raid_cost * resources[1], -0.5*resources[0])]);

        raid_value = raid_gain + raid_loss + raid_cost; #sum of gains and losses

        out[0] = raid_value[0];
        out[1] = raid_value[1];

        return out;

    def raid_trade(self, resources) -> np.ndarray:
        out = np.array([0,0]);

        max_raid_value = self.max_raid_value * resources[0];
        raid_value = resources[1] * self.raid_factor;
        raid_value = __smooth_Max__(raid_value, max_raid_value);

        raid_cost = max(-self.raid_cost * resources[0], -0.5*resources[1]); #you use some of your_resources to raid

        #raid_value = raid_value + raid_cost;

        out[0] = raid_value + raid_cost;
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

        return out;



def __smooth_Max__(value, max_value) -> float:
    if value < 0:
        return value;
    #todo: its hard writing a soft max, i give up 
    return min(value, max_value);