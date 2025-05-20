# pylint: disable=missing-function-docstring, missing-module-docstring, useless-suppression

"""
Módulo base com tipos e utilitários para manipulação de caminhos.

Este módulo fornece:
- Enumerações para representar o tipo (`PathType`) e status (`PathStatus`) de um caminho.
- Uma classe de dados (`PathData`) para encapsular metadados de caminhos de arquivos ou diretórios.
- Exceções customizadas para operações com caminhos inválidos ou inexistentes.

É útil em sistemas que realizam validações, leituras ou operações CRUD sobre o sistema de arquivos.
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Union

# === ENUMS COM MÉTODOS DE PARSING ===


class PathType(str, Enum):
    """
    Enum para representar o tipo de caminho.

    Valores possíveis:
        - FILE: Arquivo.
        - DIRECTORY: Diretório.
        - UNKNOWN: Tipo desconhecido.
        - ERROR: Erro na classificação.
    """

    FILE = "File"
    DIRECTORY = "Directory"
    UNKNOWN = "unknown"
    ERROR = "error"

    @classmethod
    def from_str(cls, valor: str) -> "PathType":
        """
        Constrói um PathType a partir de uma string.

        Retorna:
            - O valor correspondente se existir.
            - PathType.UNKNOWN se a string for inválida.
        """
        try:
            return cls(valor)
        except ValueError:
            return cls.UNKNOWN


class PathStatus(str, Enum):
    """
    Enum para representar o status de um caminho no sistema.

    Valores possíveis:
        - EXISTS: O caminho existe.
        - NOT_EXISTS: O caminho não existe.
        - CREATED: Caminho foi criado recentemente.
        - UPDATED: Caminho foi modificado.
        - DELETED: Caminho foi removido.
        - UNKNOWN: Status desconhecido.
        - ERROR: Erro ao determinar o status.
    """

    EXISTS = "existe"
    NOT_EXISTS = "nao_existe"
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    UNKNOWN = "unknown"
    ERROR = "error"

    @classmethod
    def from_str(cls, valor: str) -> "PathStatus":
        """
        Constrói um PathStatus a partir de uma string.

        Retorna:
            - O valor correspondente se existir.
            - PathStatus.UNKNOWN se a string for inválida.
        """
        try:
            return cls(valor)
        except ValueError:
            return cls.UNKNOWN


# === DATACLASS DE CORRELAÇÃO ===


@dataclass
class PathData:
    """
    Representa os metadados básicos de um caminho de arquivo ou diretório.

    Atributos:
        nome (str): Nome do arquivo ou pasta.
        tipo (PathType): Tipo do caminho (arquivo, diretório, etc.).
        caminho (str): Caminho absoluto completo.
        status (PathStatus): Status atual do caminho no sistema.
    """

    nome: str
    tipo: PathType
    caminho: str
    status: PathStatus

    @classmethod
    def from_path(cls, caminho_str: Union[str, Path]) -> "PathData":
        """
        Cria uma instância de PathData a partir de um caminho fornecido.

        Args:
            caminho_str (str | Path): Caminho a ser analisado.

        Raises:
            PathInvalidError: Se o caminho for vazio ou inválido.
            PathNotFoundError: Se o caminho não existir no sistema.

        Retorna:
            PathData: Instância com os metadados extraídos.
        """
        if not caminho_str or not isinstance(caminho_str, (str, Path)):
            raise PathInvalidError(str(caminho_str))

        caminho = Path(caminho_str).expanduser().resolve()

        if not caminho.exists():
            raise PathNotFoundError(str(caminho))

        tipo = (
            PathType.FILE
            if caminho.is_file()
            else PathType.DIRECTORY
            if caminho.is_dir()
            else PathType.UNKNOWN
        )

        return cls(
            nome=caminho.name,
            tipo=tipo,
            caminho=str(caminho),
            status=PathStatus.EXISTS,
        )

    def to_dict(self) -> dict[str, str]:
        """
        Converte a instância em um dicionário serializável.

        Retorna:
            dict[str, str]: Representação dos dados em formato dicionário.
        """
        return {
            "nome": self.nome,
            "tipo": self.tipo.value,
            "caminho": self.caminho,
            "status": self.status.value,
        }


# === EXCEÇÕES PERSONALIZADAS ===


class PathOperationError(Exception):
    """
    Exceção base para erros relacionados a operações com caminhos.

    Atributos:
        path (str): Caminho envolvido no erro.
        message (str): Mensagem explicativa.
    """

    def __init__(self, path: str, message: str):
        self.path = path
        self.message = message
        super().__init__(f"{message} [Path: {path}]")


class PathNotFoundError(PathOperationError):
    """
    Erro lançado quando o caminho não é encontrado no sistema.
    """

    def __init__(self, path: str):
        super().__init__(path, "Caminho não encontrado")


class PathInvalidError(PathOperationError):
    """
    Erro lançado quando o caminho fornecido é inválido ou vazio.
    """

    def __init__(self, path: str):
        super().__init__(path, "Caminho inválido")


class PathAlreadyExistsError(PathOperationError):
    """
    Erro lançado quando uma operação tenta criar algo que já existe.
    """

    def __init__(self, path: str):
        super().__init__(path, "Caminho já existe")
