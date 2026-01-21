import os
import sqlite3

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


def get_sql_query(user_question):
    """Usa el nuevo SDK google-genai para convertir texto a SQL."""

    prompt = f"""
    Eres un experto en SQLite. Tu tarea es transformar preguntas en lenguaje natural a consultas SQL.
    Tabla: 'titanic'
    Columnas: survived (int), pclass (int), sex (str), age (float), sibsp (int), parch (int), 
              fare (float), embarked (str), class (str), who (str), adult_male (bool), 
              embark_town (str), alive (str), alone (bool)

    Pregunta: {user_question}
    
    Instrucciones:
    - Devuelve SOLO la consulta SQL.
    - No uses bloques de código (```sql).
    - Si la pregunta no se puede responder con la tabla, devuelve: SELECT 'No se puede procesar'.
    """

    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
        http_options={"base_url": os.getenv("GEMINI_ENDPOINT")},
    )
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite", contents=prompt
    )
    return response.text.strip()


def show_dataset_context():
    with st.expander("📊 Información sobre el Dataset Titanic", expanded=False):
        st.write(
            """
        El conjunto de datos del Titanic es un conjunto de datos muy conocido que contiene información sobre los pasajeros del barco Titanic. Incluye variables como la edad, el sexo, la clase, la tarifa y si cada pasajero sobrevivió.
        """
        )

        # Cargar datos para el resumen
        conn = sqlite3.connect("titanic.db")
        df_preview = pd.read_sql_query("SELECT * FROM titanic LIMIT 5", conn)
        total_rows = pd.read_sql_query(
            "SELECT COUNT(*) as count FROM titanic", conn
        ).iloc[0]["count"]
        # avg_fare = pd.read_sql_query("SELECT AVG(fare) as avg FROM titanic", conn).iloc[0]['avg']
        # survival_rate = pd.read_sql_query("SELECT AVG(survived) * 100 as rate FROM titanic", conn).iloc[0]['rate']
        conn.close()

        # Mostrar métricas rápidas
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Pasajeros", total_rows)
        # col2.metric("Tarifa Promedio", f"${avg_fare:.2f}")
        # col3.metric("Tasa Supervivencia", f"{survival_rate:.1f}%")

        # Mostrar muestra de datos y diccionario
        st.write("**Vistazo de los datos:**")
        st.dataframe(df_preview, height=150)

        st.markdown("### Descripción de las Columnas")
        # Definimos los datos del diccionario
        data_dict = {
            "Columna": [
                "survived",
                "pclass",
                "sex",
                "age",
                "sibsp",
                "parch",
                "fare",
                "embarked",
                "class",
                "who",
                "adult_male",
                "embark_town",
                "alive",
                "alone",
            ],
            "Descripción": [
                "Indica si sobrevivió (0 = No, 1 = Sí).",
                "Clase del ticket (1, 2, 3).",
                "Género del pasajero.",
                "Edad en años.",
                "Número de hermanos/esposos a bordo.",
                "Número de padres/hijos a bordo.",
                "Tarifa pagada por el pasajero.",
                "Puerto de embarque (C, Q, S).",
                "Clase (Duplicado de pclass).",
                "Categoría (man, woman, child).",
                "¿Es hombre adulto? (True/False).",
                "Nombre de la ciudad de embarque.",
                "¿Está vivo? (yes/no).",
                "¿Viajaba solo? (True/False).",
            ],
        }
        st.table(pd.DataFrame(data_dict))


def main():
    st.set_page_config(page_title="Titanic AI Explorer", page_icon="🚢")
    st.title("🚢 Titanic AI Assistant")

    show_dataset_context()

    st.divider()  # Línea visual separadora

    question = st.text_input(
        "Haz una pregunta sobre los datos:",
        placeholder="Inserta aqui tu pregunta, por ej: ¿Cuántas personas sobrevivieron?",
    )

    if st.button("Consultar"):
        try:
            sql_query = get_sql_query(question)

            with st.expander("Consulta SQL"):
                st.code(sql_query, language="sql")

            conn = sqlite3.connect("titanic.db")
            df_result = pd.read_sql_query(sql_query, conn)
            conn.close()

            if not df_result.empty:
                st.subheader("Resultados:")
                st.dataframe(df_result, use_container_width=True)
            else:
                st.warning("No se encontraron resultados.")

        except Exception as e:
            if "429" in str(e):
                st.error(
                    "🚨 Error 429: Límite de cuota excedido. El endpoint global está saturado, intenta de nuevo en unos segundos."
                )
            else:
                st.error(f"Error técnico: {e}")


if __name__ == "__main__":
    main()
