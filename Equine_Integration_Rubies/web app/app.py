from flask import Flask, render_template, request, jsonify
from horse_model import get_all_horse_ids, get_summary_for_horse
from model_runner import generate_local_feedback

app = Flask(__name__)

@app.route('/')
def home():
    horse_ids = get_all_horse_ids()
    return render_template('index.html', horse_ids=horse_ids)

@app.route('/run_model', methods=['POST'])
def run_model():
    horse_id = request.form['horse_id']
    summary_text = get_summary_for_horse(horse_id)

    # Check if summary is valid (not an error message)
    if summary_text.startswith("No data available") or summary_text.startswith("Summary generation failed") or summary_text.startswith("Date column missing") or summary_text.startswith("All dates are invalid"):
        return jsonify({
            "summary": summary_text,
            "feedback": "Feedback could not be generated because summary generation failed."
        })

    feedback = generate_local_feedback(summary_text)
    return jsonify({"summary": summary_text, "feedback": feedback})

if __name__ == '__main__':
    app.run(debug=True)
