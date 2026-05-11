# Recommendation System

Sistema de recomendacao de filmes desenvolvido com Flask e SQLite. O banco e populado a partir dos arquivos `tmdb_5000_movies.csv` e `tmdb_5000_credits.csv`, seguindo a estrutura definida em `schema.sql`.

## Estrutura

- `app.py`: API Flask.
- `schema.sql`: estrutura do banco SQLite.
- `populate_db.py`: recria e popula `recsys.db` com os dados dos CSVs.
- `recsys.db`: banco SQLite gerado localmente.
- `tmdb_5000_movies.csv`: dados principais dos filmes.
- `tmdb_5000_credits.csv`: elenco/equipe tecnica, usado aqui para extrair diretores.
- `main.py`, `recommender.py`, `rule_loader.py`, `rule_validator.py`: versao anterior baseada em regras JSON/terminal.

## Pre-requisitos

- Python 3.8+
- Git
- SQLite via modulo `sqlite3` do Python

Instale as dependencias usadas ate agora:

```bash
python -m pip install --upgrade pip
python -m pip install flask pandas
```

## Popular o banco

Com os arquivos `tmdb_5000_movies.csv` e `tmdb_5000_credits.csv` na raiz do projeto, execute:

```bash
python populate_db.py
```

O script:

- recria as tabelas conforme `schema.sql`;
- popula `languages`, `movies`, `genres`, `directors`;
- cria os relacionamentos `movie_genres` e `movie_directors`;
- cria alguns usuarios e avaliacoes ficticias para teste.

Ao final, ele imprime as contagens inseridas em cada tabela.

## Executar a API Flask

Na raiz do projeto:

```bash
python app.py
```

Por padrao, a API fica disponivel em:

```text
http://127.0.0.1:5000
```

## Endpoints

### `GET /`

Verifica se a API esta no ar e mostra os endpoints disponiveis.

PowerShell:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/" -Method Get
```

### `GET /generos`

Lista os generos existentes no banco.

PowerShell:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/generos" -Method Get
```

### `POST /recomendar`

Retorna recomendacoes de filmes por genero consultando o banco SQLite.

PowerShell:

```powershell
$body = @{ genero = "Action" } | ConvertTo-Json
Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/recomendar" `
  -Method Post `
  -Body $body `
  -ContentType "application/json"
```

Exemplo de corpo JSON:

```json
{
  "genero": "Action"
}
```

O endpoint aceita os nomes dos generos como estao armazenados no banco, por exemplo `Action`, `Comedy`, `Drama` e `Science Fiction`. Consulte `GET /generos` para ver os valores disponiveis.

## Sobre o endpoint antigo

Antes, o endpoint `/recomendar` usava `regras_recomendacao.json`. Depois da migracao para SQLite, esse comportamento foi atualizado em `app.py`: agora o endpoint consulta as tabelas `movies`, `genres`, `movie_genres` e a view `movie_popularity`.

Ou seja: o contrato principal continua parecido, mas agora o valor de `genero` deve vir dos dados retornados por `GET /generos`, e a fonte das recomendacoes e o banco `recsys.db`.

## Validacoes uteis

Checar se os CSVs sao compativeis:

```bash
python check_dataset_compatibility.py
```

Ver colunas do arquivo de filmes:

```bash
python check.py
```

Compilar os scripts Python para verificar erro de sintaxe:

```bash
python -m py_compile app.py populate_db.py
```
