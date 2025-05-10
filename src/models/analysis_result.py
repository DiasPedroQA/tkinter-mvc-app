# """
# Módulo que define a classe ResultadoAnalise.

# A classe ResultadoAnalise é utilizada para representar o resultado de uma análise de caminho,
# incluindo informações sobre sucesso, mensagens, caminhos tratados e objetos coletados.
# """

# from dataclasses import dataclass
# from typing import Optional, Union
# from .paths_objects import ObjetoArquivo, ObjetoPasta


# @dataclass
# class ResultadoAnalise:
#     """Classe para representar o resultado da análise de um caminho."""

#     sucesso: bool = False
#     mensagem: str = ""
#     caminho_tratado: str = ""
#     tipo_caminho: str = ""
#     objetos_coletados: Optional[Union[ObjetoArquivo, ObjetoPasta]] = None
#     caminho_corrigido: Optional[str] = None
