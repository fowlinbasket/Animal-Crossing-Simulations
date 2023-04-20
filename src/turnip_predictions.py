from turnips import *
from turnip_tree import get_probabilities
import math

def predict(probs, prices, base_price):
    if len(prices) == 0 or 1 in probs.values():
        return probs
    for step in range(1, len(prices) + 1):

        # TODO: If you ever implement more than just one step, delete this
        if step > 1: continue

        normalized_percentage = (prices[step - 1] / base_price)
        percentage_of_base = (normalized_percentage * 100)
        # Step 1: determine odds of us being in a given phase
        prob_udud = 0
        prob_bs = 0
        prob_d = 0
        prob_ss = 0
        prob_price_given_ss = 0
        match step:
            case 1:
                # Determining P(price|pattern)
                if 40 <= percentage_of_base <= 90:
                    prob_ss = 7/8
                    prob_price_given_ss = prob_ss * (1 - (percentage_of_base - 40) / (90 - 40))
                if 85 <= percentage_of_base <= 90:
                    prob_bs = 1
                    prob_d = 1
                if percentage_of_base == 90:
                    prob_price_given_ss = (7/8) * (1 - (percentage_of_base - 40) / (90 - 40)) + \
                        (1/8) * (1 - (percentage_of_base - 90) / (140 - 90))
                elif 90 <= percentage_of_base <= 140:
                    prob_udud = 6/7
                    prob_ss = 1/8
                    prob_price_given_ss = prob_ss * (1 - (percentage_of_base - 90) / (140 - 90))

                prob_price_given_udud = prob_udud * (1 - (percentage_of_base - 90) / (140 - 90))
                prob_price_given_bs = prob_bs * (1 - (percentage_of_base - 85) / (90 - 85))
                prob_price_given_d = prob_d * (1 - (percentage_of_base - 85) / (90 - 85))
        # Determining P(price)
        prob_price = probs["up-down-up-down"] * prob_price_given_udud + \
                        probs["big-spike"] * prob_price_given_bs + \
                        probs["decreasing"] * prob_price_given_d + \
                        probs["small-spike"] * prob_price_given_ss
        if prob_price == 0:
            prob_price = 1
        # Determining P(pattern|price)
        probs["up-down-up-down"] = (prob_price_given_udud * probs["up-down-up-down"]) / prob_price
        probs["big-spike"] = (prob_price_given_bs * probs["big-spike"]) / prob_price
        probs["decreasing"] = (prob_price_given_d * probs["decreasing"]) / prob_price
        probs["small-spike"] = (prob_price_given_ss * probs["small-spike"]) / prob_price
    return probs

def test_predictions(num_tests = 100_000, track_prev=True):
    correct_count = 0
    ps = PatternSelector()
    prev = None if track_prev else "i forgor"
    for test in range(num_tests):
        print(f"\rRunning test {test + 1:,}/{num_tests:,}", end="")
        probs = get_probabilities(prev)
        next = ps.next()
        prices = next.prices[2:]
        probs = predict(probs, prices, next.base_price)
        most_likely = None
        for name, probability in probs.items():
            if most_likely == None or probability > probs[most_likely]:
                most_likely = name
        if most_likely == next.getName():
            correct_count += 1
        if track_prev:
            prev = next
    print()
    correct_percentage = correct_count / num_tests
    return correct_percentage

def source_example():
    prev = BigSpike()
    base_price = 101
    prices = [88]
    probs = get_probabilities(prev)
    probs = predict(probs, prices, base_price)
    for name, probability in probs.items():
        print(f"P({name}): {probability}")

        

if __name__ == '__main__':
    correct = test_predictions(num_tests=1_000_000, track_prev=True)
    print(f"Correct {correct * 100:.2f}% of the time")


    