# import pytest
# from app.backend.servicos.analise_servico import GerenciadorArquivos

# gerenciador = GerenciadorArquivos()

# def test_dados_basicos_do_sistema():
#     assert gerenciador.sistema in ["Linux", "Windows", "Darwin"]
#     assert isinstance(gerenciador.usuario, str)
#     assert gerenciador.base_usuario.startswith("/home") or gerenciador.base_usuario.startswith("C:\\")

# def test_analise_arquivo_valido():
#     caminho = "/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html"
#     resultado = gerenciador.server_analisar_caminhos(caminho)
#     assert resultado.sucesso is True
#     assert resultado.tipo_caminho.startswith("absoluto")
#     assert resultado.objetos_coletados.tipo_item == "Arquivo"

# def test_analise_pasta_valida():
#     caminho = "/home/pedro-pm-dias/Downloads/Firefox"
#     resultado = gerenciador.server_analisar_caminhos(caminho)
#     assert resultado.sucesso is True
#     assert resultado.objetos_coletados.tipo_item == "Pasta"

# def test_analise_caminho_invalido():
#     caminho = "/caminho/que/nao/existe"
#     resultado = gerenciador.server_analisar_caminhos(caminho)
#     assert resultado.sucesso is False
