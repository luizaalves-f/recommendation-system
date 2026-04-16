# Sistema simples de recomendacao de filmes desenvolvido em Python.
# Neste exemplo, a ideia central e o paradigma orientado a dados:
# as recomendacoes sao definidas por estruturas de dados, e o programa
# interpreta essas estruturas para decidir o que exibir ao usuario.

import json
from recomendador import recomendar

# As regras de recomendacao foram movidas para um arquivo JSON externo.
# Com isso, os dados ficam separados da logica do programa, reforcando
# a abordagem orientada a dados e facilitando a reutilizacao da estrutura
# em outros contextos de recomendacao.
with open("regras_recomendacao.json", "r", encoding="utf-8") as f:
    dados = json.load(f)
    regras = dados["regras_recomendacao"]

# O menu e gerado automaticamente a partir das regras cadastradas.
# Isso evita repeticao de codigo e demonstra que a interface tambem
# pode ser construida com base nos dados disponiveis.
for i, regra in enumerate(regras, start=1):
    genero = regra["condicao"]["genero"]
    print(f"{i} - {genero.capitalize()}")

# O usuario informa sua preferencia selecionando um dos generos exibidos.
escolha = input("Escolha um genero: ")

# A primeira validacao verifica se a entrada pode ser convertida em numero.
# Esse tratamento reduz erros de execucao e melhora a confiabilidade do programa.
if not escolha.isdigit():
    print("Entrada invalida")
else:
    indice = int(escolha) - 1

    # Aqui e verificado se o numero informado corresponde a uma opcao existente.
    # Assim, o sistema impede acessos fora dos limites da lista de regras.
    if indice < 0 or indice >= len(regras):
        print("Opcao invalida")
    else:
        # O perfil do usuario tambem e representado por dados.
        # Nesse caso, apenas o genero escolhido e necessario para a busca.
        usuario = {
            "genero": regras[indice]["condicao"]["genero"]
        }

        # A resposta final surge da interpretacao das regras cadastradas.
        # Isso evidencia o papel dos dados na conducao do comportamento do sistema.
        recomendacoes = recomendar(usuario, regras)
        print("\nRecomendacoes:")
        for filme in recomendacoes:
            print("-", filme)
