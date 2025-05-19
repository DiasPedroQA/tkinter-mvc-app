# from models.path_system_model import CaminhoModel
# from tools.path_toolkit import validar_caminho
# # from tools.path_utils import (
# #     atualizar_arquivo,
# #     criar_novo_arquivo,
# #     gerar_id_para_path,
# #     ler_conteudo,
# # )


# class PathController:
#     def __init__(self, caminhos: list[str]) -> None:
#         self.caminhos: list[str] = caminhos

#     # === MÉTODOS READ ===

#     def ler_caminhos(self) -> list[dict[str, CaminhoModel]]:
#         """Lê e valida todos os caminhos fornecidos na inicialização."""
#         resultados: list[CaminhoModel] = []
#         for caminho in self.caminhos:
#             if validar_caminho(caminho=caminho):
#                 modelo: CaminhoModel = CaminhoModel.from_path(caminho_str=caminho)
#                 resultados.append(modelo)
#         return [m.__dict__ for m in resultados]

#     # def read_id_path(self, path: str) -> str:
#     #     """Gera um ID único para um caminho."""
#     #     return gerar_id_para_path(path)

#     # def read_path_content(self, path: str) -> str:
#     #     """Lê o conteúdo do arquivo, se aplicável."""
#     #     return ler_conteudo(path)

#     # # === MÉTODOS CREATE / UPDATE ===

#     # def create_new_path(self, path: str, conteudo: str) -> str:
#     #     """Cria um novo arquivo com o conteúdo fornecido."""
#     #     return criar_novo_arquivo(path, conteudo)

#     # def update_path(self, path: str, conteudo: str) -> str:
#     #     """Atualiza o conteúdo de um arquivo existente."""
#     #     return atualizar_arquivo(path, conteudo)

#     # # === MÉTODO UTILITÁRIO ===

#     # @staticmethod
#     # def converter_conteudo(conteudo: str) -> str:
#     #     """Exemplo simples de conversão: transforma em caixa alta."""
#     #     return conteudo.upper()
