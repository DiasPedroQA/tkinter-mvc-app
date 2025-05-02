# main.py
# -*- coding: utf-8 -*-
# pylint: disable=C, R0911, E0401

"""
Módulo de modelos para manipulação de arquivos e pastas.

Contém:
- ArquivoModel: interface para operações com arquivos (criar, ler, atualizar).
- PastaModel: interface para operações com pastas (criar, ler, atualizar).
"""

# import shutil
# from typing import Optional, Dict, List
# from pathlib import Path

# from backend.tools.app_ferramentas import validar_caminho


# class ManipuladorDeCaminhos:
#     """
#     Classe para criação, leitura e atualização de arquivos e pastas.
#     """

#     @staticmethod
#     def criar_caminho(caminho_a_criar: str, conteudo: Optional[str] = None) -> Dict[str, str]:
#         """
#         Cria arquivo (se conteúdo for passado) ou pasta (se não for).
#         """
#         # caminho_arquivo = True, conteudo = False
#         # caminho_arquivo = False, conteudo = True
#         # caminho_pasta = True, conteudo = True
#         # caminho_pasta = False, conteudo = False

#         caminho = Path(caminho_a_criar)
#         if conteudo is None:
#             try:
#                 with open(file=caminho_a_criar, mode="r", encoding="utf-8") as criar_arquivo:
#                     peso = criar_arquivo.write(conteudo)
#                 return {
#                     "status": "sucesso",
#                     "mensagem": f"Arquivo criado em {caminho} - peso: {peso}"}
#             except FileNotFoundError:
#                 return {
#                     "status": "erro",
#                     "mensagem": "Diretório não encontrado para criação do arquivo.",
#                 }
#             except PermissionError:
#                 return {"status": "erro", "mensagem": "Permissão negada para criar o arquivo."}
#             except IsADirectoryError:
#                 return {
#                     "status": "erro",
#                     "mensagem": "O caminho aponta para uma pasta, não um arquivo.",
#                 }
#             except OSError as e:
#                 return {"status": "erro", "mensagem": f"Erro do sistema ao criar arquivo: {str(e)}"}
#         else:
#             try:
#                 caminho.parent.mkdir(parents=True, exist_ok=True)
#                 caminho.write_text(conteudo, encoding="utf-8")
#                 return {"status": "sucesso", "mensagem": f"Pasta criada em {caminho}"}
#             except FileNotFoundError:
#                 return {
#                     "status": "erro",
#                     "mensagem": "Caminho base inexistente para criar a pasta.",
#                 }
#             except FileExistsError:
#                 return {
#                     "status": "erro",
#                     "mensagem": "Já existe uma pasta com esse nome no local."
#                 }
#             except PermissionError:
#                 return {"status": "erro", "mensagem": "Permissão negada para criar a pasta."}
#             except NotADirectoryError:
#                 return {
#                     "status": "erro",
#                     "mensagem": "Um dos componentes do caminho não é uma pasta.",
#                 }

#     @staticmethod
#     def ler_caminho(caminho: str) -> Dict[str, str]:
#         """
#         Lê um arquivo (retorna conteúdo) ou pasta (retorna lista de itens).
#         """
#         path = Path(caminho)
#         if validar_caminho(caminho, "arquivo") == "Sim":
#             try:
#                 conteudo: str = path.read_text(encoding="utf-8")
#                 return {"status": "sucesso", "conteudo": conteudo}
#             except FileNotFoundError:
#                 return {"status": "erro", "mensagem": "Arquivo não encontrado."}
#             except PermissionError:
#                 return {"status": "erro", "mensagem": "Permissão negada para leitura do arquivo."}
#             except IsADirectoryError:
#                 return {
#                     "status": "erro",
#                     "mensagem": "O caminho fornecido é uma pasta, não um arquivo.",
#                 }
#         elif validar_caminho(caminho, "pasta") == "Sim":
#             try:
#                 conteudo: List[str] = [item.name for item in path.iterdir()]
#                 return {"status": "sucesso", "conteudo": conteudo}
#             except FileNotFoundError:
#                 return {"status": "erro", "mensagem": "Pasta não encontrada."}
#             except PermissionError:
#                 return {"status": "erro", "mensagem": "Permissão negada para leitura da pasta."}
#             except NotADirectoryError:
#                 return {"status": "erro", "mensagem": "O caminho fornecido não é uma pasta."}
#         else:
#             existencia = validar_caminho(caminho, 'existe')
#             return {"status": "erro", "mensagem": f"Erro: caminho inválido. Existe? {existencia}"}

#     @staticmethod
#     def atualizar_caminho(
#         caminho: str,
#         novo_conteudo: Optional[str] = None,
#         novo_nome: Optional[str] = None,
#         nova_localizacao: Optional[str] = None,
#     ) -> Dict[str, str]:
#         """
#         Atualiza conteúdo (se for arquivo), nome e/ou localização (arquivo ou pasta).
#         """
#         path = Path(caminho)
#         tipo = "arquivo" if path.is_file() else "pasta" if path.is_dir() else None
#         if tipo is None:
#             return "Erro: caminho não é um arquivo nem uma pasta."

#         if tipo == "arquivo" and novo_conteudo is not None:
#             try:
#                 path.write_text(novo_conteudo, encoding="utf-8")
#                 return {"status": "sucesso", "mensagem": f"Arquivo atualizado: {caminho}"}
#             except FileNotFoundError:
#                 return {"status": "erro", "mensagem": "Arquivo original não encontrado."}
#             except PermissionError:
#                 return {"status": "erro", "mensagem": "Permissão negada para atualizar o arquivo."}
#             except IsADirectoryError:
#                 return {"status": "erro", "mensagem": "O caminho é uma pasta, não um arquivo."}
#             except OSError as e:
#                 return {
#                     "status": "erro",
#                     "mensagem": f"Erro do sistema ao atualizar o arquivo: {str(e)}",
#                 }

#         if novo_nome or nova_localizacao:
#             try:
#                 destino = Path(nova_localizacao) if nova_localizacao else path.parent
#                 destino.mkdir(parents=True, exist_ok=True)
#                 novo_nome_final = novo_nome or path.name
#                 novo_caminho = destino / novo_nome_final
#                 shutil.move(str(path), str(novo_caminho))
#                 return {"status": "sucesso", "mensagem": f"Pasta atualizada: {caminho}"}
#             except FileNotFoundError:
#                 return {"status": "erro", "mensagem": "Pasta original não encontrada."}
#             except FileExistsError:
#                 return {
#                     "status": "erro",
#                     "mensagem": "Já existe uma pasta com o novo nome no destino."}
#             except PermissionError:
#                 return {
#                     "status": "erro",
#                     "mensagem": "Permissão negada para renomear ou mover a pasta.",
#                 }
#             except NotADirectoryError:
#                 return {"status": "erro", "mensagem": "O caminho original não é uma pasta."}

#         return f"{tipo.capitalize()} atualizado com sucesso."

import os
import sys

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))


from app.backend.tools.app_ferramentas import AnaliseDeCaminho

if __name__ == "__main__":
    C = "/home/pedro-pm-dias/Downloads/Firefox/"
    analise = AnaliseDeCaminho(caminho=C)
    print(analise)
