
# Given input values
biomarker_x_reduction = 0.30
x_to_progression_correlation_range = (0.20, 0.70)
progression_to_mortality_correlation_range = (0.50, 0.90)

# Calculate the minimum and maximum possible overall mortality reduction
min_mortality_reduction = biomarker_x_reduction * x_to_progression_correlation_range[0] * progression_to_mortality_correlation_range[0]
max_mortality_reduction = biomarker_x_reduction * x_to_progression_correlation_range[1] * progression_to_mortality_correlation_range[1]

# Write the results to a file
with open("mortality_effect_range.txt", "w") as f:
    f.write(f"{min_mortality_reduction:.3f}\n")
    f.write(f"{max_mortality_reduction:.3f}\n")

print("Calculation complete. Results written to mortality_effect_range.txt")
