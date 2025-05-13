# -*- coding: utf-8 -*-
"""Testes para o módulo GerenciadorDeDataHora (datetime_utils.py)."""

from datetime import datetime, timedelta
from typing import Dict, Union

import pytest

from src.tools.datetime_utils import GerenciadorDeDataHora


@pytest.fixture
def dados() -> Dict[str, Union[str, int, float]]:
    """
    Fixture para fornecer timestamps de teste.
    """
    now = datetime.now()
    return {
        "modificacao": now.timestamp(),
        "acesso": (now - timedelta(days=1)).timestamp(),
        "criacao": (now - timedelta(days=10)).timestamp(),
        "dias_antes": 5,
    }


def test_formatar_data_e_hora(dados: Dict[str, Union[str, int, float]]) -> None:
    """
    Testa se o método formatar_data_e_hora retorna uma string formatada corretamente.
    """
    gerenciador = GerenciadorDeDataHora()
    timestamp = float(dados["modificacao"])
    data_formatada = gerenciador.formatar_data_e_hora(timestamp)
    assert isinstance(data_formatada, str)
    assert datetime.strptime(data_formatada, "%d/%m/%Y %H:%M:%S")


def test_dias_desde_timestamp(dados: Dict[str, Union[str, int, float]]) -> None:
    """
    Testa o cálculo de dias desde um timestamp fornecido.
    """
    gerenciador = GerenciadorDeDataHora()
    timestamp = float(dados["criacao"])
    dias_passados = gerenciador.dias_desde_timestamp(timestamp)
    assert isinstance(dias_passados, int)
    assert dias_passados == 10


def test_timestamp_ha_n_dias_atras(dados: Dict[str, Union[str, int, float]]) -> None:
    """
    Testa se o método retorna o timestamp correto para n dias atrás.
    """
    gerenciador = GerenciadorDeDataHora()
    n_dias = int(dados["dias_antes"])
    timestamp_calculado = gerenciador.timestamp_ha_n_dias_atras(n_dias)
    assert isinstance(timestamp_calculado, float)
    data_calculada = datetime.fromtimestamp(timestamp_calculado).date()
    data_esperada = (datetime.now() - timedelta(days=n_dias)).date()
    assert data_calculada == data_esperada


def test_obter_informacoes_com_todos_timestamps(dados: Dict[str, Union[str, int, float]]) -> None:
    """
    Testa o método obter_informacoes com todos os timestamps fornecidos.
    """
    gerenciador = GerenciadorDeDataHora(
        timestamp_modificacao=float(dados["modificacao"]),
        timestamp_acesso=float(dados["acesso"]),
        timestamp_criacao=float(dados["criacao"]),
        dias_antes=int(dados["dias_antes"]),
    )
    informacoes = gerenciador.obter_informacoes()

    assert "datas_formatadas" in informacoes
    assert "timestamps" in informacoes

    # Verifica informações de modificação
    assert "timestamp_modificacao" in informacoes["timestamps"]
    assert "data_modificacao_formatada" in informacoes["datas_formatadas"]
    assert "dias_desde_modificacao" in informacoes["datas_formatadas"]

    # Verifica informações de acesso
    assert "timestamp_acesso" in informacoes["timestamps"]
    assert "data_acesso_formatada" in informacoes["datas_formatadas"]
    assert "dias_desde_acesso" in informacoes["datas_formatadas"]

    # Verifica informações de criação
    assert "timestamp_criacao" in informacoes["timestamps"]
    assert "data_criacao_formatada" in informacoes["datas_formatadas"]
    assert "dias_desde_criacao" in informacoes["datas_formatadas"]

    # Verifica informações de 'n' dias atrás
    assert "timestamp_n_dias_atras" in informacoes["timestamps"]
    assert "data_n_dias_atras_formatada" in informacoes["datas_formatadas"]


def test_obter_informacoes_com_timestamps_parciais(
    dados: Dict[str, Union[str, int, float]],
) -> None:
    """
    Testa o método obter_informacoes com apenas alguns timestamps fornecidos.
    """
    gerenciador = GerenciadorDeDataHora(
        timestamp_modificacao=float(dados["modificacao"]),
        timestamp_acesso=None,
        timestamp_criacao=None,
    )
    informacoes = gerenciador.obter_informacoes()

    # Verifica informações de modificação
    assert "timestamp_modificacao" in informacoes["timestamps"]
    assert "data_modificacao_formatada" in informacoes["datas_formatadas"]
    assert "dias_desde_modificacao" in informacoes["datas_formatadas"]

    # Verifica que informações de acesso e criação estão ausentes
    assert "timestamp_acesso" not in informacoes["timestamps"]
    assert "data_acesso_formatada" not in informacoes["datas_formatadas"]
    assert "dias_desde_acesso" not in informacoes["datas_formatadas"]

    assert "timestamp_criacao" not in informacoes["timestamps"]
    assert "data_criacao_formatada" not in informacoes["datas_formatadas"]
    assert "dias_desde_criacao" not in informacoes["datas_formatadas"]


def test_obter_informacoes_sem_timestamps() -> None:
    """
    Testa o método obter_informacoes sem nenhum timestamp fornecido.
    """
    gerenciador = GerenciadorDeDataHora()
    informacoes = gerenciador.obter_informacoes()

    # Verifica que todas as informações estão ausentes
    assert "datas_formatadas" in informacoes
    assert "timestamps" in informacoes
    assert not informacoes["datas_formatadas"]
    assert not informacoes["timestamps"]


def test_formatar_data_e_hora_invalid_timestamp() -> None:
    """
    Testa o comportamento do método formatar_data_e_hora com um timestamp inválido.
    """
    gerenciador = GerenciadorDeDataHora()
    invalid_timestamp = "invalid"
    with pytest.raises(TypeError):
        gerenciador.formatar_data_e_hora(invalid_timestamp)  # type: ignore


def test_dias_desde_timestamp_invalid_timestamp() -> None:
    """
    Testa o comportamento do método dias_desde_timestamp com um timestamp inválido.
    """
    gerenciador = GerenciadorDeDataHora()
    invalid_timestamp = "invalid"
    with pytest.raises(TypeError):
        gerenciador.dias_desde_timestamp(invalid_timestamp)  # type: ignore


def test_timestamp_ha_n_dias_atras_negative_days() -> None:
    """
    Testa o comportamento do método timestamp_ha_n_dias_atras com um número negativo de dias.
    """
    gerenciador = GerenciadorDeDataHora()
    n_dias = -5
    timestamp_calculado = gerenciador.timestamp_ha_n_dias_atras(n_dias)
    assert isinstance(timestamp_calculado, float)
    data_calculada = datetime.fromtimestamp(timestamp_calculado).date()
    data_esperada = (datetime.now() - timedelta(days=n_dias)).date()
    assert data_calculada == data_esperada
