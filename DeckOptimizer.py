import scipy.stats as stats
import numpy as np

# Parameters for the problem
n = 10  # total draws per attempt

# Number of each color needed
blue_needed = 3
red_needed = 2
yellow_needed_1 = 2  # For condition 1
yellow_needed_2 = 1  # For condition 2
green_needed = 1
orange_needed = 1  # New success condition

# Function to calculate the overall success probability for a given distribution of cards
def calculate_success_probability(blue_total, red_total, yellow_total, green_total, orange_total):
    N = blue_total + red_total + yellow_total + green_total + orange_total

    # For Condition 1: 3 blue, 2 red, 2 yellow, 1 green
    blue_prob = 1 - stats.hypergeom.cdf(blue_needed - 1, N, blue_total, n)
    red_prob = 1 - stats.hypergeom.cdf(red_needed - 1, N, red_total, n)
    yellow_prob_1 = 1 - stats.hypergeom.cdf(yellow_needed_1 - 1, N, yellow_total, n)
    green_prob = 1 - stats.hypergeom.cdf(green_needed - 1, N, green_total, n)
    condition_1_prob = blue_prob * red_prob * yellow_prob_1 * green_prob

    # For Condition 2: 3 blue, 2 red, 1 yellow, 1 orange
    yellow_prob_2 = 1 - stats.hypergeom.cdf(yellow_needed_2 - 1, N, yellow_total, n)
    orange_prob = 1 - stats.hypergeom.cdf(orange_needed - 1, N, orange_total, n)
    condition_2_prob = blue_prob * red_prob * yellow_prob_2 * orange_prob

    # For both conditions simultaneously: 3 blue, 2 red, 2 yellow, 1 green, 1 orange
    both_conditions_prob = blue_prob * red_prob * yellow_prob_1 * green_prob * orange_prob

    # Overall probability of success in either condition
    overall_prob = condition_1_prob + condition_2_prob - both_conditions_prob
    return overall_prob

# Try different distributions of cards that sum to 100
best_distribution = None
best_probability = 0

# Loop over possible card distributions that add up to 100
for blue_total in range(20, 41):  # Range of blue cards
    for red_total in range(15, 31):  # Range of red cards
        for yellow_total in range(10, 26):  # Range of yellow cards
            for green_total in range(5, 16):  # Range of green cards
                orange_total = 100 - (blue_total + red_total + yellow_total + green_total)  # Ensure total is 100

                # Ensure orange total is within a valid range
                if orange_total >= 5 and orange_total <= 15:
                    probability = calculate_success_probability(blue_total, red_total, yellow_total, green_total, orange_total)

                    # Track the best distribution
                    if probability > best_probability:
                        best_probability = probability
                        best_distribution = (blue_total, red_total, yellow_total, green_total, orange_total)

# Print the best distribution and probability
print(f"Best distribution: Blue: {best_distribution[0]}, Red: {best_distribution[1]}, "
      f"Yellow: {best_distribution[2]}, Green: {best_distribution[3]}, Orange: {best_distribution[4]}")
print(f"Best probability: {best_probability:.4f}")
