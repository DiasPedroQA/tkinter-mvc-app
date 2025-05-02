# -*- coding: utf-8 -*-
# mypy: ignore-errors
# pylint: disable=C0103, C0114, C0115, C0116, C0301, W0613, W0621, W0718

"""
Simulador de operações CRUD para arquivos e diretórios.
Permite criar, ler e atualizar caminhos com respostas padronizadas.
"""

# from app.backend.controller.app_controller import CaminhoController
# from app.backend.tools.app_ferramentas import Validador

# # Caminhos reais
# BASE_REAL = "/home/pedro-pm-dias/Downloads"
# CAMINHO_REAL_PASTA = f"{BASE_REAL}/Firefox"
# CAMINHO_REAL_ARQUIVO = f"{CAMINHO_REAL_PASTA}/bookmarks.html"

# # Caminhos fake
# BASE_FAKE = "/fake/teste"
# CAMINHO_FAKE_PASTA = f"{BASE_FAKE}/pasta_fake"
# CAMINHO_FAKE_ARQUIVO = f"{CAMINHO_FAKE_PASTA}/arquivo_fake.txt"


# def processar_entrada(entrada: dict, validador: Validador = Validador()) -> dict:
#     caminho = entrada.get("caminho")
#     acao = entrada.get("acao")

#     # FLUXO DE LEITURA: só se for um caminho real
#     if acao == "ler":
#         if not validador.existe(caminho):
#             return {"status": "erro", "mensagem": "Caminho real não encontrado"}

#         if validador.eh_arquivo(caminho):
#             print(f"[LOG] Lendo ARQUIVO real: {caminho}")
#         elif validador.eh_pasta(caminho):
#             print(f"[LOG] Lendo PASTA real: {caminho}")
#         else:
#             return {"status": "erro", "mensagem": "Tipo de caminho não identificado"}

#     else:
#         caminho_fake = gerar_caminho_fake(caminho)
#         entrada["caminho"] = caminho_fake
#         print(f"[LOG] {acao.upper()} em caminho FAKE: {caminho_fake}")

#     return CaminhoController().executar(entrada)


# def gerar_caminho_fake(caminho_usuario: str) -> str:
#     """
#     Cria uma rota fake a partir do caminho informado pelo usuário
#     Ex: "/documentos/novo.txt" → "/fake/teste/documentos/novo.txt"
#     """
#     return f"{BASE_FAKE}/{caminho_usuario.removeprefix(" / ")}"
