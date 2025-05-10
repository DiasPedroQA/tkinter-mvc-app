from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Union


@dataclass
class ObjetoArquivo:
    tipo_item: str = "Arquivo"
    extensao_arquivo: str = ""
    tamanho_bytes: int = 0
    ultima_modificacao: float = 0.0
    caminho_arquivo: str = ""

    @property
    def ultima_modificacao_formatada(self) -> str:
        return datetime.fromtimestamp(self.ultima_modificacao).strftime('%Y-%m-%d %H:%M:%S')


@dataclass
class ObjetoPasta:
    tipo_item: str = "Pasta"
    subitens: list[str] = field(default_factory=list)
    caminho_pasta: str = ""


@dataclass
class ResultadoAnalise:
    sucesso: bool = False
    mensagem: str = ""
    caminho_tratado: str = ""
    tipo_caminho: str = ""
    objetos_coletados: Optional[Union[ObjetoArquivo, ObjetoPasta]] = None
    caminho_corrigido: Optional[str] = None
