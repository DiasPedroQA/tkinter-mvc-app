"""
Módulo com utilitários para manipulação de datas e horários usando timestamp (float).

Este módulo oferece funções para:
- Converter timestamp para data legível ou string formatada;
- Obter a quantidade de dias desde um timestamp;
- Gerar timestamp de dias anteriores a partir da data atual.

Todas as funções utilizam timestamp no formato float (segundos desde a época Unix).
"""

import locale
from datetime import datetime, timedelta
from typing import Optional

# Tenta aplicar o locale em português (funciona em sistemas com suporte, ex: Linux)
try:
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
except locale.Error:
    # Fallback caso o sistema não tenha suporte a "pt_BR.UTF-8"
    locale.setlocale(locale.LC_TIME, "")


class GerenciadorDeDataHora:
    """
    Classe para gerenciar operações com datas e horas utilizando timestamps.

    Funcionalidades:
    - Converte timestamps para data/hora legível.
    - Formata timestamps como string.
    - Retorna data/hora atual formatada.
    - Calcula o número de dias desde um timestamp.
    - Gera timestamp de 'n' dias atrás a partir de agora.
    """

    def __init__(self, timestamp: Optional[float] = None) -> None:
        """
        Inicializa com um timestamp (ou usa a hora atual se não for informado).

        Args:
            timestamp (Optional[float]): Timestamp em segundos desde a época Unix.
        """
        self.timestamp_informado: float = timestamp or datetime.now().timestamp()

        # Formatações prontas para exibição
        self.data_formatada: str = self.formatar_data_e_hora(self.timestamp_informado)
        self.data_hora_informada: str = self.formatar_data_e_hora(
            self.timestamp_informado, "%d/%m/%Y %H:%M:%S"
        )
        self.dias_desde: int = self.dias_desde_timestamp(self.timestamp_informado)
        self.data_atual_legivel: str = self.data_hora_legivel(datetime.now())

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

    def data_hora_legivel(self, data: datetime) -> str:
        """
        Retorna uma string da data em formato longo e legível (em português).

        Args:
            data (datetime): Objeto datetime para formatação.

        Returns:
            str: Data/hora formatada em formato longo.
        """
        return data.strftime("%A, %d de %B de %Y %H:%M:%S")

    def dias_desde_timestamp(self, timestamp: float) -> int:
        """
        Calcula quantos dias se passaram desde o timestamp informado.

        Args:
            timestamp (float): Timestamp em segundos desde a época Unix.

        Returns:
            int: Número de dias desde o timestamp informado.
        """
        data_informada: datetime = datetime.fromtimestamp(timestamp)
        return (datetime.now() - data_informada).days

    def timestamp_ha_n_dias_atras(self, n: int) -> float:
        """
        Gera um timestamp equivalente a 'n' dias atrás.

        Args:
            n (int): Número de dias atrás.

        Returns:
            float: Timestamp correspondente.
        """
        return (datetime.now() - timedelta(days=n)).timestamp()

    def obter_informacoes(self) -> dict[str, str | float | int]:
        """
        Retorna as informações principais de data e hora de forma legível.

        Returns:
            dict[str, str | float | int]: Dicionário com informações de data/hora.
        """
        return {
            "timestamp_informado": self.timestamp_informado,
            "data_hora_informada": self.data_hora_informada,
            "data_formatada": self.data_formatada,
            "quantidade_de_dias_passados": self.dias_desde,
            "resumo_dias_passados": (
                f"Já se passaram {self.dias_desde} dias desde a data informada."
            ),
            "data_atual_legivel": self.data_atual_legivel,
        }


# Exemplo de uso:
if __name__ == "__main__":
    gerenciador = GerenciadorDeDataHora(1656998400)  # Exemplo de timestamp
    informacoes: dict[str, str | float | int] = gerenciador.obter_informacoes()
    for chave, valor in informacoes.items():
        print(f"{chave}: {valor}")
