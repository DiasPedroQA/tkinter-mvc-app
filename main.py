# -*- coding: utf-8 -*-

"""
Ponto de entrada da aplicação.

Este módulo inicia a aplicação Tkinter ao importar e executar a função `criar_app`,
que retorna a instância principal da interface gráfica.
"""

from aplicativo.meu_app import criar_app

if __name__ == '__main__':
    app = criar_app()
    app.mainloop()
