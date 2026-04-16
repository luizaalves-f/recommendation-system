from pathlib import Path
import json

from flask import Flask, request, jsonify

from recommender import recomendar
from rule_validator import validar_regras

app = Flask(__name__)
CAMINHO_REGRAS = Path(__file__).resolve().parent / "regras_recomendacao.json"


# Esta funcao carrega as regras de recomendacao a partir
# de um arquivo JSON externo.
# Alem de ler os dados, ela trata erros esperados de arquivo e de formato,
# aumentando a robustez da aplicacao web.
def carregar_regras():
    try:
        with open(CAMINHO_REGRAS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            regras = dados["regras_recomendacao"]
            validar_regras(regras)
            return regras
    except FileNotFoundError:
        app.logger.error("Arquivo de regras nao encontrado.")
    except json.JSONDecodeError:
        app.logger.error("Erro ao ler o arquivo JSON.")
    except KeyError:
        app.logger.error("Estrutura do arquivo JSON invalida.")
    except ValueError as erro:
        app.logger.error(f"Erro de validacao das regras: {erro}")

    return None


# Esta rota inicial permite verificar rapidamente se a aplicacao Flask
# esta em execucao e orienta como utilizar o endpoint principal.
@app.route("/", methods=["GET"])
def pagina_inicial():
    return jsonify({
        "mensagem": "API de recomendacao de filmes em execucao.",
        "endpoint": "/recomendar",
        "metodo": "POST",
        "exemplo_body": {"genero": "acao"},
    })


@app.route("/recomendar", methods=["POST"])
def recomendar_filmes():
    # As regras sao carregadas no momento da requisicao.
    # Isso evita que a API fique permanentemente em erro caso o arquivo
    # seja corrigido depois da inicializacao do servidor.
    regras = carregar_regras()

    if regras is None:
        return jsonify({"erro": "Falha ao carregar regras."}), 500

    # O corpo da requisicao deve estar em formato JSON.
    # O uso de silent=True impede excecoes e permite tratar o erro com clareza.
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"erro": "Envie um corpo JSON valido."}), 400

    genero = data.get("genero")

    # Esta validacao garante que o campo 'genero' exista
    # e contenha um texto valido para a recomendacao.
    if not isinstance(genero, str) or not genero.strip():
        return jsonify({"erro": "Genero nao informado ou invalido."}), 400

    usuario = {"genero": genero.strip().lower()}
    recomendacoes = recomendar(usuario, regras)

    return jsonify({"recomendacoes": recomendacoes})


if __name__ == "__main__":
    app.run(debug=True)
