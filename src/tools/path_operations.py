"""
Módulo com utilitários para análise e manipulação de caminhos de arquivos e pastas,
baseado na biblioteca pathlib. Permite validações, normalizações e coleta de informações.
"""

import re
import difflib
from pathlib import Path
from typing import Union, Optional


class GerenciadorDeCaminho:
    """
    Classe que representa um caminho de arquivo ou pasta e fornece
    diversas informações e utilitários sobre ele.
    """

    def __init__(self, caminho: Union[str, Path]) -> None:
        """
        Inicializa o objeto com um caminho e realiza todas as verificações e normalizações.

        Args:
            caminho (Union[str, Path]): Caminho bruto a ser analisado.
        """
        self.caminho_bruto: str = str(caminho)
        self.caminho: Path = self._sanitizar_path(caminho)
        self.existe: bool = self.caminho.exists()
        self.eh_arquivo: bool = self.caminho.is_file()
        self.eh_pasta: bool = self.caminho.is_dir()
        self.eh_absoluto: bool = self.caminho.is_absolute()
        self.eh_relativo: bool = not self.eh_absoluto
        self.nome: str = self.caminho.name
        self.extensao: str = self.caminho.suffix.lstrip(".") if self.eh_arquivo else ""
        self.pai: str = str(self.caminho.parent)

    def obter_info(self) -> dict[str, Union[str, bool, Optional[Path]]]:
        """
        Retorna todas as informações sobre o caminho em forma de dicionário.

        Returns:
            dict[str, Union[str, bool, Optional[Path]]]: Dicionário
            contendo informações sobre o caminho.
        """
        info: dict[str, Union[str, bool, Optional[Path]]] = {
            "caminho_bruto": self.caminho_bruto,
            "caminho_normalizado": str(self.caminho),
            "existe": self.existe,
            "eh_arquivo": self.eh_arquivo,
            "eh_pasta": self.eh_pasta,
            "eh_absoluto": self.eh_absoluto,
            "eh_relativo": self.eh_relativo,
            "nome": self.nome,
            "extensao": self.extensao,
            "pai": self.pai,
        }

        caminho_corrigido: Optional[Path] = self.tentar_corrigir()
        if caminho_corrigido:
            info["caminho_corrigido"] = caminho_corrigido
        else:
            info["caminho_corrigido"] = None

        return info

    def tentar_corrigir(self) -> Optional[Path]:
        """
        Tenta corrigir o caminho com base em similaridade com diretórios existentes.

        Returns:
            Optional[Path]: Caminho corrigido, se possível.
        """
        partes: tuple[str, ...] = self.caminho.parts
        caminho_atual: Path = Path(partes[0]) if self.caminho.is_absolute() else Path()
        for parte in partes[1:]:
            if not caminho_atual.exists():
                return None
            try:
                opcoes: list[str] = [p.name for p in caminho_atual.iterdir()]
            except (PermissionError, FileNotFoundError, NotADirectoryError):
                return None
            similares: list[str] = difflib.get_close_matches(parte, opcoes, n=1, cutoff=0.6)
            caminho_atual = caminho_atual / (similares[0] if similares else parte)
        return caminho_atual if caminho_atual.exists() else None

    def criar_diretorio(self) -> None:
        """Cria o diretório atual se ele não existir (incluindo pais)."""
        if not self.eh_arquivo and not self.caminho.exists():
            self.caminho.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _sanitizar_path(caminho: Union[str, Path]) -> Path:
        """
        Sanitiza o caminho aplicando limpeza e conversão segura para Path.

        Args:
            caminho (Union[str, Path]): Caminho de entrada.

        Returns:
            Path: Caminho normalizado.
        """
        try:
            caminho_str: str = str(caminho) if isinstance(caminho, Path) else caminho
            caminho_normal: str = caminho_str.strip()
            caminho_normal = re.sub(r"[\\]+", "/", caminho_normal)
            caminho_normal = re.sub(r"\s*/\s*", "/", caminho_normal)
            caminho_normal = re.sub(r"/{2,}", "/", caminho_normal)
            caminho_normal = re.sub(r"[<>:\"|?*]", "", caminho_normal)
            while caminho_normal.startswith("../"):
                caminho_normal = caminho_normal[3:]
            return Path(caminho_normal).expanduser().resolve(strict=False)
        except Exception as e:
            raise ValueError(f"Caminho inválido: {caminho}") from e


# Exemplo de uso:

if __name__ == "__main__":
    analisador = GerenciadorDeCaminho("~/Downloads/Firefox/bookmarks.html")
    print(analisador.obter_info())
