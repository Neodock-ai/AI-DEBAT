
import openai
import requests
import json

def get_model_response(model, full_history, api_key):
    if "OpenAI" in model:
        client = openai.OpenAI(api_key=api_key)
        model_engine = "gpt-3.5-turbo" if "3.5" in model else "gpt-4"
        response = client.chat.completions.create(
            model=model_engine,
            messages=full_history,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()

    elif "Claude" in model:
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        body = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 512,
            "messages": full_history
        }
        response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=body)
        parsed = response.json()
        return parsed.get("content", [{}])[0].get("text", "Claude did not return content.")

    elif "Gemini" in model:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        body = {"contents": [{"parts": [{"text": full_history[-1]['content']}]}]}
        response = requests.post(url, headers=headers, data=json.dumps(body))
        parsed = response.json()
        try:
            return parsed["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception:
            return "Gemini did not return a valid response."

    elif "HuggingFace" in model:
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {"inputs": full_history[-1]["content"]}
        response = requests.post(
            "https://api-inference.huggingface.co/models/meta-llama/Llama-2-13b-chat-hf",
            headers=headers, json=payload)
        parsed = response.json()
        try:
            return parsed[0]["generated_text"].strip()
        except Exception:
            return "HF model did not return a valid response."

    else:
        return "Unsupported model."

def analyze_debate(models, transcript, api_keys):
    summary = "## 🤖 Judge Report\n"
    feedback_prompt = (
        f"You are an expert debate judge. Analyze this conversation and give:
"
        f"1. Overall Feedback
"
        f"2. Score out of 10 for each debater
"
        f"3. Declare a winner.

"
        f"Transcript:
{transcript}"
    )
    for model in models:
        try:
            if not api_keys.get(model):
                summary += f"### Judge: {model}
⚠️ No API key provided.

"
                continue
            full_msg = [{"role": "user", "content": feedback_prompt}]
            result = get_model_response(model, full_msg, api_keys[model])
            summary += f"### Judge: {model}
{result}

"
        except Exception as e:
            summary += f"### Judge: {model}
❌ Error: {str(e)}

"
    return summary
