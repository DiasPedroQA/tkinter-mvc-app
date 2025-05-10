import pytest
from datetime import datetime, timedelta
from src.tools.datetime_utils import GerenciadorDeDataHora


def test_formatar_data_e_hora():
    timestamp = 1656998400  # Corresponds to 05/07/2022 00:00:00
    gerenciador = GerenciadorDeDataHora(timestamp)
    assert gerenciador.formatar_data_e_hora(timestamp) == "05/07/2022 00:00:00"
    assert gerenciador.formatar_data_e_hora(timestamp, "%Y-%m-%d") == "2022-07-05"


def test_data_hora_legivel():
    timestamp = 1656998400
    gerenciador = GerenciadorDeDataHora(timestamp)
    data = datetime.fromtimestamp(timestamp)
    assert gerenciador.data_hora_legivel(data).startswith("terça-feira, 05 de julho de 2022")


def test_dias_desde_timestamp():
    timestamp = (datetime.now() - timedelta(days=10)).timestamp()
    gerenciador = GerenciadorDeDataHora(timestamp)
    assert gerenciador.dias_desde_timestamp(timestamp) == 10


def test_timestamp_ha_n_dias_atras():
    gerenciador = GerenciadorDeDataHora()
    n = 5
    timestamp_n_dias = gerenciador.timestamp_ha_n_dias_atras(n)
    assert datetime.fromtimestamp(timestamp_n_dias).date() == (datetime.now() - timedelta(days=n)).date()


def test_obter_informacoes():
    timestamp = 1656998400
    gerenciador = GerenciadorDeDataHora(timestamp)
    informacoes = gerenciador.obter_informacoes()

    assert informacoes["timestamp_informado"] == timestamp
    assert informacoes["data_hora_informada"] == "05/07/2022 00:00:00"
    assert informacoes["data_formatada"] == "05/07/2022 00:00:00"
    assert isinstance(informacoes["quantidade_de_dias_passados"], int)
    assert "Já se passaram" in informacoes["resumo_dias_passados"]
    assert isinstance(informacoes["data_atual_legivel"], str)
