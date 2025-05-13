# -*- coding: utf-8 -*-
# pylint: disable=W0621

"""
Testes para o módulo GerenciadorDeCaminhos, que obtém informações sobre arquivos e pastas.
"""

from pathlib import Path

import pytest

from src.tools.path_operations import GerenciadorDeCaminhos


@pytest.fixture
def arquivo_teste(tmp_path: Path) -> Path:
    caminho = tmp_path / "exemplo.txt"
    caminho.write_text("conteúdo de teste")
    return caminho


@pytest.fixture
def pasta_teste(tmp_path: Path) -> Path:
    pasta = tmp_path / "pasta_exemplo"
    pasta.mkdir()
    (pasta / "arquivo1.txt").write_text("teste 1")
    (pasta / "arquivo2.txt").write_text("teste 2")
    return pasta


@pytest.fixture
def caminho_inexistente(tmp_path: Path) -> Path:
    return tmp_path / "inexistente"


def test_sanitizacao_de_path(arquivo_teste: Path) -> None:
    caminho_str = str(arquivo_teste).replace("\\", "\\\\")
    gerenciador = GerenciadorDeCaminhos(caminho_str)
    assert gerenciador._caminho_sanitizado.exists()


def test_determinar_tipo_arquivo(arquivo_teste: Path) -> None:
    gerenciador = GerenciadorDeCaminhos(arquivo_teste)
    assert gerenciador.tipo == "Arquivo"


def test_determinar_tipo_pasta(pasta_teste: Path) -> None:
    gerenciador = GerenciadorDeCaminhos(pasta_teste)
    assert gerenciador.tipo == "Pasta"


def test_determinar_tipo_inexistente(caminho_inexistente: str) -> None:
    gerenciador = GerenciadorDeCaminhos(caminho_inexistente)
    assert gerenciador.tipo == "Inexistente"


def test_tamanho_arquivo(arquivo_teste: Path) -> None:
    gerenciador = GerenciadorDeCaminhos(arquivo_teste)
    assert gerenciador._tamanho_bytes > 0
    assert "B" in gerenciador._tamanho_formatado


def test_tamanho_pasta(pasta_teste: Path) -> None:
    gerenciador = GerenciadorDeCaminhos(pasta_teste)
    assert gerenciador._tamanho_bytes > 0
    assert "KB" in gerenciador._tamanho_formatado or "B" in gerenciador._tamanho_formatado


def test_permissoes(arquivo_teste: Path) -> None:
    gerenciador = GerenciadorDeCaminhos(arquivo_teste)
    permissoes = gerenciador.permissoes
    assert isinstance(permissoes, str)
    assert len(permissoes) == 9


def test_informacoes_de_caminho_arquivo(arquivo_teste: Path) -> None:
    gerenciador = GerenciadorDeCaminhos(arquivo_teste)
    info = gerenciador.informacoes_de_caminho()
    assert "geral" in info
    assert "datas" in info
    assert info["geral"]["tipo_caminho"] == "Arquivo"
    assert info["geral"]["extensao_arquivo"] == ".txt"


def test_informacoes_de_caminho_pasta(pasta_teste: Path) -> None:
    gerenciador = GerenciadorDeCaminhos(pasta_teste)
    info = gerenciador.informacoes_de_caminho()
    assert "geral" in info
    assert "datas" in info
    assert info["geral"]["tipo_caminho"] == "Pasta"
    assert "extensao_arquivo" not in info["geral"]


def test_informacoes_para_caminho_inexistente(caminho_inexistente: str) -> None:
    gerenciador = GerenciadorDeCaminhos(caminho_inexistente)
    info = gerenciador.informacoes_de_caminho()
    assert info["geral"]["caminho_existe"] == "Não"
    assert info["geral"]["tipo_caminho"] == "Inexistente"
    assert info["datas"]["timestamp_modificacao"] == 0.0
