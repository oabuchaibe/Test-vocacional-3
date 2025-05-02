import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime
import os

st.set_page_config(page_title="Aventura Vocacional", layout="centered")

st.title("🚀 Aventura Vocacional")
st.markdown("Bienvenido a tu viaje de descubrimiento profesional. Responde las misiones y descubre tu perfil vocacional.")

if "page" not in st.session_state:
    st.session_state.page = 0

if "respuestas" not in st.session_state:
    st.session_state.respuestas = {}

if "nombre" not in st.session_state:
    st.session_state.nombre = ""

if "fecha" not in st.session_state:
    st.session_state.fecha = datetime.date.today().strftime("%d/%m/%Y")

def next_page():
    st.session_state.page += 1

def reset():
    st.session_state.page = 0
    st.session_state.respuestas = {}

Likert = ["1", "2", "3", "4", "5"]

if st.session_state.page == 0:
    st.header("👤 Datos del estudiante")
    st.session_state.nombre = st.text_input("Nombre del estudiante")
    st.session_state.fecha = st.date_input("Fecha de aplicación", value=datetime.date.today()).strftime("%d/%m/%Y")
    if st.button("Iniciar test"):
        next_page()

elif st.session_state.page == 1:
    st.header("Misión 1: Intereses Vocacionales")
    for i, pregunta in enumerate([
        "Me interesa comprender cómo piensan y sienten las personas.",
        "Me motiva resolver desafíos técnicos o prácticos.",
        "Disfruto crear cosas nuevas desde cero.",
        "Prefiero colaborar con otros en actividades sociales.",
        "Me atrae la idea de emprender o liderar."
    ]):
        st.session_state.respuestas[f"int_{i+1}"] = st.radio(pregunta, Likert, key=f"int_{i+1}")
    st.button("Siguiente misión", on_click=next_page)

elif st.session_state.page == 2:
    st.header("Misión 2: Aptitudes Técnicas")
    for i, pregunta in enumerate([
        "Comprendo bien gráficos, tablas o esquemas.",
        "Aprendo rápido a usar programas digitales.",
        "Puedo resolver cálculos sin problema.",
        "Se me da bien entender instrucciones técnicas.",
        "Identifico patrones con facilidad."
    ]):
        st.session_state.respuestas[f"apt_{i+1}"] = st.radio(pregunta, Likert, key=f"apt_{i+1}")
    st.button("Siguiente misión", on_click=next_page)

elif st.session_state.page == 3:
    st.header("Misión 3: Habilidades Blandas")
    for i, pregunta in enumerate([
        "Soy empático/a y entiendo a los demás.",
        "Trabajo bien en equipo y comunico ideas.",
        "Me adapto con facilidad a los cambios.",
        "Me esfuerzo incluso si algo es difícil.",
        "Suelo organizar actividades o tiempos."
    ]):
        st.session_state.respuestas[f"soft_{i+1}"] = st.radio(pregunta, Likert, key=f"soft_{i+1}")
    st.button("Ver resultados", on_click=next_page)

elif st.session_state.page == 4:
    st.header("🎯 Resultados preliminares")
    st.markdown("Gracias por completar esta fase. Tus resultados están siendo procesados.")

    def calcular_promedio(prefijo):
        valores = [int(v) for k, v in st.session_state.respuestas.items() if k.startswith(prefijo)]
        return round(sum(valores) / len(valores), 2)

    intereses = calcular_promedio("int")
    aptitudes = calcular_promedio("apt")
    blandas = calcular_promedio("soft")

    st.subheader("📊 Resultados por dimensión")
    st.write(f"**Intereses vocacionales:** {intereses}/5")
    st.write(f"**Aptitudes técnicas:** {aptitudes}/5")
    st.write(f"**Habilidades blandas:** {blandas}/5")

    st.subheader("📈 Visualización del perfil")
    fig, ax = plt.subplots()
    categorias = ["Intereses", "Aptitudes Técnicas", "Habilidades Blandas"]
    puntajes = [intereses, aptitudes, blandas]
    ax.bar(categorias, puntajes, color=["skyblue", "orange", "lightgreen"])
    ax.set_ylim(0, 5)
    ax.set_ylabel("Puntaje promedio")
    plt.tight_layout()
    chart_path = "grafico_resultados.png"
    fig.savefig(chart_path)
    st.pyplot(fig)

    st.subheader("🎓 Carreras sugeridas")
    recomendacion = ""
    if intereses >= 4 and aptitudes >= 4:
        recomendacion = "Podrías destacar en carreras como Ingeniería, Tecnología o Ciencias Aplicadas."
    elif intereses >= 4 and blandas >= 4:
        recomendacion = "Podrías destacar en Psicología, Educación, Trabajo Social o Comunicación."
    elif aptitudes >= 4:
        recomendacion = "Podrías destacar en áreas técnicas como Sistemas, Mecatrónica o Análisis de Datos."
    elif blandas >= 4:
        recomendacion = "Podrías destacar en áreas sociales como Recursos Humanos, Orientación o Liderazgo comunitario."
    else:
        recomendacion = "Explora más opciones con tu orientador. Este es un perfil mixto que puede adaptarse a varias áreas."

    st.success(recomendacion)

    def generar_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Informe de Orientación Vocacional", ln=True, align='C')
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Nombre: {st.session_state.nombre}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha: {st.session_state.fecha}", ln=True)
        pdf.ln(5)
        pdf.cell(200, 10, txt=f"Intereses vocacionales: {intereses}/5", ln=True)
        pdf.cell(200, 10, txt=f"Aptitudes técnicas: {aptitudes}/5", ln=True)
        pdf.cell(200, 10, txt=f"Habilidades blandas: {blandas}/5", ln=True)
        pdf.ln(10)
        pdf.multi_cell(0, 10, txt=f"Carreras sugeridas: {recomendacion}")
        pdf.ln(5)
        pdf.image(chart_path, x=30, w=150)
        pdf.ln(10)
        pdf.cell(200, 10, txt="Firmado: Dr. Naim", ln=True)
        pdf.cell(200, 10, txt="Científico en Desarrollo Vocacional - Trulivers", ln=True)
        pdf_path = "Informe_Vocacional_Personalizado.pdf"
        pdf.output(pdf_path)
        return pdf_path

    if st.button("📄 Descargar informe PDF"):
        pdf_path = generar_pdf()
        with open(pdf_path, "rb") as file:
            st.download_button(
                label="Haz clic aquí para descargar tu informe",
                data=file,
                file_name="Informe_Vocacional.pdf",
                mime="application/pdf"
            )

    st.button("🔄 Reiniciar test", on_click=reset)
