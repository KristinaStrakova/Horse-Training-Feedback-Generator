from flask import Flask, render_template, request
from flask import request, render_template
from horse_model import get_all_horse_ids, get_summary_for_horse, get_horse_dataframe
from model_runner import generate_local_feedback
from model_runner import  generate_personalized_feedback
from utils.summary_plot_bars import plot_training_summary_bars
from utils.summary_plot_bars import plot_training_summary_bars
import os


# Mapping of Horse ID to display name
HORSE_NAME_MAP = {
    257: "257 – Dem",
    483: "483 – Kizzy",
    311: "311 – Timmy",
    601: "601 – Mumbles",
    602: "602 – Beaufort"
}

app = Flask(__name__)

@app.route('/')
def home():
    horse_ids = get_all_horse_ids()
    return render_template('index.html',
                           horse_ids=horse_ids,
                           selected_horse_id=None,
                           summary_text=None,
                           feedback=None,
                           chart_path=None,
                           HORSE_NAME_MAP=HORSE_NAME_MAP)



@app.route('/run_model', methods=['POST'])
def run_model():
    horse_id = request.form.get('horse_id')
    if not horse_id:
        horse_ids = get_all_horse_ids()
        error_message = "Please select a horse ID before submitting."
        return render_template("_results.html",
                       horse_ids=horse_ids,
                       selected_horse_id=None,
                       summary_text=None,
                       feedback=None,
                       personalized_feedback=None,
                       chart_path=None,
                       error_message=error_message,
                       is_dutch=False,
                       HORSE_NAME_MAP=HORSE_NAME_MAP)  # Default to English


    horse_ids = get_all_horse_ids()
    summary_text = get_summary_for_horse(horse_id)

    if summary_text.startswith("No data available") or "Summary generation failed" in summary_text:
        return render_template("_results.html",
                       horse_ids=horse_ids,
                       summary_text=summary_text,
                       feedback=None,
                       personalized_feedback=None,
                       chart_path=None,
                       selected_horse_id=horse_id,
                       selected_horse_name=HORSE_NAME_MAP.get(int(horse_id), horse_id),
                       is_dutch=int(horse_id) in [257, 483],
                       HORSE_NAME_MAP=HORSE_NAME_MAP)


    feedback = generate_local_feedback(horse_id, summary_text)
    personalized_feedback = generate_personalized_feedback(horse_id, summary_text)

    df_horse = get_horse_dataframe(horse_id)
    chart_filename = f"training_summary_{horse_id}.png"
    chart_path = os.path.join("static", "charts", chart_filename)

    #plot_training_summary(df_horse, chart_path)


    is_dutch = int(horse_id) in [257, 483]
    plot_training_summary_bars(df_horse, output_dir="static/charts", horse_id=horse_id, is_dutch=is_dutch)

    return render_template("_results.html",
                       horse_ids=horse_ids,
                       summary_text=summary_text,
                       feedback=feedback,
                       personalized_feedback=personalized_feedback,
                       chart_path=f"charts/{chart_filename}",
                       selected_horse_id=horse_id,
                       selected_horse_name=HORSE_NAME_MAP.get(int(horse_id), horse_id),
                       is_dutch=is_dutch,
                       HORSE_NAME_MAP=HORSE_NAME_MAP)


if __name__ == '__main__':
    app.run(debug=True)
