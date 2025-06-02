from flask import Flask, render_template, request
from horse_model import get_all_horse_ids, get_summary_for_horse, get_horse_dataframe
from model_runner import generate_local_feedback
from utils.summary_plot import plot_training_summary
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
    horse_id = request.form['horse_id']
    horse_ids = get_all_horse_ids()
    
    summary_text = get_summary_for_horse(horse_id)

    if summary_text.startswith("No data available") or "Summary generation failed" in summary_text:
        return render_template("index.html",
                               horse_ids=horse_ids,
                               summary_text="[Error fetching summary]",
                               feedback="[Error fetching feedback]",
                               chart_path=None,
                               horse_id=horse_id)

    feedback = generate_local_feedback(summary_text)

    # Generate the summary chart
    df_horse = get_horse_dataframe(horse_id)
    chart_filename = f"training_summary_{horse_id}.png"
    chart_path = os.path.join("static", "charts", chart_filename)
    plot_training_summary(df_horse, chart_path)

    return render_template("index.html",
                       horse_ids=horse_ids,
                       summary_text=summary_text,
                       feedback=feedback,
                       chart_path=f"charts/{chart_filename}",
                       horse_id=horse_id,
                       selected_horse_id=horse_id)


if __name__ == '__main__':
    app.run(debug=True)
