# Sistema simples de recomendacao de filmes desenvolvido em Python.
# Neste exemplo, a ideia central e o paradigma orientado a dados:
# as recomendacoes sao definidas por estruturas de dados, e o programa
# interpreta essas estruturas para decidir o que exibir ao usuario.

import json
import sys
from pathlib import Path
from recommender import recomendar
from rule_validator import validar_regras

CAMINHO_REGRAS = Path(__file__).resolve().parent / "regras_recomendacao.json"


# Esta funcao carrega as regras de recomendacao a partir
# de um arquivo JSON externo.
# Alem de ler os dados, ela trata erros de arquivo e de formato,
# aumentando a robustez da aplicacao.
def carregar_regras():
    try:
        with open(CAMINHO_REGRAS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            regras = dados["regras_recomendacao"]
            validar_regras(regras)
            return regras
    except FileNotFoundError:
        print("Arquivo de regras nao encontrado.")
    except json.JSONDecodeError:
        print("Erro ao ler o arquivo JSON.")
    except KeyError:
        print("Estrutura do arquivo JSON inválida.")
    except ValueError as erro:
        print(f"Erro de validacao das regras: {erro}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    return None


# Esta funcao exibe o menu de opcoes com base nas regras cadastradas.
# Como o menu e construido a partir dos dados, a interface acompanha
# automaticamente a estrutura definida no arquivo externo.
def mostrar_menu(regras):
    for i, regra in enumerate(regras, start=1):
        genero = regra["condicao"]["genero"]
        print(f"{i} - {genero.capitalize()}")


# Esta funcao coleta e valida a escolha do usuario.
# O objetivo e garantir que o perfil retornado esteja coerente
# com as opcoes disponiveis no conjunto de regras.
def obter_usuario(regras):
    escolha = input("Escolha um genero: ")

    if not escolha.isdigit():
        print("Entrada inválida")
        return None

    indice = int(escolha) - 1

    if indice < 0 or indice >= len(regras):
        print("Opção inválida")
        return None

    usuario = {
        "genero": regras[indice]["condicao"]["genero"]
    }

    if not usuario.get("genero"):
        print("Genero invalido")
        return None

    return usuario


# As regras de recomendacao foram movidas para um arquivo JSON externo.
# Com isso, os dados ficam separados da logica do programa, reforcando
# a abordagem orientada a dados e facilitando a reutilizacao da estrutura
# em outros contextos de recomendacao.
regras = carregar_regras()

# O restante da execucao so acontece se as regras forem carregadas corretamente.
# Isso impede que o programa continue em um estado inconsistente.
if regras is None:
    print("Falha ao carregar regras.")
    sys.exit()

mostrar_menu(regras)

usuario = obter_usuario(regras)

if usuario is not None:
    recomendacoes = recomendar(usuario, regras)
    print("\nRecomendações:")
    for filme in recomendacoes:
        print("-", filme)
