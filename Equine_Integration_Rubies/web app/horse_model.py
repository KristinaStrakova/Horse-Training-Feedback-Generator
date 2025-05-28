import pandas as pd
import os
from datetime import timedelta

# Load and preprocess the data once
base_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(base_dir, "data")

# This joins the data subdirectory and file name
data_path = os.path.join(data_folder, "Horse_Readiness_CLEANED.json")

print("Looking inside:", data_folder)
print("Files found:", os.listdir(data_folder))
print("Looking for file at:", data_path)

# Now load the file using the correct absolute path
with open(data_path, 'r') as file:
    df_clean = pd.read_json(file)

# Ensure Date column is parsed as datetime
df_clean["Date"] = pd.to_datetime(df_clean["Date"], errors='coerce')

print("Sample of cleaned data:")
print(df_clean.head(2))

def get_all_horse_ids():
    """Return a sorted list of unique horse IDs from the dataset."""
    return sorted(df_clean["HorseID"].unique())

def get_risk_zone(acwr):
    if acwr < 0.8:
        return "Undertrained"
    elif acwr > 1.5:
        return "Overtrained"
    else:
        return "Optimal"

def summarize_recent_7_days(df_horse):
    if "Date" not in df_horse.columns:
        raise ValueError("Date column missing for this horse.")

    if df_horse["Date"].isnull().all():
        raise ValueError("All dates are invalid or missing.")

    df_recent = df_horse.sort_values("Date").tail(7)
    summary = "Recent 7 Days Training Summary:\n"

    for _, row in df_recent.iterrows():
        summary += f"{row['Date'].strftime('%Y-%m-%d')}:\n"
        for gait in ["walk", "trot", "canter", "galop"]:
            load_col = f"iTrimp_{gait}_Load_Today"
            acwr_col = f"iTrimp_{gait}_ACWR"
            if load_col in row and acwr_col in row:
                load = row[load_col]
                acwr = row[acwr_col]
                zone = get_risk_zone(acwr) if load > 0 else "Not Trained"
                summary += f"  {gait.capitalize()} - Load: {load:.1f} | ACWR: {acwr:.2f} | Zone: {zone}\n"
    return summary


def summarize_weekly_averages(df_horse):
    df_sorted = df_horse.sort_values("Date")
    df_sorted['Week'] = df_sorted['Date'].dt.to_period('W').apply(lambda r: r.start_time)

    weeks = sorted(df_sorted['Week'].unique())[-6:-1]  # Previous 5 full weeks

    summary = "\nPrevious 5 Weeks Overview:\n"

    for week_start in weeks:
        week_data = df_sorted[df_sorted['Week'] == week_start]
        if len(week_data) == 0:
            continue
        avg_load = week_data["iTrimp_overall_Load_Today"].mean()
        avg_acwr = week_data["iTrimp_overall_ACWR"].mean()
        zone = get_risk_zone(avg_acwr)
        week_end = week_start + timedelta(days=6)
        summary += f"Week ({week_start.date()} to {week_end.date()}): Avg Load: {avg_load:.1f} | Avg ACWR: {avg_acwr:.2f} | Zone: {zone}\n"
    return summary


def get_summary_for_horse(horse_id):
    """Filter dataset to a horse and return a combined summary."""
    df_horse = df_clean[df_clean["HorseID"] == int(horse_id)].copy()
    print(f"Columns for horse {horse_id} :", df_horse.columns)
    if df_horse.empty:
        return "No data available for this horse."

    try:
        summary1 = summarize_recent_7_days(df_horse)
        summary2 = summarize_weekly_averages(df_horse)
        return summary1 + "\n" + summary2
    except Exception as e:
        return f"Summary generation failed: {str(e)}"

