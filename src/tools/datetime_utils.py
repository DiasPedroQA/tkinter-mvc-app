# -*- coding: utf-8 -*-
# pylint: disable=R
"""
Módulo com utilitários para manipulação de datas e horários usando timestamp (float).
"""

from datetime import datetime, timedelta
import locale
from typing import Union

try:
    locale.setlocale(category=locale.LC_TIME, locale="pt_BR.UTF-8")
except locale.Error:
    locale.setlocale(category=locale.LC_TIME, locale="")


class FormatadorDeDataHora:
    """
    Classe para gerenciar operações com datas e horas utilizando múltiplos timestamps.
    """

    def __init__(
        self,
        timestamp_modificacao: float | None,
        timestamp_acesso: float | None,
        timestamp_criacao: float | None,
        dias_antes: int | None,
    ) -> None:
        self.timestamp_modificacao = timestamp_modificacao
        self.timestamp_acesso = timestamp_acesso
        self.timestamp_criacao = timestamp_criacao
        self.dias_antes = dias_antes
        self.timestamp_n_dias_atras = (
            self._timestamp_ha_n_dias_atras(dias_antes) if dias_antes is not None else None
        )

    def _formatar_data(self, timestamp: float, formato: str = "%d/%m/%Y %H:%M:%S") -> str:
        return datetime.fromtimestamp(timestamp).strftime(formato)

    def _dias_desde(self, timestamp: float) -> int:
        return (datetime.now().date() - datetime.fromtimestamp(timestamp).date()).days

    def _timestamp_ha_n_dias_atras(self, dias: int) -> float:
        return (datetime.now() - timedelta(days=dias)).timestamp()

    def _adicionar_info_timestamp(
        self,
        chave_base: str,
        timestamp: float,
        dict_timestamps: dict[str, float],
        dict_datas: dict[str, str | int],
    ) -> None:
        """
        Adiciona informações relacionadas a um tipo de timestamp.

        Args:
            chave_base (str): Nome base como 'modificacao', 'acesso', etc.
            timestamp (float): Valor do timestamp.
            dict_timestamps (dict): Dicionário que receberá o timestamp.
            dict_datas (dict): Dicionário que receberá datas formatadas e dias.
        """
        dict_timestamps[f"timestamp_{chave_base}"] = timestamp
        dict_datas[f"data_{chave_base}_formatada"] = self._formatar_data(timestamp)

        if chave_base != "n_dias_atras":
            dict_datas[f"dias_desde_{chave_base}"] = self._dias_desde(timestamp)

    def infos_de_data_e_hora(self) -> dict[str, Union[str, int, float]]:
        """
        Retorna as informações principais de data e hora de forma legível,
        combinando timestamps e datas formatadas em um único dicionário.
        """
        timestamps: dict[str, float] = {}
        datas_formatadas: dict[str, str | int] = {}

        if self.timestamp_modificacao is not None:
            self._adicionar_info_timestamp(
                "modificacao", self.timestamp_modificacao, timestamps, datas_formatadas
            )

        if self.timestamp_acesso is not None:
            self._adicionar_info_timestamp(
                "acesso", self.timestamp_acesso, timestamps, datas_formatadas
            )

        if self.timestamp_criacao is not None:
            self._adicionar_info_timestamp(
                "criacao", self.timestamp_criacao, timestamps, datas_formatadas
            )

        if self.timestamp_n_dias_atras is not None:
            self._adicionar_info_timestamp(
                "n_dias_atras", self.timestamp_n_dias_atras, timestamps, datas_formatadas
            )

        # Junta tudo num dicionário só
        info_data_e_hora: dict[str, Union[str, int, float]] = {}
        info_data_e_hora.update(timestamps)
        info_data_e_hora.update(datas_formatadas)

        return info_data_e_hora


# # Exemplo de uso
# if __name__ == "__main__":
#     formatador = FormatadorDeDataHora(
#         timestamp_modificacao=1746943012.377489,
#         timestamp_acesso=1746943055.3704522,
#         timestamp_criacao=1746943012.377489,
#         dias_antes=30,
#     )

#     informacoes: dict[str, Union[str, int, float]] = formatador.infos_de_data_e_hora()

#     print("Imprimindo o objeto: formatador.infos_de_data_e_hora")
#     for chave, valor in informacoes.items():
#         print(f"{chave}: {valor}")
