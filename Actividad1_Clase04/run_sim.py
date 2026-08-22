import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('tmdb_5000_movies - Copy (1).csv')
df['overview'] = df['overview'].fillna('')

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['overview'])

target_idx = df[df['title'] == 'Star Trek Beyond'].index[0]
cosine_sim = cosine_similarity(tfidf_matrix[target_idx], tfidf_matrix).flatten()
df['similitud'] = cosine_sim

top3 = df[df['title'] != 'Star Trek Beyond'].sort_values(by='similitud', ascending=False).head(3)
print('Top 3 más similares a "Star Trek Beyond":')
print(top3[['title', 'similitud', 'overview']].to_string(index=False))
