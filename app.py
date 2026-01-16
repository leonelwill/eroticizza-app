import streamlit as st
from openai import OpenAI
from fpdf import FPDF
import os
from dotenv import load_dotenv

# Carrega a chave do arquivo .env
load_dotenv()

# Configuração da Página
st.set_page_config(page_title="Eroticizza", layout="wide")

# --- CONFIGURAÇÃO DA IA (OpenRouter) ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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", # Cole sua chave real aqui dentro das aspas
)

def gerar_texto(prompt_sistema, prompt_usuario):
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://seu-site.com", # Pode ser qualquer coisa
                "X-Title": "Eroticizza App",
            },
            model="nousresearch/nous-hermes-2-mixtral-8x7b-dpo", # Modelo excelente e sem filtro
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario},
            ],
            temperature=0.8, # Criatividade alta
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Erro na IA: {e}"
      # --- INICIALIZAÇÃO DE ESTADO (Memória) ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'historia_completa' not in st.session_state:
    st.session_state.historia_completa = ""
if 'personagens' not in st.session_state:
    st.session_state.personagens = []
if 'cenario' not in st.session_state:
    st.session_state.cenario = ""

# --- PASSO 1: ESCOLHA DOS PERSONAGENS ---
if st.session_state.step == 1:
    st.title("🔥 Escolha o Elenco")
    st.write("Selecione os dois protagonistas da sua fantasia.")
    
    # Simulação de imagens (substitua pelos caminhos reais das suas pastas ex: "assets/chars/foto1.png")
    # Para testar agora, vou usar placeholders
    imgs_chars = {
        "O Executivo": "https://via.placeholder.com/150/000000/FFFFFF?text=Executivo",
        "A Humanitária": "https://via.placeholder.com/150/FF0000/FFFFFF?text=Humanitaria",
        "A Curadora": "https://via.placeholder.com/150/0000FF/FFFFFF?text=Curadora",
        "O Lutador": "https://via.placeholder.com/150/008000/FFFFFF?text=Lutador"
    }
    
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    
    selected = st.multiselect("Selecione 2 nomes:", list(imgs_chars.keys()), max_selections=2)
    
    # Mostra as imagens para ajudar a escolher
    for i, (nome, url) in enumerate(imgs_chars.items()):
        with cols[i]:
            st.image(url, caption=nome)

    if len(selected) == 2:
        if st.button("Confirmar Elenco"):
            st.session_state.personagens = selected
            st.session_state.step = 2
            st.rerun()

# --- PASSO 2: CENÁRIO E CONTEXTO INICIAL ---
elif st.session_state.step == 2:
    st.title("📍 Onde tudo começa?")
    
    cenarios = ["Escritório Noturno", "Quarto de Hotel", "Clube Subterrâneo"]
    st.session_state.cenario = st.selectbox("Escolha o local:", cenarios)
    
    st.subheader("O Gatilho Inicial")
    contexto_inicial = st.text_area("Como eles se encontram? Qual o clima? (Seja criativo)", 
                                    "Eles se odeiam mas são obrigados a trabalhar juntos. A tensão é alta.")
    
    if st.button("Começar a História"):
        # Gera o primeiro parágrafo
        with st.spinner("A IA está imaginando a cena..."):
            sistema = "Você é um autor de contos eróticos sofisticados e intensos. Escreva em Português."
            prompt = f"Inicie uma história com {st.session_state.personagens[0]} e {st.session_state.personagens[1]} no {st.session_state.cenario}. Contexto: {contexto_inicial}. Escreva cerca de 2 parágrafos introdutórios estabelecendo a tensão."
            
            texto_gerado = gerar_texto(sistema, prompt)
            st.session_state.historia_completa += f"### O Início\n\n{texto_gerado}\n\n"
            st.session_state.step = 3
            st.rerun()

# --- PASSO 3: O LOOP DA AÇÃO (Aqui entra sua ideia da cocriação) ---
elif st.session_state.step == 3:
    st.title("📖 A Narrativa")
    
    # Mostra o texto atual
    st.markdown(st.session_state.historia_completa)
    st.markdown("---")
    
    st.subheader("O que acontece agora?")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("**Escolha a Vibe Visual (Silhueta):**")
        # Aqui você colocaria suas imagens de "assets/shadows/"
        vibe = st.radio("Selecione a imagem mental:", ["Beijo Agressivo", "Toque Suave", "Dominação/Ajoelhar", "Cama/Missionário"])
    
    with col2:
        st.write("**Dê a Direção (Cocriação):**")
        input_usuario = st.text_area("Descreva o que eles fazem (Pode ser explícito):", 
                                     placeholder="Ex: Ela empurra ele na cama e toma o controle...")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Gerar Próxima Cena"):
            with st.spinner("Escrevendo..."):
                sistema = f"Continue a história erótica. Mantenha o tom intenso. Personagens: {st.session_state.personagens}."
                prompt = f"História até agora: {st.session_state.historia_completa[-500:]}. \n\nO usuário quer que a próxima cena tenha a vibe visual de '{vibe}' e aconteça o seguinte: '{input_usuario}'. Descreva as sensações, o toque e a ação com detalhes."
                
                novo_texto = gerar_texto(sistema, prompt)
                st.session_state.historia_completa += f"#### Cena: {vibe}\n\n{novo_texto}\n\n"
                st.rerun()
                
    with c2:
        if st.button("Finalizar e Baixar PDF"):
            st.session_state.step = 4
            st.rerun()

# --- PASSO 4: EXPORTAÇÃO (PDF) ---
elif st.session_state.step == 4:
    st.title("💾 Seu Conto Está Pronto")
    st.success("História finalizada!")
    
    # Mostra o texto final
    with st.expander("Ler História Completa"):
        st.markdown(st.session_state.historia_completa)
    
    # Função simples de PDF
    def create_pdf(text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        # O FPDF tem problemas com caracteres especiais (acentos), 
        # num app real usaríamos uma fonte TTF que suporte utf-8 ou limparíamos o texto.
        # Aqui vamos fazer um encode simples para não quebrar o exemplo.
        clean_text = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, clean_text)
        return pdf.output(dest="S").encode("latin-1")

    if st.download_button(
        label="Baixar PDF do Conto",
        data=create_pdf(st.session_state.historia_completa),
        file_name="meu_conto_erotico.pdf",
        mime="application/pdf"
    ):
        st.balloons()
        
    if st.button("Criar Nova História"):
        st.session_state.clear()
        st.rerun()
