# -*- coding: utf-8 -*-

"""Validador de Caminhos Avançado com pathlib e json"""


import os
from datetime import datetime
from typing import Union


class Tools:
    """
    Classe de ferramentas para validação de caminhos de arquivos e diretórios.
    Esta classe fornece métodos para normalizar caminhos, verificar
    a existência de arquivos/diretórios, obter informações sobre permissões
    e gerar estatísticas do sistema de arquivos.
    A classe é projetada para ser usada em sistemas operacionais
    compatíveis com POSIX e Windows.

    Atributos:
        os_name (str): Nome do sistema operacional.

    Métodos:
        normalize_path(path: str) -> str: Normaliza um caminho de arquivo/diretório.
        get_current_timestamp() -> str: Retorna o timestamp atual no formato ISO.
        validate_path_exists(path: str) -> bool: Verifica se o caminho existe.
        get_path_type(path: str) -> str: Retorna o tipo do caminho (arquivo,
        diretório ou inexistente).
        generate_basic_validation(path: str) -> dict: Gera o dicionário de validação básica.
        generate_filesystem_stats(path: str) -> Union[dict, None]: Gera
        estatísticas do sistema de arquivos.
        generate_permissions(path: str) -> Union[dict, None]: Gera informações de permissão.
    """

    def __init__(self) -> None:
        """Configuração inicial do validador de caminhos"""
        self.os_name: str = os.name  # Identificação do sistema operacional

    @staticmethod
    def normalize_path(path: str) -> str:
        """Normaliza um caminho de arquivo/diretório"""
        return os.path.normpath(path)

    @staticmethod
    def get_current_timestamp() -> str:
        """Retorna timestamp atual no formato ISO"""
        return datetime.now().isoformat()

    @staticmethod
    def validate_path_exists(path: str) -> bool:
        """Verifica se o caminho existe"""
        return os.path.exists(path)

    @staticmethod
    def get_path_type(path: str) -> str:
        """Retorna o tipo do caminho (arquivo, diretório ou inexistente)"""
        if os.path.isfile(path):
            return "arquivo"
        elif os.path.isdir(path):
            return "diretorio"
        return "inexistente"

    def generate_basic_validation(self, path: str) -> dict:
        """Gera o dicionário de validação básica"""
        exists: bool = self.validate_path_exists(path)
        return {
            "existe": "Sim" if exists else "Não",
            "tipo": self.get_path_type(path) if exists else "inexistente",
            "absoluto": os.path.isabs(path),
            "oculto": path.split('/')[-1].startswith('.'),
            "valido": exists,
        }

    def generate_filesystem_stats(self, path: str) -> Union[dict, None]:
        """Gera estatísticas do sistema de arquivos"""
        if not self.validate_path_exists(path):
            return None

        stat: os.stat_result = os.stat(path)
        return {
            "tamanho_bytes": stat.st_size,
            "ultima_modificacao": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "criacao": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "direitos_acesso": oct(stat.st_mode)[-3:],
        }

    def generate_permissions(self, path: str) -> Union[dict, None]:
        """Gera informações de permissão"""
        if not self.validate_path_exists(path):
            return None

        return {
            "leitura": os.access(path, os.R_OK),
            "escrita": os.access(path, os.W_OK),
            "execucao": os.access(path, os.X_OK),
        }
