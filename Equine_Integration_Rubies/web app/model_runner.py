import subprocess
import shutil
import os
from personalized_prompts import get_personalized_prompt

# Utility to resolve Ollama CLI path
def get_ollama_path():
    ollama_path = shutil.which("ollama")

    if not ollama_path:
        fallback_path = r"C:\Users\riste\AppData\Local\Programs\Ollama\ollama.exe"
        if os.path.exists(fallback_path):
            ollama_path = fallback_path
        else:
            raise FileNotFoundError("Ollama is not installed or not found in system PATH.")

    return ollama_path


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
- Comment on each gait (walk, trot, canter, galop) based on Load and ACWR for the current week.
- Point out gaits that are undertrained or overtrained (based on Zone).
- Note that some days have Load = 0 (recovery days).
- Give clear advice on adjusting training or giving rest.

Provide only the feedback with explanations. No summaries.

--- Training Summary Start ---
{summary_text}
--- Training Summary End ---

Trainer Feedback:
"""

    ollama_path = get_ollama_path()

    result = subprocess.run(
        [ollama_path, "run", "gemma:7b"],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )

    return result.stdout.decode("utf-8").strip()


def generate_personalized_feedback(horse_id, summary_text):
    prompt_template = get_personalized_prompt(horse_id)

    if not prompt_template:
        raise ValueError(f"No prompt found for horse ID {horse_id}")

    prompt = prompt_template.format(summary_text=summary_text)
    ollama_path = get_ollama_path()

    result = subprocess.run(
        [ollama_path, "run", "gemma:7b"],
        input=prompt.encode(),
        stdout=subprocess.PIPE
    )

    return result.stdout.decode("utf-8").strip()
