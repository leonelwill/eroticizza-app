import streamlit as st
import requests
from fpdf import FPDF

# Configuração da Página
st.set_page_config(page_title="Eroticizza Pro", layout="wide")

# ==========================================
# BARRA LATERAL (Login)
# ==========================================
st.sidebar.title("🔐 Login")
st.sidebar.markdown("Cole sua chave OpenRouter abaixo.")

# Campo de senha
api_key = st.sidebar.text_input("Chave (sk-or-v1...):", type="password")

if api_key:
    st.sidebar.success("Chave inserida!")
else:
    st.sidebar.warning("Cole a chave para usar.")

# ==========================================
# CÉREBRO DA IA (Euryale 70B - O Sucessor do Midnight Rose)
# ==========================================
def gerar_texto(prompt_sistema, prompt_usuario, chave):
    if not chave:
        return "⚠️ ERRO: Cole a chave na barra lateral esquerda!"

    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {chave}",
        "HTTP-Referer": "https://eroticizza.streamlit.app",
        "X-Title": "Eroticizza",
        "Content-Type": "application/json"
    }
    
    # Prompt Blindado para Português
    sistema_refinado = (
        f"{prompt_sistema} "
        "DIRETRIZES DE QUALIDADE:"
        "1. IDIOMA: Escreva EXCLUSIVAMENTE em Português do Brasil natural."
        "2. VOCABULÁRIO: Não use palavras estrangeiras (nada de 'leggermente', 'softly', etc)."
        "3. LÓGICA: Mantenha a coerência física da cena."
        "4. CENSURA: Zero. Descreva com realismo."
    )
    
    data = {
        # ESTE É O MODELO QUE FUNCIONA HOJE E CORRIGE O PORTUGUÊS
        "model": "sao10k/l3-euryale-70b", 
        "messages": [
            {"role": "system", "content": sistema_refinado},
            {"role": "user", "content": prompt_usuario}
        ],
        "temperature": 0.7, 
        "max_tokens": 2500
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Erro OpenRouter ({response.status_code}): {response.text}"
            
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
    st.title("🔥 Eroticizza (Euryale Edition)")
    st.markdown("Motor atual: **Euryale 70B** (Melhor coerência em PT-BR).")
    
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
    local = st.selectbox("Local:", ["Escritório", "Hotel", "Vestiário", "Carro"])
    ctx = st.text_area("Situação:", "Ex: Tensão sexual reprimida...")
    
    if st.button("Iniciar História"):
        if not api_key:
            st.error("Cole a chave na lateral!")
        else:
            with st.spinner("Escrevendo... (Alta qualidade demora um pouco)"):
                sys = "Você é um autor de literatura adulta sofisticada."
                user = f"Escreva o início de um conto com {st.session_state.personagens} no {local}. Contexto: {ctx}."
                res = gerar_texto(sys, user, api_key)
                st.session_state.historia += f"### O Início\n\n{res}\n\n"
                st.session_state.step = 3
                st.rerun()

# TELA 3
elif st.session_state.step == 3:
    st.markdown(st.session_state.historia)
    st.divider()
    c1, c2 = st.columns([1,2])
    vibe = c1.radio("Vibe:", ["Romance", "Ação Física", "Diálogo"])
    acao = c2.text_area("Ação:", "O que acontece agora?")
    
    if st.button("Continuar"):
        with st.spinner("Escrevendo..."):
            sys = "Continue a narrativa."
            user = f"História: {st.session_state.historia[-1500:]}. Ação: {acao}. Vibe: {vibe}."
            res = gerar_texto(sys, user, api_key)
            st.session_state.historia += f"#### {vibe}\n\n{res}\n\n"
            st.rerun()

    if st.button("Finalizar"):
        st.session_state.step = 4
        st.rerun()

# TELA 4
elif st.session_state.step == 4:
    st.success("Fim!")
    st.markdown(st.session_state.historia)
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
