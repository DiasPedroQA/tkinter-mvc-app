# """
# Testes para a classe ResultadoAnalise.

# Este módulo contém testes unitários para verificar o comportamento da classe
# ResultadoAnalise, incluindo métodos como adicionar_mensagem, foi_corrigido e
# a representação em string.
# """

# from models.analysis_result import ResultadoAnalise
# from models.paths_objects import ObjetoArquivo, ObjetoPasta


# def test_adicionar_mensagem() -> None:
#     """
#     Testa o método adicionar_mensagem para verificar se as mensagens
#     são concatenadas corretamente.
#     """
#     resultado = ResultadoAnalise()
#     resultado.adicionar_mensagem("Primeira mensagem.")
#     assert resultado.mensagem == "Primeira mensagem."

#     resultado.adicionar_mensagem("Segunda mensagem.")
#     assert resultado.mensagem == "Primeira mensagem. | Segunda mensagem."


# def test_foi_corrigido() -> None:
#     """
#     Testa o método foi_corrigido para verificar se ele retorna True
#     quando o caminho foi corrigido.
#     """
#     resultado = ResultadoAnalise()
#     assert not resultado.foi_corrigido()

#     resultado.caminho_corrigido = "/caminho/corrigido"
#     assert resultado.foi_corrigido()


# def test_str_representation() -> None:
#     """
#     Testa a representação em string da classe ResultadoAnalise para
#     garantir que todos os atributos relevantes estão incluídos.
#     """
#     resultado = ResultadoAnalise(
#         sucesso=True,
#         mensagem="Teste de sucesso.",
#         caminho_tratado="/caminho/teste",
#         tipo_caminho="absoluto",
#     )
#     resultado.caminho_corrigido = "/caminho/corrigido"

#     resultado_str = str(resultado)
#     assert "Sucesso" in resultado_str
#     assert "Teste de sucesso." in resultado_str
#     assert "/caminho/teste" in resultado_str
#     assert "absoluto" in resultado_str
#     assert "Corrigido: /caminho/corrigido" in resultado_str


# def test_objetos_coletados() -> None:
#     """
#     Testa o atributo objetos_coletados para verificar se ele aceita
#     tanto ObjetoArquivo quanto ObjetoPasta.
#     """
#     arquivo = ObjetoArquivo(caminho_arquivo="/caminho/arquivo")
#     resultado = ResultadoAnalise(objetos_coletados=arquivo)
#     assert isinstance(resultado.objetos_coletados, ObjetoArquivo)
#     assert resultado.objetos_coletados.caminho_arquivo == "/caminho/arquivo"

#     pasta = ObjetoPasta(caminho_pasta="/caminho/pasta")
#     resultado.objetos_coletados = pasta
#     assert isinstance(resultado.objetos_coletados, ObjetoPasta)
#     assert resultado.objetos_coletados.caminho_pasta == "/caminho/pasta"
