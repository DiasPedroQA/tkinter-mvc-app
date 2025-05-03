# -*- coding: utf-8 -*-

"""
Módulo responsável por coordenar a interação entre a `View` e o `Model`.
Contém a lógica de controle da aplicação, tratando eventos e atualizando a interface.
"""

from aplicativo.backend.models.model import AnalisadorModel
from aplicativo.frontend.views.main_view import TelaPrincipal
from aplicativo.backend.tools.dados_servidor import SistemaArquivoInfo


class Controller:
    """
    Classe responsável por controlar a lógica da aplicação.
    Conecta a camada de visualização (View) com a camada de dados e regras de negócio (Model).
    """

    def __init__(self, model: AnalisadorModel, view: TelaPrincipal) -> None:
        """
        Inicializa o controller e conecta os componentes do modelo e da interface gráfica.

        Args:
            model (AnalisadorModel): Instância do modelo responsável pela lógica de análise.
            view (TelaPrincipal): Instância da interface gráfica.
        """
        self.model = model
        self.view = view

        # Define o comportamento do botão e carrega os dados do sistema
        self.view.set_callback_botao(self.analisar_texto)
        self.carregar_dados_sistema()

    def analisar_texto(self, texto: str) -> None:
        """
        Recebe um texto de entrada pela interface, processa com o model e envia o resultado para exibição.

        Args:
            texto (str): Texto inserido pelo usuário para análise.
        """
        resultado: str = self.model.objeto_resultado(texto)
        self.view.mostrar_resultado(resultado)

    def carregar_dados_sistema(self) -> None:
        """
        Coleta informações básicas do sistema e atualiza a interface com esses dados.
        """
        info_sistema: SistemaArquivoInfo = SistemaArquivoInfo()
        dados: dict[str, str] = {
            "Sistema": info_sistema.sistema_local(),
            "Usuário": info_sistema.pegar_usuario_logado(),
            "Versão": info_sistema.pegar_versao(),
            "Arquitetura": info_sistema.pegar_maquina(),
        }
        self.view.atualizar_infos_sistema(infos=dados)
