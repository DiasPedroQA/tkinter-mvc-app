# -*- coding: utf-8 -*-
# pylint: disable=C0114, W0621

import os
from datetime import datetime
from pathlib import Path

import pytest

from app.backend.tools.app_tools import Tools


@pytest.fixture
def tools() -> Tools:
    """Fixture para criar uma instância da classe Tools"""
    return Tools()


def test_normalize_path(tools: Tools) -> None:
    """Testa a normalização de caminhos"""
    assert tools.normalize_path("folder//subfolder/../file.txt") == os.path.normpath(
        "folder/file.txt"
    )


def test_get_current_timestamp(tools: Tools) -> None:
    """Testa a geração de timestamp atual"""
    timestamp: str = tools.get_current_timestamp()
    assert datetime.fromisoformat(timestamp)  # Validates ISO format


def test_validate_path_exists(tools: Tools, tmp_path: Path) -> None:
    """Testa a validação da existência de caminhos"""
    file: Path = tmp_path / "test_file.txt"
    file.write_text("test")
    assert tools.validate_path_exists(str(file)) is True
    assert tools.validate_path_exists("non_existent_path") is False


def test_get_path_type(tools: Tools, tmp_path: Path) -> None:
    """Testa a obtenção do tipo de caminho"""
    file: Path = tmp_path / "test_file.txt"
    file.write_text("test")
    directory: Path = tmp_path / "test_dir"
    directory.mkdir()

    assert tools.get_path_type(str(file)) == "arquivo"
    assert tools.get_path_type(str(directory)) == "diretorio"
    assert tools.get_path_type("non_existent_path") == "inexistente"


def test_generate_basic_validation(tools: Tools, tmp_path: Path) -> None:
    """Testa a geração de validação básica"""
    file: Path = tmp_path / "test_file.txt"
    file.write_text("test")
    validation = tools.generate_basic_validation(str(file))

    assert validation["existe"] == "Sim"
    assert validation["tipo"] == "arquivo"
    assert validation["absoluto"] is True
    assert validation["oculto"] is False
    assert validation["valido"] is True

    non_existent_validation = tools.generate_basic_validation("non_existent_path")
    assert non_existent_validation["existe"] == "Não"
    assert non_existent_validation["tipo"] == "inexistente"
    assert non_existent_validation["valido"] is False


def test_generate_filesystem_stats(tools: Tools, tmp_path: Path) -> None:
    """Testa a geração de estatísticas do sistema de arquivos"""
    file: Path = tmp_path / "test_file.txt"
    file.write_text("test")
    stats = tools.generate_filesystem_stats(str(file))

    assert stats is not None
    assert stats["tamanho_bytes"] == 4
    assert "ultima_modificacao" in stats
    assert "criacao" in stats
    assert stats["direitos_acesso"] is not None

    assert tools.generate_filesystem_stats("non_existent_path") is None


def test_generate_permissions(tools: Tools, tmp_path: Path) -> None:
    """Testa a geração de permissões"""
    file = tmp_path / "test_file.txt"
    file.write_text("test")
    permissions = tools.generate_permissions(str(file))

    assert permissions is not None
    assert permissions["leitura"] is True
    assert permissions["escrita"] is True
    assert permissions["execucao"] is False

    assert tools.generate_permissions("non_existent_path") is None
