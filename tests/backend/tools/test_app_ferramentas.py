# -*- coding: utf-8 -*-
# pylint: disable=W0212, W0621

"""
Módulo de testes para a classe AnaliseDeCaminho.
"""

from pathlib import Path
import pytest

from app.backend.tools.app_ferramentas import AnaliseDeCaminho


@pytest.fixture
def caminho_teste() -> Path:
    """Cria um caminho de teste com um arquivo temporário."""
    arquivo_teste: str = "/home/pedro-pm-dias/API_LOCAL/GitHub/tkinter-mvc-app/.logs/app.log"
    # arquivo_teste: str = "/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html"
    return Path(arquivo_teste)


def test_init_analise(caminho_teste: Path) -> None:
    """Testa a inicialização da classe AnaliseDeCaminho."""
    analise = AnaliseDeCaminho(str(caminho_teste))
    assert analise.resultado.caminho_original == str(caminho_teste)


def test_deteccao_comparacao_validacao(caminho_teste: Path) -> None:
    """Testa a detecção, comparação e validação do caminho."""
    analise = AnaliseDeCaminho(str(caminho_teste))
    analise._detectar_comparar_e_validar()

    mensagens_possiveis: list[str] = [
        "O caminho pode existir.",
        "Arquivo não encontrado.",
        "Não é um diretório.",
        "Permissão negada.",
        "Sistemas incompatíveis para verificar existência.",
    ]
    assert analise.resultado.mensagem_existencia in mensagens_possiveis
    assert isinstance(analise.resultado.permissoes, dict)
    # assert "leitura" in analise.resultado.permissoes
    assert isinstance(analise.resultado.timestamps, dict)
    assert "data_criacao" in analise.resultado.timestamps


def test_verificacao_caracteres_invalidos(caminho_teste: Path) -> None:
    """Testa a verificação de caracteres inválidos no caminho."""
    analise = AnaliseDeCaminho(str(caminho_teste))
    analise.resultado.sistema_detectado = "Linux"
    analise._verificar_caracteres_invalidos()

    if analise.resultado.erros:
        assert "Caractere(s) inválido(s)" in analise.resultado.erros
    else:
        assert analise.resultado.sintaxe_permitida and (
            "Caminho válido para o sistema atual" in analise.resultado.sintaxe_permitida
        )


def test_dados_localizacao(caminho_teste: Path) -> None:
    """Testa a obtenção de dados de localização do caminho."""
    analise = AnaliseDeCaminho(str(caminho_teste))
    analise.resultado.sistema_detectado = "Linux"
    analise._obter_dados_localizacao()
    local = analise.resultado.localizacao

    assert local["nome_do_item"] == "app.log"
    assert local["pasta_pai"] == str(caminho_teste.parent)
    assert local["tipo_caminho"] == "absoluto"
    assert isinstance(local["raiz"], str)


def test_execucao_geral(caminho_teste: Path) -> None:
    """Testa a execução completa da análise e o retorno em JSON."""
    analise = AnaliseDeCaminho(str(caminho_teste))
    resultado_json = analise.executar()
    assert isinstance(resultado_json, str)
    assert "caminho_original" in resultado_json
