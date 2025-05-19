# from controllers.path_manager_controller import PathController
# from models.path_system_model import CaminhoModel
# from views.path_visualization import exibir_tabela_json


# def main() -> None:
#     caminhos: list[str] = [
#         "~/Documentos",
#         "~/Downloads/Firefox/bookmarks.html",
#         "~/Downloads/Firefox/",
#         "~/Downloads/Firefox/nao_existe",
#     ]

#     controller = PathController(caminhos=caminhos)
#     resultados: list[dict[str, CaminhoModel]] = controller.ler_caminhos()
#     exibir_tabela_json(lista_modelos=resultados)


# if __name__ == "__main__":
#     main()
