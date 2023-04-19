# Example

If we know what pattern the previous week was, we also know the probability of each pattern occurring this week. For example, if the previous week had a Small Spike pattern:

$$P(\text{UDUD}) = 0.45$$
$$P(\text{BS}) = 0.25$$
$$P(\text{D})= 0.15$$
$$P(\text{SS}) = 0.15$$

If we do not know the past week's pattern was, we can simulate the decision tree around selecting the probabilities of each pattern to get a general idea of the probability of a pattern occurring given no prior knowledge of the past week:

$$P(\text{UDUD}) = 0.35$$
$$P(\text{BS}) = 0.2625$$
$$P(\text{D}) = 0.1375$$
$$P(\text{SS}) = 0.25$$

In either case, these probabilities represent our prior knowledge, or our hypothesis. 

Next, we need to determine the probability of being in a particular phase. Let's say the base price of turnips on Sunday was 102 bells per turnip and we are on time step 1 out of 12 (Monday AM), and the current price of turnips is 118 bells. This is approximately a 115% increase in price.

Because the price increased to 115% of the base price, we cannot be in phase B of small spike, phase A of big spike, phase A of decreasing, or phase A of small spike. In fact, we cannot be in a big spike or decreasing pattern at all. At this time step, there is a 1 in 8 chance that we are in phase B of a small spike (with a 0% chance of being in phase A), and a 6 in 7 chance that we are in Phase A of up down up down (with a 0% chance that we are in phase B). Then, the probabilities of getting this price on time step 1 given that we are in each pattern is:

$$P(\text{price change}|\text{pattern}) = P(\text{phase}|\text{price}) \cdot (1 - \frac{\text{price change} - \text{low for phase}}{\text{high for phase} - \text{low for phase}})$$
$$P(115\%|\text{UDUD}) = \frac{6}{7} (1 - \frac{1.15 - 0.9}{1.4 - 0.9}) = 0.43$$
$$P(115\%|\text{BS}) = 0$$
$$P(115\%|\text{D}) = 0$$
$$P(115\%|\text{SS}) = \frac{1}{8} (1 - \frac{1.15 - 0.9}{1.4 - 0.9}) = 0.0625$$

The total probability of this price on this time step is then:
$$P(115\%) = \sum_{\text{pattern}} P(\text{pattern})P(115\%|\text{pattern})$$
$$P(115\%) = 0.45\cdot0.43 + 0.25\cdot0 + 0.15\cdot0 + 0.15\cdot0.0625 = 0.2$$

Now that we have our normalizing constant, the Bayes' model can now be updated with our new data:
$$P(\text{pattern}|115\%) = \frac{P(115\%|\text{pattern})P(\text{pattern})}{P(115\%)}$$
$$P(\text{UDUD}|115\%) = \frac{0.43\cdot0.45}{0.2} \approx 0.97$$
$$P(\text{BS}|115\%) = \frac{0\cdot0.25}{0.2} = 0$$
$$P(\text{D}|115\%) = \frac{0\cdot0.15}{0.2} = 0$$
$$P(\text{SS}|115\%) = \frac{0.0625\cdot0.15}{0.2} \approx 0.05$$

Our new model for this week's pattern is:

$$P(\text{UDUD}) = 0.97$$
$$P(\text{BS}) = 0$$
$$P(\text{D})= 0$$
$$P(\text{SS}) = 0.05$$

# Abstracting it into an algorithm

Now we have a general algorithm we can use to predict what pattern we are in very early on in the week:

1. Determine initial probabilities
    - This is either the known probabilities based on last week's pattern or the generalized probabilities if we do not know last week's pattern: 
$$P(\text{UDUD}) = 0.35$$
$$P(\text{BS}) = 0.2625$$
$$P(\text{D}) = 0.1375$$
$$P(\text{SS}) = 0.25$$
2. Determine the probabilty of the current price happening at the current time step given each pattern: $$P(\text{price change}|\text{pattern}) = P(\text{phase}|\text{price}) \cdot (1 - \frac{\text{price change} - \text{low for phase}}{\text{high for phase} - \text{low for phase}})$$
3. Determine the total probability of the current price happening at the current time step (normalizing constant):
$$P(115\%) = \sum_{\text{pattern}} P(\text{pattern})P(115\%|\text{pattern})$$
4. Update the prior:
$$P(\text{pattern}|115\%) = \frac{P(115\%|\text{pattern})P(\text{pattern})}{P(115\%)}$$
