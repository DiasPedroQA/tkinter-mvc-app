# from model import PathModel
# from tools import normalize_path, is_absolute_path, path_exists, get_path_type

# class PathController:
#     def __init__(self):
#         self.model = PathModel()

#     def validate_path(self, raw_path):
#         """Valida um caminho e armazena o resultado no model"""
#         try:
#             path = normalize_path(raw_path)

#             if not is_absolute_path(path):
#                 raise ValueError("Caminho deve ser absoluto")

#             if not path_exists(path):
#                 raise FileNotFoundError("Caminho não existe")

#             path_type = get_path_type(path)

#             self.model.add_valid_path({
#                 'original': raw_path,
#                 'normalized': path,
#                 'type': path_type
#             })

#             return {
#                 'status': 'valid',
#                 'path': path,
#                 'type': path_type
#             }
#         except Exception as e:
#             self.model.add_invalid_path({
#                 'original': raw_path,
#                 'error': str(e)
#             })
#             return {
#                 'status': 'invalid',
#                 'path': raw_path,
#                 'error': str(e)
#             }

#     def get_validation_stats(self):
#         return self.model.get_stats()

# from typing import Union
# from pathlib import Path
# import platform

# from backend.models.app_model import AppModel


# class AppController:
#     """Controla as operações da aplicação.

#     Este controlador gerencia informações sobre o sistema operacional
#     e o usuário atual.
#     """
#     def __init__(self) -> None:
#         """Configuração inicial do controlador de aplicativo."""
#         self.sistema_operacional = self.detectar_sistema_operacional()
#         # self._nome_usuario = self.obter_nome_usuario()

#     def detectar_sistema_operacional(self) -> str:
#         """Detecta o sistema operacional do usuário."""

#         sistema = platform.system()
#         if sistema == "Windows":
#             return "Windows"
#         elif sistema == "Linux":
#             return "Linux"
#         elif sistema == "Darwin":
#             return "macOS"
#         else:
#             raise ValueError("Sistema operacional não suportado.")

#     def obter_nome_usuario(self, usuario_padrao: str = "~") -> Union[str, Path]:
#         """Obtém o nome do usuário atual do sistema operacional."""
#         nome_usuario = Path.home()
#         if nome_usuario == Path(usuario_padrao):
#             return nome_usuario
#         else:
#             raise ValueError("Nome de usuário inválido.")
