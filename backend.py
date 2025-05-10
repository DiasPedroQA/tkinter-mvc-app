# -*- coding: utf-8 -*-
"""
Módulo backend para operações com arquivos e informações do sistema - Versão Completa.
"""

from dataclasses import dataclass, field
from datetime import datetime
import difflib
import getpass
from pathlib import Path
import platform
import re
from typing import Optional, Union


@dataclass
class ObjetoArquivo:
    """Classe para armazenar detalhes de um arquivo."""

    tipo_item: str = "Arquivo"
    extensao_arquivo: str = ""
    tamanho_bytes: int = 0
    ultima_modificacao: float = 0.0
    caminho_arquivo: str = ""

    @property
    def ultima_modificacao_formatada(self) -> str:
        """Retorna a data de modificação formatada."""
        return datetime.fromtimestamp(self.ultima_modificacao).strftime('%Y-%m-%d %H:%M:%S')


@dataclass
class ObjetoPasta:
    """Classe para armazenar detalhes de uma pasta."""

    tipo_item: str = "Pasta"
    subitens: list[str] = field(default_factory=list)
    caminho_pasta: str = ""


@dataclass
class ResultadoAnalise:
    """Classe para representar o resultado da análise de um caminho."""

    sucesso: bool = False
    mensagem: str = ""
    caminho_tratado: str = ""
    tipo_caminho: str = ""
    objetos_coletados: Optional[Union[ObjetoArquivo, ObjetoPasta]] = None
    caminho_corrigido: Optional[str] = None


class GerenciadorArquivos:
    """Classe principal para gerenciamento de operações com arquivos."""

    def __init__(self) -> None:
        self._sistema = platform.system().capitalize()
        self._usuario = getpass.getuser()
        self._base_usuario = self._detectar_sistema_servidor()

    @property
    def sistema(self) -> str:
        """Retorna o sistema operacional atual."""
        return self._sistema

    @property
    def usuario(self) -> str:
        """Retorna o usuário atual."""
        return self._usuario

    @property
    def base_usuario(self) -> str:
        """Retorna o caminho base do usuário."""
        return self._base_usuario

    def _detectar_sistema_servidor(self) -> str:
        """Retorna o caminho base do usuário atual conforme o sistema."""
        if self._sistema == "Windows":
            return f"C:\\Users\\{self._usuario}"
        if self._sistema == "Darwin":
            return f"/Users/{self._usuario}"
        if self._sistema == "Linux":
            return f"/home/{self._usuario}"
        raise ValueError(f"Sistema operacional desconhecido: '{self._sistema}'")

    def _normalizar_caminho(self, caminho_bruto: str) -> Path:
        """
        Limpa e normaliza um caminho bruto usando regex.
        Remove espaços, múltiplas barras, corrige barras invertidas e remove '../' iniciais.
        """
        caminho_normal = caminho_bruto.strip()
        caminho_normal = re.sub(r"[\\]+", "/", caminho_normal)  # barras invertidas para /
        caminho_normal = re.sub(
            r"\s*/\s*", "/", caminho_normal
        )  # remove espaços ao redor das barras
        caminho_normal = re.sub(r"/{2,}", "/", caminho_normal)  # barras duplicadas
        caminho_normal = re.sub(r"[<>:\"|?*]", "", caminho_normal)  # remove caracteres inválidos

        # Remove prefixos "../" até que não existam mais no início
        while caminho_normal.startswith("../"):
            caminho_normal = caminho_normal[3:]

        return Path(caminho_normal)

    def _tentar_corrigir_caminho(self, caminho_com_erro: Path) -> Optional[Path]:
        """
        Tenta corrigir partes do caminho (caminho_com_erro) com base
        em similaridade com o conteúdo do sistema de arquivos.
        Retorna um novo Path se conseguir corrigir, ou None se não conseguir.
        """
        partes = caminho_com_erro.parts
        caminho_atual = Path(partes[0]) if caminho_com_erro.is_absolute() else Path()
        for parte in partes[1:]:
            if not caminho_atual.exists():
                return None
            try:
                opcoes = [p.name for p in caminho_atual.iterdir()]
            except (PermissionError, FileNotFoundError, NotADirectoryError):
                return None
            caminho_similares = difflib.get_close_matches(parte, opcoes, n=1, cutoff=0.6)
            caminho_atual = (
                caminho_atual / caminho_similares[0] if caminho_similares else caminho_atual / parte
            )
        return caminho_atual if caminho_atual.exists() else None

    def _filtrar_por_extensao(self, caminho_de_pasta: Path, extensao_desejada: str) -> list[str]:
        """
        Retorna uma lista com nomes de arquivos que possuem a extensão desejada,
        dentro do caminho informado (apenas arquivos diretos, sem recursão).
        """
        if not caminho_de_pasta.is_dir():
            return []

        return sorted(
            [
                p.name
                for p in caminho_de_pasta.iterdir()
                if p.is_file() and p.suffix.lower() == extensao_desejada.lower()
            ]
        )

    def server_analisar_caminhos(
        self, caminho_entrada: str, extensao_arquivo: str = ""
    ) -> ResultadoAnalise:
        """
        Analisa um caminho informado: detecta se é relativo ou absoluto, converte, valida e tenta corrigir.

        Args:
            caminho_entrada: Caminho a ser analisado
            extensao_arquivo: Extensão para filtrar conteúdo de pastas (opcional)

        Returns:
            ResultadoAnalise: Objeto com todos os detalhes da análise
        """
        objeto_analisado: ResultadoAnalise = ResultadoAnalise()

        # 1. Normalizar entrada
        caminho_normalizadao: Path = self._normalizar_caminho(caminho_bruto=caminho_entrada)

        # 2. Converter caminho relativo
        if not caminho_normalizadao.is_absolute():
            caminho_normalizadao = (Path(self.base_usuario) / caminho_normalizadao).resolve()
            objeto_analisado.tipo_caminho = "absoluto_convertido"
        else:
            caminho_normalizadao = caminho_normalizadao.resolve()
            objeto_analisado.tipo_caminho = "absoluto_natural"

        objeto_analisado.caminho_tratado = str(caminho_normalizadao)

        # 3. Verificar se existe
        if caminho_normalizadao.exists():
            objeto_analisado.sucesso = True
            if caminho_normalizadao.is_dir():
                objeto_analisado.mensagem = "Pasta identificada com sucesso."
                objeto_analisado.objetos_coletados = ObjetoPasta(
                    subitens=self._filtrar_por_extensao(
                        caminho_de_pasta=caminho_normalizadao, extensao_desejada=extensao_arquivo
                    ),
                    caminho_pasta=str(caminho_normalizadao),
                )
            elif caminho_normalizadao.is_file():
                objeto_analisado.mensagem = "Arquivo identificado com sucesso."
                objeto_analisado.objetos_coletados = ObjetoArquivo(
                    extensao_arquivo=caminho_normalizadao.suffix,
                    tamanho_bytes=caminho_normalizadao.stat().st_size,
                    ultima_modificacao=caminho_normalizadao.stat().st_mtime,
                    caminho_arquivo=str(caminho_normalizadao),
                )
            return objeto_analisado

        # 4. Tentar corrigir caminho
        if caminho_corrigido := self._tentar_corrigir_caminho(
            caminho_com_erro=caminho_normalizadao
        ):
            objeto_analisado.sucesso = True
            objeto_analisado.caminho_corrigido = str(caminho_corrigido)

            if caminho_corrigido.is_dir():
                objeto_analisado.mensagem = (
                    "Caminho corrigido, encontrado e identificado como Pasta."
                )
                objeto_analisado.objetos_coletados = ObjetoPasta(
                    subitens=self._filtrar_por_extensao(
                        caminho_de_pasta=caminho_corrigido, extensao_desejada=extensao_arquivo
                    ),
                    caminho_pasta=str(caminho_corrigido),
                )
            elif caminho_corrigido.is_file():
                objeto_analisado.mensagem = (
                    "Caminho corrigido, encontrado e identificado como Arquivo."
                )
                objeto_analisado.objetos_coletados = ObjetoArquivo(
                    extensao_arquivo=caminho_corrigido.suffix,
                    tamanho_bytes=caminho_corrigido.stat().st_size,
                    ultima_modificacao=caminho_corrigido.stat().st_mtime,
                    caminho_arquivo=str(caminho_corrigido),
                )
            return objeto_analisado

        # 5. Caminho inválido mesmo após tentativa
        objeto_analisado.mensagem = "O caminho não foi encontrado e não foi possível corrigi-lo."
        return objeto_analisado

    def server_converter_arquivos(
        self,
        caminhos_encontrados: Union[str, list[str]],
        extensao_conversao: str,
        extensao_origem: str = "",
    ) -> None:
        """
        Converte arquivos mantendo todas as validações de caminho da classe.

        Args:
            caminhos_encontrados: Caminho único ou lista de caminhos (aceita relativos/absolutos)
            extensao_conversao: Extensão desejada para os arquivos convertidos (ex: "json", "csv")
            extensao_origem: Extensão dos arquivos a serem convertidos (opcional para pastas)
        """
        # Normaliza para sempre trabalhar com lista
        caminhos = (
            [caminhos_encontrados]
            if isinstance(caminhos_encontrados, str)
            else caminhos_encontrados
        )

        for caminho in caminhos:
            # Validação do caminho (reutiliza toda a lógica existente)
            analise = self.server_analisar_caminhos(
                caminho_entrada=caminho, extensao_arquivo=extensao_origem
            )

            if not analise.sucesso:
                print(f"⛔ Falha na validação: {analise.mensagem}")
                continue

            if isinstance(analise.objetos_coletados, ObjetoArquivo):
                self._converter_arquivo_individual(
                    analise.objetos_coletados,
                    extensao_conversao,
                    analise.caminho_corrigido or analise.caminho_tratado,
                )
            elif isinstance(analise.objetos_coletados, ObjetoPasta):
                # Processamento para pasta
                print(f"\n📁 Processando pasta: {analise.objetos_coletados.caminho_pasta}")
                if not analise.objetos_coletados.subitens:
                    print("(i) Nenhum arquivo encontrado para conversão")
                    continue

                for arquivo in analise.objetos_coletados.subitens:
                    caminho_arquivo = Path(analise.objetos_coletados.caminho_pasta) / arquivo
                    analise_arquivo = self.server_analisar_caminhos(str(caminho_arquivo))

                    if analise_arquivo.sucesso and isinstance(
                        analise_arquivo.objetos_coletados, ObjetoArquivo
                    ):
                        self._converter_arquivo_individual(
                            analise_arquivo.objetos_coletados,
                            extensao_conversao,
                            analise_arquivo.caminho_corrigido or analise_arquivo.caminho_tratado,
                        )

    def _converter_arquivo_individual(
        self,
        arquivo: ObjetoArquivo,
        extensao_conversao: str,
        caminho_original: str,  # Mantido para consistência
    ) -> None:
        """Método auxiliar para converter um arquivo individual

        Args:
            arquivo: Objeto contendo informações do arquivo
            extensao_conversao: Nova extensão desejada
            caminho_original: Caminho antes de correções (não utilizado nesta versão)
        """
        _ = caminho_original  # Explicitamente marcado como não utilizado

        arquivo_path = Path(arquivo.caminho_arquivo)
        caminho_saida = str(arquivo_path.with_suffix(f".{extensao_conversao.lstrip('.')}"))

        print(f"\n🔁 Convertendo: {arquivo_path.name} → {Path(caminho_saida).name}")
        print(f"📂 Origem: {arquivo.caminho_arquivo}")
        print(f"📂 Destino: {caminho_saida}")
        print("🔄 Simulando conversão do conteúdo...")

        try:
            # conteúdo = self._ler_arquivo(arquivo_path)  # Futura implementação
            # dados_convertidos = self._converter(conteúdo)   # Futura implementação
            # self._salvar_arquivo(caminho_saida, dados_convertidos)
            print(f"✅ Conversão simulada concluída para: {caminho_saida}")
        except Exception as e:
            print(f"⚠ Erro durante conversão: {str(e)}")


# Exemplo de uso
if __name__ == "__main__":
    print("=== Teste da Classe GerenciadorArquivos ===")
    gerenciador = GerenciadorArquivos()

    # Teste básico do sistema
    # print(f"\n\nSistema detectado: {gerenciador.sistema}")
    # print(f"Usuário atual: {gerenciador.usuario}")
    # print(f"Base do usuário: {gerenciador.base_usuario}")

    # Teste de análise de caminhos
    caminhos_teste = {
        "caminho absoluto de arquivo": "/home/pedro-pm-dias/Downloads/Firefox/bookmarks.html",
        "caminho absoluto de pasta": "/home/pedro-pm-dias/Downloads",
        "caminho errado de arquivo": "/home///pedro-pm-dias//Downlodes/Firfox/bookmrks.html",
        "caminho errado de pasta": "/home///pedro-pm-dias//Downlodes/Firfoxx",
        "caminho relativo de arquivo": "../Downloads/Firefox/bookmarks.html",
        "caminho relativo de pasta": "../Downloads",
    }
    extensao_buscada: str = ".html"

    print("\n\n=== Teste de análise de caminhos ===")
    for nome, entrada in caminhos_teste.items():
        print(f"\n🔎Trabalhando com um {nome}", "\n", entrada)
        resultado = gerenciador.server_analisar_caminhos(
            caminho_entrada=entrada, extensao_arquivo=extensao_buscada
        )

        print(f"Sucesso: {resultado.sucesso}")
        print(f"Mensagem: {resultado.mensagem}")
        print(f"Caminho tratado: {resultado.caminho_tratado}")
        print(f"Tipo caminho: {resultado.tipo_caminho}")

        if resultado.caminho_corrigido:
            print(f"Caminho corrigido: {resultado.caminho_corrigido}")

        if resultado.objetos_coletados:
            print("\nObjeto:")
            if isinstance(resultado.objetos_coletados, ObjetoArquivo):
                print(f"Tipo do item: {resultado.objetos_coletados.tipo_item}")
                print(f"Extensão: {resultado.objetos_coletados.extensao_arquivo}")
                print(f"Tamanho: {resultado.objetos_coletados.tamanho_bytes} bytes")
                print(f"Modificação: {resultado.objetos_coletados.ultima_modificacao_formatada}")
            elif isinstance(resultado.objetos_coletados, ObjetoPasta):
                print(f"Tipo do item: {resultado.objetos_coletados.tipo_item}")
                print(f"Arquivos encontrados: {len(resultado.objetos_coletados.subitens)}")
                if resultado.objetos_coletados.subitens:
                    print("Primeiros 5 itens:", resultado.objetos_coletados.subitens[:5])

    # # Teste da nova função de conversão
    # print("\n\n=== Teste de conversão de arquivos ===")
    # arquivos_para_converter = [
    #     "/home/pedro-pm-dias/Downloads",
    #     "/home///pedro-pm-dias//Downlodes/Firfox/bookmrks.html",
    #     "/home///pedro-pm-dias//Downlodes/Firfoxx",
    #     "../Downloads/Firefox/bookmarks.html",
    #     "../Downloads",
    # ]
    # gerenciador.server_converter_arquivos(
    #     caminhos_encontrados=arquivos_para_converter,
    #     extensao_conversao="json",
    #     extensao_origem=".html",  # Só converter arquivos .html
    # )
