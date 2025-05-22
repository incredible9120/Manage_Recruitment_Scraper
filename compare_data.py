import pandas as pd
import json
import csv

# Read the JSON data
with open("camps_data.json", "r") as f:
    camps_data = json.load(f)

# Read the CSV file
df = pd.read_csv("nike_soccer_camps_formatted.csv")

# Create a list to store comparison results
comparison_results = []

# Iterate through JSON data
for camp_id, camp_info in camps_data.items():
    state = camp_info["state"]
    camp_name = camp_info["camp_name"]
    city = camp_info["city"]

    # Find matching row in CSV
    matching_rows = df[
        df["Event Details"].str.contains(camp_name, case=False, na=False)
    ]

    for _, row in matching_rows.iterrows():
        comparison_results.append(
            {
                "State": state,
                "City": city,
                "Camp Name (JSON)": camp_name,
                "Event Details (CSV)": row["Event Details"],
                "Matched": camp_name.lower() in row["Event Details"].lower(),
            }
        )

# Write results to CSV
output_file = "camp_comparison_results.csv"
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "State",
            "City",
            "Camp Name (JSON)",
            "Event Details (CSV)",
            "Matched",
        ],
    )
    writer.writeheader()
    writer.writerows(comparison_results)

print(f"Comparison results have been written to {output_file}")

# Print summary statistics
total_camps = len(camps_data)
matched_camps = sum(1 for result in comparison_results if result["Matched"])
print(f"\nSummary:")
print(f"Total camps in JSON: {total_camps}")
print(f"Total matches found: {matched_camps}")
print(f"Match rate: {(matched_camps/total_camps)*100:.2f}%")
