import streamlit as st
import requests
import json
from fpdf import FPDF

# ==========================================
# CONFIGURAÇÃO GERAL
# ==========================================

# SUA CHAVE (Recuperada do chat anterior)
API_KEY = "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"

# Configuração da Página do Streamlit
st.set_page_config(page_title="Eroticizza", layout="wide")

# ==========================================
# CÉREBRO DA IA (Conexão Manual)
# ==========================================
def gerar_texto(prompt_sistema, prompt_usuario):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://eroticizza.streamlit.app",
        "X-Title": "Eroticizza",
        "Content-Type": "application/json"
    }
    
    # Prompt do Sistema Reforçado (Anti-Portunhol e Anti-Alucinação)
    sistema_blindado = (
        f"{prompt_sistema} "
        "DIRETRIZES RÍGIDAS: "
        "1. Escreva EXCLUSIVAMENTE em Português do Brasil natural e fluente. "
        "2. Não use palavras em italiano, espanhol ou inglês soltas no texto. "
        "3. Mantenha consistência lógica (não invente objetos que não cabem no cenário). "
        "4. Use um vocabulário rico, sensual e literário."
    )
    
    data = {
        # O MODELO "FERRARI" (Midnight Rose 70B - Alta Qualidade)
        "model": "sophosympatheia/midnight-rose-70b", 
        "messages": [
            {"role": "system", "content": sistema_blindado},
            {"role": "user", "content": prompt_usuario}
        ],
        # Temperatura 0.78 = Criativo mas focado (evita delírios)
        "temperature": 0.78, 
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            # Captura o erro detalhado se houver
            erro = response.json()
            msg_erro = erro.get('error', {}).get('message', 'Erro desconhecido')
            return f"Erro OpenRouter ({response.status_code}): {msg_erro}"
            
    except Exception as e:
        return f"Erro de conexão grave: {e}"

# ==========================================
# INTERFACE DO APP (Frontend)
# ==========================================

# Inicialização de Variáveis (Memória)
if 'step' not in st.session_state: st.session_state.step = 1
if 'historia' not in st.session_state: st.session_state.historia = ""
if 'personagens' not in st.session_state: st.session_state.personagens = []

# --- TELA 1: ELENCO ---
if st.session_state.step == 1:
    st.title("🔥 Eroticizza Premium")
    st.markdown("*Motor: Midnight Rose 70B (Alta Literatura)*")
    
    # Placeholders de Imagens
    imgs = {
        "O Executivo": "https://via.placeholder.com/300?text=Executivo",
        "A Humanitária": "https://via.placeholder.com/300?text=Humanitaria",
        "A Curadora": "https://via.placeholder.com/300?text=Curadora",
        "O Lutador": "https://via.placeholder.com/300?text=Lutador"
    }
    
    cols = st.columns(4)
    sel = st.multiselect("Selecione 2 Protagonistas:", list(imgs.keys()), max_selections=2)
    
    for i, (k,v) in enumerate(imgs.items()):
        cols[i].image(v, caption=k)

    if len(sel) == 2:
        if st.button("Confirmar Elenco"):
            st.session_state.personagens = sel
            st.session_state.step = 2
            st.rerun()

# --- TELA 2: CONTEXTO ---
elif st.session_state.step == 2:
    st.title("📍 O Cenário")
    
    local = st.selectbox("Onde eles estão?", ["Escritório do CEO", "Quarto de Hotel de Luxo", "Vestiário da Academia", "Masmorra Privada"])
    ctx = st.text_area("Contexto e Tensão:", "Eles são rivais nos negócios, mas ficaram presos juntos no elevador...")
    
    if st.button("Gerar Início da História"):
        with st.spinner("A IA está escrevendo... (Isso pode levar uns 10-15 segundos, o modelo é potente)"):
            sys = "Você é um autor premiado de literatura erótica."
            user = f"Escreva o início de um conto com {st.session_state.personagens} no local '{local}'. Contexto: {ctx}. Descreva o ambiente e a tensão inicial."
            
            res = gerar_texto(sys, user)
            
            if "Erro OpenRouter" in res:
                st.error(res)
            else:
                st.session_state.historia += f"### O Início\n\n{res}\n\n"
                st.session_state.step = 3
                st.rerun()

# --- TELA 3: NARRATIVA INTERATIVA ---
elif st.session_state.step == 3:
    st.markdown(st.session_state.historia)
    st.divider()
    
    c1, c2 = st.columns([1,2])
    vibe = c1.radio("Direção da Cena:", ["Romance Intenso", "Sexo Explícito", "Dominação/Poder", "Preliminares"])
    acao = c2.text_area("O que eles fazem agora?", "Ele toma a iniciativa...")
    
    if st.button("Escrever Continuação"):
        with st.spinner("Continuando a história..."):
            sys = "Continue a narrativa mantendo o estilo literário e sensual."
            user = f"História até agora: {st.session_state.historia[-1500:]}. \n\nAÇÃO DO USUÁRIO: {acao}. \nVIBE DESEJADA: {vibe}."
            
            res = gerar_texto(sys, user)
            st.session_state.historia += f"#### {vibe}\n\n{res}\n\n"
            st.rerun()
            
    if st.button("Finalizar Conto"):
        st.session_state.step = 4
        st.rerun()

# --- TELA 4: EXPORTAR ---
elif st.session_state.step == 4:
    st.success("História Finalizada!")
    st.markdown(st.session_state.historia)
    
    def create_pdf(text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        try: txt = text.encode('latin-1', 'replace').decode('latin-1')
        except: txt = text
        pdf.multi_cell(0, 10, txt)
        return pdf.output(dest="S").encode("latin-1")

    st.download_button("Baixar PDF", create_pdf(st.session_state.historia), "conto_erotico.pdf")
    
    if st.button("Criar Nova História"):
        st.session_state.clear()
        st.rerun()
