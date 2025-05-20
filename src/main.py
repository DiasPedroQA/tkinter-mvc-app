# pylint: disable=missing-function-docstring, missing-module-docstring

# src/main.py

# import sys

# from controllers.path_manager_controller import PathController
# from views.path_visualization import PathView


# def iniciar_gui() -> None:
#     app = PathView()
#     app.mainloop()


# def iniciar_terminal() -> None:
#     controller = PathController()
#     PathView.exibir_cabecalho("Explorador de Caminhos (Terminal)")

#     caminho = input("Digite o caminho a ser explorado: ").strip()
#     if not caminho:
#         PathView.exibir_mensagem("alerta", "Nenhum caminho fornecido.")
#         return

#     try:
#         dados = controller.ler_caminho(caminho)
#         if dados["tipo"] == "diretorio":
#             PathView.exibir_conteudo_diretorio(caminho, dados["filhos"])
#         else:
#             conteudo = controller.ler_arquivo_texto(caminho)
#             PathView.exibir_conteudo_arquivo(caminho, conteudo)
#     except Exception as e:
#         PathView.exibir_erro(e)


# def main() -> None:
#     modo = "gui"  # padrão pode ser "gui" ou "terminal"
#     if len(sys.argv) > 1 and sys.argv[1].lower() == "terminal":
#         modo = "terminal"

#     if modo == "terminal":
#         iniciar_terminal()
#     else:
#         iniciar_gui()


# if __name__ == "__main__":
#     main()
