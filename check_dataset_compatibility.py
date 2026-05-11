import pandas as pd

# 1. Carregar os arquivos
movies = pd.read_csv('tmdb_5000_movies.csv')
credits = pd.read_csv('tmdb_5000_credits.csv')

# 2. Verificar a Correspondência (antes de mesclar)
# Este passo é muito útil e vai te dar total confiança!
# Ele verifica se todos os IDs em 'credits' existem em 'movies'
ids_em_credits_existem = credits['movie_id'].isin(movies['id']).all()
print(f"Todos os IDs do arquivo de créditos estão no de filmes? {ids_em_credits_existem}")
# A saída provavelmente será 'True', confirmando a compatibilidade!

# 3. Padronizar o nome da coluna chave para 'id'
credits = credits.rename(columns={'movie_id': 'id'})

# 4. Realizar o Merge (combinação) dos dois DataFrames pela coluna 'id'
df_completo = pd.merge(movies, credits, on='id')