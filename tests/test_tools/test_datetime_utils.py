# -*- coding: utf-8 -*-
# pylint: disable=C, W, I

"""Testes para o módulo FormatadorDeDataHora (datetime_utils.py)."""

# tests/test_datetime_utils.py

from datetime import datetime, timedelta

from src.tools.datetime_utils import FormatadorDeDataHora


def test_formatar_data() -> None:
    """Testa a formatação de uma data a partir de um timestamp fixo."""
    timestamp = 1700000000.0  # equivalente a 14/11/2023
    f = FormatadorDeDataHora(
        timestamp_modificacao=None,
        timestamp_acesso=None,
        timestamp_criacao=None,
        dias_antes=None,
    )
    resultado: str = f._formatar_data(timestamp=timestamp)
    assert resultado.startswith("14/11/2023")


def test_dias_desde() -> None:
    """Testa a quantidade de dias desde uma data passada."""
    dias_atras = 10
    timestamp: float = (datetime.now() - timedelta(days=dias_atras)).timestamp()
    f = FormatadorDeDataHora(
        timestamp_modificacao=None,
        timestamp_acesso=None,
        timestamp_criacao=None,
        dias_antes=None,
    )
    resultado: int = f._dias_desde(timestamp=timestamp)
    assert resultado == dias_atras


def test_timestamp_ha_n_dias_atras() -> None:
    """Testa se o timestamp gerado há N dias bate com o esperado (tolerância de 2 segundos)."""
    dias = 5
    f = FormatadorDeDataHora(
        timestamp_modificacao=None,
        timestamp_acesso=None,
        timestamp_criacao=None,
        dias_antes=dias,
    )
    resultado: float = f._timestamp_ha_n_dias_atras(dias=dias)
    esperado: float = (datetime.now() - timedelta(days=dias)).timestamp()
    assert abs(resultado - esperado) < 2  # tolerância de 2 segundos


def test_adicionar_info_timestamp() -> None:
    """Testa se os dicionários são preenchidos corretamente com as informações do timestamp."""
    f = FormatadorDeDataHora(
        timestamp_modificacao=None,
        timestamp_acesso=None,
        timestamp_criacao=None,
        dias_antes=None,
    )
    timestamp: float = datetime(
        year=2024, month=1, day=1, hour=12, minute=0, second=0
    ).timestamp()

    dict_ts: dict = {}
    dict_datas: dict = {}
    f._adicionar_info_timestamp(
        chave_base="modificacao",
        timestamp=timestamp,
        dict_timestamps=dict_ts,
        dict_datas=dict_datas,
    )

    assert "timestamp_modificacao" in dict_ts
    assert "data_modificacao_formatada" in dict_datas
    assert "dias_desde_modificacao" in dict_datas

    assert isinstance(dict_ts["timestamp_modificacao"], float)
    assert isinstance(dict_datas["data_modificacao_formatada"], str)
    assert isinstance(dict_datas["dias_desde_modificacao"], int)


def test_infos_de_data_e_hora() -> None:
    """Testa o dicionário final retornado com todas as combinações preenchidas."""
    dias = 7
    agora: datetime = datetime.now()
    timestamp_mod: float = (agora - timedelta(days=2)).timestamp()
    timestamp_acesso: float = (agora - timedelta(days=5)).timestamp()
    timestamp_criacao: float = (agora - timedelta(days=10)).timestamp()

    f = FormatadorDeDataHora(
        timestamp_modificacao=timestamp_mod,
        timestamp_acesso=timestamp_acesso,
        timestamp_criacao=timestamp_criacao,
        dias_antes=dias,
    )

    resultado: dict[str, str | int | float] = f.infos_de_data_e_hora()

    # Verifica se todas as chaves esperadas estão presentes
    chaves_esperadas: list[str] = [
        "timestamp_modificacao",
        "timestamp_acesso",
        "timestamp_criacao",
        "timestamp_n_dias_atras",
        "data_modificacao_formatada",
        "data_acesso_formatada",
        "data_criacao_formatada",
        "data_n_dias_atras_formatada",
        "dias_desde_modificacao",
        "dias_desde_acesso",
        "dias_desde_criacao",
    ]

    for chave in chaves_esperadas:
        assert chave in resultado

    # Verifica os tipos das saídas
    for _, valor in resultado.items():
        assert isinstance(valor, (str, int, float))
