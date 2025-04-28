# -*- coding: utf-8 -*-
# pylint: disable=E0401

"""
Modelo de Caminho para validação de arquivos e diretórios
Este módulo contém a classe FileSystemModel, que representa um caminho
de arquivo ou diretório e fornece métodos para validação e
informações adicionais.
"""

from backend.tools.app_tools import Tools

# from backend.model.app_model import FileSystemModel


# Criando instância de Tools
ferramentas = Tools()
print(f"Sistema operacional do servidor -> {ferramentas.os_name}")

arquivo: str = "/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html"
# Normalizando o caminho
caminho_normalizado = ferramentas.normalize_path(path=arquivo)
print(f"Caminho normalizado: {caminho_normalizado}")

# Verificar o tipo do caminho
tipo_caminho = ferramentas.get_path_type(path=arquivo)
print(f"Tipo do caminho: {tipo_caminho}")

# Validando um caminho de arquivo
validacao_basica = ferramentas.generate_basic_validation(path=arquivo)
print(f"Validação para {arquivo}: {validacao_basica}")

# Obtendo estatísticas
stats = ferramentas.generate_filesystem_stats(path=arquivo)
print(f"Estatísticas: {stats}")

# Obtendo permissões
permissoes = ferramentas.generate_permissions(path=arquivo)
print(f"Permissões: {permissoes}")

# # Criando modelo para um arquivo/diretório
# path_model = FileSystemModel("/home/pedro-pm-dias/Downloads/Firefox/")

# # Acessando propriedades
# print(f"Caminho normalizado: {path_model.normalized_path}")
# print(f"Tipo: {path_model.get_path_type()}")
# print(f"É válido? {path_model.is_valid()}")

# # Obtendo representação JSON
# print("Representação completa:")
# print(path_model.to_json())
