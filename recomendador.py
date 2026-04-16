# Esta funcao representa o motor de recomendacao.
# Ela percorre a base de regras e procura uma condicao compativel
# com o genero escolhido pelo usuario.
def recomendar(usuario, regras):
    for regra in regras:
        if regra["condicao"]["genero"] == usuario["genero"]:
            return regra["recomendacoes"]
    return ["Nenhuma recomendacao encontrada"]
