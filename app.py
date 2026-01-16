import streamlit as st
import requests
import json
from fpdf import FPDF

# ==========================================
# CONFIGURAÇÃO DA CHAVE (Sua chave OpenRouter)
# ==========================================
# Estou usando a chave que você forneceu. 
# Nota: Como ela foi exposta no chat, use para testar agora e depois crie uma nova.
API_KEY = "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"

st.set_page_config(page_title="Eroticizza", layout="wide")

# Função de Conexão MANUAL (Bypass de Biblioteca)
def gerar_texto(prompt_sistema, prompt_usuario):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://eroticizza.streamlit.app", # Necessário para o OpenRouter
        "X-Title": "Eroticizza",
        "Content-Type": "application/json"
    }
    
    data = {
        # MODELO: MythoMax (O rei do erotismo sem censura)
        "model": "gryphe/mythomax-l2-13b", 
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ],
        "temperature": 0.85, # Temperatura alta para mais criatividade
        "max_tokens": 2000
    }
    
    try:
        # Envia o pedido direto para o servidor (sem passar por bibliotecas bugadas)
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            # Se der erro, mostra exatamente o que é (ex: falta de crédito)
            erro = response.json()
            return f"Erro OpenRouter: {response.status_code} - {erro.get('error', {}).get('message', 'Erro desconhecido')}"
            
    except Exception as e:
        return f"Erro de conexão: {e}"

# ==========================================
# LÓGICA DO APP
# ==========================================

if 'step' not in st.session_state: st.session_state.step = 1
if 'historia' not in st.session_state: st.session_state.historia = ""
if 'personagens' not in st.session_state: st.session_state.personagens = []

# TELA 1: ELENCO
if st.session_state.step == 1:
    st.title("🔥 Eroticizza (Motor: MythoMax)")
    st.write("Crie contos intensos e sem censura.")
    
    imgs = {
        "O Executivo": "https://via.placeholder.com/300?text=Executivo",
        "A Humanitária": "https://via.placeholder.com/300?text=Humanitaria",
        "A Curadora": "https://via.placeholder.com/300?text=Curadora",
        "O Lutador": "https://via.placeholder.com/300?text=Lutador"
    }
    cols = st.columns(4)
    sel = st.multiselect("Escolha 2 Personagens:", list(imgs.keys()), max_selections=2)
    for i, (k,v) in enumerate(imgs.items()): cols[i].image(v, caption=k)

    if len(sel) == 2:
        if st.button("Confirmar Elenco"):
            st.session_state.personagens = sel
            st.session_state.step = 2
            st.rerun()

# TELA 2: CONTEXTO
elif st.session_state.step == 2:
    st.title("📍 Onde tudo começa")
    local = st.selectbox("Local:", ["Escritório Noturno", "Quarto de Hotel", "Masmorra", "Vestiário"])
    ctx = st.text_area("Contexto Inicial:", "Eles se odeiam, mas a tensão sexual é insuportável.")
    
    if st.button("Gerar Início"):
        with st.spinner("O MythoMax está escrevendo... (Isso pode ser picante)"):
            sys = "Você é um autor de literatura erótica. Escreva cenas com detalhes sensoriais, foco em toques, cheiros e psicologia. Sem censura."
            user = f"Escreva o início de um conto com {st.session_state.personagens} no {local}. Contexto: {ctx}."
            
            res = gerar_texto(sys, user)
            
            if "Erro" in res:
                st.error(res)
            else:
                st.session_state.historia += f"### O Início\n\n{res}\n\n"
                st.session_state.step = 3
                st.rerun()

# TELA 3: NARRATIVA
elif st.session_state.step == 3:
    st.markdown(st.session_state.historia)
    st.divider()
    
    c1, c2 = st.columns([1,2])
    vibe = c1.radio("Próxima Cena:", ["Romântico", "Hardcore/Sexo", "Dominação", "Oral"])
    acao = c2.text_area("O que acontece?", "Descreva a ação...")
    
    if st.button("Continuar"):
        with st.spinner("Escrevendo continuação..."):
            sys = "Continue a história erótica. Seja explícito se necessário."
            user = f"História anterior: {st.session_state.historia[-1000:]}. Ação: {acao}. Vibe: {vibe}."
            res = gerar_texto(sys, user)
            st.session_state.historia += f"#### {vibe}\n\n{res}\n\n"
            st.rerun()
            
    if st.button("Finalizar"):
        st.session_state.step = 4
        st.rerun()

# TELA 4: FINAL
elif st.session_state.step == 4:
    st.success("Conto Finalizado!")
    st.markdown(st.session_state.historia)
    if st.button("Reiniciar"): st.session_state.clear(); st.rerun()
