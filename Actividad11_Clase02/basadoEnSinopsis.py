"""Script organizado para encontrar las 3 películas más similares a una película objetivo
usando la distancia de Levenshtein sobre los títulos.

Ubicación esperada del CSV por defecto: ./tmdb_5000_movies.csv (mismo directorio que este script)
Uso: python basadoEnSinopsis.py --csv tmdb_5000_movies.csv --target "Star Trek Beyond" --sample 100
"""

# Tipos, parsing de argumentos y librerías de trabajo con datos
from typing import List, Dict
import argparse
import pandas as pd
import numpy as np


def levenshtein_distance(s1: str, s2: str) -> int:
    # Calcular la distancia de Levenshtein entre dos cadenas.

    # La implementación usa una matriz (programación dinámica). Devuelve un int.
    # Maneja None convirtiéndolo a cadena vacía.

    s1 = '' if s1 is None else str(s1)
    s2 = '' if s2 is None else str(s2)
    rows, cols = len(s1) + 1, len(s2) + 1
    dist = np.zeros((rows, cols), dtype=int)

    # Inicializar primera fila y columna con los costos de insertar/eliminar
    for i in range(rows):
        dist[i, 0] = i
    for j in range(cols):
        dist[0, j] = j

    # Rellenar la tabla de costos
    for j in range(1, cols):
        for i in range(1, rows):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dist[i, j] = min(
                dist[i - 1, j] + 1,        # eliminación
                dist[i, j - 1] + 1,        # inserción
                dist[i - 1, j - 1] + cost  # sustitución
            )

    return int(dist[rows - 1, cols - 1])


def load_dataset(csv_path: str) -> pd.DataFrame:
    # Cargar el CSV en un DataFrame de pandas.
    return pd.read_csv(csv_path)


def find_target(df: pd.DataFrame, target_title: str) -> pd.Series:
    # Localizar la fila de la película objetivo por título.

    # Busca en `title` y, si existe, en `original_title` (búsqueda case-insensitive).
    # Lanza `ValueError` si no se encuentra.
    
    matches = df[df['title'].str.contains(target_title, case=False, na=False)]
    if matches.empty and 'original_title' in df.columns:
        matches = df[df['original_title'].str.contains(target_title, case=False, na=False)]
    if matches.empty:
        raise ValueError(f"No se encontró la película '{target_title}' en el dataset.")
    return matches.iloc[0]


def sample_movies(df: pd.DataFrame, target_idx: int, n: int = 100) -> pd.DataFrame:
    # Tomar una muestra aleatoria de `n` películas excluyendo la objetivo.

    # Devuelve un DataFrame con una columna `index` que contiene el índice original.
    
    df_others = df.drop(index=target_idx)
    n_sample = min(n, len(df_others))
    sampled = df_others.sample(n=n_sample, random_state=42).reset_index(drop=False)
    return sampled


def compute_top_k_similar(target_title: str, sample_df: pd.DataFrame, k: int = 3) -> List[Dict]:
    # Calcular la distancia Levenshtein entre `target_title` y cada título de la muestra.

    # Devuelve una lista con los `k` elementos con menor distancia.
    # Cada elemento es un dict con `original_index`, `title` y `distance`.

    def normalize(s):
        return '' if s is None else str(s).lower().strip()

    target_norm = normalize(target_title)
    results = []
    for _, row in sample_df.iterrows():
        other_title = normalize(row.get('title', ''))
        d = levenshtein_distance(target_norm, other_title)
        results.append({'original_index': int(row['index']), 'title': row.get('title', ''), 'distance': int(d)})

    # Ordenar por distancia ascendente (0 = idéntico)
    results.sort(key=lambda x: x['distance'])
    return results[:k]


def main():
    # Punto de entrada: parsear argumentos y ejecutar el flujo principal.
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', default='tmdb_5000_movies.csv', help='Ruta al archivo CSV')
    parser.add_argument('--target', default='Star Trek Beyond', help='Título de la película objetivo')
    parser.add_argument('--sample', type=int, default=100, help='Número de películas a muestrear del dataset')
    args = parser.parse_args()

    # Cargar datos y localizar objetivo
    df = load_dataset(args.csv)
    target_row = find_target(df, args.target)
    # obtener índice original (puede ser int)
    target_idx = int(target_row.name)
    print(f"Película objetivo: {target_row['title']} (índice original: {target_idx})")

    # Tomar muestra y calcular similitudes
    sample_df = sample_movies(df, target_idx, n=args.sample)
    print(f"Muestra tomada: {len(sample_df)} películas")

    top3 = compute_top_k_similar(target_row['title'], sample_df, k=3)
    print('\nTop 3 películas más similares (según distancia de Levenshtein):')
    for i, item in enumerate(top3, start=1):
        print(f"{i}. {item['title']} (índice original: {item['original_index']}) — distancia: {item['distance']}")


if __name__ == '__main__':
    main()
