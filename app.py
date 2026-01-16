import streamlit as st
from openai import OpenAI
from fpdf import FPDF

# --- ÁREA DE CONFIGURAÇÃO (MEXA AQUI) ---

# COLE SUA CHAVE NOVA DENTRO DAS ASPAS ABAIXO
# Cuidado para não deixar espaços em branco antes ou depois da chave!
MINHA_CHAVE_OPENROUTER = "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"

# --- FIM DA ÁREA DE CONFIGURAÇÃO ---

# Configuração da Página
st.set_page_config(page_title="Eroticizza", layout="wide")

# Configuração do Cliente de IA
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=MINHA_CHAVE_OPENROUTER,
)

# Função para chamar a IA
# Função para chamar a IA
def gerar_texto(prompt_sistema, prompt_usuario):
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://localhost:8501", 
                "X-Title": "Eroticizza App",
            },
            # Trocamos para o Llama 3 Free que costuma estar sempre online
            model="meta-llama/llama-3-8b-instruct:free", 
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario},
            ],
            temperature=0.8,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"ERRO CRÍTICO NA IA: {e}"
        
# --- INICIALIZAÇÃO DE MEMÓRIA ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'historia_completa' not in st.session_state:
    st.session_state.historia_completa = ""
if 'personagens' not in st.session_state:
    st.session_state.personagens = []
if 'cenario' not in st.session_state:
    st.session_state.cenario = ""

# --- PASSO 1: ESCOLHA DO ELENCO ---
if st.session_state.step == 1:
    st.title("🔥 Eroticizza: Monte sua Cena")
    st.write("Escolha os protagonistas da sua história.")
    
    # Imagens temporárias (Placeholders)
    imgs_chars = {
        "O Executivo Dominador": "https://via.placeholder.com/300x300/000000/FFFFFF?text=Executivo",
        "A Humanitária Intensa": "https://via.placeholder.com/300x300/FF0000/FFFFFF?text=Humanitaria",
        "A Curadora Elegante": "https://via.placeholder.com/300x300/0000FF/FFFFFF?text=Curadora",
        "O Lutador Bruto": "https://via.placeholder.com/300x300/008000/FFFFFF?text=Lutador"
    }
    
    col1, col2, col3, col4 = st.columns(4)
    cols = [col1, col2, col3, col4]
    
    selected = st.multiselect("Selecione EXATAMENTE 2 personagens:", list(imgs_chars.keys()), max_selections=2)
    
    for i, (nome, url) in enumerate(imgs_chars.items()):
        with cols[i]:
            st.image(url, caption=nome, use_container_width=True)

    if len(selected) == 2:
        if st.button("Confirmar Elenco e Avançar"):
            st.session_state.personagens = selected
            st.session_state.step = 2
            st.rerun()

# --- PASSO 2: CENÁRIO E INÍCIO ---
elif st.session_state.step == 2:
    st.title("📍 Onde eles estão?")
    
    cenarios = ["Escritório Noturno (Manila)", "Quarto de Hotel (Lagos)", "Vestiário de Boxe", "Galeria de Arte"]
    st.session_state.cenario = st.selectbox("Escolha o local:", cenarios)
    
    st.divider()
    st.subheader("O Gatilho da História")
    contexto_inicial = st.text_area("Descreva o clima inicial (Ex: Eles se odeiam, ou é um reencontro proibido...)", 
                                    "Eles estão sozinhos pela primeira vez em meses. A tensão sexual é alta.")
    
    if st.button("Gerar Início da História"):
        with st.spinner("A IA está escrevendo... (Isso pode levar uns 10 segundos)"):
            sistema = "Você é um escritor de contos adultos criativos. Escreva em Português do Brasil."
            prompt = f"Crie o início de um conto erótico com {st.session_state.personagens[0]} e {st.session_state.personagens[1]} no {st.session_state.cenario}. Contexto: {contexto_inicial}. Escreva 2 parágrafos envolventes."
            
            texto_gerado = gerar_texto(sistema, prompt)
            
            # Verifica se deu erro antes de continuar
            if "ERRO CRÍTICO" in texto_gerado:
                st.error(texto_gerado)
            else:
                st.session_state.historia_completa += f"### O Início\n\n{texto_gerado}\n\n"
                st.session_state.step = 3
                st.rerun()

# --- PASSO 3: NARRATIVA INTERATIVA ---
elif st.session_state.step == 3:
    st.title("📖 A História em Andamento")
    
    st.markdown(st.session_state.historia_completa)
    st.markdown("---")
    
    st.subheader("Você é o Diretor: O que acontece agora?")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.info("Escolha a Vibe Visual")
        vibe = st.radio("Foco da cena:", ["Beijo Intenso", "Toque/Mãos", "Dominação", "Sexo Oral", "Penetração"])
    
    with col2:
        st.info("Dê a direção para a IA")
        input_usuario = st.text_area("O que eles devem fazer? (Seja criativo/explícito)", 
                                     placeholder="Ex: Ela empurra ele na parede e assume o controle...")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Gerar Próxima Cena"):
            with st.spinner("Escrevendo continuação..."):
                sistema = "Continue a história com foco em sensações físicas e emoções."
                prompt = f"História anterior: {st.session_state.historia_completa[-600:]}. \n\nAção desejada pelo usuário: '{input_usuario}'. Vibe visual: '{vibe}'. Escreva mais 2 parágrafos."
                
                novo_texto = gerar_texto(sistema, prompt)
                st.session_state.historia_completa += f"#### Cena: {vibe}\n\n{novo_texto}\n\n"
                st.rerun()
                
    with c2:
        if st.button("Finalizar História"):
            st.session_state.step = 4
            st.rerun()

# --- PASSO 4: PDF ---
elif st.session_state.step == 4:
    st.title("💾 Conto Finalizado")
    st.success("Sua história está pronta!")
    
    with st.expander("Ler Texto Completo"):
        st.markdown(st.session_state.historia_completa)
    
    # Gerador de PDF Simples
    def create_pdf(text):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        # Tratamento básico para acentos (latin-1)
        try:
            clean_text = text.encode('latin-1', 'replace').decode('latin-1')
        except:
            clean_text = text
        pdf.multi_cell(0, 10, clean_text)
        return pdf.output(dest="S").encode("latin-1")

    st.download_button(
        label="Baixar PDF",
        data=create_pdf(st.session_state.historia_completa),
        file_name="conto_eroticizza.pdf",
        mime="application/pdf"
    )
    
    if st.button("Criar Nova História"):
        st.session_state.clear()
        st.rerun()
