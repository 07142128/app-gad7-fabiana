
import streamlit as st
import io

st.set_page_config(page_title="GAD-7 | Psicóloga Fabiana Felix", layout="centered")

# --- ESTILO PERSONALIZADO ---
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

# --- LOGO NO TOPO ---
st.image("logo_fabiana_simbolo_psicologia.png", use_column_width=True)

# --- CABEÇALHO ---
st.title("Autoavaliação de Ansiedade - GAD-7")
st.markdown("**Psicóloga Fabiana Felix | CRP 0560756**")
st.markdown("Esta autoavaliação é baseada na escala validada GAD-7 e serve como triagem para ansiedade.")

# --- FORMULÁRIO ---
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

# --- CAPTURA DE DADOS ---
st.markdown("---")
st.markdown("### Antes de ver seu resultado:")
nome = st.text_input("Nome")
email = st.text_input("E-mail")
whatsapp = st.text_input("WhatsApp (com DDD)")

# --- PROCESSAMENTO ---
if st.button("Ver meu resultado"):
    if not email:
        st.warning("Por favor, insira seu e-mail.")
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
        st.markdown("Esse resultado é uma triagem inicial e **não substitui avaliação clínica profissional**.")
        st.markdown("### O que você deseja fazer agora?")

        st.markdown(f"[**Quero conversar com a Psicóloga Fabiana**](https://wa.me/5521995272617)")
        st.markdown(f"[**Quero entrar no grupo de apoio emocional e autocuidado**](https://chat.whatsapp.com/GbEyyhCMaBtAa2EugkGYcZ)")

        # Simulação de PDF
        pdf_texto = f"""
        Resultado do Teste GAD-7

        Nome: {nome}
        E-mail: {email}
        WhatsApp: {whatsapp}

        Pontuação: {pontuacao}/21
        Classificação: {nivel}

        Esse resultado é apenas uma triagem inicial e não substitui uma avaliação profissional.
        """

        buffer = io.BytesIO()
        buffer.write(pdf_texto.encode())
        buffer.seek(0)
        st.download_button(
            label="Baixar resultado em PDF",
            data=buffer,
            file_name="resultado_gad7_fabiana.pdf",
            mime="application/pdf"
        )

# --- RODAPÉ ---
st.markdown("---")
st.markdown("<center><small>Desenvolvido por Psicóloga Fabiana Felix | CRP 0560756</small></center>", unsafe_allow_html=True)
