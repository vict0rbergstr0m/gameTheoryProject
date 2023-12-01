import nashpy as nash;
import nashpy.repeated_games as create_repeated_games;
import numpy as np;

harvest_factor = 1.1;
raid_factor = 0.8;
trade_factor = 0.5;

start_res_1 = 1000;
start_res_2 = 1000;

resources = np.array([start_res_1, start_res_2]);

def harvest_harvest(resources) -> np.array:
    out = np.array([0,0]);

    out[0] = resources[0]*harvest_factor;
    out[1] = resources[1]*harvest_factor;

    return out;

def harvest_raid(resources) -> np.array:
    out = np.array([0,0]);

    raid_value = resources[0] * raid_factor;

    out[0] = -raid_value;
    out[1] = raid_value;

    return out;

def raid_harvest(resources) -> np.array:
    return harvest_raid(resources[::-1])[::-1];

def harvest_trade(resources) -> np.array:
    out = np.array([0,0]);

    trade_value =  0;

    out[0] = resources[0]*harvest_factor;
    out[1] = trade_value;

    return out;

def raid_raid(resources) -> np.array:
    out = np.array([0,0]);

    out[0] = -resources[0] * raid_factor + resources[1] * raid_factor;
    out[1] = -resources[1] * raid_factor + resources[0] * raid_factor;

    return out;