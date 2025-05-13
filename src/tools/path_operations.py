# -*- coding: utf-8 -*-
"""
Módulo para manipulação e análise de caminhos de arquivos e pastas com uso de pathlib.
"""

import os
from pathlib import Path
import re
from typing import Optional, Union

from src.tools.datetime_utils import FormatadorDeDataHora


class GerenciadorDeCaminhos:
    """
    Classe para análise de caminhos de arquivos e diretórios.
    """

    def __init__(self, caminho_entrada: Union[str, Path]) -> None:
        """
        Inicializa o gerenciador com um caminho e prepara os dados.

        Args:
            caminho_entrada: Caminho absoluto ou relativo (str ou Path).
        """
        self._caminho_original: str = str(caminho_entrada)
        self._caminho_sanitizado: Path = self._sanitizar_path(caminho_entrada)

        self._existe: bool = self._caminho_sanitizado.exists()
        self._tipo: str = self._determinar_tipo()
        self._estatisticas: Optional[os.stat_result] = (
            self._caminho_sanitizado.stat() if self._existe else None
        )

        self._tamanho_bytes: int = self._obter_tamanho()
        self._tamanho_formatado: str = self._formatar_tamanho(self._tamanho_bytes)

        self._gerenciador_data_hora = FormatadorDeDataHora(
            timestamp_modificacao=self._estatisticas.st_mtime if self._estatisticas else 0.0,
            timestamp_acesso=self._estatisticas.st_atime if self._estatisticas else 0.0,
            timestamp_criacao=self._estatisticas.st_ctime if self._estatisticas else 0.0,
            dias_antes=7,
        )

    @staticmethod
    def _sanitizar_path(caminho_bruto: Union[str, Path]) -> Path:
        """Sanitiza e normaliza o caminho fornecido."""
        caminho_str = str(caminho_bruto).strip()
        caminho_normalizado = re.sub(r"[\\]+", "/", caminho_str)
        return Path(caminho_normalizado).expanduser().resolve(strict=False)

    def _determinar_tipo(self) -> str:
        """Determina se o caminho é um arquivo, pasta ou inexistente."""
        if not self._existe:
            return "Inexistente"
        return "Arquivo" if self._caminho_sanitizado.is_file() else "Pasta"

    def _obter_tamanho(self) -> int:
        """Obtém o tamanho do item: arquivo (direto) ou pasta (recursivamente)."""
        if not self._existe:
            return 0
        if self._caminho_sanitizado.is_file():
            return self._estatisticas.st_size if self._estatisticas else 0
        # Soma recursiva do tamanho dos arquivos em uma pasta
        return sum(f.stat().st_size for f in self._caminho_sanitizado.rglob("*") if f.is_file())

    @staticmethod
    def _formatar_tamanho(tamanho_bytes: int) -> str:
        """Converte o tamanho de bytes para uma string legível."""
        unidades = ["B", "KB", "MB", "GB", "TB"]
        tamanho = float(tamanho_bytes)
        for unidade in unidades:
            if tamanho < 1024:
                return f"{tamanho:.2f} {unidade}"
            tamanho /= 1024
        return f"{tamanho:.2f} PB"

    @staticmethod
    def _formatar_permissoes(modo: int) -> str:
        """Converte as permissões numéricas para rwxr-xr-x."""
        permissoes = [
            (modo & 0o400, "r"),
            (modo & 0o200, "w"),
            (modo & 0o100, "x"),
            (modo & 0o040, "r"),
            (modo & 0o020, "w"),
            (modo & 0o010, "x"),
            (modo & 0o004, "r"),
            (modo & 0o002, "w"),
            (modo & 0o001, "x"),
        ]
        return "".join(letra if flag else "-" for flag, letra in permissoes)

    @property
    def permissoes(self) -> str:
        """Permissões do item no formato legível."""
        if not self._estatisticas:
            return self._formatar_permissoes(0)
        try:
            return self._formatar_permissoes(self._estatisticas.st_mode)
        except Exception:
            return self._formatar_permissoes(0)

    @property
    def tipo(self) -> str:
        """Tipo do caminho analisado."""
        return self._tipo

    def informacoes_de_caminho(self) -> dict:
        """
        Retorna um dicionário com informações gerais e de datas.
        """
        info_data_e_hora: dict[str, Union[str, int, float]] = (
            self._gerenciador_data_hora.infos_de_data_e_hora()
        )

        dados_gerais: dict[str, str] = {
            "caminho_original": str(self._caminho_original),
            "caminho_corrigido": str(self._caminho_sanitizado),
            "caminho_existe": "Sim" if self._existe else "Não",
            "tipo_caminho": str(self._tipo),
            "nome_caminho": str(self._caminho_sanitizado.name),
            "diretorio_pai_caminho": str(self._caminho_sanitizado.parent),
            "permissoes": str(self.permissoes),
            "tamanho_formatado": self._tamanho_formatado,
        }

        if self._tipo == "Arquivo":
            dados_gerais["extensao_arquivo"] = self._caminho_sanitizado.suffix

        dados_data: dict[str, Union[str, int, float]] = {
            "timestamp_modificacao": info_data_e_hora.get("timestamp_modificacao", 0.0),
            "timestamp_acesso": info_data_e_hora.get("timestamp_acesso", 0.0),
            "timestamp_criacao": info_data_e_hora.get("timestamp_criacao", 0.0),
            "timestamp_n_dias_atras": info_data_e_hora.get("timestamp_n_dias_atras", 0.0),
            "data_modificacao_formatada": info_data_e_hora.get("data_modificacao_formatada", ""),
            "dias_desde_modificacao": info_data_e_hora.get("dias_desde_modificacao", 0),
            "data_acesso_formatada": info_data_e_hora.get("data_acesso_formatada", ""),
            "dias_desde_acesso": info_data_e_hora.get("dias_desde_acesso", 0),
            "data_criacao_formatada": info_data_e_hora.get("data_criacao_formatada", ""),
            "dias_desde_criacao": info_data_e_hora.get("dias_desde_criacao", 0),
            "data_n_dias_atras_formatada": info_data_e_hora.get("data_n_dias_atras_formatada", ""),
        }

        return {
            "geral": dados_gerais,
            "datas": dados_data,
        }


# Exemplo de uso
if __name__ == "__main__":
    caminho_arquivo = "~/Downloads/Firefox/bookmarks.html"
    caminho_pasta = "~/Downloads/"

    gerenciador_arquivo = GerenciadorDeCaminhos(caminho_arquivo)
    info_arquivo = gerenciador_arquivo.informacoes_de_caminho()
    print(f"\n\nAnalisando arquivo: {caminho_arquivo}")
    for chave, valor in info_arquivo.items():
        print(f"\n{chave}: {valor}")

    gerenciador_pasta = GerenciadorDeCaminhos(caminho_pasta)
    info_pasta = gerenciador_pasta.informacoes_de_caminho()
    print(f"\n\nAnalisando pasta: {caminho_pasta}")
    for chave, valor in info_pasta.items():
        print(f"\n{chave}: {valor}")
