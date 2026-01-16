import streamlit as st
import requests
import json
from fpdf import FPDF

# --- COLE SUA CHAVE AQUI ---
MINHA_CHAVE_GOOGLE = "AIzaSyBuxA433U7YWXQ5baurlLbzj8QFQzSa2v4" 

st.set_page_config(page_title="Eroticizza", layout="wide")

def gerar_texto(prompt_usuario):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={MINHA_CHAVE_GOOGLE}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": f"Você é um escritor de contos adultos (ficção). {prompt_usuario}"}]}],
        "safetySettings": [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
        ]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Erro: {response.text}"
    except Exception as e:
        return f"Erro de conexão: {e}"

if 'step' not in st.session_state: st.session_state.step = 1
if 'historia' not in st.session_state: st.session_state.historia = ""
if 'personagens' not in st.session_state: st.session_state.personagens = []

if st.session_state.step == 1:
    st.title("🔥 Eroticizza")
    sel = st.multiselect("Personagens", ["Executivo", "Humanitária", "Lutador"], max_selections=2)
    if len(sel) == 2:
        if st.button("Confirmar"):
            st.session_state.personagens = sel
            st.session_state.step = 2
            st.rerun()

elif st.session_state.step == 2:
    st.title("📍 Contexto")
    local = st.selectbox("Local", ["Escritório", "Hotel"])
    ctx = st.text_area("Situação", "Atração fatal.")
    if st.button("Gerar"):
        res = gerar_texto(f"Crie conto com {st.session_state.personagens} no {local}. {ctx}")
        st.session_state.historia += res
        st.session_state.step = 3
        st.rerun()

elif st.session_state.step == 3:
    st.markdown(st.session_state.historia)
    if st.button("Reiniciar"): st.session_state.clear(); st.rerun()
