# -*- coding: utf-8 -*-

# """
# FileMaster - Interface gráfica para conversão de arquivos
# """

# from pathlib import Path
# import tkinter as tk
# from tkinter import messagebox, scrolledtext, ttk
# from typing import Optional

# from ttkthemes import ThemedStyle

# from backend import GerenciadorArquivos, ObjetoArquivo, ObjetoPasta, ResultadoAnalise


# class FileMasterApp:
#     def __init__(self, janela: tk.Tk) -> None:
#         self.janela = janela
#         self.janela.title("FileMaster Pro")
#         self.janela.geometry("800x750")
#         self.janela.minsize(600, 600)

#         # Configuração do backend
#         self.backend = GerenciadorArquivos()

#         # Estado da aplicação
#         self.resultado_analise: Optional[ResultadoAnalise] = None
#         self.arquivos_selecionados: list[str] = []

#         # Configuração de tema
#         self._configurar_estilo()
#         self._criar_widgets()
#         self._configurar_eventos()

#     def _configurar_estilo(self) -> None:
#         """Configura o tema visual da aplicação"""
#         self.style = ThemedStyle(self.janela)
#         self.style.set_theme("equilux")  # Tema escuro moderno
#         self.style.configure("TButton", padding=6)
#         self.style.configure("TCombobox", padding=5)

#     def _criar_widgets(self) -> None:
#         """Cria todos os componentes da interface"""
#         self._criar_cabecalho()
#         self._criar_painel_controle()
#         self._criar_painel_visualizacao()
#         self._criar_rodape()

#     def _criar_cabecalho(self) -> None:
#         """Cria o cabeçalho da aplicação"""
#         cabecalho = ttk.Frame(self.janela, padding="10 5")
#         cabecalho.pack(fill=tk.X)

#         ttk.Label(
#             cabecalho,
#             text="Conversor de Arquivos HTML",
#             font=("Segoe UI", 18, "bold"),
#             foreground="#4fc3f7",
#         ).pack(side=tk.LEFT)

#         ttk.Label(
#             cabecalho,
#             text=f"Sistema: {self.backend.sistema} | Usuário: {self.backend.usuario}",
#             font=("Segoe UI", 9),
#         ).pack(side=tk.RIGHT)

#     def _criar_painel_controle(self) -> None:
#         """Cria o painel de controle com entradas e botões"""
#         painel = ttk.LabelFrame(self.janela, text="Controle", padding=10)
#         painel.pack(fill=tk.X, padx=10, pady=5)

#         # Frame para caminho de origem
#         elemento_caminho_origem = ttk.Frame(painel)
#         elemento_caminho_origem.pack(fill=tk.X, pady=5)

#         ttk.Label(elemento_caminho_origem, text="Caminho de Origem:").pack(side=tk.LEFT)
#         self.entrada_origem = ttk.Entry(elemento_caminho_origem)
#         self.entrada_origem.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

#         self.combo_extensao_origem = ttk.Combobox(
#             elemento_caminho_origem,
#             values=[".txt", ".csv", ".json", ".html", ".pdf"],
#             width=7,
#             state="readonly",
#         )
#         self.combo_extensao_origem.set(".txt")
#         self.combo_extensao_origem.pack(side=tk.LEFT, padx=5)

#         ttk.Button(
#             elemento_caminho_origem,
#             text="Analisar",
#             command=self.botao_analisar_caminhos,
#             style="Accent.TButton",
#         ).pack(side=tk.LEFT)

#         # Frame para caminho de destino
#         elemento_caminho_destino = ttk.Frame(painel)
#         elemento_caminho_destino.pack(fill=tk.X, pady=5)

#         ttk.Label(elemento_caminho_destino, text="Caminho de Destino:").pack(side=tk.LEFT)
#         self.entrada_destino = ttk.Entry(elemento_caminho_destino)
#         self.entrada_destino.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

#         self.combo_extensao_destino = ttk.Combobox(
#             elemento_caminho_destino,
#             values=[".txt", ".csv", ".json", ".html", ".pdf"],
#             width=7,
#             state="readonly",
#         )
#         self.combo_extensao_destino.set(".json")
#         self.combo_extensao_destino.pack(side=tk.LEFT, padx=5)

#         ttk.Button(
#             elemento_caminho_destino,
#             text="Converter",
#             command=self.botao_converter_arquivos,
#             style="Accent.TButton",
#         ).pack(side=tk.LEFT)

#     def _criar_painel_visualizacao(self) -> None:
#         """Cria o painel de visualização com abas"""
#         painel = ttk.Frame(self.janela)
#         painel.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

#         # Notebook (abas)
#         self.notebook = ttk.Notebook(painel)
#         self.notebook.pack(fill=tk.BOTH, expand=True)

#         # Aba de resultados
#         self.aba_resultados = ttk.Frame(self.notebook)
#         self.notebook.add(self.aba_resultados, text="Resultados")

#         self.treeview = ttk.Treeview(
#             self.aba_resultados,
#             columns=("tipo", "tamanho", "modificacao"),
#             show="headings",
#             selectmode="extended",
#         )
#         self.treeview.heading("tipo", text="Tipo")
#         self.treeview.heading("tamanho", text="Tamanho")
#         self.treeview.heading("modificacao", text="Modificação")
#         self.treeview.column("tipo", width=100)
#         self.treeview.column("tamanho", width=100)
#         self.treeview.column("modificacao", width=150)

#         scroll_y = ttk.Scrollbar(
#             self.aba_resultados, orient=tk.VERTICAL, command=self.treeview.yview
#         )
#         scroll_x = ttk.Scrollbar(
#             self.aba_resultados, orient=tk.HORIZONTAL, command=self.treeview.xview
#         )
#         self.treeview.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

#         self.treeview.grid(row=0, column=0, sticky="nsew")
#         scroll_y.grid(row=0, column=1, sticky="ns")
#         scroll_x.grid(row=1, column=0, sticky="ew")

#         self.aba_resultados.grid_rowconfigure(0, weight=1)
#         self.aba_resultados.grid_columnconfigure(0, weight=1)

#         # Aba de logs
#         self.aba_logs = ttk.Frame(self.notebook)
#         self.notebook.add(self.aba_logs, text="Logs")

#         self.log_text = scrolledtext.ScrolledText(
#             self.aba_logs, wrap=tk.WORD, font=("Consolas", 10)
#         )
#         self.log_text.pack(fill=tk.BOTH, expand=True)

#         ttk.Button(self.aba_logs, text="Limpar Logs", command=self._limpar_logs).pack(pady=5)

#     def _criar_rodape(self) -> None:
#         """Cria o rodapé da aplicação"""
#         rodape = ttk.Frame(self.janela, padding="5")
#         rodape.pack(fill=tk.X)

#         ttk.Label(
#             rodape, text=f"Base do usuário: {self.backend.base_usuario}", font=("Segoe UI", 8)
#         ).pack(side=tk.LEFT)

#         ttk.Label(rodape, text="v1.0 © 2023 FileMaster Pro", font=("Segoe UI", 8)).pack(
#             side=tk.RIGHT
#         )

#     def _configurar_eventos(self) -> None:
#         """Configura eventos da interface"""
#         self.entrada_origem.bind("<Return>", lambda e: self.botao_analisar_caminhos())
#         self.entrada_destino.bind("<Return>", lambda e: self.botao_converter_arquivos())
#         self.treeview.bind("<Double-1>", self._selecionar_item)

#     def botao_analisar_caminhos(self) -> None:
#         """Analisa o caminho informado e exibe os resultados"""
#         caminho = self.entrada_origem.get()
#         extensao = self.combo_extensao_origem.get().lstrip(".")

#         if not caminho:
#             messagebox.showwarning("Aviso", "Por favor, informe um caminho para análise")
#             return

#         self._log(f"Analisando caminho: {caminho}")

#         try:
#             self.resultado_analise = self.backend.server_analisar_caminhos(caminho, extensao)
#             self._exibir_resultados()
#         except Exception as e:
#             self._log(f"Erro na análise: {str(e)}", erro=True)
#             messagebox.showerror("Erro", f"Falha ao analisar caminho:\n{str(e)}")

#     def _exibir_resultados(self) -> None:
#         """Exibe os resultados da análise na TreeView"""
#         if not self.resultado_analise or not self.resultado_analise.sucesso:
#             return

#         self.treeview.delete(*self.treeview.get_children())

#         if isinstance(self.resultado_analise.objetos_coletados, ObjetoPasta):
#             for arquivo in self.resultado_analise.objetos_coletados.subitens:
#                 self.treeview.insert("", tk.END, values=(arquivo, "Pasta", ""))
#         elif isinstance(self.resultado_analise.objetos_coletados, ObjetoArquivo):
#             detalhes = self.resultado_analise.objetos_coletados
#             self.treeview.insert(
#                 "",
#                 tk.END,
#                 values=(
#                     Path(detalhes.caminho_arquivo).name,
#                     "Arquivo",
#                     f"{detalhes.tamanho_bytes / 1024:.2f} KB",
#                     detalhes.ultima_modificacao_formatada,
#                 ),
#             )

#     def botao_converter_arquivos(self) -> None:
#         """Converte os arquivos selecionados"""
#         if not self.resultado_analise:
#             messagebox.showwarning("Aviso", "Analise um caminho primeiro")
#             return

#         extensao = self.combo_extensao_destino.get().lstrip(".")

#         try:
#             self._log(f"Iniciando conversão para {extensao}...")
#             self.backend.server_converter_arquivos(
#                 self.arquivos_selecionados or [self.resultado_analise.caminho_tratado], extensao
#             )
#             self._log("Conversão concluída com sucesso!")
#         except Exception as e:
#             self._log(f"Erro na conversão: {str(e)}", erro=True)
#             messagebox.showerror("Erro", f"Falha na conversão:\n{str(e)}")

#     def _selecionar_item(self, event: tk.Event) -> None:
#         """Manipula a seleção de itens na TreeView
#         Args:
#             event: Objeto de evento tkinter com detalhes do clique
#         """
#         if item_id := self.treeview.identify_row(event.y):
#             item = self.treeview.item(item_id)
#             valores = item["values"]
#             self.arquivos_selecionados.append(valores[0])
#             self._log(f"Arquivo selecionado: {valores[0]}")

#     def _log(self, mensagem: str, erro: bool = False) -> None:
#         """Adiciona uma mensagem ao log"""
#         tag = "erro" if erro else "info"
#         self.log_text.configure(state="normal")
#         self.log_text.insert(tk.END, mensagem + "\n", tag)
#         self.log_text.configure(state="disabled")
#         self.log_text.see(tk.END)

#     def _limpar_logs(self) -> None:
#         """Limpa o conteúdo dos logs"""
#         self.log_text.configure(state="normal")
#         self.log_text.delete(1.0, tk.END)
#         self.log_text.configure(state="disabled")


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = FileMasterApp(root)

#     # Configuração adicional de estilo
#     style = ThemedStyle(root)
#     style.configure("Accent.TButton", foreground="white", background="#0078d7")

#     root.mainloop()
