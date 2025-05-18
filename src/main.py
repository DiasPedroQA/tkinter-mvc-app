# # src/main.py
# # -*- coding: utf-8 -*-
# """
# Módulo principal da aplicação.

# Este módulo serve como ponto de entrada para simular a leitura de caminhos
# de arquivos e pastas. Ele utiliza o controlador `PathManagerController`
# para identificar e processar os dados dos caminhos informados.

# Ao executar este módulo diretamente, são analisados:
# - Um caminho de pasta (para listar o conteúdo).
# - Um caminho de arquivo (para obter metadados e informações relevantes).

# Classes:
#     PathManagerController

# Funções:
#     main -- função principal que executa a simulação de leitura de caminhos.
# """

# from controllers.path_manager_controller import PathController


# def main() -> None:
#     """
#     Executa a simulação de leitura e análise de caminhos.

#     Esta função inicializa o controlador `PathManagerController`, fornece
#     dois caminhos (um de pasta e outro de arquivo) e imprime no terminal
#     os resultados da leitura, organizados em dicionários com dados formatados.

#     Exemplos:
#         📁 Analisando pasta:
#         {'tipo': 'pasta', 'conteudo': [...], ...}

#         📄 Analisando arquivo:
#         {'tipo': 'arquivo', 'extensao': '.html', ...}
#     """
#     caminho_pasta = "/home/pedro-pm-dias/Downloads/Firefox/"
#     # "~/Downloads/Firefox/"
#     caminho_arquivo = "/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html"
#     # "~/Downloads/Firefox/bookmarks.html"

#     controller = PathController()

#     print("📁 Analisando pasta:")
#     pasta: dict[str, str] = controller.read(
#         caminho=caminho_pasta, ler_conteudo=True, recursivo=True
#     )
#     print(pasta)

#     print("\n📄 Analisando arquivo:")
#     arquivo: dict[str, str] = controller.read(caminho=caminho_arquivo)
#     print(arquivo)


# if __name__ == "__main__":
#     main()
