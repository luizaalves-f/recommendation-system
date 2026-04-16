# Sistema simples de recomendacao de filmes desenvolvido em Python.
# Neste exemplo, a ideia central e o paradigma orientado a dados:
# as recomendacoes sao definidas por estruturas de dados, e o programa
# interpreta essas estruturas para decidir o que exibir ao usuario

import json

# Esta funcao carrega as regras de recomendacao a partir
# de um arquivo JSON externo.
def carregar_regras():
    with open("regras_recomendacao.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
        return dados["regras_recomendacao"]

# Esta funcao representa o motor de recomendacao.
# Ela percorre a base de regras e procura uma condicao compativel
# com o genero escolhido pelo usuario.
def recomendar(usuario, regras):
    for regra in regras:
        if regra["condicao"]["genero"] == usuario["genero"]:
            return regra["recomendacoes"]
    return ["Nenhuma recomendacao encontrada"]

# As regras de recomendacao foram movidas para um arquivo JSON externo.
# Com isso, os dados ficam separados da logica do programa, reforcando
# a abordagem orientada a dados e facilitando a reutilizacao da estrutura
# em outros contextos de recomendacao.
regras_recomendacao = carregar_regras()

# O menu e gerado automaticamente a partir das regras cadastradas.
# Isso evita repeticao de codigo e demonstra que a interface tambem
# pode ser construida com base nos dados disponiveis.
for i, regra in enumerate(regras_recomendacao, start=1):
    genero = regra["condicao"]["genero"]
    print(f"{i} - {genero.capitalize()}")

# O usuario informa sua preferencia selecionando um dos generos exibidos.
escolha = input("Qual genero de filme voce gosta? ")

# A primeira validacao verifica se a entrada pode ser convertida em numero.
# Esse tratamento reduz erros de execucao e melhora a confiabilidade do programa.
if not escolha.isdigit():
    print("Entrada invalida")
else:
    indice = int(escolha) - 1

    # Aqui e verificado se o numero informado corresponde a uma opcao existente.
    # Assim, o sistema impede acessos fora dos limites da lista de regras.
    if indice < 0 or indice >= len(regras_recomendacao):
        print("Opcao invalida")
    else:
        # O perfil do usuario tambem e representado por dados.
        # Nesse caso, apenas o genero escolhido e necessario para a busca.
        usuario = {
            "genero": regras_recomendacao[indice]["condicao"]["genero"]
        }

        # A resposta final surge da interpretacao das regras cadastradas.
        # Isso evidencia o papel dos dados na conducao do comportamento do sistema.
        recomendacoes = recomendar(usuario, regras_recomendacao)
        print("\nRecomendacoes:")
        for filme in recomendacoes:
            print("-", filme)
