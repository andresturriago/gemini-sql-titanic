import sqlite3

# import pandas as pd
import seaborn as sns


def setup_database():
    """Carga el dataset Titanic y lo guarda en SQLite."""
    titanic = sns.load_dataset("titanic")
    # Convertimos columnas de tipo 'category' u 'object' a string para evitar conflictos en SQL
    for col in titanic.select_dtypes(["category", "object"]).columns:
        titanic[col] = titanic[col].astype(str)

    conn = sqlite3.connect("titanic.db")
    titanic.to_sql("titanic", conn, if_exists="replace", index=False)
    conn.close()


if __name__ == "__main__":
    setup_database()
