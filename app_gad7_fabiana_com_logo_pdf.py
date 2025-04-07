
import streamlit as st
from fpdf import FPDF
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
st.image("logo_fabiana_simbolo_psicologia.png", use_container_width=True)

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

# --- DADOS DO USUÁRIO ---
st.markdown("---")
st.markdown("### Antes de ver seu resultado:")
nome = st.text_input("Nome")
email = st.text_input("E-mail")
whatsapp = st.text_input("WhatsApp (com DDD)")

# --- FUNÇÃO PDF ---
class GAD7PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.set_text_color(163, 177, 138)
        self.cell(0, 10, "Resultado do Teste GAD-7", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(100)
        self.cell(0, 10, "Psicóloga Fabiana Felix - CRP 0560756", align="C")

    def corpo(self, nome, email, whatsapp, pontuacao, nivel, mensagem):
        self.set_font("Arial", "", 12)
        self.set_text_color(0)
        self.cell(0, 10, f"Nome: {nome}", ln=True)
        self.cell(0, 10, f"E-mail: {email}", ln=True)
        self.cell(0, 10, f"WhatsApp: {whatsapp}", ln=True)
        self.ln(5)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"Pontuação Total: {pontuacao}/21", ln=True)
        self.cell(0, 10, f"Classificação: {nivel}", ln=True)
        self.ln(10)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 10, mensagem)

def gerar_mensagem(pontuacao):
    if pontuacao <= 4:
        nivel = "Ansiedade mínima"
        mensagem = """Sua pontuação está dentro da faixa considerada normal. Isso indica que, neste momento, seus níveis de ansiedade estão sob controle.

Recomendações:
- Continue investindo em momentos de descanso e lazer;
- Mantenha rotinas que te façam bem;
- Exercício sugerido: Escreva 3 coisas que funcionam bem na sua vida emocional atualmente."""
    elif pontuacao <= 9:
        nivel = "Ansiedade leve"
        mensagem = """Você apresenta alguns sinais leves de ansiedade. Isso é comum e pode estar relacionado a situações do dia a dia. Ainda assim, é importante observar se esses sintomas estão se repetindo com frequência.

Recomendações:
- Perceba gatilhos que aumentam sua ansiedade;
- Pratique respiração ou meditação curta;
- Exercício sugerido: Escreva o que te causa ansiedade e uma resposta possível para cada ponto."""
    elif pontuacao <= 14:
        nivel = "Ansiedade moderada"
        mensagem = """Essa pontuação indica que você está sentindo impactos mais significativos da ansiedade na sua rotina.

Recomendações:
- Converse com um(a) psicólogo(a) para compreender os gatilhos;
- Técnicas de respiração e auto-observação podem ser úteis;
- Exercício sugerido: Registre por 3 dias seguidos os momentos em que sentiu ansiedade."""
    else:
        nivel = "Ansiedade elevada"
        mensagem = """Sua pontuação mostra que os sintomas estão intensos e podem estar afetando sua qualidade de vida emocional, física e social.

Recomendações:
- Inicie acompanhamento psicológico se ainda não estiver;
- Evite autocrítica e acolha seus sentimentos;
- Exercício sugerido: Liste 5 preocupações da semana e reflita: posso controlar? posso aceitar? posso pedir ajuda?"""
    return nivel, mensagem

# --- RESULTADO E PDF ---
if st.button("Ver meu resultado"):
    if not email:
        st.warning("Por favor, insira seu e-mail.")
    else:
        pontuacao = sum(respostas)
        nivel, mensagem = gerar_mensagem(pontuacao)

        st.success(f"Sua pontuação: {pontuacao}/21")
        st.markdown(f"**Classificação: {nivel}**")
        st.markdown("---")
        st.markdown(mensagem)
        st.markdown("### O que você deseja fazer agora?")
        st.markdown(f"[**Quero conversar com a Psicóloga Fabiana**](https://wa.me/5521995272617)")
        st.markdown(f"[**Quero entrar no grupo de apoio emocional e autocuidado**](https://chat.whatsapp.com/GbEyyhCMaBtAa2EugkGYcZ)")

        # Gerar PDF com conteúdo formatado
        pdf = GAD7PDF()
        pdf.add_page()
        pdf.corpo(nome, email, whatsapp, pontuacao, nivel, mensagem)

        buffer = io.BytesIO()
        pdf.output(buffer)
        buffer.seek(0)

        st.download_button(
            label="Baixar resultado em PDF",
            data=buffer,
            file_name="resultado_gad7_fabiana.pdf",
            mime="application/pdf"
        )
