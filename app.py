import streamlit as st
import os
from groq import Groq
from fpdf import FPDF

# ==========================================
# CONFIGURAÇÃO DA CHAVE (COLE AQUI)
# ==========================================
MINHA_CHAVE_GROQ = "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" 
# Exemplo: "gsk_8A7s9d8a7s9d8a7s..." (Mantenha as aspas!)

# Configuração da Página
st.set_page_config(page_title="Eroticizza", layout="wide")

# Função de Geração de Texto
def gerar_texto(prompt_sistema, prompt_usuario):
    try:
        # Inicializa o cliente Groq
        client = Groq(api_key=MINHA_CHAVE_GROQ)
        
        chat_completion = client.chat.completions.create(
            # Modelo Mixtral (Excelente, rápido e criativo)
            model="model="llama3-70b-8192", 
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario},
            ],
            temperature=0.7, # Criatividade equilibrada
            max_tokens=2000, # Permite textos longos
        )
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        # Mostra o erro na tela para a gente saber o que foi
        return f"ERRO NA IA: {e}"

# ==========================================
# LÓGICA DO APP
# ==========================================

# Memória da Sessão
if 'step' not in st.session_state: st.session_state.step = 1
if 'historia_completa' not in st.session_state: st.session_state.historia_completa = ""
if 'personagens' not in st.session_state: st.session_state.personagens = []
if 'cenario' not in st.session_state: st.session_state.cenario = ""

# --- TELA 1: ELENCO ---
if st.session_state.step == 1:
    st.title("🔥 Eroticizza (Motor Groq)")
    st.write("Selecione os protagonistas.")
    
    # Placeholders de imagens (Substitua pelos seus links depois)
    imgs = {
        "O Executivo": "https://via.placeholder.com/300?text=Executivo",
        "A Humanitária": "https://via.placeholder.com/300?text=Humanitaria",
        "A Curadora": "https://via.placeholder.com/300?text=Curadora",
        "O Lutador": "https://via.placeholder.com/300?text=Lutador"
    }
    
    cols = st.columns(4)
    sel = st.multiselect("Escolha 2:", list(imgs.keys()), max_selections=2)
    
    for i, (k, v) in enumerate(imgs.items()):
        cols[i].image(v, caption=k)

    if len(sel) == 2:
        if st.button("Confirmar Elenco"):
            st.session_state.personagens = sel
            st.session_state.step = 2
            st.rerun()

# --- TELA 2: CONTEXTO ---
elif st.session_state.step == 2:
    st.title("📍 Onde e Como?")
    
    st.session_state.cenario = st.selectbox("Local:", ["Escritório", "Quarto de Hotel", "Clube", "Natureza"])
    contexto = st.text_area("Situação Inicial:", "Tensão sexual acumulada. Eles estão sozinhos.")
    
    if st.button("Iniciar História"):
        with st.spinner("A Groq está escrevendo..."):
            sys = "Você é um escritor de contos eróticos em Português do Brasil. Escreva com detalhes sensoriais."
            user = f"Escreva o início de um conto com {st.session_state.personagens} no {st.session_state.cenario}. Contexto: {contexto}."
            
            res = gerar_texto(sys, user)
            
            if "ERRO" in res:
                st.error(res) # Mostra o erro vermelho se falhar
            else:
                st.session_state.historia_completa += f"### Início\n\n{res}\n\n"
                st.session_state.step = 3
                st.rerun()

# --- TELA 3: NARRATIVA ---
elif st.session_state.step == 3:
    st.title("📖 A História")
    st.markdown(st.session_state.historia_completa)
    st.divider()
    
    c1, c2 = st.columns([1,2])
    vibe = c1.radio("Vibe da Próxima Cena:", ["Beijo", "Toque", "Dominação", "Sexo"])
    acao = c2.text_area("O que acontece agora?", placeholder="Ex: Ela toma a iniciativa...")
    
    if st.button("Gerar Continuação"):
        with st.spinner("Escrevendo..."):
            sys = "Continue o conto erótico. Mantenha o tom intenso."
            user = f"História anterior: {st.session_state.historia_completa[-500:]}. Ação do usuário: {acao}. Vibe: {vibe}."
            
            res = gerar_texto(sys, user)
            st.session_state.historia_completa += f"#### {vibe}\n\n{res}\n\n"
            st.rerun()
            
    if st.button("Finalizar"):
        st.session_state.step = 4
        st.rerun()

# --- TELA 4: PDF ---
elif st.session_state.step == 4:
    st.success("História Pronta!")
    st.markdown(st.session_state.historia_completa)
    
    def create_pdf(text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        # Tratamento simples de caracteres
        try: txt = text.encode('latin-1', 'replace').decode('latin-1')
        except: txt = text
        pdf.multi_cell(0, 10, txt)
        return pdf.output(dest="S").encode("latin-1")

    st.download_button("Baixar PDF", create_pdf(st.session_state.historia_completa), "conto.pdf")
    
    if st.button("Reiniciar"):
        st.session_state.clear()
        st.rerun()
