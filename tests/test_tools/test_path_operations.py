from pathlib import Path

import pytest

from tools.path_operations import GerenciadorDeCaminhos


@pytest.fixture
def arquivo_tmp(tmp_path: Path) -> Path:
    """
    Cria um arquivo temporário para os testes.
    """
    arquivo = tmp_path / "arquivo_teste.txt"
    arquivo.write_text("Conteúdo de teste")
    return arquivo


@pytest.fixture
def pasta_tmp(tmp_path: Path) -> Path:
    """
    Cria uma pasta temporária para os testes.
    """
    pasta = tmp_path / "pasta_teste"
    pasta.mkdir()
    return pasta


def test_tipo_arquivo(arquivo_tmp: Path) -> None:
    """
    Testa se o tipo do caminho é identificado como 'Arquivo'.
    """
    gerenciador = GerenciadorDeCaminhos(arquivo_tmp)
    assert gerenciador.tipo == "Arquivo"


def test_tipo_pasta(pasta_tmp: Path) -> None:
    """
    Testa se o tipo do caminho é identificado como 'Pasta'.
    """
    gerenciador = GerenciadorDeCaminhos(pasta_tmp)
    assert gerenciador.tipo == "Pasta"


def test_tipo_inexistente() -> None:
    """
    Testa se o tipo do caminho é identificado como 'inexistente' para caminhos inválidos.
    """
    caminho_inexistente = "/caminho/que/nao/existe"
    gerenciador = GerenciadorDeCaminhos(caminho_inexistente)
    assert gerenciador.tipo == "inexistente"


def test_permissoes_arquivo(arquivo_tmp: Path) -> None:
    """
    Testa se as permissões do arquivo são retornadas corretamente.
    """
    gerenciador = GerenciadorDeCaminhos(arquivo_tmp)
    permissoes = gerenciador.permissoes
    assert permissoes is not None
    assert "r" in permissoes  # Verifica se há permissões de leitura


def test_permissoes_pasta(pasta_tmp: Path) -> None:
    """
    Testa se as permissões da pasta são retornadas corretamente.
    """
    gerenciador = GerenciadorDeCaminhos(pasta_tmp)
    permissoes = gerenciador.permissoes
    assert permissoes is not None
    assert "r" in permissoes  # Verifica se há permissões de leitura


def test_obter_informacoes_arquivo(arquivo_tmp: Path) -> None:
    """
    Testa se as informações do arquivo são retornadas corretamente.
    """
    gerenciador = GerenciadorDeCaminhos(arquivo_tmp)
    informacoes = gerenciador.obter_informacoes()

    assert informacoes["geral"]["tipo_caminho"] == "Arquivo"
    assert informacoes["geral"]["caminho_existe"] is True
    assert informacoes["arquivo"]["extensao"] == ".txt"
    assert informacoes["arquivo"]["tamanho_bytes"] > 0


def test_obter_informacoes_pasta(pasta_tmp: Path) -> None:
    """
    Testa se as informações da pasta são retornadas corretamente.
    """
    gerenciador = GerenciadorDeCaminhos(pasta_tmp)
    informacoes = gerenciador.obter_informacoes()

    assert informacoes["geral"]["tipo_caminho"] == "Pasta"
    assert informacoes["geral"]["caminho_existe"] is True
    assert "pasta" in informacoes
    assert "permissoes" in informacoes["pasta"]


def test_obter_informacoes_inexistente() -> None:
    """
    Testa se as informações de um caminho inexistente são retornadas corretamente.
    """
    caminho_inexistente = "/caminho/que/nao/existe"
    gerenciador = GerenciadorDeCaminhos(caminho_inexistente)
    informacoes = gerenciador.obter_informacoes()

    assert informacoes["geral"]["tipo_caminho"] == "inexistente"
    assert informacoes["geral"]["caminho_existe"] is False
    assert "datas" in informacoes
    assert informacoes["datas"] == {
        "data_acesso": "31/12/1969 21:00:00",
        "data_criacao": "31/12/1969 21:00:00",
        "data_modificacao": "31/12/1969 21:00:00",
    }


def test_sanitizar_path() -> None:
    """
    Testa se o método _sanitizar_path normaliza corretamente o caminho.
    """
    caminho_bruto = "~/Downloads/../Downloads/teste.txt"
    caminho_sanitizado = GerenciadorDeCaminhos._sanitizar_path(caminho_bruto)
    assert caminho_sanitizado == Path("~/Downloads/teste.txt").expanduser().resolve(strict=False)
