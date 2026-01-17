import streamlit as st
import requests
from fpdf import FPDF

# ==========================================
# CONFIGURAÇÃO DE SEGURANÇA
# ==========================================
CHAVE_BRUTA = "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"
API_KEY = CHAVE_BRUTA.strip() 

st.set_page_config(page_title="Eroticizza Hermes", layout="wide")

# ==========================================
# MOTOR DA IA: Hermes 3 (Llama 3.1 70B Uncensored)
# ==========================================
def gerar_texto(prompt_sistema, prompt_usuario):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://eroticizza.streamlit.app",
        "X-Title": "Eroticizza",
        "Content-Type": "application/json"
    }
    
    # Prompt "Hardcore" Mantido
    sistema_calibrado = (
        f"{prompt_sistema} "
        "DIRETRIZES OBRIGATÓRIAS (MODO HARDCORE):"
        "1. VOCABULÁRIO SUJO: Use palavras reais e cruas: pau, pica, rola, cu, rabo, buceta, gozo, porra. Nada de termos médicos."
        "2. ANATOMIA VISCERAL: Descreva veias, glande, lubrificação, cheiros e contrações musculares."
        "3. SEM POESIA: Proibido usar metáforas como 'membro', 'lampião', 'vênus'. Seja direto."
        "4. HUMILHAÇÃO REAL: Se a cena pede dominação, descreva o medo, a submissão e a degradação verbal."
        "5. IDIOMA: Português do Brasil natural. NUNCA use inglês."
        "6. LÓGICA: Mantenha a coerência da cena (sem objetos mágicos)."
    )
    
    data = {
        # MUDANÇA: Hermes 3 (Inteligente E Sem Censura)
        "model": "nousresearch/hermes-3-llama-3.1-70b", 
        "messages": [
            {"role": "system", "content": sistema_calibrado},
            {"role": "user", "content": prompt_usuario}
        ],
        "temperature": 0.75, # Um pouco mais alta para criatividade
        "max_tokens": 2500,
        
        # A CURA DO "NÃCA NÃCA":
        "repetition_penalty": 1.1, # Penaliza a IA se ela começar a repetir palavras
        "top_p": 0.9
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            try:
                erro = response.json()
                msg = erro.get('error', {}).get('message', str(erro))
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

# TELA 1
if st.session_state.step == 1:
    st.title("🔥 Eroticizza (Hermes 3 Edition)")
    st.markdown("**Motor:** Hermes 3 - Llama 3.1 70B (Inteligente & Sujo).")
    
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
    local = st.selectbox("Local:", ["Escritório", "Vestiário", "Motel", "Carro"])
    
    ctx = st.text_area("Descreva a cena (Seja explícito):", "O Lutador cobra a dívida do Executivo. Ele quer humilhação total. O Executivo sente medo e prazer.")
    
    if st.button("Gerar Início"):
        with st.spinner("O Hermes está escrevendo..."):
            sys = "Você é um escritor de contos eróticos hardcore."
            user = f"Escreva o início com {st.session_state.personagens} no {local}. Contexto: {ctx}. Use linguagem suja e anatômica."
            
            res = gerar_texto(sys, user)
            
            if "Erro" in res:
                st.error(res)
            else:
                st.session_state.historia += f"### O Início\n\n{res}\n\n"
                st.session_state.step = 3
                st.rerun()

# TELA 3
elif st.session_state.step == 3:
    st.markdown(st.session_state.historia)
    st.divider()
    
    c1, c2 = st.columns([1,2])
    vibe = c1.radio("Foco:", ["Humilhação Verbal", "Sexo Oral", "Anal Brutal", "Dominação"])
    acao = c2.text_area("Ação:", "O que acontece agora?")
    
    if st.button("Continuar"):
        with st.spinner("Escrevendo..."):
            sys = "Continue a narrativa mantendo o tom sujo."
            user = f"História anterior: {st.session_state.historia[-1500:]}. Ação: {acao}. Vibe: {vibe}."
            res = gerar_texto(sys, user)
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
