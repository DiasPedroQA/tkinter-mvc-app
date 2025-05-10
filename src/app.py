# """
# Código para testar o servidor de arquivos.
# """

# import platform
# import getpass
# from controllers.file_manager_controller import GerenciadorArquivos


# if __name__ == "__main__":
#     sistema = platform.system().capitalize()
#     usuario = getpass.getuser()
#     base_usuario = f"/home/{usuario}" if sistema == "Linux" else f"C:\\Users\\{usuario}"

#     gerenciador = GerenciadorArquivos(sistema, usuario, base_usuario)
#     resultado = gerenciador.server_analisar_caminhos("/home/pedro-pm-dias/Downloads")
#     print(resultado)
