import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend
import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_grouped_bars(data, categories, title, ylabel, save_path, zone_shading=None):
    x = range(len(data))
    bar_width = 0.2

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['skyblue', 'orange', 'seagreen', 'crimson']
    for i, cat in enumerate(categories):
        values = [row[cat] for row in data]
        ax.bar([p + i * bar_width for p in x], values, width=bar_width, label=cat.capitalize(), color=colors[i % len(colors)])

    ax.set_xticks([p + bar_width * (len(categories)-1)/2 for p in x])
    ax.set_xticklabels([row['label'] for row in data])
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    ax.grid(True, axis='y')

    if zone_shading:
        for (low, high, color, label) in zone_shading:
            ax.axhspan(low, high, color=color, alpha=0.1, label=label)

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()


def plot_training_summary_bars(df_horse, output_dir, horse_id, is_dutch=False):
    gaits = ["walk", "trot", "canter", "galop"]
    df_horse = df_horse.sort_values("Date")
    df_recent = df_horse.tail(7)

    recent_labels = df_recent["Date"].dt.strftime("%Y-%m-%d").tolist()

    # Zone shading
    zone_shading_en = [(0, 0.8, 'blue', 'Undertrained'), (0.8, 1.5, 'green', 'Optimal'), (1.5, 2.0, 'red', 'Overtrained')]
    zone_shading_nl = [(0, 0.8, 'blue', 'Ondergetraind'), (0.8, 1.5, 'green', 'Optimaal'), (1.5, 2.0, 'red', 'Overtraind')]
    shading = zone_shading_nl if is_dutch else zone_shading_en

    # Translation for Dutch
    title_load = "Recent 7 dagen – Trainingsbelasting per gang" if is_dutch else "Recent 7 Days - Load per Gait"
    title_acwr = "Recent 7 dagen – ACWR per gang" if is_dutch else "Recent 7 Days - ACWR per Gait"
    title_weekly_load = "Gemiddelde wekelijkse belasting per gang (Laatste 5 weken)" if is_dutch else "Weekly Avg Load per Gait (Last 5 Weeks)"
    title_weekly_acwr = "Gemiddelde wekelijkse ACWR per gang (Laatste 5 weken)" if is_dutch else "Weekly Avg ACWR per Gait (Last 5 Weeks)"
    label_load = "Belasting" if is_dutch else "Load"
    label_acwr = "ACWR"

    # Load chart
    load_data = []
    for _, row in df_recent.iterrows():
        entry = {"label": row["Date"].strftime("%Y-%m-%d")}
        for gait in gaits:
            entry[gait] = row.get(f"iTrimp_{gait}_Load_Today", 0)
        load_data.append(entry)

    plot_grouped_bars(
        load_data, gaits,
        title=title_load,
        ylabel=label_load,
        save_path=os.path.join(output_dir, f"bars_load_{horse_id}.png")
    )

    # ACWR chart
    acwr_data = []
    for _, row in df_recent.iterrows():
        entry = {"label": row["Date"].strftime("%Y-%m-%d")}
        for gait in gaits:
            entry[gait] = row.get(f"iTrimp_{gait}_ACWR", 0)
        acwr_data.append(entry)

    plot_grouped_bars(
        acwr_data, gaits,
        title=title_acwr,
        ylabel=label_acwr,
        save_path=os.path.join(output_dir, f"bars_acwr_{horse_id}.png"),
        zone_shading=shading
    )

    # Weekly load
    df_horse["Week"] = df_horse["Date"].dt.to_period("W").apply(lambda r: r.start_time)
    last_weeks = df_horse["Week"].dropna().unique()[-5:]
    df_weekly = df_horse[df_horse["Week"].isin(last_weeks)]

    weekly_load_data = []
    for week in last_weeks:
        week_str = pd.Timestamp(week).strftime('%Y-%m-%d')
        entry = {"label": week_str}
        week_df = df_weekly[df_weekly["Week"] == week]
        for gait in gaits:
            entry[gait] = week_df[f"iTrimp_{gait}_Load_Today"].mean()
        weekly_load_data.append(entry)

    plot_grouped_bars(
        weekly_load_data, gaits,
        title=title_weekly_load,
        ylabel=label_load,
        save_path=os.path.join(output_dir, f"bars_weekly_load_{horse_id}.png")
    )

    # Weekly ACWR
    weekly_acwr_data = []
    for week in last_weeks:
        week_str = pd.Timestamp(week).strftime('%Y-%m-%d')
        entry = {"label": week_str}
        week_df = df_weekly[df_weekly["Week"] == week]
        for gait in gaits:
            entry[gait] = week_df[f"iTrimp_{gait}_ACWR"].mean()
        weekly_acwr_data.append(entry)

    plot_grouped_bars(
        weekly_acwr_data, gaits,
        title=title_weekly_acwr,
        ylabel=label_acwr,
        save_path=os.path.join(output_dir, f"bars_weekly_acwr_{horse_id}.png"),
        zone_shading=shading
    )
