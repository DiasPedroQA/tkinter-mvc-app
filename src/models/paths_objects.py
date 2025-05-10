'''
Modelos para representar arquivos, pastas e caminhos do sistema.
'''

from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import sys

# Adiciona a pasta 'src/' ao sys.path
sys.path.append(str(Path(__file__).resolve().parent / 'src'))

from tools.datetime_utils import GerenciadorDeDataHora
from tools.path_operations import GerenciadorDeCaminho


@dataclass
class ObjetoCaminho:
    caminho: str
    tipo_item: str
    ultima_modificacao: float = 0.0
    data_acesso: float = 0.0
    data_criacao: float = 0.0

    @property
    def ultima_modificacao_formatada(self) -> str:
        return GerenciadorDeDataHora.timestamp_para_str(self.ultima_modificacao)

    @property
    def data_acesso_formatada(self) -> str:
        return GerenciadorDeDataHora.timestamp_para_str(self.data_acesso)

    @property
    def data_criacao_formatada(self) -> str:
        return GerenciadorDeDataHora.timestamp_para_str(self.data_criacao)


@dataclass
class ObjetoArquivo(ObjetoCaminho):
    extensao: str = ""
    tamanho_bytes: int = 0
    permissoes: str = ""

    @classmethod
    def from_path(cls, path: Path):
        info = GerenciadorDeCaminho.obter_info_arquivo(path)
        return cls(
            caminho=str(path),
            tipo_item="Arquivo",
            extensao=info.extensao,
            tamanho_bytes=info.tamanho,
            ultima_modificacao=info.modificacao,
            data_acesso=info.acesso,
            data_criacao=info.criacao,
            permissoes=info.permissoes,
        )

    def atualizar_dados(self):
        atualizado = self.from_path(Path(self.caminho))
        self.__dict__.update(atualizado.__dict__)

    @property
    def tamanho_formatado(self) -> str:
        return GerenciadorDeCaminho.formatar_tamanho(self.tamanho_bytes)

    def eh_arquivo_grande(self, limite_mb: int = 100) -> bool:
        return self.tamanho_bytes > limite_mb * 1024 * 1024

    def eh_recente(self, dias: int = 7) -> bool:
        return GerenciadorDeDataHora.eh_recente(self.ultima_modificacao, dias)

    def exibir_detalhes(self) -> dict:
        return {
            "caminho": self.caminho,
            "tipo_item": self.tipo_item,
            "extensao": self.extensao,
            "tamanho_bytes": self.tamanho_bytes,
            "tamanho_formatado": self.tamanho_formatado,
            "permissoes": self.permissoes,
            "ultima_modificacao": self.ultima_modificacao_formatada,
            "data_acesso": self.data_acesso_formatada,
            "data_criacao": self.data_criacao_formatada,
        }


@dataclass
class ObjetoPasta(ObjetoCaminho):
    subitens: List[str] = field(default_factory=list)
    tamanho_total_bytes: int = 0

    @classmethod
    def from_path(cls, path: Path):
        info = GerenciadorDeCaminho.obter_info_pasta(path)
        return cls(
            caminho=str(path),
            tipo_item="Pasta",
            subitens=info.subitens,
            tamanho_total_bytes=info.tamanho,
            ultima_modificacao=info.modificacao,
            data_acesso=info.acesso,
            data_criacao=info.criacao,
        )

    def atualizar_dados(self):
        atualizado = self.from_path(Path(self.caminho))
        self.__dict__.update(atualizado.__dict__)

    @property
    def tamanho_total_formatado(self) -> str:
        return GerenciadorDeCaminho.formatar_tamanho(self.tamanho_total_bytes)

    @property
    def quantidade_subitens(self) -> int:
        return len(self.subitens)

    def esta_vazia(self) -> bool:
        return not self.subitens

    def contem_arquivos_com_extensao(self, extensao: str) -> List[str]:
        return [item for item in self.subitens if item.endswith(extensao)]

    def exibir_detalhes(self) -> dict:
        return {
            "caminho": self.caminho,
            "tipo_item": self.tipo_item,
            "quantidade_subitens": self.quantidade_subitens,
            "tamanho_total_bytes": self.tamanho_total_bytes,
            "tamanho_total_formatado": self.tamanho_total_formatado,
            "ultima_modificacao": self.ultima_modificacao_formatada,
            "data_acesso": self.data_acesso_formatada,
            "data_criacao": self.data_criacao_formatada,
        }


if __name__ == "__main__":
    # Caminhos
    caminho_arquivo = Path("/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html")
    caminho_pasta = Path("/home/pedro-pm-dias/Downloads/")

    # Criando o objeto de arquivo
    arquivo = ObjetoArquivo.from_path(caminho_arquivo)
    print("=== Detalhes do Arquivo ===")
    print(arquivo.exibir_detalhes())

    # Criando o objeto de pasta
    pasta = ObjetoPasta.from_path(caminho_pasta)
    print("\n=== Detalhes da Pasta ===")
    print(pasta.exibir_detalhes())
