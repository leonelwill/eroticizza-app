import streamlit as st
from openai import OpenAI
from fpdf import FPDF

# ==========================================
# CONFIGURAÇÃO (VOLTANDO PARA OPENROUTER)
# ==========================================
# Cole sua chave do OPENROUTER aqui (sk-or-v1...)
MINHA_CHAVE = "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"

# Configuração da Página
st.set_page_config(page_title="Eroticizza", layout="wide")

# Função de Geração
def gerar_texto(prompt_sistema, prompt_usuario):
    try:
        # Apontando para o OpenRouter
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=MINHA_CHAVE,
        )
        
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://seu-app.com", 
                "X-Title": "Eroticizza",
            },
            # O MODELO MÁGICO: MythoMax (Especialista em Roleplay/Sem Censura)
            model="gryphe/mythomax-l2-13b", 
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario},
            ],
            temperature=0.8, # Criatividade alta para evitar texto robótico
            max_tokens=2000,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"ERRO NA IA: {e}"

# ==========================================
# LÓGICA DO APP (Igual ao anterior)
# ==========================================

if 'step' not in st.session_state: st.session_state.step = 1
if 'historia_completa' not in st.session_state: st.session_state.historia_completa = ""
if 'personagens' not in st.session_state: st.session_state.personagens = []
if 'cenario' not in st.session_state: st.session_state.cenario = ""

# TELA 1
if st.session_state.step == 1:
    st.title("🔥 Eroticizza (Mode: MythoMax)")
    st.write("Selecione o Elenco.")
    
    imgs = {
        "Executivo": "https://via.placeholder.com/300?text=Executivo",
        "Humanitária": "https://via.placeholder.com/300?text=Humanitaria",
        "Lutador": "https://via.placeholder.com/300?text=Lutador",
        "Curadora": "https://via.placeholder.com/300?text=Curadora"
    }
    cols = st.columns(4)
    sel = st.multiselect("Escolha 2:", list(imgs.keys()), max_selections=2)
    for i, (k,v) in enumerate(imgs.items()): cols[i].image(v, caption=k)

    if len(sel) == 2:
        if st.button("Confirmar"):
            st.session_state.personagens = sel
            st.session_state.step = 2
            st.rerun()

# TELA 2
elif st.session_state.step == 2:
    st.title("📍 Contexto")
    st.session_state.cenario = st.selectbox("Local:", ["Escritório", "Hotel", "Masmorra"])
    ctx = st.text_area("Situação:", "Tensão alta, dominação.")
    
    if st.button("Iniciar"):
        with st.spinner("Escrevendo..."):
            sys = "Você é um autor de literatura erótica sofisticada em Português. Foco em sensações, psicologia e detalhes físicos. Não há censura."
            user = f"Escreva o início com {st.session_state.personagens} no {st.session_state.cenario}. Contexto: {ctx}."
            res = gerar_texto(sys, user)
            st.session_state.historia_completa += f"### Início\n\n{res}\n\n"
            st.session_state.step = 3
            st.rerun()

# TELA 3
elif st.session_state.step == 3:
    st.title("📖 História")
    st.markdown(st.session_state.historia_completa)
    st.divider()
    
    c1, c2 = st.columns([1,2])
    vibe = c1.radio("Vibe:", ["Romântico", "Hardcore", "BDSM", "Oral"])
    acao = c2.text_area("Ação:", "Descreva o que acontece...")
    
    if st.button("Continuar"):
        with st.spinner("Escrevendo..."):
            sys = "Continue a história erótica. Seja detalhista e intenso."
            user = f"História anterior: {st.session_state.historia_completa[-600:]}. Ação: {acao}. Vibe: {vibe}."
            res = gerar_texto(sys, user)
            st.session_state.historia_completa += f"#### {vibe}\n\n{res}\n\n"
            st.rerun()

    if st.button("Finalizar"):
        st.session_state.step = 4
        st.rerun()

# TELA 4
elif st.session_state.step == 4:
    st.success("Fim!")
    st.markdown(st.session_state.historia_completa)
    def create_pdf(text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        try: txt = text.encode('latin-1', 'replace').decode('latin-1')
        except: txt = text
        pdf.multi_cell(0, 10, txt)
        return pdf.output(dest="S").encode("latin-1")
    st.download_button("Baixar PDF", create_pdf(st.session_state.historia_completa), "conto.pdf")
    if st.button("Reiniciar"):
        st.session_state.clear(); st.rerun()
