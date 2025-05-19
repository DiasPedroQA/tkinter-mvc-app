# import uuid
# from pathlib import Path


# def gerar_id_para_path(caminho: str) -> str:
#     return str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name=caminho))


# def ler_conteudo(caminho: str) -> str:
#     caminho_atual: Path = Path(caminho).expanduser()
#     if caminho_atual.is_file():
#         return caminho_atual.read_text(encoding="utf-8")
#     return ""


# def criar_novo_arquivo(caminho: str, conteudo: str) -> str:
#     caminho_atual: Path = Path(caminho).expanduser()
#     caminho_atual.parent.mkdir(parents=True, exist_ok=True)
#     caminho_atual.write_text(conteudo, encoding="utf-8")
#     return str(caminho_atual.resolve())


# def atualizar_arquivo(caminho: str, novo_conteudo: str) -> str:
#     caminho_atual: Path = Path(caminho).expanduser()
#     if caminho_atual.is_file():
#         caminho_atual.write_text(data=novo_conteudo, encoding="utf-8")
#         return str(caminho_atual.resolve())
#     raise FileNotFoundError(f"Caminho {caminho} não encontrado.")


# def validar_caminho(caminho: str) -> bool:
#     return Path(caminho).expanduser().exists()
