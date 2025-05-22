import json
import pandas as pd

# Replace this with loading from a file if needed
with open("camps_data.json", "r") as f:
    json_data = json.load(f)

# Prepare the rows
formatted_rows = []
event_counter = 1

for key, camp in json_data.items():
    first_event_row = True
    for session in camp["sessions"]:
        first_session_row = True
        for subsession in session["subsessions"]:
            row = {
                "No": event_counter if first_event_row else "",
                "Event Details": camp["camp_name"] if first_event_row else "",
                "Latitude": camp["latitude"] if first_event_row else "",
                "Longitude": camp["longitude"] if first_event_row else "",
                "City": camp["city"] if first_event_row else "",
                "State": camp["state"].upper() if first_event_row else "",
                "Period": session["period"] if first_session_row else "",
                "Age": session["age"] if first_session_row else "",
                "Gender": session["gender"] if first_session_row else "",
                "Skills": subsession["skill"]
                .replace("<strong>", "")
                .replace("</strong>", ""),
                "Type": subsession["type"],
                "Payment": subsession["cost"],
            }
            formatted_rows.append(row)
            first_event_row = False
            first_session_row = False
    event_counter += 1

# Create DataFrame and export to CSV
df = pd.DataFrame(formatted_rows)
df.to_csv("nike_soccer_camps_formatted1.csv", index=False)

print("CSV saved as nike_soccer_camps_formatted.csv")
