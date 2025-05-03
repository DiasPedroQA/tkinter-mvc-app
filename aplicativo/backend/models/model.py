# -*- coding: utf-8 -*-

"""
Módulo responsável por realizar análises simples sobre textos.
Atualmente, calcula a quantidade de palavras em uma string.
"""

from aplicativo.backend.tools.dados_servidor import AnaliseDeCaminho as CriadorObjeto


class AnalisadorModel:
    """
    Classe que realiza análises básicas sobre textos fornecidos.
    """

    def objeto_resultado(self, dado_entrada: str) -> str:
        criador = CriadorObjeto(caminho=dado_entrada)
        return criador.montar_objeto_caminho()
