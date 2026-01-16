import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# ==========================================
# COLE SUA CHAVE DO GOOGLE AQUI (AIza...)
# ==========================================
MINHA_CHAVE_GOOGLE = "AIzaSyBuxA433U7YWXQ5baurlLbzj8QFQzSa2v4" 

# Configuração da Página
st.set_page_config(page_title="Eroticizza", layout="wide")

# Configuração da IA (Google Gemini)
try:
    genai.configure(api_key=MINHA_CHAVE_GOOGLE)
    
    # CONFIGURAÇÃO DE SEGURANÇA (Tentando liberar o conteúdo)
    # Estamos dizendo para o filtro: "Bloqueie NADA ou SÓ O EXTREMO"
    safety_settings = [
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_ONLY_HIGH" 
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
    ]
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        safety_settings=safety_settings
    )
except Exception as e:
    st.error(f"Erro na configuração da chave: {e}")

# Função de Geração
def gerar_texto(prompt_usuario):
    try:
        # O prompt do sistema vai junto com o usuário no Gemini
        prompt_completo = f"Você é um escritor de contos adultos (ficção). Escreva de forma criativa e detalhada. {prompt_usuario}"
        
        response = model.generate_content(prompt_completo)
        return response.text
    except Exception as e:
        # Se o Gemini bloquear, ele joga um erro específico
        return f"⚠️ O Gemini bloqueou este trecho por segurança ou deu erro. Tente suavizar o pedido. Erro: {e}"

# ==========================================
# LÓGICA DO APP
# ==========================================

if 'step' not in st.session_state: st.session_state.step = 1
if 'historia_completa' not in st.session_state: st.session_state.historia_completa = ""
if 'personagens' not in st.session_state: st.session_state.personagens = []
if 'cenario' not in st.session_state: st.session_state.cenario = ""

# --- TELA 1 ---
if st.session_state.step == 1:
    st.title("🔥 Eroticizza (Powered by Google Gemini)")
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

# --- TELA 2 ---
elif st.session_state.step == 2:
    st.title("📍 Contexto")
    st.session_state.cenario = st.selectbox("Local:", ["Escritório", "Hotel", "Masmorra"])
    ctx = st.text_area("Situação:", "Eles estão sozinhos e a atração é forte.")
    
    if st.button("Iniciar"):
        with st.spinner("O Gemini está escrevendo..."):
            prompt = f"Escreva o início de um conto erótico/romântico com {st.session_state.personagens} no {st.session_state.cenario}. Contexto: {ctx}."
            res = gerar_texto(prompt)
            st.session_state.historia_completa += f"### Início\n\n{res}\n\n"
            st.session_state.step = 3
            st.rerun()

# --- TELA 3 ---
elif st.session_state.step == 3:
    st.title("📖 História")
    st.markdown(st.session_state.historia_completa)
    st.divider()
    
    c1, c2 = st.columns([1,2])
    vibe = c1.radio("Vibe:", ["Romance Intenso", "Toque Físico", "Dominação Leve", "Sedução"])
    acao = c2.text_area("Ação:", "Descreva o que acontece...")
    
    if st.button("Continuar"):
        with st.spinner("Escrevendo..."):
            prompt = f"História anterior: {st.session_state.historia_completa[-1000:]}. \n\nAção desejada: {acao}. Vibe: {vibe}. Continue a narrativa com detalhes."
            res = gerar_texto(prompt)
            st.session_state.historia_completa += f"#### {vibe}\n\n{res}\n\n"
            st.rerun()

    if st.button("Finalizar"):
        st.session_state.step = 4
        st.rerun()

# --- TELA 4 ---
elif st.session_state.step == 4:
    st.success("Pronto!")
    
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
