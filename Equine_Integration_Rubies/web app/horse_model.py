import pandas as pd
import os
from datetime import timedelta

# Load and preprocess the data once
base_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(base_dir, "data")
data_path = os.path.join(data_folder, "Horse_Readiness_CLEANED.json")

with open(data_path, 'r') as file:
    df_clean = pd.read_json(file)

df_clean["Date"] = pd.to_datetime(df_clean["Date"], errors='coerce')

# Horse IDs that require Dutch feedback
horses_nl = [257, 483]
  # Extend this list with more Dutch horses as needed

# Gait translation for Dutch output
gait_translation = {
    "walk": "stap",
    "trot": "draf",
    "canter": "arbeidsgalop",
    "galop": "galop"
}

def get_all_horse_ids():
    return sorted(df_clean["HorseID"].unique())

# English feedback zone logic
def get_risk_zone(acwr):
    if acwr < 0.8:
        return "Undertrained"
    elif acwr > 1.5:
        return "Overtrained"
    else:
        return "Optimal"

# Dutch feedback zone logic
def get_risk_zone_nl(acwr):
    if acwr < 0.8:
        return "Ondergetraind"
    elif acwr > 1.5:
        return "Overtraind"
    else:
        return "Optimaal"

# English summary (recent 7 days)
def summarize_recent_7_days(df_horse):
    df_recent = df_horse.sort_values("Date").tail(7)
    summary = "Recent 7 Days Training Summary:\n"
    for _, row in df_recent.iterrows():
        summary += f"{row['Date'].strftime('%Y-%m-%d')}:\n"
        for gait in ["walk", "trot", "canter", "galop"]:
            load = row[f"iTrimp_{gait}_Load_Today"]
            acwr = row[f"iTrimp_{gait}_ACWR"]
            zone = get_risk_zone(acwr) if load > 0 else "Not Trained"
            summary += f"  {gait.capitalize()} - Load: {load:.1f} | ACWR: {acwr:.2f} | Zone: {zone}\n"
    return summary

# English summary (weekly average)
def summarize_weekly_averages(df_horse):
    df_sorted = df_horse.sort_values("Date")
    df_sorted['Week'] = df_sorted['Date'].dt.to_period('W').apply(lambda r: r.start_time)
    weeks = sorted(df_sorted['Week'].unique())[-6:-1]
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

# Dutch summary (recent 7 days)
def summarize_recent_7_days_nl(df_horse):
    df_recent = df_horse.sort_values("Date").tail(7)
    summary = "Recente 7-daagse trainingssamenvatting:\n"
    for _, row in df_recent.iterrows():
        summary += f"{row['Date'].strftime('%Y-%m-%d')}:\n"
        for gait in ["walk", "trot", "canter", "galop"]:
            load = row[f"iTrimp_{gait}_Load_Today"]
            acwr = row[f"iTrimp_{gait}_ACWR"]
            zone = get_risk_zone_nl(acwr) if load > 0 else "Niet getraind"
            gait_nl = gait_translation.get(gait, gait)
            summary += f"  {gait_nl.capitalize()} - Treinlading: {load:.1f} | ACWR: {acwr:.2f} | Zone: {zone}\n"
    return summary

# Dutch summary (weekly average)
def summarize_weekly_averages_nl(df_horse):
    df_sorted = df_horse.sort_values("Date")
    df_sorted['Week'] = df_sorted['Date'].dt.to_period('W').apply(lambda r: r.start_time)
    weeks = sorted(df_sorted['Week'].unique())[-6:-1]
    summary = "\nVorige 5 weken overzicht:\n"
    for week_start in weeks:
        week_data = df_sorted[df_sorted['Week'] == week_start]
        if len(week_data) == 0:
            continue
        avg_load = week_data["iTrimp_overall_Load_Today"].mean()
        avg_acwr = week_data["iTrimp_overall_ACWR"].mean()
        zone = get_risk_zone_nl(avg_acwr)
        week_end = week_start + timedelta(days=6)
        summary += f"Week ({week_start.date()} naar {week_end.date()}): Gemiddelde treinlading: {avg_load:.1f} | Gemiddelde ACWR: {avg_acwr:.2f} | Zone: {zone}\n"
    return summary

# Universal summary fetcher
def get_summary_for_horse(horse_id):
    df_horse = df_clean[df_clean["HorseID"] == int(horse_id)].copy()
    df_horse["Date"] = pd.to_datetime(df_horse["Date"], errors='coerce')

    if df_horse.empty:
        return "No data available for this horse."

    try:
        if int(horse_id) in horses_nl:
            summary1 = summarize_recent_7_days_nl(df_horse)
            summary2 = summarize_weekly_averages_nl(df_horse)
        else:
            summary1 = summarize_recent_7_days(df_horse)
            summary2 = summarize_weekly_averages(df_horse)
        return summary1 + "\n" + summary2
    except Exception as e:
        return f"Summary generation failed: {str(e)}"

def get_horse_dataframe(horse_id):
    df_horse = df_clean[df_clean["HorseID"] == int(horse_id)].copy()
    df_horse["Date"] = pd.to_datetime(df_horse["Date"], errors='coerce')
    return df_horse
