# app/main.py
from app.backend.servicos.analise_servico import GerenciadorArquivos

if __name__ == "__main__":
    gerenciador = GerenciadorArquivos()

    caminho_teste = "/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html"
    resultado = gerenciador.server_analisar_caminhos(caminho_teste)

    print("Mensagem:", resultado.mensagem)
    print("Caminho tratado:", resultado.caminho_tratado)
