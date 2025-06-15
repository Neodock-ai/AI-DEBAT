
# 🤖 AI Debate Arena

A Streamlit-based web app that lets you pit two AI models against each other in a turn-based debate. Users select models, provide API keys (OpenAI, Claude, Gemini, Hugging Face), and watch a conversation unfold. Unused models serve as judges.

## 🌟 Features

- Choose any two debater models via dropdown
- Provide API keys per model (support for OpenAI GPT-3.5/4, Claude 3, Gemini, HF LLaMA/Mistral)
- Turn-by-turn live debate
- Debate ends by stop button or concession
- Unused models act as judges
- Downloadable final report

## 🚀 How to Run

1. Upload project to [Streamlit Cloud](https://streamlit.io/cloud)
2. Set `app.py` as the entry point
3. Deploy and use

## 🔐 API Keys

Each model requires its own key:
- OpenAI: https://platform.openai.com/
- Anthropic Claude: https://console.anthropic.com/
- Gemini (Google): https://makersuite.google.com/app/apikey
- HuggingFace: https://huggingface.co/settings/tokens

## 📦 Dependencies

```
pip install -r requirements.txt
```

## 🧠 Future Improvements

- Add chat history persistence
- Upload your own judging logic
- Add speech synthesis / avatars

---
Made with ❤️ using Streamlit + modern LLM APIs.
