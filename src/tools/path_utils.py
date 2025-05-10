# """
# Módulo que fornece utilitários para manipulação de caminhos.

# Este módulo contém funções para normalizar caminhos e tentar corrigir caminhos inválidos
# com base em similaridade, utilizando regex e operações no sistema de arquivos.
# """

# import re
# from pathlib import Path
# import difflib


# def normalizar_caminho(caminho_bruto: str) -> Path:
#     """Limpa e normaliza um caminho bruto usando regex."""
#     caminho_normal = caminho_bruto.strip()
#     caminho_normal = re.sub(r"[\\]+", "/", caminho_normal)  # barras invertidas para /
#     caminho_normal = re.sub(
#         r"\s*/\s*", "/", caminho_normal
#     )  # remove espaços ao redor das barras
#     caminho_normal = re.sub(r"/{2,}", "/", caminho_normal)  # barras duplicadas
#     caminho_normal = re.sub(
#         r"[<>:\"|?*]", "", caminho_normal
#     )  # remove caracteres inválidos

#     # Remove prefixos "../" até que não existam mais no início
#     while caminho_normal.startswith("../"):
#         caminho_normal = caminho_normal[3:]

#     return Path(caminho_normal)


# def tentar_corrigir_caminho(caminho_com_erro: Path) -> Path:
#     """Tenta corrigir partes do caminho com base em similaridade."""
#     partes = caminho_com_erro.parts
#     caminho_atual = Path(partes[0]) if caminho_com_erro.is_absolute() else Path()
#     for parte in partes[1:]:
#         if not caminho_atual.exists():
#             return None
#         try:
#             opcoes = [p.name for p in caminho_atual.iterdir()]
#         except (PermissionError, FileNotFoundError, NotADirectoryError):
#             return None
#         caminho_similares = difflib.get_close_matches(parte, opcoes, n=1, cutoff=0.6)
#         caminho_atual = (
#             caminho_atual / caminho_similares[0]
#             if caminho_similares
#             else caminho_atual / parte
#         )
#     return caminho_atual if caminho_atual.exists() else None
