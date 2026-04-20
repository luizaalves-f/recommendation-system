# Recommendation System

Sistema de recomendação de filmes desenvolvido com Flask, SQLite e paradigma **Data-Driven** (orientado a dados).  
O comportamento do sistema é guiado pelos dados armazenados no banco, sem regras de negócio fixas no código.

## 📁 Estrutura do Projeto

- `app.py` – API Flask com endpoints de recomendação
- `schema.sql` – Definição do banco de dados (tabelas, índices, views)
- `recsys.db` – Banco SQLite (gerado após execução do schema)
- `scripts/` – (opcional) scripts para popular o banco a partir de datasets

## 🧰 Pré-requisitos

- Python 3.8+
- SQLite3 (geralmente já incluso no Python)
- Git

## 🚀 Configuração e Execução

```bash
# 1) Clonar o repositório
git clone https://github.com/luizaalves-f/recommendation-system
cd recommendation-system

# 2) Criar e ativar ambiente virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate.bat
# Linux/Mac:
# source .venv/bin/activate

# 3) Atualizar pip e instalar dependências
python -m pip install --upgrade pip
python -m pip install flask pandas numpy scikit-learn

# 4) Criar o banco de dados (executar o schema)
sqlite3 recsys.db < schema.sql

# 5) (Opcional) Popular o banco com dados iniciais
# python scripts/populate_db.py

# 6) Executar a aplicação
python app.py