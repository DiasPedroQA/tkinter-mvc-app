# test_resultado.py

"""Testes para a estrutura de dados e representação da análise do sistema."""

import json
from aplicativo.backend.tools.resultado import ResultadoAnalise


def test_resultadoanalise_initialization() -> None:
    """
    Testa a inicialização da classe ResultadoAnalise com valores padrão.
    """
    resultado = ResultadoAnalise(caminho_original="/path/to/dir")
    assert resultado.caminho_original == "/path/to/dir"
    assert resultado.sistema_detectado is None
    assert resultado.sistema_local is None
    assert resultado.sistemas_iguais is None
    assert resultado.mensagem_existencia is None
    assert resultado.permissoes == {}
    assert resultado.timestamps == {}
    assert resultado.erros is None
    assert resultado.sintaxe_permitida is None
    assert resultado.localizacao == {}


def test_resultadoanalise_custom_initialization() -> None:
    """
    Testa a inicialização da classe ResultadoAnalise com valores personalizados.
    """
    resultado = ResultadoAnalise(
        caminho_original="/path/to/dir",
        sistema_detectado="Linux",
        sistema_local="Linux",
        sistemas_iguais="Sim",
        mensagem_existencia="Caminho existe",
        permissoes={"leitura": "permitido", "escrita": "negado"},
        timestamps={"criação": "2023-01-01", "modificação": "2023-01-02"},
        erros="Nenhum erro",
        sintaxe_permitida="Válida",
        localizacao={"cidade": "São Paulo", "estado": "SP"},
    )
    assert resultado.caminho_original == "/path/to/dir"
    assert resultado.sistema_detectado == "Linux"
    assert resultado.sistema_local == "Linux"
    assert resultado.sistemas_iguais == "Sim"
    assert resultado.mensagem_existencia == "Caminho existe"
    assert resultado.permissoes == {"leitura": "permitido", "escrita": "negado"}
    assert resultado.timestamps == {"criação": "2023-01-01", "modificação": "2023-01-02"}
    assert resultado.erros == "Nenhum erro"
    assert resultado.sintaxe_permitida == "Válida"
    assert resultado.localizacao == {"cidade": "São Paulo", "estado": "SP"}


def test_resultadoanalise_to_json() -> None:
    """
    Testa o método to_json da classe ResultadoAnalise.
    """
    resultado = ResultadoAnalise(
        caminho_original="/path/to/dir",
        sistema_detectado="Linux",
        sistema_local="Linux",
        sistemas_iguais="Sim",
        mensagem_existencia="Caminho existe",
        permissoes={"leitura": "permitido", "escrita": "negado"},
        timestamps={"criação": "2023-01-01", "modificação": "2023-01-02"},
        erros="Nenhum erro",
        sintaxe_permitida="Válida",
        localizacao={"cidade": "São Paulo", "estado": "SP"},
    )
    json_result = resultado.to_json()
    expected_json = json.dumps(
        {
            "caminho_original": "/path/to/dir",
            "sistema_detectado": "Linux",
            "sistema_local": "Linux",
            "sistemas_iguais": "Sim",
            "mensagem_existencia": "Caminho existe",
            "permissoes": {"leitura": "permitido", "escrita": "negado"},
            "timestamps": {"criação": "2023-01-01", "modificação": "2023-01-02"},
            "erros": "Nenhum erro",
            "sintaxe_permitida": "Válida",
            "localizacao": {"cidade": "São Paulo", "estado": "SP"},
        },
        ensure_ascii=False,
        indent=4,
        sort_keys=True,
    )
    assert json_result == expected_json
