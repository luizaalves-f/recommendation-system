# Esta funcao valida a estrutura das regras carregadas do arquivo externo.
# O objetivo e garantir que os dados tenham o formato esperado antes de serem
# utilizados pela aplicacao.
def validar_regras(regras):
    if not isinstance(regras, list):
        raise ValueError("As regras devem ser armazenadas em uma lista.")

    for regra in regras:
        if not isinstance(regra, dict):
            raise ValueError("Cada regra deve ser representada por um dicionario.")

        if "condicao" not in regra or "recomendacoes" not in regra:
            raise ValueError("Cada regra deve conter 'condicao' e 'recomendacoes'.")

        if not isinstance(regra["condicao"], dict):
            raise ValueError("O campo 'condicao' deve ser um dicionario.")

        if "genero" not in regra["condicao"]:
            raise ValueError("O campo 'condicao' deve conter a chave 'genero'.")

        if not isinstance(regra["condicao"]["genero"], str) or not regra["condicao"]["genero"].strip():
            raise ValueError("O genero da regra deve ser um texto nao vazio.")

        if not isinstance(regra["recomendacoes"], list) or not regra["recomendacoes"]:
            raise ValueError("O campo 'recomendacoes' deve ser uma lista nao vazia.")

        for recomendacao in regra["recomendacoes"]:
            if not isinstance(recomendacao, str) or not recomendacao.strip():
                raise ValueError("Cada recomendacao deve ser um texto nao vazio.")
