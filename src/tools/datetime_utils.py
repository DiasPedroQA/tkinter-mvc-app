# -*- coding: utf-8 -*-

"""
Módulo com utilitários para manipulação de datas e horários usando timestamp (float).

Este módulo oferece funções para:
- Converter timestamp para data legível ou string formatada;
- Obter a quantidade de dias desde um timestamp;
- Gerar timestamp de dias anteriores a partir da data atual.

Todas as funções utilizam timestamp no formato float (segundos desde a época Unix).
"""

from datetime import datetime, timedelta
import locale
from typing import Mapping, Optional, Union

# Tenta aplicar o locale em português (funciona em sistemas com suporte, ex: Linux)
try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
except locale.Error:
    # Fallback caso o sistema não tenha suporte a "pt_BR.UTF-8"
    locale.setlocale(locale.LC_TIME, "")


class GerenciadorDeDataHora:
    """
    Classe para gerenciar operações com datas e horas utilizando múltiplos timestamps.

    Funcionalidades:
    - Converte timestamps para data/hora legível.
    - Calcula o número de dias desde cada timestamp.
    - Gera timestamp de 'n' dias atrás a partir da data atual.
    """

    def __init__(
        self,
        timestamp_modificacao: Optional[float] = None,
        timestamp_acesso: Optional[float] = None,
        timestamp_criacao: Optional[float] = None,
        dias_antes: Optional[int] = None,
    ) -> None:
        """
        Inicializa o gerenciador com os timestamps fornecidos.

        Args:
            timestamp_modificacao (Optional[float]): Timestamp de última modificação.
            timestamp_acesso (Optional[float]): Timestamp de último acesso.
            timestamp_criacao (Optional[float]): Timestamp de criação.
            dias_antes (Optional[int]): Número de dias para calcular o timestamp passado.
        """
        self.timestamp_modificacao = timestamp_modificacao
        self.timestamp_acesso = timestamp_acesso
        self.timestamp_criacao = timestamp_criacao
        self.dias_antes = dias_antes

        # Calcula o timestamp de 'n' dias atrás, se fornecido
        self.timestamp_n_dias_atras = (
            self.timestamp_ha_n_dias_atras(dias_antes) if dias_antes is not None else None
        )

    def formatar_data_e_hora(self, timestamp: float, formato: str = "%d/%m/%Y %H:%M:%S") -> str:
        """
        Converte timestamp para string com formato especificado.

        Args:
            timestamp (float): Timestamp em segundos desde a época Unix.
            formato (str): Formato da data/hora para exibição.

        Returns:
            str: Data/hora formatada como string.
        """
        return datetime.fromtimestamp(timestamp).strftime(formato)

    def dias_desde_timestamp(self, timestamp: float) -> int:
        """
        Calcula quantos dias se passaram desde o timestamp informado.

        Args:
            timestamp (float): Timestamp em segundos desde a época Unix.

        Returns:
            int: Número de dias desde o timestamp informado.
        """
        data_informada = datetime.fromtimestamp(timestamp).date()  # Apenas a data (sem horas)
        data_atual = datetime.now().date()  # Apenas a data (sem horas)
        return (data_atual - data_informada).days

    def timestamp_ha_n_dias_atras(self, n: int) -> float:
        """
        Gera um timestamp equivalente a 'n' dias atrás.

        Args:
            n (int): Número de dias atrás.

        Returns:
            float: Timestamp correspondente.
        """
        return (datetime.now() - timedelta(days=n)).timestamp()

    def obter_informacoes(self) -> Mapping[str, dict[str, Union[str, float]]]:
        """
        Retorna as informações principais de data e hora de forma legível.

        Returns:
            Mapping[str, dict[str, Union[str, float]]]: Dicionário com informações de data/hora.
        """
        informacoes: dict[str, dict[str, Union[str, float]]] = {
            "datas_formatadas": {},
            "timestamps": {},
        }

        # Adiciona informações de modificação, se disponível
        if self.timestamp_modificacao is not None:
            informacoes["timestamps"]["timestamp_modificacao"] = self.timestamp_modificacao
            informacoes["datas_formatadas"]["data_modificacao_formatada"] = (
                self.formatar_data_e_hora(self.timestamp_modificacao)
            )
            informacoes["datas_formatadas"]["dias_desde_modificacao"] = self.dias_desde_timestamp(
                self.timestamp_modificacao
            )

        # Adiciona informações de acesso, se disponível
        if self.timestamp_acesso is not None:
            informacoes["timestamps"]["timestamp_acesso"] = self.timestamp_acesso
            informacoes["datas_formatadas"]["data_acesso_formatada"] = self.formatar_data_e_hora(
                self.timestamp_acesso
            )
            informacoes["datas_formatadas"]["dias_desde_acesso"] = self.dias_desde_timestamp(
                self.timestamp_acesso
            )

        # Adiciona informações de criação, se disponível
        if self.timestamp_criacao is not None:
            informacoes["timestamps"]["timestamp_criacao"] = self.timestamp_criacao
            informacoes["datas_formatadas"]["data_criacao_formatada"] = self.formatar_data_e_hora(
                self.timestamp_criacao
            )
            informacoes["datas_formatadas"]["dias_desde_criacao"] = self.dias_desde_timestamp(
                self.timestamp_criacao
            )

        # Adiciona informações de 'n' dias atrás, se disponível
        if self.timestamp_n_dias_atras is not None:
            informacoes["timestamps"]["timestamp_n_dias_atras"] = self.timestamp_n_dias_atras
            informacoes["datas_formatadas"]["data_n_dias_atras_formatada"] = (
                self.formatar_data_e_hora(self.timestamp_n_dias_atras)
            )

        return informacoes


# # Exemplo de uso:
# if __name__ == "__main__":
#     # gerenciador = GerenciadorDeDataHora(
#     #     timestamp_modificacao=1746943012.377489,
#     #     timestamp_acesso=1746943055.3704522,
#     #     timestamp_criacao=1746943012.377489,
#     # )
#     gerenciador = GerenciadorDeDataHora(
#         timestamp_modificacao=1746943012.377489,
#         timestamp_acesso=1746943055.3704522,
#         timestamp_criacao=1746943012.377489,
#         dias_antes=30,
#     )

#     informacoes = gerenciador.obter_informacoes()

#     # Exibe os dados de forma detalhada
#     for chave, valor in informacoes.items():
#         print(f"\nChave: {chave}")
#         if isinstance(valor, dict):
#             for sub_chave, sub_valor in valor.items():
#                 print(f"  {sub_chave}: {sub_valor}")
#         else:
#             print(f"  Valor: {valor}")
