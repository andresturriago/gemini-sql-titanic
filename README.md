# 🚢 Titanic GenAI Explorer: Text-to-SQL Assistant

Este proyecto es un prototipo funcional que demuestra cómo la **IA Generativa** puede transformar la interacción con datos estructurados. Utiliza un modelo de lenguaje (LLM) para convertir preguntas en lenguaje natural en consultas SQL precisas, ejecutadas sobre el histórico dataset del Titanic.

## 🚀 Características
- **Text-to-SQL**: Traducción de lenguaje natural a consultas SQLite usando Google Gemini 1.5 Flash.
- **Interfaz Interactiva**: UI construida con Streamlit para visualización de datos en tiempo real.
- **Contexto Integrado**: Incluye un diccionario de datos y estadísticas descriptivas del dataset.
- **Seguridad**: Gestión de credenciales mediante variables de entorno.

## 🛠️ Stack Tecnológico
- **Lenguaje**: Python 3.x
- **LLM**: [Google GenAI SDK](https://pypi.org/project/google-genai/) (Gemini 2.5 Flash)
- **Frontend**: Streamlit
- **Base de Datos**: SQLite3
- **Dataset**: Seaborn Titanic Dataset

## 📐 Arquitectura y Flujo de Datos
El sistema sigue un flujo de procesamiento desde la entrada del usuario hasta la ejecución en base de datos:



1. **Usuario**: Ingresa una pregunta (ej. "¿Cuál es el promedio de edad de los sobrevivientes?").
2. **Backend**: Recupera el esquema de la tabla y construye un prompt enriquecido.
3. **Gemini API**: Procesa el prompt y devuelve una consulta SQL válida.
4. **SQLite**: Ejecuta la consulta sobre `titanic.db`.
5. **Streamlit**: Muestra los resultados tabulares y la consulta generada para transparencia.

## ⚙️ Configuración del Proyecto

### 1. Clonar el repositorio
```bash
git clone [https://github.com/tu-usuario/titanic-genai-explorer.git](https://github.com/tu-usuario/titanic-genai-explorer.git)
cd titanic-genai-explorer
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crea un archivo .env
```bash
GEMINI_API_KEY=""
GEMINI_ENDPOINT=""
```

### 4. Ejecutar la aplicación
```bash
streamlit run app.py
```
