# -*- coding: utf-8 -*-
"""
Módulo simplificado para manipulação de caminhos com operações seguras e eficientes.
"""

import grp
from os import stat_result
from pathlib import Path
import pwd
import re
from typing import Any, Optional, Union

from src.tools.datetime_utils import GerenciadorDeDataHora


class GerenciadorDeCaminhos:
    """
    Classe para gerenciamento de caminhos de arquivos e diretórios.
    """

    def __init__(self, caminho_entrada: Union[str, Path]) -> None:
        """
        Inicializa o gerenciador com um caminho e validações básicas.

        Args:
            caminho_entrada: Caminho absoluto ou relativo como string ou objeto Path
        """
        self._caminho_original: str = str(caminho_entrada)
        self._caminho_sanitizado: Path = self._sanitizar_path(caminho_entrada)
        self._estatisticas: Optional[stat_result] = None
        self._inicializar_propriedades()

        # Inicializa o GerenciadorDeDataHora com base nas estatísticas do caminho
        self._gerenciador_data_hora = GerenciadorDeDataHora(
            timestamp_modificacao=self._estatisticas.st_mtime if self._estatisticas else 0.0,
            timestamp_acesso=self._estatisticas.st_atime if self._estatisticas else 0.0,
            timestamp_criacao=self._estatisticas.st_ctime if self._estatisticas else 0.0,
            dias_antes=7,
        )

    def _inicializar_propriedades(self) -> None:
        """Inicializa as propriedades básicas do caminho."""
        self._estatisticas = (
            self._caminho_sanitizado.stat() if self._caminho_sanitizado.exists() else None
        )

    @property
    def tipo(self) -> str:
        """Retorna o tipo do item: 'arquivo', 'pasta' ou 'inexistente'."""
        if not self._caminho_sanitizado.exists():
            return "inexistente"
        return "Arquivo" if self._caminho_sanitizado.is_file() else "Pasta"

    @property
    def permissoes(self) -> Optional[str]:
        """Retorna as permissões no formato legível."""
        if not self._estatisticas:
            return None
        try:
            modo = self._estatisticas.st_mode
            user = pwd.getpwuid(self._estatisticas.st_uid).pw_name
            group = grp.getgrgid(self._estatisticas.st_gid).gr_name
            permissoes = self._formatar_permissoes(modo)
            return f"{permissoes} {user}:{group}"
        except (KeyError, PermissionError):
            return None

    def obter_informacoes(self) -> dict[str, Any]:
        """Retorna um dicionário completo com todas as informações do caminho."""
        informacoes = self._gerenciador_data_hora.obter_informacoes()
        info_datas_convertidas = informacoes.get("datas_formatadas", {})

        dados = {
            "geral": {
                "caminho_original": self._caminho_original,
                "caminho_corrigido": str(self._caminho_sanitizado),
                "tipo_caminho": self.tipo,
                "caminho_existe": self._caminho_sanitizado.exists(),
                "nome_caminho": self._caminho_sanitizado.name,
                "diretorio_pai_caminho": str(self._caminho_sanitizado.parent),
            },
            "datas": {
                "data_modificacao": info_datas_convertidas.get("data_modificacao_formatada", ""),
                "data_acesso": info_datas_convertidas.get("data_acesso_formatada", ""),
                "data_criacao": info_datas_convertidas.get("data_criacao_formatada", ""),
            },
        }

        if self.tipo == "Arquivo":
            dados["arquivo"] = {
                "extensao": self._caminho_sanitizado.suffix,
                "tamanho_bytes": self._estatisticas.st_size if self._estatisticas else 0,
                "permissoes": self.permissoes,
            }
        elif self.tipo == "Pasta":
            dados["pasta"] = {
                "permissoes": self.permissoes,
            }

        return dados

    @staticmethod
    def _sanitizar_path(caminho_bruto: Union[str, Path]) -> Path:
        """Normaliza e sanitiza um caminho bruto de forma segura."""
        caminho_str = str(caminho_bruto).strip()
        caminho_normal = re.sub(r"[\\]+", "/", caminho_str)
        return Path(caminho_normal).expanduser().resolve(strict=False)

    @staticmethod
    def _formatar_permissoes(modo: int) -> str:
        """Converte as permissões para o formato legível (rwxr-xr-x)."""
        permissoes = [
            (modo & 0o400, "r"),
            (modo & 0o200, "w"),
            (modo & 0o100, "x"),  # Dono
            (modo & 0o040, "r"),
            (modo & 0o020, "w"),
            (modo & 0o010, "x"),  # Grupo
            (modo & 0o004, "r"),
            (modo & 0o002, "w"),
            (modo & 0o001, "x"),  # Outros
        ]
        return "".join(letra if flag else "-" for flag, letra in permissoes)


# # Exemplo de uso
# if __name__ == "__main__":
#     caminho_arquivo = "~/Downloads/Firefox/bookmarks.html"
#     caminho_pasta = "~/Downloads/"

#     def exibir_em_tabela(titulo: str, dados: dict[str, Any]) -> None:
#         print("\n" + "=" * 60)
#         print(f"{titulo.upper():^60}")
#         print("=" * 60)
#         for chave, valor in dados.items():
#             print(f"{chave}: {valor}")

#     gerenciador_arquivo = GerenciadorDeCaminhos(caminho_arquivo)
#     info_arquivo = gerenciador_arquivo.obter_informacoes()
#     exibir_em_tabela(f"Analisando arquivo: {caminho_arquivo}", info_arquivo)

#     gerenciador_pasta = GerenciadorDeCaminhos(caminho_pasta)
#     info_pasta = gerenciador_pasta.obter_informacoes()
#     exibir_em_tabela(f"Analisando pasta: {caminho_pasta}", info_pasta)
