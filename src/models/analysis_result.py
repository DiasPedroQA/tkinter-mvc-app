# # # -*- coding: utf-8 -*-

# # """
# # Módulo que define a classe ResultadoAnalise.

# # A classe ResultadoAnalise é utilizada para representar
# # o resultado de uma análise de caminho, incluindo informações
# # sobre sucesso, mensagens, caminhos tratados e objetos coletados.

# # Atributos:
# # - sucesso: Indica se a análise foi bem-sucedida.
# # - mensagem: Mensagem descritiva do resultado da análise.
# # - caminho_tratado: Caminho analisado após normalização.
# # - tipo_caminho: Tipo do caminho analisado (ex.: "absoluto", "relativo").
# # - objetos_coletados: Objeto associado ao caminho (arquivo ou pasta).
# # - caminho_corrigido: Caminho corrigido, caso o original seja inválido.

# # Métodos:
# # - adicionar_mensagem: Adiciona uma mensagem ao resultado.
# # - foi_corrigido: Verifica se o caminho foi corrigido.
# # - possui_objetos_coletados: Verifica se há objetos associados ao caminho.
# # - resumo: Retorna um resumo simplificado do resultado da análise.
# # """

# # from dataclasses import dataclass
# # from typing import Optional, Union

# # from src.models.paths_objects import ObjetoArquivo, ObjetoPasta


# # @dataclass
# # class ResultadoAnalise:
# #     """Classe para representar o resultado da análise de um caminho."""

# #     sucesso: bool = False
# #     mensagem: str = ""
# #     caminho_tratado: str = ""
# #     tipo_caminho: str = ""
# #     objetos_coletados: Optional[Union[ObjetoArquivo, ObjetoPasta]] = None
# #     caminho_corrigido: Optional[str] = None

# #     def adicionar_mensagem(self, nova_mensagem: str) -> None:
# #         """
# #         Adiciona uma mensagem ao resultado da análise.

# #         Args:
# #             nova_mensagem (str): Mensagem adicional a ser anexada.
# #         """
# #         if self.mensagem:
# #             self.mensagem += f" | {nova_mensagem}"
# #         else:
# #             self.mensagem = nova_mensagem

# #     def foi_corrigido(self) -> bool:
# #         """
# #         Verifica se o caminho foi corrigido.

# #         Returns:
# #             bool: True se o caminho foi corrigido, False caso contrário.
# #         """
# #         return True if self.caminho_corrigido is not None else False

# #     def possui_objetos_coletados(self) -> bool:
# #         """
# #         Verifica se há objetos associados ao caminho.

# #         Returns:
# #             bool: True se há objetos coletados, False caso contrário.
# #         """
# #         return self.objetos_coletados is not None

# #     def resumo(self) -> str:
# #         """
# #         Retorna um resumo simplificado do resultado da análise.

# #         Returns:
# #             str: Resumo contendo o status, caminho tratado e mensagem.
# #         """
# #         status = "Sucesso" if self.sucesso else "Falha"
# #         return f"[{status}] {self.caminho_tratado} - {self.mensagem}"

#     def __str__(self) -> str:
#         """
#         Retorna uma representação legível do resultado da análise.

#         Returns:
#             str: Representação textual do resultado.
#         """
#         status = "Sucesso" if self.sucesso else "Falha"
#         corrigido = (
#             f", Corrigido: {self.caminho_corrigido}"
#             if self.caminho_corrigido
#             else ""
#         )
#         objetos = (
#             f", Objetos Coletados: {self.objetos_coletados}"
#             if self.objetos_coletados
#             else ""
#         )
#         return (
#             f"ResultadoAnalise(Status: {status}, "
#             f"Mensagem: '{self.mensagem}', "
#             f"Caminho Tratado: '{self.caminho_tratado}', "
#             f"Tipo: '{self.tipo_caminho}'"
#             f"{corrigido}{objetos})"
#         )


# # Exemplo de uso
# if __name__ == "__main__":
#     # Criando um resultado de análise
#     resultado = ResultadoAnalise(
#         sucesso=True,
#         mensagem="",
#         caminho_tratado="/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html",
#         tipo_caminho="absoluto",
#         objetos_coletados=ObjetoArquivo(),
#     )

#     # Adicionando uma mensagem
#     resultado.adicionar_mensagem("Arquivo identificado como válido.")

#     # Verificando se o caminho foi corrigido
#     print("Caminho foi modificado?", resultado.foi_corrigido())  # False

#     # Exibindo o resumo
#     print("Resumo: ", resultado.resumo())

#     # Exibindo o resultado completo
#     print("Resultado: ", resultado)
