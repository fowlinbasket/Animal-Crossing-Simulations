from turnips import *
from turnip_tree import get_probabilities

def predict(probs, prices, base_price):
    if len(prices) == 0 or 1 in probs.values():
        return probs
    for step in range(1, len(prices) + 1):
        normalized_percentage = (prices[step - 1] / base_price)
        percentage_of_base = normalized_percentage * 100
        # Step 1: determine odds of us being in a given phase
        prob_udud = 0
        prob_bs = 0
        prob_d = 0
        prob_ss = 0
        prob_price_given_ss = 0
        match step:
            case 1:
                if 40 <= percentage_of_base <= 90:
                    prob_ss = 7/8
                    prob_price_given_ss = prob_ss * (1 - (percentage_of_base - 40) / (90 - 40))
                if 85 <= percentage_of_base <= 90:
                    prob_bs = 1
                    prob_d = 1
                if percentage_of_base == 90:
                    prob_price_given_ss = 0.125
                elif 90 <= percentage_of_base <= 140:
                    prob_udud = 6/7
                    prob_ss = 1/8
                    prob_price_given_ss = prob_ss * (1 - (percentage_of_base - 90) / (140 - 90))

                prob_price_given_udud = prob_udud * (1 - (percentage_of_base - 90) / (140 - 90))
                prob_price_given_bs = prob_bs * (1 - (percentage_of_base - 90) / (90 - 85))
                prob_price_given_d = prob_d * (1 - (percentage_of_base - 90) / (90 - 85))
        prob_price = probs["up-down-up-down"] * prob_price_given_udud + \
                        probs["big-spike"] * prob_price_given_bs + \
                        probs["decreasing"] * prob_price_given_d + \
                        probs["small-spike"] * prob_price_given_ss
        if prob_price == 0:
            raise Exception("An impossible price was given")
        probs["up-down-up-down"] = (prob_price_given_udud * probs["up-down-up-down"]) / prob_price
        probs["big-spike"] = (prob_price_given_bs * probs["big-spike"]) / prob_price
        probs["decreasing"] = (prob_price_given_d * probs["decreasing"]) / prob_price
        probs["small-spike"] = (prob_price_given_ss * probs["small-spike"]) / prob_price
    return probs


if __name__ == '__main__':
    prev = SmallSpike()
    probs = get_probabilities("i forgor")
    base_price = 107
    prices = [999]
    probs = predict(probs, prices, base_price)
    for pattern, prob in probs.items():
        print(f"P({pattern}) : {prob:.3f}")


    