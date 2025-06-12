from flask import Flask, render_template, request
from flask import request, render_template, jsonify
from horse_model import get_all_horse_ids, get_summary_for_horse, get_horse_dataframe
from model_runner import generate_local_feedback
from model_runner import  generate_personalized_feedback
from utils.summary_plot import plot_training_summary
from utils.summary_plot_bars import plot_training_summary_bars
import os

app = Flask(__name__)

@app.route('/')
def home():
    horse_ids = get_all_horse_ids()
    return render_template('index.html',
                           horse_ids=horse_ids,
                           selected_horse_id=None,
                           summary_text=None,
                           feedback=None,
                           chart_path=None)



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
                            error_message=error_message)

    horse_ids = get_all_horse_ids()
    summary_text = get_summary_for_horse(horse_id)

    if summary_text.startswith("No data available") or "Summary generation failed" in summary_text:
        return render_template("_results.html",
                               horse_ids=horse_ids,
                               summary_text=summary_text,
                               feedback=None,
                               personalized_feedback=None,
                               chart_path=None,
                               selected_horse_id=horse_id)

    feedback = generate_local_feedback(summary_text)
    personalized_feedback = generate_personalized_feedback(horse_id, summary_text)

    df_horse = get_horse_dataframe(horse_id)
    chart_filename = f"training_summary_{horse_id}.png"
    chart_path = os.path.join("static", "charts", chart_filename)

    plot_training_summary(df_horse, chart_path)
    plot_training_summary_bars(df_horse, output_dir="static/charts", horse_id=horse_id)

    return render_template("_results.html",
                           horse_ids=horse_ids,
                           summary_text=summary_text,
                           feedback=feedback,
                           personalized_feedback=personalized_feedback,
                           chart_path=f"charts/{chart_filename}",
                           selected_horse_id=horse_id)

if __name__ == '__main__':
    app.run(debug=True)
