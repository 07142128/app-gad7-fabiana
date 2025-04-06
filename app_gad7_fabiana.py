
import streamlit as st

st.set_page_config(page_title="Teste de Ansiedade GAD-7", layout="centered")

st.title("Autoavaliação de Ansiedade - GAD-7")
st.markdown("Desenvolvido por **Psicóloga Fabiana Felix** | CRP em processo de validação")

st.write("Responda as perguntas abaixo com base nos últimos 14 dias.")

# Escala de resposta
opcoes = {
    "Nunca (0)": 0,
    "Vários dias (1)": 1,
    "Mais da metade dos dias (2)": 2,
    "Quase todos os dias (3)": 3
}

# Perguntas do GAD-7
perguntas = [
    "1. Sentiu-se nervoso(a), ansioso(a) ou com os nervos à flor da pele?",
    "2. Não conseguiu parar ou controlar a preocupação?",
    "3. Preocupou-se excessivamente com diferentes coisas?",
    "4. Teve dificuldade de relaxar?",
    "5. Sentiu-se tão inquieto(a) que era difícil ficar parado(a)?",
    "6. Irritou-se facilmente ou sentiu-se incomodado(a)?",
    "7. Sentiu medo como se algo horrível fosse acontecer?"
]

# Coleta de respostas
respostas = []
for pergunta in perguntas:
    resposta = st.selectbox(pergunta, list(opcoes.keys()), key=pergunta)
    respostas.append(opcoes[resposta])

# Captura de informações pessoais
st.markdown("---")
st.subheader("Antes de ver seu resultado:")

nome = st.text_input("Nome (opcional)")
email = st.text_input("E-mail para receber o resultado")
whatsapp = st.text_input("WhatsApp (opcional, com DDD)")

# Botão para calcular resultado
if st.button("Ver meu resultado"):
    if not email:
        st.warning("Por favor, insira seu e-mail para prosseguir.")
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

        st.markdown("---")
        st.markdown("Esse teste é uma triagem inicial e **não substitui avaliação clínica profissional.**")

        # Botões de ação
        st.markdown("### O que você deseja fazer agora?")
        st.markdown("[Quero conversar com uma psicóloga](https://wa.me/SEUNUMEROAQUI)")
        st.markdown("[Sou profissional e quero aplicar esse teste](https://SEULINKDECURSOAQUI)")
