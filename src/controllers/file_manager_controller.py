# """
# Módulo que define a classe GerenciadorArquivos.

# A classe GerenciadorArquivos é responsável por
# gerenciar operações relacionadas a arquivos e pastas,
# incluindo análise de caminhos e tentativa de correção de caminhos inválidos.
# """

# from pathlib import Path
# from models.file_objects import ObjetoArquivo, ObjetoPasta
# from models.analysis_result import ResultadoAnalise
# from tools.path_utils import normalizar_caminho, tentar_corrigir_caminho


# class GerenciadorArquivos:
#     """Classe principal para gerenciamento de operações com arquivos."""

#     def __init__(self, sistema: str, usuario: str, base_usuario: str) -> None:
#         self._sistema = sistema
#         self._usuario = usuario
#         self._base_usuario = base_usuario

#     def server_analisar_caminhos(self, caminho_entrada: str) -> ResultadoAnalise:
#         """Analisa um caminho informado."""
#         objeto_analisado = ResultadoAnalise()
#         caminho_normalizado = normalizar_caminho(caminho_entrada)

#         # Converter caminho relativo
#         if not caminho_normalizado.is_absolute():
#             caminho_normalizado = (
#                 Path(self._base_usuario) / caminho_normalizado
#             ).resolve()
#             objeto_analisado.tipo_caminho = "absoluto_convertido"
#         else:
#             caminho_normalizado = caminho_normalizado.resolve()
#             objeto_analisado.tipo_caminho = "absoluto_natural"

#         objeto_analisado.caminho_tratado = str(caminho_normalizado)

#         # Verificar se existe
#         if caminho_normalizado.exists():
#             objeto_analisado.sucesso = True
#             if caminho_normalizado.is_dir():
#                 objeto_analisado.mensagem = "Pasta identificada com sucesso."
#                 objeto_analisado.objetos_coletados = ObjetoPasta(
#                     caminho_pasta=str(caminho_normalizado),
#                 )
#             elif caminho_normalizado.is_file():
#                 objeto_analisado.mensagem = "Arquivo identificado com sucesso."
#                 objeto_analisado.objetos_coletados = ObjetoArquivo(
#                     caminho_arquivo=str(caminho_normalizado),
#                 )
#             return objeto_analisado

#         # Tentar corrigir caminho
#         caminho_corrigido = tentar_corrigir_caminho(caminho_normalizado)
#         if caminho_corrigido:
#             objeto_analisado.sucesso = True
#             objeto_analisado.caminho_corrigido = str(caminho_corrigido)
#             return objeto_analisado

#         # Caminho inválido
#         objeto_analisado.mensagem = (
#             "O caminho não foi encontrado e não foi possível corrigi-lo."
#         )
#         return objeto_analisado
# src/controllers/file_manager_controller.py

from src.models.paths_objects import ObjetoArquivo, ObjetoPasta
from pathlib import Path


class FileManagerController:
    """Controlador responsável por criar, atualizar e fornecer objetos de arquivos ou pastas."""

    def criar_objeto(self, caminho: str):
        """Cria e retorna o objeto correspondente ao caminho (arquivo ou pasta)."""
        path = Path(caminho)

        if path.is_file():
            return ObjetoArquivo.from_path(path)
        elif path.is_dir():
            return ObjetoPasta.from_path(path)
        else:
            raise FileNotFoundError(f"Caminho inválido: {caminho}")

    def atualizar_objeto(self, obj):
        """Atualiza os dados do objeto fornecido, seja arquivo ou pasta."""
        if isinstance(obj, ObjetoArquivo):
            obj.atualizar_dados()
        elif isinstance(obj, ObjetoPasta):
            obj.atualizar_dados()
        else:
            raise TypeError("Tipo de objeto não reconhecido.")

    def ler_objeto_formatado(self, obj):
        """Retorna um dicionário com os dados formatados de um ObjetoArquivo ou ObjetoPasta."""
        return obj.to_dict()
