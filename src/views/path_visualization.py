# # src/views/path_visualization.py

# class VisualizadorDeCaminhos:
#     """Apresenta dados de objetos de arquivo ou pasta."""

#     def exibir_arquivo(self, arquivo: dict) -> str:
#         linhas: list[str] = [
#             f"📄 Arquivo: {arquivo['nome']}",
#             f"Extensão: {arquivo['extensao']}",
#             f"Caminho: {arquivo['caminho']}",
#             f"Tamanho: {arquivo['tamanho']} bytes",
#             f"Permissões: {arquivo['permissoes']}",
#             f"Usuário: {arquivo['usuario']}",
#             f"Criado em: {arquivo['criacao']}",
#             f"Modificado em: {arquivo['modificacao']}",
#             f"Acessado em: {arquivo['acesso']}",
#             f"Oculto: {'Sim' if arquivo['oculto'] else 'Não'}",
#             f"Link simbólico: {'Sim' if arquivo['link'] else 'Não'}",
#             f"Montagem: {'Sim' if arquivo['montagem'] else 'Não'}",
#         ]
#         return "\n".join(linhas)

#     def exibir_pasta(self, pasta: dict) -> str:
#         linhas: list[str] = [
#             f"📁 Pasta: {pasta['nome']}",
#             f"Caminho: {pasta['caminho']}",
#             f"Itens: {pasta['quantidade_itens']}",
#             f"Conteúdo: {', '.join(pasta['conteudo'])}",
#             f"Permissões: {pasta['permissoes']}",
#             f"Usuário: {pasta['usuario']}",
#             f"Criada em: {pasta['criacao']}",
#             f"Modificada em: {pasta['modificacao']}",
#             f"Acessada em: {pasta['acesso']}",
#             f"Oculta: {'Sim' if pasta['oculto'] else 'Não'}",
#             f"Link simbólico: {'Sim' if pasta['link'] else 'Não'}",
#             f"Montagem: {'Sim' if pasta['montagem'] else 'Não'}",
#         ]
#         return "\n".join(linhas)
