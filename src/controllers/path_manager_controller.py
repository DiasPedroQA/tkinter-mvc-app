# -*- coding: utf-8 -*-

"""
Controller CRUD para operações com caminhos do sistema de arquivos.

Esta controller integra os módulos de models e tools para fornecer operações
de criação e leitura de arquivos e diretórios com validações e funcionalidades
adicionais.

Funcionalidades implementadas:
- Criação inteligente de arquivos ou diretórios baseado no caminho
- Leitura automática de arquivos ou diretórios
- Validações de extensão e permissões
- Leitura recursiva de diretórios (até 5 níveis)
"""

import os
from pathlib import Path
from typing import Any

from models.path_system_model import ModeloArquivo, ModeloCaminho, ModeloDiretorio
from tools.path_toolkit import ExtratorDeCaminhos

# Constantes
NIVEIS_MAX_RECURSAO = 5
EXTENSOES_PERMITIDAS: set[str] = {".txt", ".csv", ".json", ".md"}  # Exemplo


class PathController:
    """Controller para operações CRUD com caminhos do sistema de arquivos."""

    def __init__(self) -> None:
        self.extrator = ExtratorDeCaminhos()

    def create(self, caminho: str, conteudo: str | None = None) -> str | None:
        """Cria um novo arquivo ou diretório no caminho especificado.

        Detecta automaticamente se deve criar arquivo ou diretório baseado em:
        - Se conteudo for fornecido -> cria arquivo
        - Se caminho terminar com barra -> cria diretório
        - Caso contrário -> cria arquivo

        Args:
            caminho: Caminho onde o item será criado
            conteudo: Conteúdo a ser escrito (obrigatório para arquivos)

        Returns:
            ModeloArquivo | ModeloDiretorio: Objeto representando o item criado
            None: Se a operação falhar

        Raises:
            ValueError: Se os parâmetros forem inválidos
            PermissionError: Se não tiver permissões para criação
        """
        try:
            # Remove barra final para padronização
            caminho = caminho.rstrip("/")

            # Verifica se deve criar diretório
            if conteudo is None:
                return self._create_dir(caminho=caminho)
            return self._create_file(caminho=caminho, conteudo=conteudo)
        except Exception as e:
            print(f"Erro ao criar {caminho}: {str(e)}")
            return None

    def _create_file(self, caminho: str, conteudo: str) -> str:
        """Método interno para criação de arquivos."""
        path_obj = Path(caminho)

        if path_obj.exists():
            if path_obj.is_dir():
                raise IsADirectoryError(f"O caminho é um diretório: {caminho}")
            raise FileExistsError(f"Arquivo já existe: {caminho}")

        path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(path_obj, "w", encoding="utf-8") as f:
            f.write(conteudo)

        return ModeloCaminho(caminho_bruto=str(path_obj)).to_json()

    def _create_dir(self, caminho: str) -> str:
        """Método interno para criação de diretórios."""
        path_obj = Path(caminho)

        if path_obj.exists():
            if path_obj.is_dir():
                return ModeloCaminho(caminho_bruto=str(path_obj)).to_json()
            raise FileExistsError(f"Caminho já existe e não é um diretório: {caminho}")

        path_obj.mkdir(parents=True)
        return ModeloCaminho(caminho_bruto=str(path_obj)).to_json()

    def read(
        self,
        caminho: str,
        ler_conteudo: bool = False,
        recursivo: bool = True
    ) -> dict[str, Any] | None:
        """Lê um arquivo ou diretório no caminho especificado.

        Detecta automaticamente se o caminho é arquivo ou diretório.

        Args:
            caminho: Caminho a ser lido
            ler_conteudo: Se True e for arquivo, inclui o conteúdo na resposta
            recursivo: Se True e for diretório, faz leitura recursiva

        Returns:
            dict: Dicionário com os dados do item
            None: Se a leitura falhar
        """
        try:
            path_obj = Path(caminho)

            if not path_obj.exists():
                raise FileNotFoundError(f"Caminho não encontrado: {caminho}")

            if path_obj.is_file():
                return self._read_file(path_obj=path_obj, ler_conteudo=ler_conteudo)

            # Se chegou aqui, é diretório
            if recursivo:
                return self._read_dir_recursivo(path_obj=path_obj)

            return ModeloCaminho(caminho_bruto=str(path_obj)).montar_objeto().__dict__

        except Exception as e:
            print(f"Erro ao ler {caminho}: {str(e)}")
            return None

    def _read_file(self, path_obj: Path, ler_conteudo: bool) -> dict[str, Any]:
        """Método interno para leitura de arquivos com validações."""
        # Valida extensão
        if path_obj.suffix.lower() not in EXTENSOES_PERMITIDAS:
            raise ValueError(f"Extensão não permitida: {path_obj.suffix}")

        # Valida permissões
        if not os.access(path_obj, os.R_OK):
            raise PermissionError(f"Sem permissão para ler o arquivo: {path_obj}")

        # Monta o objeto básico
        modelo: ModeloArquivo | ModeloDiretorio = ModeloCaminho(
            caminho_bruto=str(path_obj)
        ).montar_objeto()
        resultado: dict[str, Any] = modelo.__dict__

        # Adiciona conteúdo se solicitado
        if ler_conteudo:
            with open(path_obj, "r", encoding="utf-8") as f:
                resultado["conteudo"] = f.read()

        return resultado

    def _read_dir_recursivo(
        self, path_obj: Path, nivel_atual: int = 0
    ) -> dict[str, Any]:
        """Método interno para leitura recursiva de diretórios."""
        if nivel_atual >= NIVEIS_MAX_RECURSAO:
            return {}

        modelo: ModeloArquivo | ModeloDiretorio = ModeloCaminho(
            caminho_bruto=str(path_obj)
        ).montar_objeto()
        resultado: dict[str, Any] = modelo.__dict__
        resultado["subitens_detalhados"] = []

        for item in path_obj.iterdir():
            try:
                if item.is_file():
                    item_model: ModeloArquivo | ModeloDiretorio = ModeloCaminho(
                        caminho_bruto=str(item)
                    ).montar_objeto()
                    resultado["subitens_detalhados"].append(item_model.__dict__)
                if item.is_dir():
                    subdir: dict[Any, Any] = self._read_dir_recursivo(
                        path_obj=item, nivel_atual=nivel_atual + 1
                    )
                    resultado["subitens_detalhados"].append(subdir)
            except Exception as e:
                print(f"Erro ao processar {item}: {str(e)}")
                continue

        return resultado

    # Métodos vazios para o CRUD completo (a implementar no futuro)
    def update(self) -> NotImplementedError:
        """Atualiza um arquivo ou diretório."""
        raise NotImplementedError("Método update não implementado")

    def delete(self, caminho: str) -> NotImplementedError:
        """Remove um arquivo ou diretório."""
        raise NotImplementedError("Método delete não implementado")


# Exemplo de uso
if __name__ == "__main__":
    controller = PathController()

    # Exemplo de criação de arquivo (automático pelo conteúdo)
    # novo_arquivo: str | None = controller.create(
    #     caminho="~/Downloads/Firefox/novo_bookmarks.html",
    #     conteudo="Conteúdo de exemplo",  # Presença de conteúdo -> cria arquivo
    # )
    # print("Arquivo criado:", novo_arquivo)

    # Exemplo de criação de diretório (automático pela ausência de conteúdo)
    # nova_pasta: str | None = controller.create(
    #     caminho="~/Downloads/Firefox/nova_pasta"  # Sem conteúdo -> cria diretório
    # )
    # print("Pasta criada:", nova_pasta)

    # Exemplo de leitura de arquivo
    dados_arquivo: dict[str, Any] | None = controller.read(
        caminho="~/Downloads/Firefox/bookmarks.html", ler_conteudo=True
    )
    print("Dados do arquivo:", dados_arquivo)

    # Exemplo de leitura de pasta (não recursiva)
    dados_pasta: dict[str, Any] | None = controller.read(
        caminho="~/Downloads/Firefox", recursivo=False
    )
    print("Dados da pasta (não recursivo):", dados_pasta)

    # Exemplo de leitura recursiva
    dados_pasta_recursiva: dict[str, Any] | None = controller.read(
        caminho="~/Downloads", recursivo=True
    )
    print("Dados da pasta (recursivo):", dados_pasta_recursiva)
