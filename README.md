# Horse Feedback AI Generator + Set Up

A locally running AI-powered tool to help generate training feedback and insights for horses based on input metrics, using a local LLM via Ollama.

---

## Project Overview

This project uses **Visual Studio** and runs a **Python app** that communicates with a local LLM (Large Language Model) like **Gemma** through **Ollama**.

>  Example usage:
> *"Horse's ACWR has been above 1.5 for 4 days. Suggest training advice."*
> *"Tell me a short joke about horses."*

---

## Prerequisites

Before running the project, you need to set up **Ollama** locally.

---

## 🧠 Setting Up Ollama

### 1. **Install Ollama**

For **Windows**, download and install Ollama from:

 [https://ollama.com/download](https://ollama.com/download)

---

### 2. **Download a Model**

> Important: Use a **regular terminal** (not the VS Code integrated terminal).

Run the following command to download the Gemma model:

```bash
ollama pull gemma:7b
```

---

### 3. **Test the Model**

Check that it's working by running:

```bash
ollama run gemma:7b
```

You can try prompts like:

```
Horse's ACWR has been above 1.5 for 4 days. Suggest training advice.
```

If you receive a response, the model is running correctly!

---

## Running the App

1. **Open the project in Visual Studio**.

2. Ensure you're in the correct folder **before running the script**:

```bash
cd '.\Equine_Integration_Rubies\web app\'
```

3. Run the app using:

```bash
python app.py
```

The app will launch and communicate with the local Ollama model on link:
 [http://127.0.0.1:5000](http://127.0.0.1:5000)


