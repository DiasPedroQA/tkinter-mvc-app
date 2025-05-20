# pylint: disable=missing-function-docstring, missing-module-docstring

"""
Módulo de modelo de dados para caminhos de arquivos e diretórios.

Define a classe CaminhoModel, que representa um caminho no sistema de arquivos
com informações estruturadas como nome, tipo, existência e status. A modelagem
é baseada nas definições reutilizáveis do módulo `tools.path_definitions`.

Inclui:
- Conversão de string ou Path para objeto de modelo.
- Verificações robustas de existência e tipo.
- Compatibilidade com PathData.
- Função de exemplo `main()` com caminhos de teste.
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from tools.path_definitions import (
    PathData,
    PathInvalidError,
    PathNotFoundError,
    PathStatus,
    PathType,
)


@dataclass
class CaminhoModel:
    """
    Modelo de dados para representar informações de um caminho no sistema de arquivos.

    Atributos:
        nome (str): Nome base do caminho (arquivo ou diretório).
        tipo (PathType): Tipo do caminho (FILE, DIRECTORY, UNKNOWN, ERROR).
        caminho (str): Caminho absoluto.
        status (PathStatus): Estado atual do caminho (EXISTS, NOT_EXISTS, etc.).
    """

    nome: str
    tipo: PathType
    caminho: str
    status: PathStatus = PathStatus.UNKNOWN

    @classmethod
    def from_path(cls, caminho_input: Union[str, Path]) -> "CaminhoModel":
        """
        Cria uma instância de CaminhoModel a partir de uma string ou objeto Path.

        Realiza resolução do caminho, verifica sua existência e tipo, e retorna
        uma instância da model. Erros são tratados com retorno controlado.

        Args:
            caminho_input (str | Path): Caminho como string ou objeto Path.

        Returns:
            CaminhoModel: Instância da model preenchida com os metadados.
        """
        try:
            if not caminho_input or not isinstance(caminho_input, (str, Path)):
                raise PathInvalidError(str(caminho_input))

            caminho = Path(caminho_input).expanduser().resolve()

            if not caminho.exists():
                raise PathNotFoundError(str(caminho))

            tipo = (
                PathType.DIRECTORY
                if caminho.is_dir()
                else PathType.FILE
                if caminho.is_file()
                else PathType.UNKNOWN
            )

            return cls(
                nome=caminho.name,
                tipo=tipo,
                caminho=str(caminho),
                status=PathStatus.EXISTS,
            )

        except PathNotFoundError as e:
            logging.warning(" Caminho não encontrado -> %s", e.path)
            return cls(
                nome=Path(caminho_input).name,
                tipo=PathType.UNKNOWN,
                caminho=str(Path(caminho_input).expanduser().resolve()),
                status=PathStatus.NOT_EXISTS,
            )
        except PathInvalidError as e:
            logging.error(" Caminho inválido -> %s", e.path)
            return cls(
                nome=str(caminho_input),
                tipo=PathType.ERROR,
                caminho=str(caminho_input),
                status=PathStatus.ERROR,
            )
        except (OSError, ValueError):
            logging.exception(
                " Erro inesperado ao processar caminho -> %s", caminho_input
            )
            return cls(
                nome=str(caminho_input),
                tipo=PathType.ERROR,
                caminho=str(caminho_input),
                status=PathStatus.ERROR,
            )

    def to_dict(self) -> dict[str, str | bool]:
        """
        Converte a instância para dicionário compatível com PathData.

        Returns:
            dict[str, str | bool]: Representação serializável dos dados do caminho.
        """
        return {
            "nome": self.nome,
            "tipo": self.tipo.value,
            "caminho": self.caminho,
            "status": self.status.value,
        }

    def to_pathdata(self) -> PathData:
        """
        Converte o objeto CaminhoModel para uma instância de PathData.

        Returns:
            PathData: Objeto equivalente com metadados principais.
        """
        return PathData(
            nome=self.nome,
            tipo=self.tipo,
            caminho=self.caminho,
            status=self.status,
        )

    def __str__(self) -> str:
        """
        Representação amigável para exibição em terminal ou logs.

        Returns:
            str: Texto formatado com dados principais.
        """
        return (
            f"{self.tipo.value.upper():<10} | {self.status.value:<10} | {self.nome} "
            f"({'Existe' if self.status.value else 'Não existe'})"
        )


def main() -> None:
    """
    Executa a análise de caminhos predefinidos e exibe os resultados no terminal.

    Utiliza a classe CaminhoModel para representar os caminhos e converte cada um
    em dicionário e PathData para demonstração de uso conjunto com path_definitions.
    """
    caminhos = [
        "~/Downloads/Firefox",
        "~/Downloads/Firefox/bookmarks.html",
        "~/Downloads/Firefox/bookmark.html",  # inexistente
        "~/Downloads/Chromium",  # inexistente
    ]

    print("\nAnálise de Caminhos:\n")
    for caminho in caminhos:
        modelo = CaminhoModel.from_path(caminho)

        # Conversão para dicionário
        print("→ Dict:", modelo.to_dict())

        # Conversão para PathData
        path_data = modelo.to_pathdata()
        print("→ PathData:", path_data)
        print("-" * 90)


if __name__ == "__main__":
    main()
