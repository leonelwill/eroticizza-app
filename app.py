import streamlit as st
import requests
from fpdf import FPDF

# ==========================================
# CONFIGURAÇÃO (Sua Chave)
# ==========================================
CHAVE_BRUTA = "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"
API_KEY = CHAVE_BRUTA.strip() 

st.set_page_config(page_title="Eroticizza Pro", layout="wide")

# ==========================================
# MOTOR DA IA: Command R+ (O Rei do Roleplay)
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
    sistema_hardcore = (
        f"{prompt_sistema} "
        "DIRETRIZES DE ESTILO (HARDCORE):"
        "1. LINGUAGEM: Use linguagem explícita, crua e vulgar quando necessário. Esqueça metáforas poéticas (nada de 'lampião', 'membros pulsantes'). Use os nomes reais e sujos: pau, pica, rola, cu, gozo."
        "2. ANATOMIA DETALHADA: Descreva a física da cena. Fale de veias saltadas, tamanho, glande, fluidos, cheiros, lubrificação e sons molhados."
        "3. TEMA: Se o usuário pediu humilhação, seja cruel. Descreva a submissão psicológica e física real."
        "4. IDIOMA: Português do Brasil coloquial e direto. NUNCA use frases em inglês."
        "5. LÓGICA: Mantenha a coerência. Se eles estão num escritório moderno, use luzes de LED, ar condicionado, não 'lampiões'."
    )
    
    data = {
        # MUDANÇA: Command R+ (cohere/command-r-plus)
        # É o modelo mais obediente e criativo para conteúdo adulto atualmente.
        "model": "cohere/command-r-plus", 
        "messages": [
            {"role": "system", "content": sistema_hardcore},
            {"role": "user", "content": prompt_usuario}
        ],
        "temperature": 0.6, # Temperatura mais baixa para focar na instrução e não "viajar"
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
    st.title("🔥 Eroticizza (Mode: Command R+ Hardcore)")
    st.markdown("**Calibragem:** Linguagem suja, anatomia detalhada e sem poesia barata.")
    
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
    st.title("📍 Contexto & Vibe")
    local = st.selectbox("Local:", ["Escritório Corporativo", "Vestiário Sujo", "Quarto de Motel", "Carro Blindado"])
    
    # Dica para o usuário
    st.info("💡 Dica: Quanto mais detalhes sujos você colocar no contexto, mais a IA vai seguir.")
    ctx = st.text_area("Contexto da Cena:", "O Executivo deve dinheiro ao Lutador. O Lutador vai cobrar a dívida com humilhação sexual. O Executivo é passivo.")
    
    if st.button("Gerar Início Brutal"):
        with st.spinner("O Command R+ está escrevendo (pode ser explícito)..."):
            sys = "Você é um escritor de contos eróticos hardcore."
            user = f"Escreva o início com {st.session_state.personagens} no {local}. Contexto: {ctx}. Descreva a tensão física, o medo e a excitação."
            
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
    vibe = c1.radio("Foco da Cena:", ["Humilhação Verbal", "Sexo Oral Profundo", "Dominação Física", "Anal Brutal"])
    acao = c2.text_area("O que acontece agora?", "Ex: O Lutador obriga o Executivo a implorar...")
    
    if st.button("Continuar"):
        with st.spinner("Escrevendo..."):
            sys = "Continue a narrativa mantendo o tom sujo e anatômico."
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
