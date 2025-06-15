
import streamlit as st
from utils import get_model_response, analyze_debate

st.set_page_config(page_title="AI vs AI Debate", layout="wide")

st.title("🤖 AI vs AI Debate Platform")

models = ["OpenAI GPT-3.5", "OpenAI GPT-4", "Claude 3", "Gemini 1.5", "HuggingFace LLaMA/Mistral"]

st.sidebar.header("🧠 Model Setup")

debater_1 = st.sidebar.selectbox("Choose Debater 1", models, key="debater1")
api_key_1 = st.sidebar.text_input("Enter API Key for Debater 1", type="password", key="api1")

debater_2 = st.sidebar.selectbox("Choose Debater 2", models, key="debater2")
api_key_2 = st.sidebar.text_input("Enter API Key for Debater 2", type="password", key="api2")

topic = st.text_input("🎯 Enter a debate topic")

if "debate_history" not in st.session_state:
    st.session_state.debate_history = []

if "turn" not in st.session_state:
    st.session_state.turn = 0

if "debating" not in st.session_state:
    st.session_state.debating = False

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("▶️ Start Debate") and topic:
        st.session_state.debating = True
        st.session_state.debate_history = []
        st.session_state.turn = 0
with col2:
    if st.button("⏹️ Stop Debate"):
        st.session_state.debating = False

# Debate logic
if st.session_state.debating:
    if st.session_state.turn == 0:
        prompt = topic
    else:
        prompt = st.session_state.debate_history[-1]["text"]

    current_debater = debater_1 if st.session_state.turn % 2 == 0 else debater_2
    current_api_key = api_key_1 if current_debater == debater_1 else api_key_2

    with st.spinner(f"{current_debater} is thinking..."):
        try:
            response = get_model_response(current_debater, prompt, current_api_key)
            st.session_state.debate_history.append({"speaker": current_debater, "text": response})
            st.session_state.turn += 1
        except Exception as e:
            st.error(f"Error from {current_debater}: {str(e)}")
            st.session_state.debating = False

st.subheader("📝 Debate Transcript")
for entry in st.session_state.debate_history:
    st.markdown(f"**{entry['speaker']}**: {entry['text']}")

if st.button("📊 Analyze Debate"):
    judges = [m for m in models if m not in [debater_1, debater_2]]
    judge_keys = {}
    for judge in judges:
        judge_keys[judge] = st.sidebar.text_input(f"API Key for Judge: {judge}", type="password", key=f"judge_{judge}")
    transcript = "\n".join([f"{e['speaker']}: {e['text']}" for e in st.session_state.debate_history])
    report = analyze_debate(judges, transcript, judge_keys)
    st.text_area("🧾 Debate Analysis Report", report, height=300)

    b64 = report.encode("utf-8").hex()
    st.markdown(f'<a href="data:file/txt;base64,{b64}" download="debate_analysis.txt">📥 Download Report</a>', unsafe_allow_html=True)
