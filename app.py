import streamlit as st
import requests
from fpdf import FPDF

# ==========================================
# CONFIGURAÇÃO (Sua Chave)
# ==========================================
CHAVE_BRUTA = "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"
API_KEY = CHAVE_BRUTA.strip() 

# Configuração da Página
st.set_page_config(page_title="Eroticizza Pro", layout="wide")

# ==========================================
# MOTOR DA IA (WizardLM-2 8x22B - O Inteligente)
# ==========================================
def gerar_texto(prompt_sistema, prompt_usuario):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://eroticizza.streamlit.app",
        "X-Title": "Eroticizza",
        "Content-Type": "application/json"
    }
    
    # Prompt de Sistema (Refinado para Lógica e Coerência)
    sistema_refinado = (
        f"{prompt_sistema} "
        "INSTRUÇÕES DE LÓGICA E NARRATIVA:"
        "1. Mantenha a COERÊNCIA absoluta. Não faça personagens agirem de forma ilógica (ex: pegar preservativo sozinho sem motivo)."
        "2. Foco na interação ENTRE os personagens presentes. Não invente terceiros (secretárias, mulheres indefesas) se eles não estão na cena."
        "3. Se a cena é entre dois homens, foque na tensão entre eles. Não crie plots moralistas de 'salvar mulheres'."
        "4. Escreva em Português do Brasil natural, nível literário alto."
        "5. Sem censura, mas com contexto lógico."
    )
    
    data = {
        # MUDANÇA AQUI: Usando o WizardLM-2 (Gigante e Inteligente)
        "model": "microsoft/wizardlm-2-8x22b", 
        "messages": [
            {"role": "system", "content": sistema_refinado},
            {"role": "user", "content": prompt_usuario}
        ],
        "temperature": 0.7, # Temperatura controlada para manter a inteligência
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            try:
                erro_json = response.json()
                msg = erro_json.get('error', {}).get('message', 'Erro desconhecido')
                return f"Erro OpenRouter ({response.status_code}): {msg}"
            except:
                return f"Erro Bruto: {response.text}"
            
    except Exception as e:
        return f"Erro de conexão: {e}"

# ==========================================
# INTERFACE DO APP
# ==========================================

if 'step' not in st.session_state: st.session_state.step = 1
if 'historia' not in st.session_state: st.session_state.historia = ""
if 'personagens' not in st.session_state: st.session_state.personagens = []

# TELA 1: ELENCO
if st.session_state.step == 1:
    st.title("🔥 Eroticizza (Wizard Intelligence)")
    st.markdown("**Motor:** Microsoft WizardLM-2 8x22B (Alta Coerência).")
    
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

# TELA 2: CONTEXTO
elif st.session_state.step == 2:
    st.title("📍 Contexto Inicial")
    local = st.selectbox("Local:", ["Escritório", "Quarto de Hotel", "Vestiário", "Carro"])
    
    # Dica: Deixei o texto padrão mais explícito para guiar a IA
    ctx = st.text_area("Situação:", "O Executivo e o Lutador estão sozinhos. Existe uma tensão sexual forte e reprimida entre eles. O Lutador veio cobrar uma dívida, mas o clima mudou.")
    
    if st.button("Gerar História"):
        with st.spinner("O WizardLM está pensando (focando na lógica)..."):
            sys = "Você é um autor de literatura adulta. Escreva com coerência lógica e narrativa."
            user = f"Escreva o início de um conto com {st.session_state.personagens} no {local}. Contexto: {ctx}. Foque na interação psicológica e física entre ELES."
            
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
    vibe = c1.radio("Próximo passo:", ["Aproximação Lenta", "Confronto Físico/Sexual", "Diálogo Intenso"])
    acao = c2.text_area("Ação:", "O que acontece agora?")
    
    if st.button("Continuar"):
        with st.spinner("Escrevendo..."):
            sys = "Continue a narrativa mantendo a lógica."
            user = f"História: {st.session_state.historia[-1500:]}. Ação: {acao}. Vibe: {vibe}."
            res = gerar_texto(sys, user)
            st.session_state.historia += f"#### {vibe}\n\n{res}\n\n"
            st.rerun()

    if st.button("Finalizar"):
        st.session_state.step = 4
        st.rerun()

# TELA 4: FINAL
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
