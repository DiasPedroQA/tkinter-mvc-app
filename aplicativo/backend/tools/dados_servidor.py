# -*- coding: utf-8 -*-
# Arquivo Novo e Único

"""
Módulo unificado responsável por fornecer informações do sistema operacional,
usuário atual e análise detalhada de caminhos do sistema de arquivos.
"""

import os
import platform
import getpass
from pathlib import Path
from datetime import datetime

from aplicativo.backend.tools.resultado import ResultadoAnalise


class SistemaArquivoInfo:
    """Classe que centraliza informações sobre sistema, máquina, usuário e regras por Sistema."""

    _REGRAS_CARACTERES = {
        "Windows": ['<', '>', ':', '"', '/', '\\', '|', '?', '*'],
        "Linux": ['\0', '\\'],
        "macOS": [":"],
    }

    _MAPA_SISTEMAS = {
        "Windows": "Windows",
        "Linux": "Linux",
        "Darwin": "macOS",
    }

    @classmethod
    def detectar_sistema(cls) -> str:
        """
        Detecta o sistema operacional atual.

        Returns:
            str: Nome técnico do sistema operacional (ex: 'Linux', 'Windows', 'Darwin').
        """
        return platform.system()

    @classmethod
    def sistema_local(cls) -> str:
        """
        Retorna o nome padronizado do sistema operacional atual.

        Returns:
            str: Nome amigável do sistema (Windows, Linux, macOS ou Desconhecido).
        """
        return cls._MAPA_SISTEMAS.get(cls.detectar_sistema(), "Desconhecido")

    @classmethod
    def caracteres_invalidos(cls, sistema: str | None = None) -> list[str]:
        """
        Retorna a lista de caracteres inválidos para o sistema especificado ou local.

        Args:
            sistema (str | None): Nome do sistema operacional ou None para autodetecção.

        Returns:
            list[str]: Lista de caracteres proibidos.
        """
        sistema = sistema or cls.detectar_sistema()
        return cls._REGRAS_CARACTERES.get(sistema, [])

    @staticmethod
    def pegar_usuario_logado() -> str:
        """Retorna o nome do usuário atualmente logado."""
        return getpass.getuser()

    @staticmethod
    def pegar_versao() -> str:
        """Retorna a versão detalhada do sistema operacional."""
        return platform.version()

    @staticmethod
    def pegar_maquina() -> str:
        """Retorna a arquitetura da máquina (ex: 'x86_64', 'arm64')."""
        return platform.machine()


class AnaliseDeCaminho:
    """
    Classe que analisa um caminho do sistema de arquivos, verificando:
    - sistema operacional
    - existência, permissões e timestamps
    - caracteres inválidos
    - localização e tipo do caminho
    """

    def __init__(self, caminho: str):
        if not isinstance(caminho, str):
            raise TypeError("O caminho deve ser uma string.")

        self.resultado = ResultadoAnalise(caminho_original=caminho)
        self.caminho_path = Path(caminho)
        self.sistema_info = SistemaArquivoInfo

        # Pipeline de etapas automáticas
        self.etapas = [
            self._detectar_e_validar_sistema,
            self._verificar_caracteres,
            self._coletar_localizacao,
        ]

    def _detectar_e_validar_sistema(self) -> None:
        """Verifica se o sistema do caminho é compatível com o sistema local, e coleta info do arquivo."""
        sistema_detectado = self.sistema_info.detectar_sistema()
        sistema_local = self.sistema_info.sistema_local()

        self.resultado.sistema_detectado = sistema_detectado
        self.resultado.sistema_local = sistema_local
        self.resultado.sistemas_iguais = "Sim" if sistema_detectado == sistema_local else "Não"

        if sistema_detectado == sistema_local:
            try:
                stats = self.caminho_path.stat()
                self.resultado.mensagem_existencia = "O caminho pode existir."
                self.resultado.permissoes = {
                    "leitura": "Sim" if self.caminho_path.exists() else "Não",
                    "escrita": "Sim" if os.access(self.caminho_path, os.W_OK) else "Não",
                    "execucao": "Sim" if os.access(self.caminho_path, os.X_OK) else "Não",
                }
                self.resultado.timestamps = {
                    "data_criacao": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                    "data_acesso": datetime.fromtimestamp(stats.st_atime).isoformat(),
                    "data_modificacao": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                }
            except FileNotFoundError as e:
                self.resultado.mensagem_existencia = f"Arquivo não encontrado: {e}"
            except NotADirectoryError as e:
                self.resultado.mensagem_existencia = f"Não é um diretório: {e}"
            except PermissionError as e:
                self.resultado.mensagem_existencia = f"Permissão negada: {e}"
            except OSError as e:
                self.resultado.mensagem_existencia = f"Erro do sistema operacional: {e}"
        else:
            self.resultado.mensagem_existencia = "Sistemas incompatíveis para verificar existência."

    def _verificar_caracteres(self) -> None:
        """Verifica se o caminho contém caracteres inválidos para o sistema operacional."""
        sistema = self.resultado.sistema_detectado or "Desconhecido"
        proibidos = self.sistema_info.caracteres_invalidos(sistema)
        if encontrados := [c for c in proibidos if c in self.resultado.caminho_original]:
            self.resultado.erros = (
                f"Caractere(s) inválido(s) para {sistema}: {', '.join(encontrados)}"
            )
        else:
            self.resultado.sintaxe_permitida = f"Caminho válido para o sistema atual: {sistema}"

    def _coletar_localizacao(self) -> None:
        """Extrai dados básicos sobre o caminho: nome, tipo, raiz e usuário."""
        self.resultado.localizacao = {
            "nome_do_item": self.caminho_path.name,
            "pasta_pai": str(self.caminho_path.parent),
            "tipo_caminho": "absoluto" if self.caminho_path.is_absolute() else "relativo",
            "raiz": self.caminho_path.anchor,
            "usuario": self.sistema_info.pegar_usuario_logado(),
        }

    def montar_objeto_caminho(self) -> str:
        """Executa todas as etapas da análise e retorna o resultado em JSON."""
        for etapa in self.etapas:
            etapa()
        return self.resultado.to_json()

    def __str__(self) -> str:
        return self.montar_objeto_caminho()
