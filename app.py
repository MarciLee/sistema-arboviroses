import streamlit as st
import joblib
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Triagem de Arboviroses - PE", layout="centered")

# Carregando os "cérebros" (IAs)
@st.cache_resource
def carregar_modelos():
    modelo_1 = joblib.load('ia_diferenciacao.joblib')
    modelo_2 = joblib.load('ia_risco_dengue.joblib')
    return modelo_1, modelo_2

ia_1, ia_2 = carregar_modelos()

st.title("🏥 Sistema Inteligente de Triagem")
st.subheader("Arboviroses em Pernambuco")
st.write("Preencha os sintomas abaixo para identificação e análise de risco.")

# Formulário de entrada
with st.form("formulario_triagem"):
    col1, col2 = st.columns(2)
    
    with col1:
        febre = st.selectbox("Febre Repentina?", [0, 1], format_func=lambda x: "Sim" if x==1 else "Não")
        cefaleia = st.selectbox("Dor de Cabeça?", [0, 1], format_func=lambda x: "Sim" if x==1 else "Não")
        mialgia = st.selectbox("Dor Muscular?", [0, 1], format_func=lambda x: "Sim" if x==1 else "Não")
        artralgia = st.selectbox("Dor Articular?", [0, 1], format_func=lambda x: "Sim" if x==1 else "Não")
        
    with col2:
        vomito = st.selectbox("Vômitos?", [0, 1], format_func=lambda x: "Sim" if x==1 else "Não")
        exantema = st.selectbox("Manchas na Pele?", [0, 1], format_func=lambda x: "Sim" if x==1 else "Não")
        retro = st.selectbox("Dor atrás dos olhos?", [0, 1], format_func=lambda x: "Sim" if x==1 else "Não")
        nausea = st.selectbox("Náuseas?", [0, 1], format_func=lambda x: "Sim" if x==1 else "Não")

    botao = st.form_submit_button("Realizar Triagem")

if botao:
    # Preparando dados para a IA
    entrada = pd.DataFrame([[febre, cefaleia, mialgia, artralgia, vomito, exantema]], 
                           columns=['sudden_fever', 'headache', 'muscle_pain', 'joint_pain', 'vomiting', 'rash'])
    
    # 1ª PRIORIDADE: Identificar Doença
    diagnostico = ia_1.predict(entrada)[0]
    
    st.markdown("---")
    st.info(f"**Diagnóstico Provável:** {diagnostico}")
    
    # 2ª PRIORIDADE: Se for Dengue, ver risco
    if diagnostico == "Dengue":
        # Sintomas específicos que a IA de risco espera (usando as colunas do Gallo)
        entrada_risco = pd.DataFrame([[febre, cefaleia, mialgia, artralgia, vomito, exantema, retro, nausea]],
                                     columns=['FEBRE', 'CEFALEIA', 'MIALGIA', 'ARTRALGIA', 'VOMITO', 'EXANTEMA', 'DOR_RETRO', 'NAUSEA'])
        
        risco = ia_2.predict(entrada_risco)[0]
        
        if risco == 1:
            st.error("⚠️ **ALERTA DE RISCO:** Sinais de gravidade detectados. Encaminhar para internação/observação.")
        else:
            st.success("✅ **DENGUE CLÁSSICA:** Caso estável. Recomenda-se repouso e hidratação.")