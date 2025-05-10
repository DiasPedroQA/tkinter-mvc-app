# # app/frontend/gui.py
# import tkinter as tk


# def create_gui() -> None:
#     """
#     Função responsável por criar a interface gráfica com Tkinter.
#     """
#     window = tk.Tk()
#     window.title("FileMaster")

#     label = tk.Label(window, text="Informe o caminho do arquivo ou pasta:")
#     label.pack()

#     entry = tk.Entry(window)
#     entry.pack()

#     def on_button_click() -> None:
#         path = entry.get()
#         # Aqui você pode chamar as funções do backend, como manipular arquivos
#         print(f"Caminho informado: {path}")

#     button = tk.Button(window, text="Analisar", command=on_button_click)
#     button.pack()

#     window.mainloop()
