
import openai
import requests
import json

def get_model_response(model, prompt, api_key):
    if "OpenAI" in model:
        openai.api_key = api_key
        model_engine = "gpt-3.5-turbo" if "3.5" in model else "gpt-4"
        response = openai.ChatCompletion.create(
            model=model_engine,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message["content"].strip()

    elif "Claude" in model:
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        body = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 512,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, headers=headers, data=json.dumps(body))
        return response.json()["content"][0]["text"].strip()

    elif "Gemini" in model:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        body = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(url, headers=headers, data=json.dumps(body))
        return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

    elif "HuggingFace" in model:
        url = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-13b-chat-hf"
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {"inputs": prompt}
        response = requests.post(url, headers=headers, json=payload)
        return response.json()[0]["generated_text"].strip()

    else:
        raise ValueError("Unsupported model")

def analyze_debate(models, transcript, api_keys):
    summary = "## 🤖 Judge Report\n"
    for model in models:
        try:
            summary += f"### Judge: {model}\n"
            feedback_prompt = (
                f"Analyze this AI debate and score both sides. "
                f"Here is the transcript:\n\n{transcript}\n\n"
                f"Provide: 1) Overall feedback, 2) Score out of 10 for each debater, 3) Declare a winner."
            )
            response = get_model_response(model, feedback_prompt, api_keys[model])
            summary += response + "\n\n"
        except Exception as e:
            summary += f"Could not get response from {model}: {str(e)}\n\n"
    return summary
