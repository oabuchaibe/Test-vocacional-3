import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Test Vocacional Integral", layout="centered")
st.title("🧠 Test Vocacional Integral y Recomendador de Carreras")

st.markdown("Este test evalúa tus afinidades con diferentes áreas profesionales y te sugiere carreras específicas al final.")

Likert = ["1 - Nada en absoluto", "2 - Poco", "3 - Neutral", "4 - Bastante", "5 - Mucho"]
scores = {}

areas = {
    "Salud y Bienestar": [
        "Me interesa cuidar a personas enfermas o necesitadas.",
        "Me gustaría estudiar medicina, enfermería o psicología."
    ],
    "Tecnología y Computación": [
        "Disfruto resolver problemas con tecnología.",
        "Me interesa programar o trabajar en inteligencia artificial."
    ],
    "Derecho y Gobierno": [
        "Me gustaría defender los derechos de las personas.",
        "Me atraen carreras como abogacía, criminología o ciencias políticas."
    ],
    "Arte y Música": [
        "Me gusta expresarme a través del arte, la música o la actuación.",
        "Disfruto crear obras originales y explorar la creatividad."
    ],
    "Deporte y Actividad Física": [
        "Practico deportes con frecuencia y disfruto el ejercicio.",
        "Me gustaría ser entrenador, fisioterapeuta o atleta profesional."
    ],
    "Oficios Técnicos y Operativos": [
        "Me gusta arreglar, construir o manipular objetos físicos.",
        "Me interesa la mecánica, electricidad o carpintería."
    ],
    "Negocios y Economía": [
        "Sueño con liderar empresas o gestionar recursos.",
        "Me interesa la administración, contabilidad o negocios internacionales."
    ],
    "Educación y Servicios Sociales": [
        "Disfruto enseñar, guiar o apoyar a otros en su desarrollo.",
        "Me gustaría trabajar como docente, orientador o trabajador social."
    ],
    "Seguridad y Servicio Público": [
        "Me atraen trabajos como policía, bombero o militar.",
        "Estoy dispuesto a actuar en situaciones de emergencia para ayudar."
    ]
}

st.markdown("## Responde las siguientes afirmaciones:")

for area, items in areas.items():
    st.markdown(f"### {area}")
    score = 0
    for i, item in enumerate(items):
        res = st.radio(item, options=Likert, key=f"{area}_{i}")
        score += int(res[0])
    scores[area] = score / len(items)

if st.button("Ver mis resultados y recomendaciones"):
    st.success("¡Gracias por responder el test!")

    df = pd.DataFrame(list(scores.items()), columns=["Área", "Puntaje promedio"])
    df = df.sort_values(by="Puntaje promedio", ascending=False)

    st.markdown("### 📊 Gráfico de afinidad por área profesional")
    fig, ax = plt.subplots()
    ax.barh(df["Área"], df["Puntaje promedio"])
    ax.invert_yaxis()
    st.pyplot(fig)

    st.markdown("### 🎯 Carreras sugeridas:")
    top_area = df.iloc[0]["Área"]
    sugerencias = {
        "Salud y Bienestar": ["Medicina", "Psicología", "Enfermería"],
        "Tecnología y Computación": ["Ingeniería de Sistemas", "Ciencia de Datos", "Desarrollo de Software"],
        "Derecho y Gobierno": ["Derecho", "Criminología", "Relaciones Internacionales"],
        "Arte y Música": ["Música", "Artes Escénicas", "Diseño Gráfico"],
        "Deporte y Actividad Física": ["Educación Física", "Fisioterapia Deportiva", "Entrenamiento Deportivo"],
        "Oficios Técnicos y Operativos": ["Mecánica Automotriz", "Electricidad", "Soldadura"],
        "Negocios y Economía": ["Administración", "Marketing", "Contaduría"],
        "Educación y Servicios Sociales": ["Pedagogía", "Trabajo Social", "Psicopedagogía"],
        "Seguridad y Servicio Público": ["Policía", "Bombero", "Militar"]
    }
    for carrera in sugerencias.get(top_area, []):
        st.write(f"- {carrera}")
