# import unittest
# from app.backend.servicos.analise_servico import GerenciadorArquivos
# from app.backend.modelos.modelos import ResultadoAnalise


# class TestGerenciadorArquivos(unittest.TestCase):

#     def setUp(self) -> None:
#         self.gerenciador = GerenciadorArquivos()

#     def test_analisar_caminhos_arquivo_valido(self) -> None:
#         resultado = self.gerenciador.server_analisar_caminhos(
#             "/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html"
#         )
#         self.assertTrue(resultado.sucesso)
#         self.assertEqual(resultado.mensagem, "Arquivo identificado com sucesso.")

#     def test_analisar_caminhos_pasta_valida(self) -> None:
#         resultado = self.gerenciador.server_analisar_caminhos("/home/pedro-pm-dias/Downloads")
#         self.assertTrue(resultado.sucesso)
#         self.assertEqual(resultado.mensagem, "Pasta identificada com sucesso.")

#     def test_analisar_caminhos_caminho_invalido(self) -> None:
#         resultado = self.gerenciador.server_analisar_caminhos(
#             "/home/pedro-pm-dias/Downloads/arquivo_inexistente.html"
#         )
#         self.assertFalse(resultado.sucesso)
#         self.assertEqual(resultado.mensagem, "Caminho não encontrado ou não corrigido.")


# if __name__ == "__main__":
#     unittest.main()
