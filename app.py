import streamlit as st
import requests
from fpdf import FPDF

# ==========================================
# CONFIGURAÇÃO DE SEGURANÇA
# ==========================================
CHAVE_BRUTA = "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"
API_KEY = CHAVE_BRUTA.strip() 

st.set_page_config(page_title="Eroticizza Hardcore", layout="wide")

# ==========================================
# MOTOR DA IA: WizardLM-2 (Com Prompt Agressivo)
# ==========================================
def gerar_texto(prompt_sistema, prompt_usuario):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://eroticizza.streamlit.app",
        "X-Title": "Eroticizza",
        "Content-Type": "application/json"
    }
    
    # AQUI ESTÁ A "CALIBRAGEM" QUE VOCÊ PEDIU
    # Estamos transformando o "Filósofo" em um "Diretor de Filme Adulto"
    sistema_calibrado = (
        f"{prompt_sistema} "
        "REGRAS DE ESTILO OBRIGATÓRIAS (MODO HARDCORE):"
        "1. VOCABULÁRIO SUJO: Pare de usar termos médicos ou poéticos. Use as palavras reais: pau, rola, pica, cu, rabo, buceta, gozo, porra, leite."
        "2. ANATOMIA VISCERAL: Descreva detalhes físicos. Fale do tamanho, da espessura, das veias saltadas, da cor da cabeça, da lubrificação."
        "3. PROIBIDO POESIA: Nunca use palavras como 'lampião', 'membro viril', 'vênus', 'cópula'. Isso é proibido. Seja cru e direto."
        "4. AÇÃO FÍSICA: Se o usuário pedir humilhação, descreva a submissão real (tapas, puxões de cabelo, ordens verbais, cuspe)."
        "5. SEM MORALISMO: Não crie lições de moral no final. É um conto erótico, o objetivo é o tesão."
        "6. IDIOMA: Português do Brasil coloquial. Sem frases em inglês."
    )
    
    data = {
        # Voltamos para o WizardLM porque ele tem lógica e está online
        "model": "microsoft/wizardlm-2-8x22b", 
        "messages": [
            {"role": "system", "content": sistema_calibrado},
            {"role": "user", "content": prompt_usuario}
        ],
        "temperature": 0.65, # Temperatura média para ele obedecer o estilo sem perder a criatividade
        "max_tokens": 2500
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
    st.title("🔥 Eroticizza (Mode: Realista/Sujo)")
    st.markdown("**Calibragem:** Vocabulário explícito e anatomia detalhada.")
    
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
    local = st.selectbox("Local:", ["Escritório Corporativo", "Vestiário da Academia", "Quarto de Motel", "Carro"])
    
    st.warning("⚠️ Dica: Para o melhor resultado, seja explícito no contexto abaixo.")
    ctx = st.text_area("Descreva a cena:", "O Lutador vai cobrar a dívida do Executivo. Ele quer humilhar o Executivo. O Executivo é passivo e tem medo, mas sente prazer.")
    
    if st.button("Gerar Início"):
        with st.spinner("Escrevendo (Estilo Hardcore)..."):
            sys = "Você é um escritor de contos eróticos explícitos (smut)."
            user = f"Escreva o início com {st.session_state.personagens} no {local}. Contexto: {ctx}. Use os nomes dos personagens. Descreva a anatomia."
            
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
    vibe = c1.radio("Foco da Cena:", ["Humilhação Verbal", "Sexo Oral Profundo", "Dominação Física", "Anal Sem Preparo"])
    acao = c2.text_area("O que acontece agora?", "Ex: O Lutador tira o pau para fora e obriga...")
    
    if st.button("Continuar"):
        with st.spinner("Escrevendo..."):
            sys = "Continue a narrativa mantendo a linguagem suja."
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
