"""
Módulo que define a classe ResultadoAnalise.

A classe ResultadoAnalise é utilizada para representar o resultado de uma análise de caminho,
incluindo informações sobre sucesso, mensagens, caminhos tratados e objetos coletados.

Atributos:
- sucesso: Indica se a análise foi bem-sucedida.
- mensagem: Mensagem descritiva do resultado da análise.
- caminho_tratado: Caminho analisado após normalização.
- tipo_caminho: Tipo do caminho analisado (ex.: "absoluto", "relativo").
- objetos_coletados: Objeto associado ao caminho (arquivo ou pasta).
- caminho_corrigido: Caminho corrigido, caso o original seja inválido.

Métodos:
- adicionar_mensagem: Adiciona uma mensagem ao resultado.
- foi_corrigido: Verifica se o caminho foi corrigido.
"""

from dataclasses import dataclass
from typing import Optional, Union
from src.models.paths_objects import ObjetoArquivo, ObjetoPasta


@dataclass
class ResultadoAnalise:
    """Classe para representar o resultado da análise de um caminho."""

    sucesso: bool = False
    mensagem: str = ""
    caminho_tratado: str = ""
    tipo_caminho: str = ""
    objetos_coletados: Optional[Union[ObjetoArquivo, ObjetoPasta]] = None
    caminho_corrigido: Optional[str] = None

    def adicionar_mensagem(self, nova_mensagem: str) -> None:
        """
        Adiciona uma mensagem ao resultado da análise.

        Args:
            nova_mensagem (str): Mensagem adicional a ser anexada.
        """
        if self.mensagem:
            self.mensagem += f" | {nova_mensagem}"
        else:
            self.mensagem = nova_mensagem

    def foi_corrigido(self) -> bool:
        """
        Verifica se o caminho foi corrigido.

        Returns:
            bool: True se o caminho foi corrigido, False caso contrário.
        """
        return self.caminho_corrigido is not None

    def __str__(self) -> str:
        """
        Retorna uma representação legível do resultado da análise.

        Returns:
            str: Representação textual do resultado.
        """
        status = "Sucesso" if self.sucesso else "Falha"
        corrigido = (
            f", Corrigido: {self.caminho_corrigido}" if self.caminho_corrigido else ""
        )
        return (
            f"ResultadoAnalise(Status: {status}, Mensagem: '{self.mensagem}', "
            f"Caminho Tratado: '{self.caminho_tratado}', Tipo: '{self.tipo_caminho}'{corrigido})"
        )


# Criando um resultado de análise
resultado = ResultadoAnalise(
    sucesso=True,
    mensagem="Análise concluída com sucesso.",
    caminho_tratado="/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html",
    tipo_caminho="absoluto",
    objetos_coletados=ObjetoArquivo(
        caminho_arquivo="/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html"
    ),
)

# Adicionando uma mensagem
resultado.adicionar_mensagem("Arquivo identificado como válido.")

# Verificando se o caminho foi corrigido
print(resultado.foi_corrigido())  # False

# Exibindo o resultado
print(resultado)
