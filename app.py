import streamlit as st
import requests
from fpdf import FPDF

# ==========================================
# CONFIGURAÇÃO DE SEGURANÇA
# ==========================================
CHAVE_BRUTA = "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"
API_KEY = CHAVE_BRUTA.strip() 

st.set_page_config(page_title="Eroticizza Slow Burn", layout="wide")

# ==========================================
# MOTOR DA IA: Hermes 3 (Com Freio de Ritmo)
# ==========================================
def gerar_texto(prompt_sistema, prompt_usuario):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://eroticizza.streamlit.app",
        "X-Title": "Eroticizza",
        "Content-Type": "application/json"
    }
    
    # PROMPT DE RITMO (SLOW BURN)
    sistema_ritmado = (
        f"{prompt_sistema} "
        "REGRAS DE RITMO E ESTRUTURA (CRUCIAIS):"
        "1. PROIBIDO FINALIZAR: Esta é apenas a INTRODUÇÃO. NÃO descreva o clímax, orgasmo ou finalização do ato sexual agora."
        "2. TENSÃO (SLOW BURN): Foque no 'antes'. Descreva a aproximação, o cheiro, o medo, a primeira humilhação verbal, o primeiro toque."
        "3. CORTA A CENA: Termine o texto num momento de suspense (cliffhanger), esperando a próxima ação do usuário."
        "4. ESTILO HARDCORE: Mantenha a linguagem suja e anatômica (pau, cu, etc), mas guarde a ação principal para depois."
        "5. SEM PRESSA: Descreva o ambiente, a respiração e a psicologia dos personagens detalhadamente."
    )
    
    data = {
        "model": "nousresearch/hermes-3-llama-3.1-70b", 
        "messages": [
            {"role": "system", "content": sistema_ritmado},
            {"role": "user", "content": prompt_usuario}
        ],
        "temperature": 0.7, 
        "max_tokens": 1500, # Diminuí os tokens para ele não se empolgar e escrever um livro
        "repetition_penalty": 1.1
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Erro: {response.text}"
            
    except Exception as e:
        return f"Erro de conexão: {e}"

# ==========================================
# INTERFACE DO APP
# ==========================================

if 'step' not in st.session_state: st.session_state.step = 1
if 'historia' not in st.session_state: st.session_state.historia = ""
if 'personagens' not in st.session_state: st.session_state.personagens = []

# TELA 1
if st.session_state.step == 1:
    st.title("🔥 Eroticizza (Ritmo Controlado)")
    st.markdown("**Calibragem:** Hardcore, mas focado em construção de tensão (sem finalização rápida).")
    
    imgs = {
        "O Executivo": "https://via.placeholder.com/300?text=Executivo",
        "A Humanitária": "https://via.placeholder.com/300?text=Humanitaria",
        "A Curadora": "https://via.placeholder.com/300?text=Curadora",
        "O Lutador": "https://via.placeholder.com/300?text=Lutador"
    }
    cols = st.columns(4)
    sel = st.multiselect("Escolha 2 Protagonistas:", list(imgs.keys()), max_selections=2)
    for i, (k,v) in enumerate(imgs.items()): cols[i].image(v, caption=k)

    if len(sel) == 2:
        if st.button("Confirmar Elenco"):
            st.session_state.personagens = sel
            st.session_state.step = 2
            st.rerun()

# TELA 2
elif st.session_state.step == 2:
    st.title("📍 Contexto")
    local = st.selectbox("Local:", ["Escritório", "Vestiário", "Carro"])
    ctx = st.text_area("Cena:", "O Lutador encurrala o Executivo. Ele quer cobrar a dívida. O Executivo sente medo.")
    
    if st.button("Gerar Tensão Inicial"):
        with st.spinner("Criando suspense..."):
            sys = "Você é um escritor de erotismo focado em 'Slow Burn' (queima lenta)."
            # Instrução explícita para parar antes do ato
            user = f"Escreva SOMENTE O INÍCIO da cena com {st.session_state.personagens} no {local}. Contexto: {ctx}. Pare antes do ato sexual começar de verdade. Crie tensão."
            
            res = gerar_texto(sys, user)
            st.session_state.historia += f"### Cena 1: A Abordagem\n\n{res}\n\n"
            st.session_state.step = 3
            st.rerun()

# TELA 3
elif st.session_state.step == 3:
    st.markdown(st.session_state.historia)
    st.divider()
    
    c1, c2 = st.columns([1,2])
    vibe = c1.radio("Agora sim, o que acontece?:", ["O Lutador tira a roupa", "O Executivo implora", "Primeiro toque agressivo"])
    acao = c2.text_area("Descreva a ação:", "Ele obriga o executivo a se ajoelhar...")
    
    if st.button("Avançar Cena"):
        with st.spinner("Escrevendo..."):
            sys = "Continue a cena. Aumente a intensidade, mas mantenha o realismo."
            user = f"História anterior: {st.session_state.historia[-1000:]}. Ação: {acao}. Vibe: {vibe}."
            res = gerar_texto(sys, user)
            st.session_state.historia += f"#### Cena 2\n\n{res}\n\n"
            st.rerun()

    if st.button("Finalizar"):
        st.session_state.step = 4
        st.rerun()

# TELA 4
elif st.session_state.step == 4:
    st.success("Fim!")
    st.markdown(st.session_state.historia)
    # (Código do PDF igual ao anterior...)
    def create_pdf(text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        try: txt = text.encode('latin-1', 'replace').decode('latin-1')
        except: txt = text
        pdf.multi_cell(0, 10, txt)
        return pdf.output(dest="S").encode("latin-1")
    st.download_button("Baixar PDF", create_pdf(st.session_state.historia), "conto.pdf")
    if st.button("Reiniciar"): st.session_state.clear(); st.rerun()
