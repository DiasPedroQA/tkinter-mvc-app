# from models.path_system_model import CaminhoModel


# def exibir_tabela_json(lista_modelos: list[dict[str, CaminhoModel]]) -> None:
#     if not lista_modelos:
#         print("Nenhum caminho válido encontrado.")
#         return

#     # Obtemos os nomes das colunas
#     colunas = list(lista_modelos[0].keys())

#     # Calcula a largura máxima de cada coluna
#     larguras: dict[str, int] = {
#         coluna: max(
#             len(str(coluna)), max(len(str(item[coluna])) for item in lista_modelos)
#         )
#         for coluna in colunas
#     }

#     # Função para imprimir uma linha formatada
#     def formatar_linha(valores: list[str]) -> str:
#         return " | ".join(f"{v:<{larguras[c]}}" for v, c in zip(valores, colunas))

#     # Linha de separação
#     separador: str = "-+-".join("-" * larguras[c] for c in colunas)

#     # Cabeçalho
#     print("\n📁 Tabela de Caminhos:\n")
#     print(formatar_linha(valores=colunas))
#     print(separador)

#     # Dados
#     for item in lista_modelos:
#         valores: list[str] = [str(item[c]) for c in colunas]
#         print(formatar_linha(valores=valores))

#     print()  # Linha em branco ao final
