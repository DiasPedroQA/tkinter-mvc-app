# -*- coding: utf-8 -*-

# resultado.py

"""
Define a estrutura de dados para representar o resultado de uma análise de sistema.
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class ResultadoAnalise:
    """
    Representa o resultado da análise de um sistema de arquivos.

    Atributos:
        caminho_original (str): Caminho analisado no sistema de arquivos.
        sistema_detectado (Optional[str]): Sistema operacional detectado automaticamente.
        sistema_local (Optional[str]): Sistema operacional informado/localmente conhecido.
        sistemas_iguais (Optional[str]): Indica se o sistema detectado e o local são iguais.
        mensagem_existencia (Optional[str]): Mensagem sobre a existência do caminho analisado.
        permissoes (Dict[str, str]): Dicionário contendo informações de
        permissões de arquivos/pastas.
        timestamps (Dict[str, str]): Dicionário com timestamps relevantes
        (criação, modificação, acesso).
        erros (Optional[str]): Mensagem de erro ocorrida durante a análise, se houver.
        sintaxe_permitida (Optional[str]): Indicação sobre a validade da sintaxe do caminho.
        localizacao (Dict[str, str]): Informações sobre localização geográfica
        ou lógica do sistema/caminho.
    """

    caminho_original: str
    sistema_detectado: Optional[str] = None
    sistema_local: Optional[str] = None
    sistemas_iguais: Optional[str] = None
    mensagem_existencia: Optional[str] = None
    permissoes: dict[str, str] = field(default_factory=dict)
    timestamps: dict[str, str] = field(default_factory=dict)
    erros: Optional[str] = None
    sintaxe_permitida: Optional[str] = None
    localizacao: dict[str, str] = field(default_factory=dict)

    def to_json(self) -> str:
        """
        Serializa os dados da instância para uma string JSON formatada.

        Returns:
            str: Representação JSON da instância da classe.
        """
        return json.dumps(asdict(self), ensure_ascii=False, indent=4, sort_keys=True)
