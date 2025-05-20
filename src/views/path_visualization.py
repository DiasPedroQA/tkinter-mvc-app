# import sys
# import tkinter as tk
# from tkinter import filedialog, messagebox, scrolledtext, ttk
# from typing import Any, Optional

# from controllers.path_controller import PathController
# from tools.path_definitions import BasePathData, PathStatus


# class PathView(tk.Tk):
#     """
#     Interface gráfica para explorar e visualizar caminhos de arquivos e diretórios.

#     Usa PathController para obter dados e exibi-los em uma Treeview e área de texto.
#     """

#     STYLES = {
#         "header": "\033[1;36m",
#         "success": "\033[1;32m",
#         "error": "\033[1;31m",
#         "warning": "\033[1;33m",
#         "info": "\033[1;34m",
#         "reset": "\033[0m",
#         "path": "\033[1;37m",
#     }

#     def __init__(self) -> None:
#         super().__init__()
#         self.title("Explorador de Caminhos")
#         self.geometry("900x600")

#         # Controlador que gerencia a lógica do sistema de arquivos
#         self.controller = PathController()

#         self._criar_widgets()

#     def _criar_widgets(self) -> None:
#         # Treeview para mostrar lista de arquivos/pastas
#         self.tree = ttk.Treeview(
#             self,
#             columns=("tipo", "tamanho", "modificado"),
#             show="headings",
#             selectmode="browse",
#         )
#         for col, text, width in [
#             ("tipo", "Tipo", 100),
#             ("tamanho", "Tamanho", 100),
#             ("modificado", "Modificado", 200),
#         ]:
#             self.tree.heading(col, text=text)
#             self.tree.column(col, width=width)
#         self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#         # Área de texto para detalhes ou conteúdos dos arquivos
#         self.text_area = scrolledtext.ScrolledText(self, width=40)
#         self.text_area.pack(side=tk.RIGHT, fill=tk.BOTH)

#         # Botão para abrir diálogo de seleção de diretório
#         abrir_btn = tk.Button(
#             self, text="Abrir Caminho", command=self._selecionar_caminho
#         )
#         abrir_btn.pack(side=tk.BOTTOM, fill=tk.X)

#         # Evento para clicar em item da tree e mostrar detalhes
#         self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

#     def _selecionar_caminho(self) -> None:
#         caminho = filedialog.askdirectory(title="Selecione um diretório")
#         if caminho:
#             try:
#                 dados = self.controller.ler_caminho(caminho)
#                 self._preencher_treeview(dados)
#                 self.text_area.delete("1.0", tk.END)
#             except Exception as e:
#                 self._exibir_erro_gui(e)

#     def _preencher_treeview(self, dados: Any) -> None:
#         self.tree.delete(*self.tree.get_children())

#         itens = (
#             dados.get("filhos")
#             if isinstance(dados, dict) and "filhos" in dados
#             else [dados]
#         )

#         for item in itens:
#             caminho = item.get("caminho", "")
#             self.tree.insert(
#                 "",
#                 "end",
#                 iid=caminho,
#                 values=(
#                     item.get("tipo", ""),
#                     item.get("tamanho", ""),
#                     item.get("modificado", ""),
#                 ),
#                 tags=(caminho,),
#             )

#     def _on_tree_select(self, event: Optional[tk.Event] = None) -> None:
#         item_id = self.tree.focus()
#         if not item_id:
#             return
#         try:
#             dados = self.controller.ler_caminho(item_id)
#             texto = self._formatar_dados_para_texto(dados)
#             self.text_area.delete("1.0", tk.END)
#             self.text_area.insert(tk.END, texto)
#         except Exception as e:
#             self._exibir_erro_gui(e)

#     def _formatar_dados_para_texto(self, dados: Any) -> str:
#         if not dados:
#             return "Nenhum dado disponível."

#         linhas = []
#         if "filhos" in dados and isinstance(dados["filhos"], list):
#             linhas.append(f"Conteúdo de {dados.get('caminho', '')}:\n")
#             for filho in dados["filhos"]:
#                 linhas.append(
#                     f"{filho.get('nome', '')} | {filho.get('tipo', '')} | "
#                     f"Tamanho: {filho.get('tamanho', '')} | Modificado: {filho.get('modificado', '')}"
#                 )
#         else:
#             for chave, valor in dados.items():
#                 linhas.append(f"{chave}: {valor}")
#         return "\n".join(linhas)

#     def _format(self, text: str, style: str) -> str:
#         if sys.stdout.isatty() and style in self.STYLES:
#             return f"{self.STYLES[style]}{text}{self.STYLES['reset']}"
#         return text

#     def _format_status(self, status: str) -> str:
#         mapa = {
#             PathStatus.EXISTS.value: ("✔ Disponível", "success"),
#             PathStatus.CREATED.value: ("✔ Criado", "success"),
#             PathStatus.UPDATED.value: ("✔ Atualizado", "success"),
#             PathStatus.NOT_EXISTS.value: ("✖ Indisponível", "error"),
#             PathStatus.ERROR.value: ("⚠️ Erro", "error"),
#             PathStatus.DELETED.value: ("✖ Removido", "warning"),
#             PathStatus.UNKNOWN.value: ("? Desconhecido", "warning"),
#         }
#         texto, estilo = mapa.get(status, (status, "info"))
#         return self._format(texto, estilo)

#     def exibir_terminal_resumo(self, dados: list[BasePathData]) -> None:
#         if not dados:
#             print(self._format("Nenhum dado para exibir.", "warning"))
#             return
#         print(self._format("\nRESUMO DOS CAMINHOS\n" + "═" * 50, "header"))
#         for item in dados:
#             nome = item["nome"]
#             tipo = {"file": "ARQUIVO", "directory": "DIRETÓRIO"}.get(
#                 item["tipo"], "DESCONHECIDO"
#             )
#             status = self._format_status(item["status"])
#             caminho = item["caminho"]
#             print(
#                 f"{nome:<20} | {tipo:^12} | {status:^16} | {self._format(caminho, 'path')}"
#             )
#         print()

#     def _exibir_erro_gui(self, erro: Exception) -> None:
#         mensagem = f"Erro: {erro.__class__.__name__}\n{str(erro)}"
#         messagebox.showerror("Erro", mensagem)
#         print(self._format("Detalhes do Erro:", "error"))
#         print(self._format(mensagem, "error"))
