from pathlib import Path
import json
from rule_validator import validar_regras

CAMINHO_REGRAS = Path(__file__).resolve().parent / "regras_recomendacao.json"

# Esta funcao carrega as regras de recomendacao a partir
# de um arquivo JSON externo.
# Alem de ler os dados, ela trata erros esperados de arquivo e de formato,
# aumentando a robustez da aplicacao web.
def carregar_regras():
    with open(CAMINHO_REGRAS, "r", encoding="utf-8") as f:
        dados = json.load(f)
        regras = dados["regras_recomendacao"]
        validar_regras(regras)
        return regras