# -*- coding: utf-8 -*-

"""
Módulo responsável por analisar um caminho do sistema de arquivos.

Funcionalidades:
1. Detectar o sistema operacional baseado no caminho.
2. Validar se há caracteres inválidos conforme o SO detectado.
3. Verificar se o SO detectado é o mesmo do sistema local.
4. Verificar existência do caminho.
5. Verificar permissões (leitura, escrita, execução).
6. Obter dados de localização (nome, pasta pai, raiz, tipo, usuário).
7. Obter timestamps (criação, modificação, acesso).
"""

import os
import json
import platform
from typing import Union
from datetime import datetime
from pathlib import Path


class AnaliseDeCaminho:
    """
    Classe que realiza uma análise completa sobre um caminho do sistema de arquivos,
    agregando informações em um único dicionário de resultados.
    """

    def __init__(self, caminho_inicial: str) -> None:
        """
        Inicializa a instância com o caminho a ser analisado.

        :param caminho_inicial: Caminho do arquivo ou diretório como string.
        """
        if not isinstance(caminho_inicial, str):
            raise TypeError("O caminho deve ser uma string.")

        # Criação das instâncias corretamente
        self.__objeto: dict = {"caminho_original": caminho_inicial}
        self.regras: dict[str, list] = {
            "Windows": ['<', '>', ':', '"', '/', '\\', '|', '?', '*'],
            "Linux": ['\0', '\\'],
            "macOS": [":"],
        }
        self.nome_local: str = platform.system()
        self.mapa: dict[str, str] = {"Windows": "Windows", "Linux": "Linux", "Darwin": "macOS"}

    def _detectar_comparar_e_validar(self, sistema_detectado: str = "Desconhecido") -> None:
        """
        Detecta o sistema operacional com base no início do caminho.
        E o compara com o sistema operacional local do ambiente atual.
        E valida se o caminho informado pode (ou não) existir no sistema operacional.
        E verifica permissões de leitura, escrita e execução usando pathlib.
        E obtém datas de criação, modificação e acesso ao caminho.
        """
        caminho_entrada: str = str(self.__objeto.get("caminho_original", ""))
        if caminho_entrada[1:3] in (':\\', ':/') and caminho_entrada[0].isalpha():
            sistema_detectado = "Windows"
        elif caminho_entrada.startswith("/home/"):
            sistema_detectado = "Linux"
        elif caminho_entrada.startswith("/Users/"):
            sistema_detectado = "macOS"

        sistema_local: str = self.mapa.get(self.nome_local, "Desconhecido")
        caminho_tratado: Path = Path(caminho_entrada)
        stats: os.stat_result = caminho_tratado.stat()
        if sistemas_iguais := "Sim" if sistema_detectado == sistema_local else "Não":
            self.__objeto.update(
                {
                    "sistemas_iguais": sistemas_iguais,
                    "mensagem_existencia": "O caminho pode tentar ser encontrado.",
                    "permissoes": {
                        "leitura": caminho_tratado.is_file() or caminho_tratado.is_dir(),
                        "escrita": caminho_tratado.exists() and os.access(caminho_tratado, os.W_OK),
                        "execucao": caminho_tratado.exists()
                        and os.access(caminho_tratado, os.X_OK),
                    },
                    "timestamps": {
                        "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
                        "accessed": datetime.fromtimestamp(stats.st_atime).isoformat(),
                        "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
                    },
                    "sistema_detectado": sistema_detectado,
                }
            )
        else:
            self.__objeto.update(
                {
                    "mensagem_existencia": "Sistemas incompatíveis para verificar existência.",
                    "sistema_detectado": sistema_detectado,
                    "sistema_local": sistema_local,
                }
            )

    def _verificar_caracteres_invalidos(self) -> None:
        """Valida se há caracteres proibidos no caminho para o sistema identificado."""
        caminho_avaliado: str = str(self.__objeto.get("caminho_original", ""))
        sistema_detectado: str = str(self.__objeto.get("sistema_detectado", ""))
        caracter_proibidos = self.regras.get(sistema_detectado, [])
        if caracter_proibidos_encontrados := [
            caracter for caracter in caracter_proibidos if caracter in caminho_avaliado
        ]:
            self.__objeto.update(
                {
                    "ERRO_caracter_invalido": (
                        f"Caractere(s) inválido(s) para o sistema {sistema_detectado}:"
                        f" {', '.join(caracter_proibidos_encontrados)}"
                    )
                }
            )
        else:
            self.__objeto.update(
                {"sintaxe_permitida": f"Caminho válido para o sistema atual: {sistema_detectado}"}
            )

    # transformar em regex
    def _obter_dados_de_localizacao(self) -> None:
        """Extrai informações de localização do caminho: nome, pasta pai, tipo, raiz e usuário."""
        caminho_original: str = str(self.__objeto.get("caminho_original", ""))
        caminho_tratado: Path = Path(caminho_original)

        tipo_caminho: str = "relativo" if caminho_original.startswith("..") else "absoluto"
        usuario: Union[str, None] = (
            caminho_tratado.parts[2] if len(caminho_tratado.parts) >= 3 else None
        )
        self.__objeto.update(
            {
                "localizacao": {
                    "nome_do_item": str(caminho_tratado.name),
                    "pasta_pai": str(caminho_tratado.parent),
                    "tipo_caminho": tipo_caminho,
                    "raiz": str(caminho_tratado.anchor),
                    "usuario": usuario,
                }
            }
        )

    def get_resultado(self) -> str:
        """
        Executa as 3 etapas principais da análise em sequência.
        E retorna os dados acumulados da análise atual, em json.
        """
        self._detectar_comparar_e_validar()
        self._verificar_caracteres_invalidos()
        self._obter_dados_de_localizacao()
        return json.dumps(self.__objeto, ensure_ascii=False, indent=4, sort_keys=True)

    def __str__(self) -> str:
        """
        Representação legível da análise atual.

        :return: String com os dados acumulados após análise.
        """
        return str(f"Objeto analisado: {self.get_resultado()}")


### ✅ **Exemplo de uso**
if __name__ == "__main__":
    analise = AnaliseDeCaminho("/home/pedro-pm-dias/Downloads/Firefox/")
    resultado = analise.get_resultado()
    print(resultado)
