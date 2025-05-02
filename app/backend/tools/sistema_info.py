# sistema_info.py

"""Classe auxiliar para obter o sistema operacional e regras de validação"""

import platform


class SistemaArquivoInfo:
    """Classe que fornece informações e regras relacionadas ao sistema operacional."""

    regras_caracteres = {
        "Windows": ['<', '>', ':', '"', '/', '\\', '|', '?', '*'],
        "Linux": ['\0', '\\'],
        "macOS": [":"],
    }

    mapa_sistemas = {
        "Windows": "Windows",
        "Linux": "Linux",
        "Darwin": "macOS",
    }

    @classmethod
    def detectar_sistema(cls, caminho: str) -> str:
        """
        Detecta o sistema operacional com base em um caminho de arquivo.

        Args:
            caminho (str): Caminho do arquivo a ser analisado.

        Returns:
            str: Nome do sistema operacional correspondente (Windows, Linux, macOS ou Desconhecido).
        """
        if caminho[1:3] in (':\\', ':/') and caminho[0].isalpha():
            return "Windows"
        if caminho.startswith("/home/"):
            return "Linux"
        return "macOS" if caminho.startswith("/Users/") else "Desconhecido"

    @classmethod
    def caracteres_invalidos(cls, sistema: str) -> list[str]:
        """
        Retorna a lista de caracteres inválidos para o sistema especificado.

        Args:
            sistema (str): Nome do sistema operacional.

        Returns:
            list[str]: Lista de caracteres inválidos.
            Retorna lista vazia se o sistema for desconhecido.
        """
        return cls.regras_caracteres.get(sistema, [])

    @classmethod
    def sistema_local(cls) -> str:
        """
        Retorna o nome do sistema operacional local, baseado na plataforma atual.

        Returns:
            str: Nome do sistema operacional (Windows, Linux, macOS ou Desconhecido).
        """
        return cls.mapa_sistemas.get(platform.system(), "Desconhecido")
