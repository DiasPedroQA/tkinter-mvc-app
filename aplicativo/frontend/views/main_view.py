"""
Módulo responsável pela criação da interface gráfica principal do aplicativo.
Contém campos de entrada, botão de análise e uma área para exibir informações do sistema.
"""

import tkinter as tk
from tkinter import ttk
from collections.abc import Callable
from typing import Union
import json
from pathlib import Path


class TelaPrincipal:
    """
    Classe que representa a tela principal da interface gráfica.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Inicializa os componentes da interface.

        Args:
            root (tk.Tk): Janela principal do Tkinter.
        """
        self.config = self._carregar_configuracoes()
        self.root = root
        self.root.title("App MVC - Informações do Sistema")
        self.root.minsize(*self.config["largura_minima"])

        self.placeholder = self.config["placeholder"]

        fonte = tuple(self.config["font_padrao"])
        padding = self.config["padding"]

        # Frame com labels de informações do sistema
        self.info_frame = tk.Frame(self.root)
        self.info_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.info_labels: dict[str, ttk.Label] = {}
        info_nomes = ["Sistema", "Usuário", "Versão", "Arquitetura"]
        for i, nome in enumerate(info_nomes):
            label = ttk.Label(self.info_frame, text=f"{nome}: ?", font=fonte)
            label.grid(row=i, column=0, sticky="w", **padding)
            self.info_labels[nome] = label

        # Label do campo de entrada
        self.label_entry = ttk.Label(self.root, text="Caminho para análise:", font=fonte)
        self.label_entry.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 5))

        # Frame que contém input e botão lado a lado
        self.entry_frame = ttk.Frame(self.root)
        self.entry_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.entry_frame.columnconfigure(0, weight=1)

        # Campo de entrada com placeholder
        self.entry = ttk.Entry(self.entry_frame, font=fonte)
        self.entry.insert(0, self.placeholder)
        self.entry.grid(row=0, column=0, sticky="ew", **padding)
        self.entry.bind("<FocusIn>", self._remover_placeholder)
        self.entry.bind("<FocusOut>", self._restaurar_placeholder)

        # Botão de análise na mesma linha do campo
        self.btn = ttk.Button(self.entry_frame, text="Analisar")
        self.btn.grid(row=0, column=1, **padding)

        # Área para exibir o resultado (Text widget permite múltiplas linhas)
        self.resultado = tk.Text(
            self.root, font=fonte, height=self.config["altura_texto"], wrap="word"
        )
        self.resultado.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.root.rowconfigure(3, weight=1)

    def _carregar_configuracoes(self) -> dict:
        """
        Carrega configurações de estilo a partir de um arquivo JSON.

        Returns:
            dict: Configurações de interface (fonte, padding, etc.).
        """
        caminho_base = Path(__file__).resolve().parent  # .../frontend/views
        caminho = (
            caminho_base.parent / "assets" / "estilos.json"
        )  # .../frontend/assets/estilos.json

        if not caminho.exists():
            raise FileNotFoundError(f"Arquivo de configuração não encontrado em: {caminho}")

        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)

    def _remover_placeholder(self, _: Union[tk.Event, None]) -> None:
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)

    def _restaurar_placeholder(self, _: Union[tk.Event, None]) -> None:
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)

    def set_callback_botao(self, callback: Callable[[str], None]) -> None:
        self.btn.config(command=lambda: callback(self.entry.get()))

    def mostrar_resultado(self, objeto_retorno: str) -> None:
        self.resultado.delete(1.0, tk.END)
        self.resultado.insert(tk.END, objeto_retorno)

    def atualizar_infos_sistema(self, infos: dict[str, str]) -> None:
        for chave, valor in infos.items():
            if chave in self.info_labels:
                self.info_labels[chave].config(text=f"{chave} -> {valor}")
