# # -*- coding: utf-8 -*-

# """
# Modelos para representar arquivos, pastas e caminhos do sistema.
# """

# from dataclasses import dataclass, field  # noqa: E402
# from typing import Any

# # from src.tools.path_operations import GerenciadorDeCaminhos  # noqa: E402


# @dataclass
# class ObjetoCaminho:
#     caminho: str
#     tipo_item: str
#     ultima_modificacao: str = ""
#     data_acesso: str = ""
#     data_criacao: str = ""

#     @classmethod
#     def from_dict(cls, geral: dict[str, Any], datas: dict[str, Any]) -> "ObjetoCaminho":
#         """
#         Cria uma instância de ObjetoCaminho a partir de dicionários de dados.

#         Args:
#             geral: Dicionário com informações gerais do caminho.
#             datas: Dicionário com informações de datas.

#         Returns:
#             ObjetoCaminho: Instância inicializada.
#         """
#         return cls(
#             caminho=geral.get("caminho_corrigido", ""),
#             tipo_item=geral.get("tipo_caminho", ""),
#             ultima_modificacao=datas.get("data_modificacao", ""),
#             data_acesso=datas.get("data_acesso", ""),
#             data_criacao=datas.get("data_criacao", ""),
#         )


# @dataclass
# class ObjetoArquivo(ObjetoCaminho):
#     extensao: str = ""
#     tamanho_bytes: int = 0
#     permissoes: str = ""

#     @classmethod
#     def from_dict(
#         cls, geral: dict[str, Any], datas: dict[str, Any], **kwargs: dict[str, Any]
#     ) -> "ObjetoArquivo":
#         arquivo = kwargs.get("arquivo", {})
#         caminho_objeto = super().from_dict(geral, datas)
#         return cls(
#             caminho=caminho_objeto.caminho,
#             tipo_item=caminho_objeto.tipo_item,
#             ultima_modificacao=caminho_objeto.ultima_modificacao,
#             data_acesso=caminho_objeto.data_acesso,
#             data_criacao=caminho_objeto.data_criacao,
#             extensao=arquivo.get("extensao", ""),
#             tamanho_bytes=arquivo.get("tamanho_bytes", 0),
#             permissoes=arquivo.get("permissoes", ""),
#         )


# @dataclass
# class ObjetoPasta(ObjetoCaminho):
#     subitens: list[str] = field(default_factory=list)
#     tamanho_total_bytes: int = 0
#     permissoes: str = ""

#     @classmethod
#     def from_dict(
#         cls, geral: dict[str, Any], datas: dict[str, Any], **kwargs: dict[str, Any]
#     ) -> "ObjetoPasta":
#         pasta = kwargs.get("pasta", {})
#         caminho_objeto = super().from_dict(geral, datas)
#         return cls(
#             caminho=caminho_objeto.caminho,
#             tipo_item=caminho_objeto.tipo_item,
#             ultima_modificacao=caminho_objeto.ultima_modificacao,
#             data_acesso=caminho_objeto.data_acesso,
#             data_criacao=caminho_objeto.data_criacao,
#             subitens=pasta.get("subitens", []),
#             tamanho_total_bytes=pasta.get("tamanho_total_bytes", 0),
#             permissoes=pasta.get("permissoes", ""),
#         )


# if __name__ == "__main__":
#     # Exemplo de dados simulados
#     dados_arquivo: dict[str, Any] = {
#         "geral": {
#             "caminho_original": "~/Downloads/Firefox/bookmarks.html",
#             "caminho_corrigido": "/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html",
#             "tipo_caminho": "Arquivo",
#             "nome_item": "bookmarks.html",
#             "diretorio_pai_caminho": "/home/pedro-pm-dias/Downloads/Firefox",
#             "caminho_absoluto": True,
#             "caminho_existe": True,
#             "caminho_foi_corrigido": False,
#         },
#         "datas": {
#             "data_modificacao": "07/05/2025 16:17:35",
#             "data_acesso": "10/05/2025 06:35:32",
#             "data_criacao": "07/05/2025 16:17:35",
#         },
#         "arquivo": {
#             "extensao": ".html",
#             "tamanho_bytes": 732677,
#             "tamanho_formatado": "715.50 KB",
#             "permissoes": "rw-r--r-- pedro-pm-dias:pedro-pm-dias",
#         },
#     }

#     dados_pasta: dict[str, Any] = {
#         "geral": {
#             "caminho_original": "~/Downloads/",
#             "caminho_corrigido": "/home/pedro-pm-dias/Downloads",
#             "tipo_caminho": "Pasta",
#             "nome_item": "Downloads",
#             "diretorio_pai_caminho": "/home/pedro-pm-dias",
#             "caminho_absoluto": True,
#             "caminho_existe": True,
#             "caminho_foi_corrigido": False,
#         },
#         "datas": {
#             "data_modificacao": "11/05/2025 02:56:52",
#             "data_acesso": "11/05/2025 02:57:35",
#             "data_criacao": "11/05/2025 02:56:52",
#         },
#         "pasta": {
#             "quantidade_itens": 110,
#             "tamanho_total_bytes": 11942036209,
#             "tamanho_total_formatado": "11.12 GB",
#             "permissoes": "rwxr-xr-x pedro-pm-dias:pedro-pm-dias",
#         },
#     }

#     # Criando o objeto de arquivo
#     arquivo = ObjetoArquivo.from_dict(
#         geral=dados_arquivo["geral"], datas=dados_arquivo["datas"], arquivo=dados_arquivo["arquivo"]
#     )
#     print("\n=== Detalhes do Arquivo ===")
#     print(arquivo)

#     # Criando o objeto de pasta
#     pasta = ObjetoPasta.from_dict(
#         geral=dados_pasta["geral"], datas=dados_pasta["datas"], pasta=dados_pasta["pasta"]
#     )
#     print("\n=== Detalhes da Pasta ===")
#     print(pasta)
