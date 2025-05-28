import subprocess
import shutil
import os

def generate_local_feedback(summary_text):
    prompt = f"""
You are an equine sports scientist. Based on the horse's training data, write a short and helpful feedback message for the trainer. Use a professional and supportive tone.

The data includes:
- Date
- Training Load (Load)
- ACWR (Acute:Chronic Workload Ratio)
- Zone (training quality: undertrained, optimal, overtrained)

Guidelines:
- Comment on the overall training balance.
- Point out gaits that are undertrained or overtrained (based on Zone).
- Note that some days have Load = 0 (recovery days).
- Give clear advice on adjusting training or giving rest.

Provide only the feedback with explanations. No summaries.

Horse Summary:
{summary_text}
--- Training Summary End ---

Trainer Feedback:
"""

    # Try to find the 'ollama' executable in the system's PATH
    ollama_path = shutil.which("ollama")

    # If not found, fallback to a known path (adjust as needed for others)
    if not ollama_path:
        fallback_path = r"C:\Users\riste\AppData\Local\Programs\Ollama\ollama.exe"
        if os.path.exists(fallback_path):
            ollama_path = fallback_path
        else:
            raise FileNotFoundError("Ollama is not installed or not found in system PATH.")

    # Run Mistral model via Ollama CLI
    result = subprocess.run(
        [ollama_path, "run", "mistral"],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )

    output = result.stdout.decode('utf-8')
    return output.strip()
