import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib
matplotlib.use("Agg")  # Use a non-GUI backend


def plot_training_summary(df_horse, save_path):
    df_horse = df_horse.sort_values("Date")
    gaits = ["walk", "trot", "canter", "galop"]

    # Prepare recent 7-day data
    df_recent = df_horse.tail(7)
    dates = df_recent["Date"].dt.strftime("%Y-%m-%d")

    # Prepare last 3 weeks
    df_horse["Week"] = df_horse["Date"].dt.to_period("W").apply(lambda r: r.start_time)
    last_5_weeks = df_horse["Week"].dropna().unique()[-5:]
    df_weekly = df_horse[df_horse["Week"].isin(last_5_weeks)]

    weekly_agg = df_weekly.groupby("Week").agg({
        **{f"iTrimp_{g}_Load_Today": 'mean' for g in gaits},
        **{f"iTrimp_{g}_ACWR": 'mean' for g in gaits}
    }).reset_index()
    weeks = weekly_agg["Week"].dt.strftime('%Y-%m-%d')

    # Plot setup
    fig, axs = plt.subplots(4, 1, figsize=(14, 16), sharex=False)

    for gait in gaits:
        axs[0].plot(dates, df_recent[f"iTrimp_{gait}_Load_Today"], marker='o', label=gait.capitalize())
    axs[0].set_ylabel("Load Today")
    axs[0].set_title("Recent 7 Days - Load per Gait")
    axs[0].legend()
    axs[0].grid(True)

    for gait in gaits:
        axs[1].plot(dates, df_recent[f"iTrimp_{gait}_ACWR"], marker='o', label=gait.capitalize())
    axs[1].axhspan(0, 0.8, color='blue', alpha=0.1)
    axs[1].axhspan(0.8, 1.5, color='green', alpha=0.1)
    axs[1].axhspan(1.5, 2.0, color='red', alpha=0.1)
    axs[1].set_ylabel("ACWR")
    axs[1].set_title("Recent 7 Days - ACWR per Gait")
    axs[1].legend()
    axs[1].grid(True)

    for gait in gaits:
        axs[2].plot(weeks, weekly_agg[f"iTrimp_{gait}_Load_Today"], marker='o', label=gait.capitalize())
    axs[2].set_title("Weekly Average Load per Gait (Last 5 Weeks)")
    axs[2].set_ylabel("Average Load")
    axs[2].legend()
    axs[2].grid(True)

    for gait in gaits:
        axs[3].plot(weeks, weekly_agg[f"iTrimp_{gait}_ACWR"], marker='x', linestyle='--', label=gait.capitalize())
    axs[3].axhspan(0, 0.8, color='blue', alpha=0.1, label='Undertrained')
    axs[3].axhspan(0.8, 1.5, color='green', alpha=0.1, label='Optimal')
    axs[3].axhspan(1.5, 2.0, color='red', alpha=0.1, label='Overtrained')
    axs[3].set_title("Weekly Average ACWR per Gait (Last 5 Weeks)")
    axs[3].set_ylabel("Average ACWR")
    axs[3].legend()
    axs[3].grid(True)
    axs[3].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()
