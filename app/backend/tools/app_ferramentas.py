# -*- coding: utf-8 -*-

"""
Módulo responsável por realizar uma análise detalhada sobre um caminho do sistema de arquivos.
"""


import contextlib
import os
from pathlib import Path
from datetime import datetime

from app.backend.tools.resultado import ResultadoAnalise
from app.backend.tools.sistema_info import SistemaArquivoInfo


class AnaliseDeCaminho:
    """Analisa um caminho de sistema de arquivos.

    Esta classe realiza uma análise completa de um determinado caminho,
    fornecendo informações sobre o sistema de arquivos, caracteres
    inválidos, localização e outros detalhes relevantes.
    """

    def __init__(self, caminho: str):
        if not isinstance(caminho, str):
            raise TypeError("O caminho deve ser uma string.")

        self.resultado = ResultadoAnalise(caminho_original=caminho)
        self.etapas = [
            self._detectar_comparar_e_validar,
            self._verificar_caracteres_invalidos,
            self._obter_dados_localizacao,
        ]

    def _detectar_comparar_e_validar(self) -> None:
        """Detecta, compara e valida o sistema de arquivos do caminho.

        Este método detecta o sistema de arquivos do caminho fornecido,
        compara-o com o sistema local e valida o caminho se os sistemas
        forem compatíveis. As informações sobre a existência do caminho,
        permissões e timestamps são armazenadas no resultado.
        """
        caminho = self.resultado.caminho_original
        sistema_detectado = SistemaArquivoInfo.detectar_sistema(caminho)
        sistema_local = SistemaArquivoInfo.sistema_local()

        self.resultado.sistema_detectado = sistema_detectado
        self.resultado.sistema_local = sistema_local
        self.resultado.sistemas_iguais = "Sim" if sistema_detectado == sistema_local else "Não"

        if sistema_detectado == sistema_local:
            caminho_path = Path(caminho)
            try:
                stats = caminho_path.stat()
                self.resultado.mensagem_existencia = "O caminho pode existir."
                self.resultado.permissoes = {
                    "leitura": "Sim" if caminho_path.exists() else "Não",
                    "escrita": "Sim" if os.access(caminho, os.W_OK) else "Não",
                    "execucao": "Sim" if os.access(caminho, os.X_OK) else "Não",
                }
                self.resultado.timestamps = {
                    "data_criacao": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                    "data_acesso": datetime.fromtimestamp(stats.st_atime).isoformat(),
                    "data_modificacao": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                }
            except FileNotFoundError:
                self.resultado.mensagem_existencia = "Arquivo não encontrado."
            except NotADirectoryError:
                self.resultado.mensagem_existencia = "Não é um diretório."
            except PermissionError:
                self.resultado.mensagem_existencia = "Permissão negada."
            except OSError as e:
                self.resultado.mensagem_existencia = f"Erro do sistema operacional: {str(e)}"
        else:
            self.resultado.mensagem_existencia = "Sistemas incompatíveis para verificar existência."

    def _verificar_caracteres_invalidos(self) -> None:
        """Verifica se o caminho contém caracteres inválidos.

        Este método verifica se o caminho fornecido contém caracteres
        inválidos para o sistema de arquivos detectado. Se caracteres
        inválidos forem encontrados, uma mensagem de erro é armazenada
        no resultado. Caso contrário, uma mensagem de confirmação é
        armazenada.
        """
        caminho = self.resultado.caminho_original
        sistema = self.resultado.sistema_detectado or "Desconhecido"
        proibidos = SistemaArquivoInfo.caracteres_invalidos(sistema)

        if encontrados := [c for c in proibidos if c in caminho]:
            self.resultado.erros = (
                f"Caractere(s) inválido(s) para o sistema {sistema}: {', '.join(encontrados)}"
            )
        else:
            self.resultado.sintaxe_permitida = f"Caminho válido para o sistema atual: {sistema}"

    def _obter_dados_localizacao(self) -> None:
        """Obtém os dados de localização do caminho.

        Este método extrai informações sobre a localização do caminho,
        como o nome do item, a pasta pai, o tipo de caminho (absoluto
        ou relativo), a raiz e o usuário (se aplicável). Os dados
        obtidos são armazenados no resultado.
        """
        caminho = Path(self.resultado.caminho_original)
        tipo = "absoluto" if caminho.is_absolute() else "relativo"
        usuario = ""

        # Heurística para tentar extrair o nome de usuário
        with contextlib.suppress(Exception):
            parts = caminho.parts
            if self.resultado.sistema_detectado == "Linux" and len(parts) >= 3:
                usuario = parts[2]
            elif self.resultado.sistema_detectado == "macOS" and len(parts) >= 3:
                usuario = parts[2]
        self.resultado.localizacao = {
            "nome_do_item": caminho.name,
            "pasta_pai": str(caminho.parent),
            "tipo_caminho": tipo,
            "raiz": caminho.anchor,
            "usuario": usuario,
        }

    def executar(self) -> str:
        """
        Gerenciador de etapas de execução de cada método para a obtenção total dos dados
        """
        for etapa in self.etapas:
            etapa()
        return self.resultado.to_json()

    def __str__(self) -> str:
        return self.executar()
