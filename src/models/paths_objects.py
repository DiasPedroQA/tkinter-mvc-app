# pylint: disable=R0902

"""
Módulo que define as classes ObjetoArquivo e ObjetoPasta.

A classe ObjetoArquivo é utilizada para armazenar detalhes de um arquivo, como tipo, extensão,
tamanho, data de modificação e caminho. Já a classe ObjetoPasta é utilizada para armazenar
detalhes de uma pasta, incluindo seus subitens e caminho.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class ObjetoArquivo:
    """Classe para armazenar detalhes de um arquivo."""

    tipo_item: str = "Arquivo"
    extensao_arquivo: str = ""
    tamanho_bytes: int = 0
    ultima_modificacao: float = 0.0  # Timestamp em segundos
    data_acesso: float = 0.0  # Timestamp em segundos
    data_criacao: float = 0.0  # Timestamp em segundos
    caminho_arquivo: str = ""
    permissoes: str = ""
    proprietario: str = ""

    @property
    def ultima_modificacao_formatada(self) -> str:
        """Retorna a data de modificação formatada."""
        return datetime.fromtimestamp(self.ultima_modificacao).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    @property
    def data_acesso_formatada(self) -> str:
        """Retorna a data de acesso formatada."""
        return datetime.fromtimestamp(self.data_acesso).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def data_criacao_formatada(self) -> str:
        """Retorna a data de criação formatada."""
        return datetime.fromtimestamp(self.data_criacao).strftime("%Y-%m-%d %H:%M:%S")

    @property
    def tamanho_formatado(self) -> str:
        """Retorna o tamanho do arquivo formatado."""
        tamanho = float(self.tamanho_bytes)
        for unidade in ["B", "KB", "MB", "GB", "TB"]:
            if tamanho < 1024:
                return f"{tamanho:.2f} {unidade}"
            tamanho /= 1024
        # return f"{tamanho:.2f} PB"  # Default case for extremely large sizes
        return f"{tamanho:.2f} TB"  # Default case for very large files

    @property
    def permissoes_legiveis(self) -> str:
        """Retorna as permissões do arquivo em formato legível."""
        return f"Permissões: {self.permissoes}"

    def eh_arquivo_grande(self, limite_mb: int = 100) -> bool:
        """Verifica se o arquivo é maior que o limite especificado em MB."""
        return self.tamanho_bytes > limite_mb * 1024 * 1024

    def eh_recente(self, dias: int = 7) -> bool:
        """Verifica se o arquivo foi modificado nos últimos 'n' dias."""
        delta = datetime.now() - datetime.fromtimestamp(self.ultima_modificacao)
        return delta.days <= dias


@dataclass
class ObjetoPasta:
    """Classe para armazenar detalhes de uma pasta."""

    tipo_item: str = "Pasta"
    subitens: List[str] = field(
        default_factory=list
    )  # Lista de nomes de arquivos/pastas
    caminho_pasta: str = ""
    ultima_modificacao: float = 0.0  # Timestamp em segundos
    data_acesso: float = 0.0  # Timestamp em segundos
    data_criacao: float = 0.0  # Timestamp em segundos
    tamanho_total_bytes: int = 0

    @property
    def quantidade_subitens(self) -> int:
        """Retorna a quantidade de subitens na pasta."""
        return len(self.subitens)

    @property
    def tamanho_total_formatado(self) -> str:
        """
        Retorna o tamanho total da pasta formatado em uma unidade legível.

        O tamanho é convertido para a unidade mais apropriada (B, KB, MB, GB, TB, PB),
        dependendo do valor de `tamanho_total_bytes`.

        Returns:
            str: O tamanho total formatado, incluindo a unidade.
        """
        tamanho = float(self.tamanho_total_bytes)
        for unidade in ["B", "KB", "MB", "GB", "TB"]:
            if tamanho < 1024:
                return f"{tamanho:.2f} {unidade}"
            tamanho /= 1024
        return f"{tamanho:.2f} PB"  # Caso padrão para tamanhos extremamente grandes

    @property
    def ultima_modificacao_formatada(self) -> str:
        """Retorna a data de modificação formatada."""
        return datetime.fromtimestamp(self.ultima_modificacao).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def esta_vazia(self) -> bool:
        """Verifica se a pasta está vazia."""
        return len(self.subitens) == 0

    def contem_arquivos_com_extensao(self, extensao: str) -> List[str]:
        """Retorna uma lista de arquivos com a extensão especificada."""
        return [arquivo for arquivo in self.subitens if arquivo.endswith(extensao)]

    @property
    def data_criacao_formatada(self) -> str:
        """Retorna a data de criação formatada."""
        return datetime.fromtimestamp(self.data_criacao).strftime("%Y-%m-%d %H:%M:%S")
