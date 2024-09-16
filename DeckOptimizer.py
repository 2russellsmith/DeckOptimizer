import scipy.stats as stats

# Parameters for the problem
n = 10  # Total draws per attempt
total_cards = 100  # Total number of cards available (including tutors)

# Number of each card type needed for each condition
land_needed = 3  # (land cards)
ramp_needed = 2  # (ramp cards)
sacrifice_with_payoff_needed_1 = 1  # (sacrifice outlets with payoff)
sacrifice_without_payoff_needed = 1  # (sacrifice outlets without payoffs)
persist_without_payoff_needed = 1  # (persist creatures without payoffs)
persist_with_payoff_needed_1 = 1  # (persist creatures with payoffs)
payoff_needed = 1  # (payoff cards)

# Max limits for each card type
max_land = 60  # Maximum number of land cards
max_ramp = 20  # Maximum number of ramp cards
max_sacrifice_with_payoff = 3  # Maximum number of sacrifice with payoff cards
max_sacrifice_without_payoff = 10  # Maximum number of sacrifice without payoff cards
max_persist_without_payoff = 8  # Maximum number of persist without payoff cards
max_persist_with_payoff = 2  # Maximum number of persist with payoff cards
max_payoff = 20  # Maximum number of payoff cards
max_tutors = 8  # Maximum number of tutors


# Function to calculate success probability for a given distribution
def calculate_success_probability(land_total, ramp_total, sacrifice_with_payoff_total, persist_without_payoff_total,
                                  sacrifice_without_payoff_total, persist_with_payoff_total, payoff_total,
                                  tutors_total):
    N = land_total + ramp_total + sacrifice_with_payoff_total + persist_without_payoff_total + sacrifice_without_payoff_total + persist_with_payoff_total + payoff_total + tutors_total

    # Adjust probabilities for tutors being able to fill any requirement
    effective_land_total = land_total + tutors_total
    effective_ramp_total = ramp_total + tutors_total
    effective_sacrifice_with_payoff_total = sacrifice_with_payoff_total + tutors_total
    effective_persist_without_payoff_total = persist_without_payoff_total + tutors_total
    effective_sacrifice_without_payoff_total = sacrifice_without_payoff_total + tutors_total
    effective_persist_with_payoff_total = persist_with_payoff_total + tutors_total
    effective_payoff_total = payoff_total + tutors_total

    # Condition 1: 3 Land, 2 Ramp, 1 Sacrifice with Payoff, 1 Persist without Payoff
    land_prob = 1 - stats.hypergeom.cdf(land_needed - 1, N, effective_land_total, n)
    ramp_prob = 1 - stats.hypergeom.cdf(ramp_needed - 1, N, effective_ramp_total, n)
    sacrifice_with_payoff_prob = 1 - stats.hypergeom.cdf(sacrifice_with_payoff_needed_1 - 1, N,
                                                         effective_sacrifice_with_payoff_total, n)
    persist_without_payoff_prob = 1 - stats.hypergeom.cdf(persist_without_payoff_needed - 1, N,
                                                          effective_persist_without_payoff_total, n)
    condition_1_prob = land_prob * ramp_prob * sacrifice_with_payoff_prob * persist_without_payoff_prob

    # Condition 2: 3 Land, 2 Ramp, 1 Sacrifice without Payoff, 1 Persist with Payoff
    sacrifice_without_payoff_prob = 1 - stats.hypergeom.cdf(sacrifice_without_payoff_needed - 1, N,
                                                            effective_sacrifice_without_payoff_total, n)
    persist_with_payoff_prob_2 = 1 - stats.hypergeom.cdf(persist_with_payoff_needed_1 - 1, N,
                                                         effective_persist_with_payoff_total, n)
    condition_2_prob = land_prob * ramp_prob * sacrifice_without_payoff_prob * persist_with_payoff_prob_2

    # Condition 3: 3 Land, 2 Ramp, 1 Sacrifice with Payoff, 1 Persist with Payoff
    persist_with_payoff_prob_3 = 1 - stats.hypergeom.cdf(persist_with_payoff_needed_1 - 1, N,
                                                         effective_persist_with_payoff_total, n)
    condition_3_prob = land_prob * ramp_prob * sacrifice_with_payoff_prob * persist_with_payoff_prob_3

    # Condition 4: 3 Land, 2 Ramp, 1 Sacrifice without Payoff, 1 Persist without Payoff, 1 Payoff
    payoff_prob = 1 - stats.hypergeom.cdf(payoff_needed - 1, N, effective_payoff_total, n)
    condition_4_prob = land_prob * ramp_prob * sacrifice_without_payoff_prob * persist_without_payoff_prob * payoff_prob

    # Combined probability (success in at least one condition)
    combined_prob = (condition_1_prob + condition_2_prob + condition_3_prob + condition_4_prob
                     - (condition_1_prob * condition_2_prob)
                     - (condition_1_prob * condition_3_prob)
                     - (condition_1_prob * condition_4_prob)
                     - (condition_2_prob * condition_3_prob)
                     - (condition_2_prob * condition_4_prob)
                     - (condition_3_prob * condition_4_prob))

    return combined_prob


# Find the best distribution
best_probability = 0
best_distribution = None

# Iterate over possible distributions of card counts, now with limits on card types
for land_total in range(min(total_cards, max_land) + 1):
    print(land_total)
    for ramp_total in range(min(total_cards - land_total, max_ramp) + 1):
        for sacrifice_with_payoff_total in range(
                min(total_cards - land_total - ramp_total, max_sacrifice_with_payoff) + 1):
            for persist_without_payoff_total in range(
                    min(total_cards - land_total - ramp_total - sacrifice_with_payoff_total,
                        max_persist_without_payoff) + 1):
                for sacrifice_without_payoff_total in range(
                        min(total_cards - land_total - ramp_total - sacrifice_with_payoff_total - persist_without_payoff_total,
                            max_sacrifice_without_payoff) + 1):
                    for persist_with_payoff_total in range(
                            min(total_cards - land_total - ramp_total - sacrifice_with_payoff_total - persist_without_payoff_total - sacrifice_without_payoff_total,
                                max_persist_with_payoff) + 1):
                        for payoff_total in range(
                                min(total_cards - land_total - ramp_total - sacrifice_with_payoff_total - persist_without_payoff_total - sacrifice_without_payoff_total - persist_with_payoff_total,
                                    max_payoff) + 1):
                            remaining_cards = total_cards - (
                                        land_total + ramp_total + sacrifice_with_payoff_total + persist_without_payoff_total + sacrifice_without_payoff_total + persist_with_payoff_total + payoff_total)
                            if remaining_cards >= 0 and remaining_cards <= max_tutors:  # Make sure tutors fit within the remaining card count
                                tutors_total = remaining_cards  # Tutors are included in the remaining cards
                                probability = calculate_success_probability(
                                    land_total,
                                    ramp_total,
                                    sacrifice_with_payoff_total,
                                    persist_without_payoff_total,
                                    sacrifice_without_payoff_total,
                                    persist_with_payoff_total,
                                    payoff_total,
                                    tutors_total
                                )

                                # Track the best configuration
                                if probability > best_probability:
                                    best_probability = probability
                                    best_distribution = {
                                        'land_total': land_total,
                                        'ramp_total': ramp_total,
                                        'sacrifice_with_payoff_total': sacrifice_with_payoff_total,
                                        'persist_without_payoff_total': persist_without_payoff_total,
                                        'sacrifice_without_payoff_total': sacrifice_without_payoff_total,
                                        'persist_with_payoff_total': persist_with_payoff_total,
                                        'payoff_total': payoff_total,
                                        'tutors_total': tutors_total,
                                        'probability': probability
                                    }

# Output the best distribution and probability
print("Best distribution found:")
for key, value in best_distribution.items():
    print(f"{key}: {value}")
