from turnips import *
import random

def get_probabilities(prev = None):
    probs = {
        "up-down-up-down": 0,
        "big-spike": 0,
        "decreasing": 0,
        "small-spike": 0,
    }
    if prev == None:
        probs["small-spike"] = 1
    elif isinstance(prev, UpDownUpDown):
        probs["up-down-up-down"] = 0.2
        probs["big-spike"] = 0.3
        probs["decreasing"] = 0.15
        probs["small-spike"] = 0.35
    elif isinstance(prev, BigSpike):
        probs["up-down-up-down"] = 0.5
        probs["big-spike"] = 0.05
        probs["decreasing"] = 0.2
        probs["small-spike"] = 0.25
    elif isinstance(prev, Decreasing):
        probs["up-down-up-down"] = 0.25
        probs["big-spike"] = 0.45
        probs["decreasing"] = 0.05
        probs["small-spike"] = 0.25
    elif isinstance(prev, SmallSpike):
        probs["up-down-up-down"] = 0.45
        probs["big-spike"] = 0.25
        probs["decreasing"] = 0.15
        probs["small-spike"] = 0.15
    else:
        probs["up-down-up-down"] = 0.35
        probs["big-spike"] = 0.2625
        probs["decreasing"] = 0.1375
        probs["small-spike"] = 0.25
    return probs


