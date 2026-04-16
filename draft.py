# Sistema simples de recomendacao de filmes desenvolvido em Python.
# Neste exemplo, a ideia central e o paradigma orientado a dados:
# as recomendacoes sao definidas por estruturas de dados, e o programa
# interpreta essas estruturas para decidir o que exibir ao usuario

# Esta funcao representa o motor de recomendacao.
# Ela percorre a base de regras e procura uma condicao compativel
# com o genero escolhido pelo usuario.
def recomendar(usuario, regras):
    for regra in regras:
        if regra["condicao"]["genero"] == usuario["genero"]:
            return regra["recomendacoes"]
    return ["Nenhuma recomendacao encontrada"]


# As regras foram organizadas em uma lista de dicionarios.
# Essa modelagem mostra uma abordagem data-driven, pois a logica
# permanece a mesma mesmo quando os dados de recomendacao mudam.
# Para ampliar o sistema, basta adicionar novas regras a esta estrutura.
regras_recomendacao = [
    {"condicao": {"genero": "acao"}, "recomendacoes": ["Mad Max", "John Wick", "Gladiador"]},
    {"condicao": {"genero": "romance"}, "recomendacoes": ["Diario de uma Paixao", "Titanic", "La La Land"]},
    {"condicao": {"genero": "comedia"}, "recomendacoes": ["Se Eu Fosse Voce", "As Branquelas", "Se Beber, Nao Case!"]},
    {"condicao": {"genero": "terror"}, "recomendacoes": ["O Exorcista", "Invocacao do Mal", "It: A Coisa"]},
    {"condicao": {"genero": "suspense"}, "recomendacoes": ["Parasite", "The Girl with the Dragon Tattoo", "Gone Girl"]},
    {"condicao": {"genero": "drama"}, "recomendacoes": ["O Poderoso Chefao", "O Iluminado", "O Homem do Meio-Dia"]},
    {"condicao": {"genero": "ficcao"}, "recomendacoes": ["Interestelar", "Matrix", "Blade Runner"]},
]

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
