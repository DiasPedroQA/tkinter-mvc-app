# -*- coding: utf-8 -*-
# pylint: disable=E0401

"""Modelo de Caminho para validação de arquivos e diretórios"""

import json
from typing import List, Optional
from backend.tools.app_tools import Tools


class FileSystemModel:
    """
    Modelo para representar e validar caminhos de arquivos e diretórios.
    Este modelo encapsula a lógica de validação e fornece métodos
    para acessar informações sobre o caminho.

    Atributos:
        path (str): Caminho original fornecido.
        normalized_path (str): Caminho normalizado.
        metadados (dict): Metadados do caminho.
        validacao_basica (dict): Resultado da validação básica.
        sistema_arquivos (dict): Dados do sistema de arquivos.
        erros (List): Lista de erros encontrados durante a validação.

    Métodos:
        _generate_metadata(): Gera os metadados do caminho.
        _generate_basic_validation(): Gera a validação básica.
        _generate_filesystem_data(): Gera os dados do sistema de arquivos.
        is_valid(): Verifica se o caminho é válido.
        get_path_type(): Retorna o tipo do caminho (arquivo ou diretório).
        to_json(): Retorna a representação JSON do modelo.
    """

    def __init__(self, path: str):
        self.tools = Tools()
        self.path = path
        self.normalized_path = self.tools.normalize_path(path)
        self.metadados = self._generate_metadata()
        self.validacao_basica = self._generate_basic_validation()
        self.sistema_arquivos = self._generate_filesystem_data()
        self.erros: List = []

    def _generate_metadata(self) -> dict:
        """Gera os metadados do caminho"""
        return {
            "caminho_original": self.path,
            "caminho_normalizado": self.normalized_path,
            "timestamp_validacao": self.tools.get_current_timestamp(),
        }

    def _generate_basic_validation(self) -> dict:
        """Gera a validação básica usando os métodos da Tools"""
        return self.tools.generate_basic_validation(self.normalized_path)

    def _generate_filesystem_data(self) -> dict:
        """Gera os dados do sistema de arquivos"""
        return {
            "estatisticas": self.tools.generate_filesystem_stats(self.normalized_path),
            "permissoes": self.tools.generate_permissions(self.normalized_path),
        }

    def is_valid(self) -> bool:
        """Verifica se o caminho é válido"""
        return self.validacao_basica.get('valido', False)

    def get_path_type(self) -> Optional[str]:
        """Retorna o tipo do caminho"""
        return self.validacao_basica.get('tipo')

    def to_json(self) -> str:
        """Retorna a representação JSON do modelo"""
        dados_completos: dict = {
            "metadados": self.metadados,
            "validacao_basica": self.validacao_basica,
            "sistema_arquivos": self.sistema_arquivos,
            "erros": self.erros,
        }
        return json.dumps(dados_completos, indent=4, ensure_ascii=False)
