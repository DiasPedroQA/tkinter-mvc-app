# -*- coding: utf-8 -*-

"""
Módulo de inicialização do aplicativo.

Este módulo configura e conecta o Model, View e Controller (MVC),
retornando a instância principal da janela Tkinter para execução.
"""

import tkinter as tk
from aplicativo.backend.controllers.controller import Controller
from aplicativo.backend.models.model import AnalisadorModel
from aplicativo.frontend.views.main_view import TelaPrincipal


def criar_app() -> tk.Tk:
    """
    Cria e configura a aplicação seguindo o padrão MVC.

    Inicializa o modelo, a interface gráfica (view) e o controlador,
    conectando todos os componentes para a execução do app.

    Returns:
        tk.Tk: Instância principal da janela Tkinter pronta para execução.
    """
    root = tk.Tk()
    model: AnalisadorModel = AnalisadorModel()
    view: TelaPrincipal = TelaPrincipal(root)
    Controller(model, view)  # Instancia o controller apenas para conectar os componentes
    return root
