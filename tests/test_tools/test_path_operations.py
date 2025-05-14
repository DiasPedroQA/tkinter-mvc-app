# -*- coding: utf-8 -*-
# pylint: disable=C, W, I

"""
Testes para o módulo GerenciadorDeCaminhos, que obtém informações sobre arquivos e pastas.
"""

from pathlib import Path

import pytest

from src.tools.path_operations import GerenciadorDeCaminhos


@pytest.fixture
def arquivo_teste(tmp_path: Path) -> Path:
    caminho: Path = tmp_path / "exemplo.txt"
    caminho.write_text(data="conteúdo de teste")
    return caminho


@pytest.fixture
def pasta_teste(tmp_path: Path) -> Path:
    pasta: Path = tmp_path / "pasta_exemplo"
    pasta.mkdir()
    (pasta / "arquivo1.txt").write_text(data="teste 1")
    (pasta / "arquivo2.txt").write_text(data="teste 2")
    return pasta


@pytest.fixture
def caminho_inexistente(tmp_path: Path) -> Path:
    return tmp_path / "inexistente"


def test_sanitizacao_de_path(arquivo_teste: Path) -> None:
    caminho_str: str = str(arquivo_teste).replace("\\", "\\\\")
    gerenciador = GerenciadorDeCaminhos(caminho_entrada=caminho_str)
    assert gerenciador._caminho_sanitizado.exists()


def test_determinar_tipo_arquivo(arquivo_teste: Path) -> None:
    gerenciador = GerenciadorDeCaminhos(caminho_entrada=arquivo_teste)
    assert gerenciador.tipo == "Arquivo"


def test_determinar_tipo_pasta(pasta_teste: Path) -> None:
    gerenciador = GerenciadorDeCaminhos(caminho_entrada=pasta_teste)
    assert gerenciador.tipo == "Pasta"


def test_determinar_tipo_inexistente(caminho_inexistente: str) -> None:
    gerenciador = GerenciadorDeCaminhos(caminho_entrada=caminho_inexistente)
    assert gerenciador.tipo == "Inexistente"


def test_tamanho_arquivo(arquivo_teste: Path) -> None:
    gerenciador = GerenciadorDeCaminhos(caminho_entrada=arquivo_teste)
    assert gerenciador._tamanho_bytes > 0
    assert "B" in gerenciador._tamanho_formatado


def test_tamanho_pasta(pasta_teste: Path) -> None:
    gerenciador = GerenciadorDeCaminhos(caminho_entrada=pasta_teste)
    assert gerenciador._tamanho_bytes > 0
    assert (
        "KB" in gerenciador._tamanho_formatado or "B" in gerenciador._tamanho_formatado
    )


def test_permissoes(arquivo_teste: Path) -> None:
    gerenciador = GerenciadorDeCaminhos(caminho_entrada=arquivo_teste)
    permissoes: str = gerenciador.permissoes
    assert isinstance(permissoes, str)
    assert len(permissoes) == 9


def test_informacoes_de_caminho_arquivo(arquivo_teste: Path) -> None:
    gerenciador = GerenciadorDeCaminhos(caminho_entrada=arquivo_teste)
    info: dict = gerenciador.informacoes_de_caminho()
    assert "geral" in info
    assert "datas" in info
    assert info["geral"]["tipo_caminho"] == "Arquivo"
    assert info["geral"]["extensao_arquivo"] == ".txt"


def test_informacoes_de_caminho_pasta(pasta_teste: Path) -> None:
    gerenciador = GerenciadorDeCaminhos(caminho_entrada=pasta_teste)
    info: dict = gerenciador.informacoes_de_caminho()
    assert "geral" in info
    assert "datas" in info
    assert info["geral"]["tipo_caminho"] == "Pasta"
    assert "extensao_arquivo" not in info["geral"]


def test_informacoes_para_caminho_inexistente(caminho_inexistente: str) -> None:
    gerenciador = GerenciadorDeCaminhos(caminho_entrada=caminho_inexistente)
    info: dict = gerenciador.informacoes_de_caminho()
    assert info["geral"]["caminho_existe"] == "Não"
    assert info["geral"]["tipo_caminho"] == "Inexistente"
    assert info["datas"]["timestamp_modificacao"] == 0.0
