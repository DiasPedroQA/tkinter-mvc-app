# # -*- coding: utf-8 -*-
# # pylint: disable=C0114, E0611, W0621

# import json
# import pytest

# from backend.model.app_model import CaminhoModelo
# from backend.tools.app_tools import Ferramentas


# @pytest.fixture
# def ferramentas() -> Ferramentas:
#     """Fixture to create a real Ferramentas instance."""
#     return Ferramentas()


# @pytest.fixture
# def modelo_caminho() -> CaminhoModelo:
#     """Fixture to create a CaminhoModelo instance with real Ferramentas."""
#     return CaminhoModelo(caminho_original="/home/pedro-pm-dias/")


# def test_init(modelo_caminho: CaminhoModelo) -> None:
#     """Test the initialization of CaminhoModelo."""
#     assert modelo_caminho.caminho_original == "//home///pedro-pm-dias/"
#     assert modelo_caminho.normalized_path == "/home/pedro-pm-dias/"
#     assert modelo_caminho.metadados == {
#         "caminho_original": "/home/pedro-pm-dias/",
#         "caminho_normalizado": "/home/pedro-pm-dias/",
#         "timestamp_validacao": "2023-01-01T00:00:00",
#     }
#     assert modelo_caminho.validacao_basica == {"valido": "Sim", "tipo": "arquivo"}
#     assert modelo_caminho.sistema_arquivos == {
#         "estatisticas": {"tamanho": 1024},
#         "permissoes": {"leitura": True, "escrita": True, "execucao": True},
#     }
#     assert modelo_caminho.erros == []


# def test_permissoes_caminho(modelo_caminho: CaminhoModelo) -> None:
#     """Test the permissoes_caminho method."""
#     permissoes = modelo_caminho.permissoes_caminho()
#     assert permissoes == {"leitura": True, "escrita": True, "execucao": False}


# def test_validar_existencia_caminho(modelo_caminho: CaminhoModelo) -> None:
#     """Test the validar_existencia_caminho method."""
#     existencia = modelo_caminho.validar_existencia_caminho()
#     assert existencia is True


# def test_eh_valido(modelo_caminho: CaminhoModelo) -> None:
#     """Test the eh_valido method."""
#     assert modelo_caminho.eh_valido() is True


# def test_tipo_caminho(modelo_caminho: CaminhoModelo) -> None:
#     """Test the tipo_caminho method."""
#     tipo = modelo_caminho.tipo_caminho()
#     assert tipo == "arquivo"


# def test_to_json(modelo_caminho: CaminhoModelo) -> None:
#     """Test the to_json method."""
#     json_data: str = modelo_caminho.to_json()
#     expected_data: dict = {
#         "metadados": {
#             "caminho_original": "/home/pedro-pm-dias/",
#             "caminho_normalizado": "/home/pedro-pm-dias/",
#             "timestamp_validacao": "2023-01-01T00:00:00",
#         },
#         "validacao_basica": {"valido": "Sim", "tipo": "arquivo"},
#         "sistema_arquivos": {
#             "estatisticas": {"tamanho": 1024},
#             "permissoes": {"leitura": True, "escrita": True, "execucao": False},
#         },
#         "erros": [],
#     }
#     assert json_data == json.dumps(expected_data, indent=4, ensure_ascii=False)
