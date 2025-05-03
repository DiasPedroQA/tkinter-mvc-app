# test_sistema_info.py

"""Classe auxiliar para obter o sistema operacional e regras de validação"""

from aplicativo.backend.tools.sistema_info import SistemaArquivoInfo


def test_detectar_sistema_windows() -> None:
    """Verifica a detecção do sistema Windows."""
    caminho = "C:\\Users\\User\\Documents\\file.txt"
    assert SistemaArquivoInfo.detectar_sistema(caminho) == "Windows"


def test_detectar_sistema_linux() -> None:
    """Verifica a detecção do sistema Linux."""
    caminho = "/home/user/documents/file.txt"
    assert SistemaArquivoInfo.detectar_sistema(caminho) == "Linux"


def test_detectar_sistema_macos() -> None:
    """Verifica a detecção do sistema macOS."""
    caminho = "/Users/user/documents/file.txt"
    assert SistemaArquivoInfo.detectar_sistema(caminho) == "macOS"


def test_detectar_sistema_desconhecido() -> None:
    """Verifica a detecção de um sistema desconhecido."""
    caminho = "unknown_path/file.txt"
    assert SistemaArquivoInfo.detectar_sistema(caminho) == "Desconhecido"


def test_caracteres_invalidos_windows() -> None:
    """Verifica os caracteres inválidos no Windows."""
    sistema = "Windows"
    assert SistemaArquivoInfo.caracteres_invalidos(sistema) == [
        '<',
        '>',
        ':',
        '"',
        '/',
        '\\',
        '|',
        '?',
        '*',
    ]


def test_caracteres_invalidos_linux() -> None:
    """Verifica os caracteres inválidos no Linux."""
    sistema = "Linux"
    assert SistemaArquivoInfo.caracteres_invalidos(sistema) == ['\0', '\\']


def test_caracteres_invalidos_macos() -> None:
    """Verifica os caracteres inválidos no macOS."""
    sistema = "macOS"
    assert SistemaArquivoInfo.caracteres_invalidos(sistema) == [":"]


def test_caracteres_invalidos_desconhecido() -> None:
    """Verifica os caracteres inválidos em um sistema desconhecido."""
    sistema = "Desconhecido"
    assert SistemaArquivoInfo.caracteres_invalidos(sistema) == []


def test_sistema_local() -> None:
    """Verifica a detecção do sistema local."""
    sistema = SistemaArquivoInfo.sistema_local()
    assert sistema in ["Windows", "Linux", "macOS", "Desconhecido"]
