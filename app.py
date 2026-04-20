import json

from flask import Flask, request, jsonify

from recommender import recomendar
from rule_loader import carregar_regras

app = Flask(__name__)

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

# Endpoint principal da API: /recomendar
@app.route("/recomendar", methods=["POST"])
def recomendar_filmes():
    try:
        # As regras sao carregadas no momento da requisicao.
        # Isso evita que a API fique permanentemente em erro caso o arquivo
        # seja corrigido depois da inicializacao do servidor.
        regras = carregar_regras()
    except FileNotFoundError:
        app.logger.error("Arquivo de regras nao encontrado.")
        return jsonify({"erro": "Falha ao carregar regras."}), 500
    except json.JSONDecodeError:
        app.logger.error("Erro ao ler o arquivo JSON.")
        return jsonify({"erro": "Falha ao carregar regras."}), 500
    except KeyError:
        app.logger.error("Estrutura do arquivo JSON invalida.")
        return jsonify({"erro": "Falha ao carregar regras."}), 500
    except ValueError as erro:
        app.logger.error(f"Erro de validacao das regras: {erro}")
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
