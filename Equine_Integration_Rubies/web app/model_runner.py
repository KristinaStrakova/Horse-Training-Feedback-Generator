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


def generate_local_feedback(horse_id, summary_text):
    horses_nl = [257, 483]  # Extend this list as needed

    if int(horse_id) in horses_nl:
        prompt = f"""
Je bent een paardensportwetenschapper. Schrijf op basis van de trainingsgegevens van het paard een kort, duidelijk en nuttig feedbackbericht voor de trainer. Gebruik een vriendelijke, professionele en ondersteunende toon. Vermijd technische termen zoals ACWR; leg dingen uit op een begrijpelijke manier voor dagelijkse praktijktoepassing.

De gegevens omvatten:
• Datum
• Trainingsbelasting (Load)
• ACWR (Acute:Chronische werklastratio)
• Zone (trainingskwaliteit: ondertraind, optimaal, overtraind)

Structuur van de feedback:
1. Algemene trainingsbalans:
    o Geef een korte beoordeling van hoe de training de afgelopen week in totaal is verlopen.
    o Noem ook of er voldoende balans is tussen inspanning en herstel.
    o Benoem hersteldagen indien aanwezig.
2. Gangen die aandacht nodig hebben:
    o Benoem expliciet welke gangen ondertraind of overtraind zijn volgens de zone-indeling.
    o Geef eventueel een mogelijke oorzaak of aandachtspunt erbij.
3. Observaties per gang:
    o Geef een kort commentaar per gang (stap, draf, arbeidsgalop, galop).
    o Beschrijf of de inspanning deze week passend was, te laag of te hoog.
    o Leg zonder vakjargon uit wat dit betekent voor de conditie of het risico op overbelasting.
4. Advies:
    o Geef duidelijke en praktische aanbevelingen voor de komende week.
    o Denk aan: rustmomenten inbouwen, een bepaalde gang juist meer of minder trainen, of letten op signalen van vermoeidheid.

Belangrijk:
    • Geef alleen de feedback (geen samenvatting van de data).
    • Houd de toon positief en gericht op het ondersteunen van de trainer in het optimaliseren van de training.

--- Trainingsoverzicht Start ---
{summary_text}
--- Trainingsoverzicht Einde ---
"""
    else:
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
