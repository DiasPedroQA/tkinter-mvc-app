# -*- coding: utf-8 -*-

"""
Modelos de representação de caminhos (arquivos e pastas).

Este módulo define classes para representação estruturada de metadados
de arquivos e diretórios, com suporte à serialização em JSON.

Classes:
    ModeloDiretorio: Representa um diretório com todos seus metadados
    ModeloArquivo: Representa um arquivo com todos seus metadados
    ModeloCaminho: Factory que cria os modelos apropriados baseado no tipo de caminho

Funcionalidades:
- Criação de objetos tipados a partir de caminhos do sistema de arquivos
- Conversão para dicionário e JSON
- Acesso organizado a todos os metadados

Autor: Pedro Dias
Data de criação: 2025-05-01
Data de modificação: 2025-05-17
Versão: 1.1.0
"""

import json
from pathlib import Path

from tools.path_toolkit import DadosArquivo, DadosDiretorio, ExtratorDeCaminhos


class ModeloDiretorio:
    """Representação estruturada de um diretório com todos seus metadados.

    Atributos:
        tipo_caminho (str): Tipo do item ('DIRETORIO')
        nome_item (str): Nome do diretório
        caminho_pai (str): Caminho do diretório pai
        caminho_absoluto (str): Caminho completo absoluto
        eh_absoluto (bool): Indica se o caminho é absoluto
        eh_link_simbolico (bool): Indica se é um link simbólico
        criado_em (str): Data de criação no formato 'YYYY-MM-DD HH:MM:SS'
        modificado_em (str): Data da última modificação
        acessado_em (str): Data do último acesso
        id_caminho (int): Número de inode
        subitens (list[str]): Lista de nomes dos itens contidos
        quantidade_total_itens (int): Total de itens no diretório
        total_arquivos (int): Quantidade de arquivos
        total_subpastas (int): Quantidade de subdiretórios
        arquivos_ocultos (list[str]): Lista de arquivos ocultos
        pastas_ocultas (list[str]): Lista de pastas ocultas
        tamanho_total_arquivos_bytes (int): Tamanho total em bytes
        tamanho_total_arquivos_formatado (str): Tamanho formatado (ex: '1.23 MB')
    """

    def __init__(
        self,
        tipo_caminho: str,
        nome_item: str,
        caminho_pai: str,
        caminho_absoluto: str,
        eh_absoluto: bool,
        eh_link_simbolico: bool,
        criado_em: str,
        modificado_em: str,
        acessado_em: str,
        id_caminho: int,
        subitens: list[str],
        quantidade_total_itens: int,
        total_arquivos: int,
        total_subpastas: int,
        arquivos_ocultos: list[str],
        pastas_ocultas: list[str],
        tamanho_total_arquivos_bytes: int,
        tamanho_total_arquivos_formatado: str,
    ) -> None:
        """Inicializa um ModeloDiretorio com todos os metadados."""
        self.tipo_caminho: str = tipo_caminho
        self.nome_item: str = nome_item
        self.caminho_pai: str = caminho_pai
        self.caminho_absoluto: str = caminho_absoluto
        self.eh_absoluto: bool = eh_absoluto
        self.eh_link_simbolico: bool = eh_link_simbolico
        self.criado_em: str = criado_em
        self.modificado_em: str = modificado_em
        self.acessado_em: str = acessado_em
        self.id_caminho: int = id_caminho

        self.subitens: list[str] = subitens
        self.quantidade_total_itens: int = quantidade_total_itens
        self.total_arquivos: int = total_arquivos
        self.total_subpastas: int = total_subpastas
        self.arquivos_ocultos: list[str] = arquivos_ocultos
        self.pastas_ocultas: list[str] = pastas_ocultas
        self.tamanho_total_arquivos_bytes: int = tamanho_total_arquivos_bytes
        self.tamanho_total_arquivos_formatado: str = tamanho_total_arquivos_formatado


class ModeloArquivo:
    """Representação estruturada de um arquivo com todos seus metadados.

    Atributos:
        tipo_caminho (str): Tipo do item ('ARQUIVO')
        nome_item (str): Nome do arquivo (com extensão)
        caminho_pai (str): Caminho do diretório pai
        caminho_absoluto (str): Caminho completo absoluto
        eh_absoluto (bool): Indica se o caminho é absoluto
        eh_link_simbolico (bool): Indica se é um link simbólico
        criado_em (str): Data de criação no formato 'YYYY-MM-DD HH:MM:SS'
        modificado_em (str): Data da última modificação
        acessado_em (str): Data do último acesso
        id_caminho (int): Número de inode
        extensao (str): Extensão do arquivo (ex: '.txt')
        nome_sem_extensao (str): Nome do arquivo sem extensão
        tamanho_bytes (int): Tamanho em bytes
        tamanho_formatado (str): Tamanho formatado (ex: '1.23 MB')
    """

    def __init__(
        self,
        tipo_caminho: str,
        nome_item: str,
        caminho_pai: str,
        caminho_absoluto: str,
        eh_absoluto: bool,
        eh_link_simbolico: bool,
        criado_em: str,
        modificado_em: str,
        acessado_em: str,
        id_caminho: int,
        extensao: str,
        nome_sem_extensao: str,
        tamanho_bytes: int,
        tamanho_formatado: str,
    ) -> None:
        """Inicializa um ModeloArquivo com todos os metadados."""
        self.tipo_caminho: str = tipo_caminho
        self.nome_item: str = nome_item
        self.caminho_pai: str = caminho_pai
        self.caminho_absoluto: str = caminho_absoluto
        self.eh_absoluto: bool = eh_absoluto
        self.eh_link_simbolico: bool = eh_link_simbolico
        self.criado_em: str = criado_em
        self.modificado_em: str = modificado_em
        self.acessado_em: str = acessado_em
        self.id_caminho: int = id_caminho

        self.extensao: str = extensao
        self.nome_sem_extensao: str = nome_sem_extensao
        self.tamanho_bytes: int = tamanho_bytes
        self.tamanho_formatado: str = tamanho_formatado


class ModeloCaminho:
    """Factory que cria modelos de caminho baseado no tipo (arquivo/diretório).

    Atributos:
        extrator (ExtratorDeCaminhos): Instância do extrator de metadados
        caminho_preparado (Path): Caminho absoluto e resolvido
        tipo_caminho (str): Tipo do caminho ('ARQUIVO' ou 'DIRETORIO')
    """

    def __init__(self, caminho_bruto: str) -> None:
        """Inicializa o ModeloCaminho e prepara o caminho fornecido.

        Args:
            caminho_bruto: Caminho a ser analisado (pode ser relativo ou conter ~)
        """
        self.extrator = ExtratorDeCaminhos()
        self.caminho_preparado: Path = self.extrator.preparar_caminho(
            caminho_raw=caminho_bruto
        )
        self.tipo_caminho: str = self.extrator.definir_tipo_caminho(
            caminho_absoluto=self.caminho_preparado
        )

    def montar_objeto(self) -> ModeloArquivo | ModeloDiretorio:
        """Cria o modelo apropriado baseado no tipo de caminho.

        Returns:
            ModeloArquivo | ModeloDiretorio: Instância do modelo concreto

        Raises:
            ValueError: Se o tipo de caminho não for reconhecido
        """
        if self.tipo_caminho == "ARQUIVO":
            dados_arquivo: DadosArquivo = self.extrator.extrair_dados_de_arquivo(
                caminho_arquivo=self.caminho_preparado
            )
            return ModeloArquivo(
                tipo_caminho=dados_arquivo["tipo_caminho"],
                nome_item=dados_arquivo["nome_item"],
                caminho_pai=dados_arquivo["caminho_pai"],
                caminho_absoluto=dados_arquivo["caminho_absoluto"],
                eh_absoluto=dados_arquivo["eh_absoluto"],
                eh_link_simbolico=dados_arquivo["eh_link_simbolico"],
                criado_em=dados_arquivo["criado_em"],
                modificado_em=dados_arquivo["modificado_em"],
                acessado_em=dados_arquivo["acessado_em"],
                id_caminho=dados_arquivo["id_caminho"],
                extensao=dados_arquivo["extensao"],
                nome_sem_extensao=dados_arquivo["nome_sem_extensao"],
                tamanho_bytes=dados_arquivo["tamanho_bytes"],
                tamanho_formatado=dados_arquivo["tamanho_formatado"],
            )

        if self.tipo_caminho == "DIRETORIO":
            dados_pasta: DadosDiretorio = self.extrator.extrair_dados_de_diretorio(
                caminho_diretorio=self.caminho_preparado
            )
            return ModeloDiretorio(
                tipo_caminho=dados_pasta["tipo_caminho"],
                nome_item=dados_pasta["nome_item"],
                caminho_pai=dados_pasta["caminho_pai"],
                caminho_absoluto=dados_pasta["caminho_absoluto"],
                eh_absoluto=dados_pasta["eh_absoluto"],
                eh_link_simbolico=dados_pasta["eh_link_simbolico"],
                criado_em=dados_pasta["criado_em"],
                modificado_em=dados_pasta["modificado_em"],
                acessado_em=dados_pasta["acessado_em"],
                id_caminho=dados_pasta["id_caminho"],
                subitens=dados_pasta["subitens"],
                quantidade_total_itens=dados_pasta["quantidade_total_itens"],
                total_arquivos=dados_pasta["total_arquivos"],
                total_subpastas=dados_pasta["total_subpastas"],
                arquivos_ocultos=dados_pasta["arquivos_ocultos"],
                pastas_ocultas=dados_pasta["pastas_ocultas"],
                tamanho_total_arquivos_bytes=dados_pasta["tamanho_total_arquivos_bytes"],
                tamanho_total_arquivos_formatado=dados_pasta[
                    "tamanho_total_arquivos_formatado"
                ],
            )

        raise ValueError(f"Tipo de caminho não reconhecido: {self.tipo_caminho}")

    def to_dict(self) -> dict[str, str | int | list[str]]:
        """Converte o modelo para dicionário.

        Returns:
            dict: Dicionário com todos os atributos do modelo
        """
        return self.montar_objeto().__dict__

    def to_json(self) -> str:
        """Serializa o modelo para JSON formatado.

        Returns:
            str: JSON indentado com todos os metadados
        """
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False, sort_keys=True)


# def main() -> None:
#     """Função principal para demonstração do uso das classes."""
#     caminhos: list[str] = [
#         "~/Downloads/Firefox/bookmarks.html",
#         "~/Downloads/Firefox/",
#     ]

#     for caminho in caminhos:
#         modelo = ModeloCaminho(caminho_bruto=caminho)
#         print(caminho, modelo.to_json())


# if __name__ == "__main__":
#     main()
