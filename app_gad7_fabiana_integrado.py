
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import io
import json

# Configurar a página
st.set_page_config(page_title="GAD-7 | Psicóloga Fabiana Felix", layout="centered")

# Estilo boho
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
            color: #3A3A3A;
        }
        .stButton button {
            background-color: #A3B18A;
            color: white;
            padding: 0.75em 1.5em;
            border: none;
            border-radius: 6px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho
st.title("Autoavaliação de Ansiedade - GAD-7")
st.markdown("**Psicóloga Fabiana Felix | CRP 0560756**")
st.markdown("Esta autoavaliação é baseada na escala validada GAD-7 e serve como triagem para ansiedade.")

# Perguntas
st.markdown("### Responda com base nos últimos 14 dias:")
opcoes = {
    "Nunca (0)": 0,
    "Vários dias (1)": 1,
    "Mais da metade dos dias (2)": 2,
    "Quase todos os dias (3)": 3
}
perguntas = [
    "1. Sentiu-se nervoso(a), ansioso(a) ou com os nervos à flor da pele?",
    "2. Não conseguiu parar ou controlar a preocupação?",
    "3. Preocupou-se excessivamente com diferentes coisas?",
    "4. Teve dificuldade de relaxar?",
    "5. Sentiu-se tão inquieto(a) que era difícil ficar parado(a)?",
    "6. Irritou-se facilmente ou sentiu-se incomodado(a)?",
    "7. Sentiu medo como se algo horrível fosse acontecer?"
]

respostas = []
for pergunta in perguntas:
    resposta = st.selectbox(pergunta, list(opcoes.keys()), key=pergunta)
    respostas.append(opcoes[resposta])

# Dados pessoais
st.markdown("---")
st.markdown("### Antes de ver seu resultado:")
nome = st.text_input("Nome completo")
email = st.text_input("E-mail")
whatsapp = st.text_input("WhatsApp (com DDD)")

if st.button("Ver meu resultado"):
    if not nome or not email or not whatsapp:
        st.warning("Por favor, preencha todos os campos antes de continuar.")
    else:
        pontuacao = sum(respostas)
        if pontuacao >= 15:
            nivel = "Ansiedade grave"
        elif pontuacao >= 10:
            nivel = "Ansiedade moderada"
        elif pontuacao >= 5:
            nivel = "Ansiedade leve"
        else:
            nivel = "Ansiedade mínima"

        st.success(f"Sua pontuação: {pontuacao}/21")
        st.markdown(f"**Classificação: {nivel}**")
        st.markdown("Esse resultado é uma triagem inicial e **não substitui avaliação clínica profissional**.")

        st.markdown("### O que você deseja fazer agora?")
        st.markdown(f"[**Conversar com a Psicóloga Fabiana**](https://wa.me/5521995272617)")
        st.markdown(f"[**Entrar no grupo de apoio emocional**](https://chat.whatsapp.com/GbEyyhCMaBtAa2EugkGYcZ)")

        # Registro no Google Sheets
        try:
            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            with open("app-gad7-fabiana.json", "r") as file:
                credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.load(file), scope)
            gc = gspread.authorize(credentials)
            sh = gc.open("respostas_gad7_fabiana")
            worksheet = sh.get_worksheet(0)
            linha = [nome, email, whatsapp, str(pontuacao), nivel, datetime.now().strftime("%d/%m/%Y %H:%M")]
            worksheet.append_row(linha)
            st.success("✅ Seus dados foram enviados com sucesso!")
            st.markdown("Em breve entrarei em contato com você para oferecer mais orientação. Obrigada por participar! 💚")
        except Exception as e:
            st.error(f"Erro ao salvar os dados: {e}")
