# pylint: disable=missing-function-docstring, missing-module-docstring, useless-suppression, use-set-for-membership

"""
Módulo de testes para os tipos, dataclasses e exceções do sistema de caminhos.

Abrange:
- Testes de enums `PathType` e `PathStatus`.
- Validação da criação de `PathData` a partir de caminhos existentes e inexistentes.
- Comportamento das exceções customizadas.
- Simulação de uso real com uma função `main()` de exemplo.
"""

from pathlib import Path

import pytest

from src.tools.path_definitions import (
    PathAlreadyExistsError,
    PathData,
    PathInvalidError,
    PathNotFoundError,
    PathOperationError,
    PathStatus,
    PathType,
)

# === TESTES PARA ENUMS ===


def test_path_type_from_str_valido() -> None:
    """Testa valores válidos para PathType."""
    assert PathType.from_str("File") == PathType.FILE
    assert PathType.from_str("Directory") == PathType.DIRECTORY


def test_path_type_from_str_invalido() -> None:
    """Testa valor inválido para PathType."""
    assert PathType.from_str("foo") == PathType.UNKNOWN


def test_path_status_from_str_valido() -> None:
    """Testa valores válidos para PathStatus."""
    assert PathStatus.from_str("existe") == PathStatus.EXISTS
    assert PathStatus.from_str("deleted") == PathStatus.DELETED


def test_path_status_from_str_invalido() -> None:
    """Testa valor inválido para PathStatus."""
    assert PathStatus.from_str("bar") == PathStatus.UNKNOWN


# === TESTES PARA PathData ===


def test_pathdata_from_path_invalido() -> None:
    """Testa exceção para entrada inválida."""
    with pytest.raises(PathInvalidError):
        PathData.from_path("")


def test_pathdata_from_path_arquivo_existente(tmp_path: Path) -> None:
    """Testa criação de PathData para arquivo existente."""
    arquivo = tmp_path / "teste.txt"
    arquivo.write_text("conteúdo")
    data = PathData.from_path(arquivo)
    assert data.nome == "teste.txt"
    assert data.tipo == PathType.FILE
    assert data.status == PathStatus.EXISTS


def test_pathdata_from_path_pasta_existente(tmp_path: Path) -> None:
    """Testa criação de PathData para diretório existente."""
    pasta = tmp_path / "meu_diretorio"
    pasta.mkdir()
    data = PathData.from_path(pasta)
    assert data.nome == "meu_diretorio"
    assert data.tipo == PathType.DIRECTORY
    assert data.status == PathStatus.EXISTS


def test_pathdata_from_path_inexistente(tmp_path: Path) -> None:
    """Testa exceção para caminho inexistente."""
    caminho_falso = tmp_path / "inexistente.txt"
    with pytest.raises(PathNotFoundError):
        PathData.from_path(caminho_falso)


def test_pathdata_to_dict(tmp_path: Path) -> None:
    """Testa conversão de PathData para dicionário."""
    arquivo = tmp_path / "exemplo.txt"
    arquivo.write_text("abc")
    data = PathData.from_path(arquivo)
    resultado = data.to_dict()
    assert resultado["nome"] == "exemplo.txt"
    assert resultado["tipo"] == "File"
    assert resultado["status"] == "existe"


# === TESTES PARA EXCEÇÕES PERSONALIZADAS ===


def test_excecao_path_invalid_error() -> None:
    """Testa mensagem da exceção PathInvalidError."""
    with pytest.raises(PathInvalidError) as exc:
        raise PathInvalidError("/caminho/errado")
    assert "Caminho inválido" in str(exc.value)


def test_excecao_path_not_found_error() -> None:
    """Testa mensagem da exceção PathNotFoundError."""
    with pytest.raises(PathNotFoundError) as exc:
        raise PathNotFoundError("/inexistente")
    assert "Caminho não encontrado" in str(exc.value)


def test_excecao_path_already_exists_error() -> None:
    """Testa mensagem da exceção PathAlreadyExistsError."""
    with pytest.raises(PathAlreadyExistsError) as exc:
        raise PathAlreadyExistsError("/existente")
    assert "Caminho já existe" in str(exc.value)


# === TESTE DA FUNÇÃO MAIN SIMULADA ===


def test_funcao_main_com_caminhos_reais() -> None:
    """
    Testa execução da função main() com caminhos de exemplo.
    Apenas verifica se PathData retorna resultados corretos ou exceções esperadas.
    """
    caminhos = [
        "~/Downloads/Firefox",
        "~/Downloads/Firefox/bookmarks.html",
        "~/Downloads/Firefox/bookmark.html",  # inexistente
        "~/Downloads/Chromium",  # inexistente
    ]

    resultados = []
    for caminho in caminhos:
        try:
            data = PathData.from_path(caminho)
            resultados.append(data.to_dict())
        except PathOperationError as erro:
            resultados.append(
                {
                    "erro": erro.__class__.__name__,
                    "mensagem": erro.message,
                    "caminho": erro.path,
                }
            )

    assert len(resultados) == 4
    assert any("erro" in r for r in resultados)
    assert any(
        r.get("tipo") in ("File", "Directory") for r in resultados if "tipo" in r
    )
