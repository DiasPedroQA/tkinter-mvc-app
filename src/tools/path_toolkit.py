# -*- coding: utf-8 -*-

"""
Ferramentas de extração de dados de caminhos (arquivos e pastas).

Este módulo fornece uma classe utilitária para extração de informações
detalhadas sobre arquivos e diretórios, com suporte à formatação JSON.

Funcionalidades:
- Identificação de tipo de caminho (arquivo ou diretório)
- Extração de metadados básicos e específicos
- Conversão de tamanhos e datas para formatos legíveis
- Tratamento de caminhos relativos, absolutos e iniciando com `~/` ou `/~/`
- Exportação dos dados em formato dicionário ou JSON

Autor: Pedro Dias
Data de criação: 2025-05-01
Data de modificação: 2025-05-17
Versão: 1.1.0
"""

import json
from datetime import datetime
from os import stat_result
from pathlib import Path
from typing import TypedDict


# Definições de tipos
class DadosBasicos(TypedDict):
    """Estrutura de dados básicos comuns a arquivos e diretórios.

    Atributos:
        tipo_caminho (str): Tipo do item ('ARQUIVO' ou 'DIRETORIO')
        nome_item (str): Nome do arquivo/diretório (com extensão, se aplicável)
        caminho_pai (str): Caminho do diretório pai
        caminho_absoluto (str): Caminho completo absoluto
        eh_absoluto (bool): Indica se o caminho é absoluto
        eh_link_simbolico (bool): Indica se é um link simbólico
        criado_em (str): Data de criação no formato 'YYYY-MM-DD HH:MM:SS'
        modificado_em (str): Data da última modificação no mesmo formato
        acessado_em (str): Data do último acesso no mesmo formato
        id_caminho (int): Número de inode (identificador único no sistema de arquivos)
    """

    tipo_caminho: str
    nome_item: str
    caminho_pai: str
    caminho_absoluto: str
    eh_absoluto: bool
    eh_link_simbolico: bool
    criado_em: str
    modificado_em: str
    acessado_em: str
    id_caminho: int


class DadosArquivo(DadosBasicos):
    """Estrutura de dados estendida para arquivos.

    Herda todos os atributos de DadosBasicos e adiciona campos específicos de arquivos.

    Atributos:
        extensao (str): Extensão do arquivo (incluindo o ponto, ex: '.txt')
        nome_sem_extensao (str): Nome do arquivo sem a extensão
        tamanho_bytes (int): Tamanho em bytes
        tamanho_formatado (str): Tamanho formatado (ex: '1.23 MB')
    """

    extensao: str
    nome_sem_extensao: str
    tamanho_bytes: int
    tamanho_formatado: str


class DadosDiretorio(DadosBasicos):
    """Estrutura de dados estendida para diretórios.

    Herda todos os atributos de DadosBasicos e adiciona campos específicos de diretórios.

    Atributos:
        subitens (list[str]): Lista de nomes de todos os itens contidos no diretório
        quantidade_total_itens (int): Quantidade total de itens no diretório
        total_arquivos (int): Quantidade de arquivos no diretório
        total_subpastas (int): Quantidade de subdiretórios
        arquivos_ocultos (list[str]): Lista de nomes de arquivos ocultos (iniciados com '.')
        pastas_ocultas (list[str]): Lista de nomes de pastas ocultas (iniciadas com '.')
        tamanho_total_arquivos_bytes (int): Soma do tamanho de todos os arquivos em bytes
        tamanho_total_arquivos_formatado (str): Tamanho total formatado (ex: '4.56 GB')
    """

    subitens: list[str]
    quantidade_total_itens: int
    total_arquivos: int
    total_subpastas: int
    arquivos_ocultos: list[str]
    pastas_ocultas: list[str]
    tamanho_total_arquivos_bytes: int
    tamanho_total_arquivos_formatado: str


class ExtratorDeCaminhos:
    """Classe utilitária para extração e tratamento de
    informações de caminhos do sistema de arquivos.

    Fornece métodos para:
    - Normalização e preparação de caminhos
    - Identificação do tipo de caminho (arquivo/diretório)
    - Extração de metadados básicos e específicos
    - Formatação de dados para saída

    Atributos:
        _caminho_original (Path | None): Caminho original fornecido
        _caminho_tratado (Path | None): Caminho após tratamento (absoluto/resolvido)
    """

    def __init__(self) -> None:
        """Inicializa o extrator com caminhos nulos."""
        self._caminho_original: Path | None = None
        self._caminho_tratado: Path | None = None

    @property
    def caminho(self) -> Path:
        """Retorna o caminho tratado atual.

        Returns:
            Path: Caminho absoluto e resolvido

        Raises:
            ValueError: Se nenhum caminho foi preparado
        """
        if self._caminho_tratado is None:
            raise ValueError("Nenhum caminho foi preparado ainda.")
        return self._caminho_tratado

    def preparar_caminho(self, caminho_raw: Path | str) -> Path:
        """Prepara e normaliza um caminho do sistema de arquivos.

        Args:
            caminho_raw: Caminho como string ou objeto Path

        Returns:
            Path: Caminho absoluto e resolvido

        Note:
            Trata caminhos com ~ substituindo por home do usuário
            Converte caminhos relativos para absolutos
        """
        if isinstance(caminho_raw, str):
            caminho_raw = caminho_raw.replace("/~/", "~/")
        caminho_path: Path = Path(caminho_raw).expanduser()
        self._caminho_original = caminho_path
        self._caminho_tratado = caminho_path.resolve().absolute()
        return self._caminho_tratado

    def eh_absoluto(self) -> bool:
        """Verifica se o caminho atual é absoluto.

        Returns:
            bool: True se for caminho absoluto
        """
        return self.caminho.is_absolute()

    def como_absoluto(self) -> Path:
        """Retorna o caminho tratado como absoluto.

        Returns:
            Path: Caminho absoluto
        """
        return self.caminho

    def definir_tipo_caminho(self, caminho_absoluto: Path) -> str:
        """Determina se o caminho é arquivo ou diretório.

        Args:
            caminho_absoluto: Caminho absoluto a ser verificado

        Returns:
            str: 'ARQUIVO' ou 'DIRETORIO'

        Raises:
            FileNotFoundError: Se o caminho não existir
        """
        if caminho_absoluto.is_file():
            return "ARQUIVO"
        if caminho_absoluto.is_dir():
            return "DIRETORIO"
        raise FileNotFoundError(f"Caminho inválido ou inexistente: {caminho_absoluto}")

    def extrair_dados_basicos(self, caminho: Path) -> DadosBasicos:
        """Extrai metadados básicos comuns a arquivos e diretórios.

        Args:
            caminho: Caminho absoluto do item

        Returns:
            DadosBasicos: Dicionário tipado com metadados básicos
        """
        dados_stat: stat_result = caminho.stat()
        return {
            "tipo_caminho": self.definir_tipo_caminho(caminho_absoluto=caminho),
            "nome_item": caminho.name,
            "caminho_pai": str(caminho.parent),
            "caminho_absoluto": str(caminho),
            "eh_absoluto": caminho.is_absolute(),
            "eh_link_simbolico": caminho.is_symlink(),
            "criado_em": self._formatar_data(marco_temporal=dados_stat.st_ctime),
            "modificado_em": self._formatar_data(marco_temporal=dados_stat.st_mtime),
            "acessado_em": self._formatar_data(marco_temporal=dados_stat.st_atime),
            "id_caminho": dados_stat.st_ino,
        }

    def extrair_dados_de_diretorio(self, caminho_diretorio: Path) -> DadosDiretorio:
        """Extrai metadados específicos de diretórios.

        Args:
            caminho_diretorio: Caminho absoluto do diretório

        Returns:
            DadosDiretorio: Dicionário tipado com metadados de diretório
        """
        lista_de_itens = list(caminho_diretorio.iterdir())
        arquivos: list[Path] = [item for item in lista_de_itens if item.is_file()]
        subpastas: list[Path] = [item for item in lista_de_itens if item.is_dir()]
        ocultos: list[Path] = [
            item for item in lista_de_itens if item.name.startswith(".")
        ]
        tamanho_total: int = sum(arquivo.stat().st_size for arquivo in arquivos)

        return {
            "subitens": [item.name for item in lista_de_itens],
            "quantidade_total_itens": len(lista_de_itens),
            "total_arquivos": len(arquivos),
            "total_subpastas": len(subpastas),
            "arquivos_ocultos": [arq.name for arq in ocultos if arq.is_file()],
            "pastas_ocultas": [dir.name for dir in ocultos if dir.is_dir()],
            "tamanho_total_arquivos_bytes": tamanho_total,
            "tamanho_total_arquivos_formatado": self._formatar_tamanho(
                tamanho_bytes=tamanho_total
            ),
            **self.extrair_dados_basicos(caminho=caminho_diretorio),
        }

    def extrair_dados_de_arquivo(self, caminho_arquivo: Path) -> DadosArquivo:
        """Extrai metadados específicos de arquivos.

        Args:
            caminho_arquivo: Caminho absoluto do arquivo

        Returns:
            DadosArquivo: Dicionário tipado com metadados de arquivo
        """
        tamanho: int = caminho_arquivo.stat().st_size
        return {
            "extensao": caminho_arquivo.suffix,
            "nome_sem_extensao": caminho_arquivo.stem,
            "tamanho_bytes": tamanho,
            "tamanho_formatado": self._formatar_tamanho(tamanho_bytes=tamanho),
            **self.extrair_dados_basicos(caminho=caminho_arquivo),
        }

    def _formatar_data(self, marco_temporal: float) -> str:
        """Formata timestamp em string de data legível.

        Args:
            marco_temporal: Timestamp Unix

        Returns:
            str: Data formatada como 'YYYY-MM-DD HH:MM:SS'
        """
        return datetime.fromtimestamp(marco_temporal).strftime("%Y-%m-%d %H:%M:%S")

    def _formatar_tamanho(self, tamanho_bytes: float) -> str:
        """Converte tamanho em bytes para unidade mais adequada.

        Args:
            tamanho_bytes: Tamanho em bytes

        Returns:
            str: Tamanho formatado com unidade (ex: '1.23 MB')
        """
        unidades: list[str] = ["bytes", "KB", "MB", "GB", "TB", "PB"]
        tamanho = float(tamanho_bytes)
        indice = 0
        while tamanho >= 1024 and indice < len(unidades) - 1:
            tamanho /= 1024
            indice += 1
        return f"{tamanho:.2f} {unidades[indice]}"

    def _como_json(
        self, metadados: DadosBasicos | DadosArquivo | DadosDiretorio
    ) -> str:
        """Converte metadados para string JSON formatada.

        Args:
            metadados: Dicionário de metadados

        Returns:
            str: JSON formatado e indentado
        """
        return json.dumps(metadados, indent=4, ensure_ascii=False, sort_keys=True)


# def main() -> None:
#     """Função principal para demonstração das funcionalidades."""
#     extrator = ExtratorDeCaminhos()

#     caminhos: list[str] = [
#         "~/Downloads/Firefox/bookmarks.html",
#         "~/Downloads/Firefox/",
#     ]

#     for caminho_raw in caminhos:
#         try:
#             caminho: Path = extrator.preparar_caminho(caminho_raw=caminho_raw)
#             tipo: str = extrator.definir_tipo_caminho(caminho_absoluto=caminho)

#             print(f"\n[DADOS BÁSICOS - {tipo}]: {caminho}")
#             dados_basicos: DadosBasicos = extrator.extrair_dados_basicos(
#                 caminho=caminho
#             )
#             print(dados_basicos)

#             print(f"\n[DADOS ESPECÍFICOS - {tipo}]")
#             if tipo == "ARQUIVO":
#                 dados_arquivo: DadosArquivo = extrator.extrair_dados_de_arquivo(
#                     caminho_arquivo=caminho
#                 )
#                 print(dados_arquivo)
#             elif tipo == "DIRETORIO":
#                 dados_diretorio: DadosDiretorio = extrator.extrair_dados_de_diretorio(
#                     caminho_diretorio=caminho
#                 )
#                 print(dados_diretorio)
#         except Exception as e:
#             print(f"\n[ERRO AO PROCESSAR '{caminho_raw}']: {e}")


# if __name__ == "__main__":
#     main()
