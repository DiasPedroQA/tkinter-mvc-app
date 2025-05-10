import difflib
import getpass
from pathlib import Path
import platform
import re
from typing import Optional

from app.backend.modelos.objetos import ObjetoArquivo, ObjetoPasta, ResultadoAnalise


class GerenciadorArquivos:
    def __init__(self) -> None:
        self._sistema = platform.system().capitalize()
        self._usuario = getpass.getuser()
        self._base_usuario = self._detectar_sistema_servidor()

    @property
    def sistema(self) -> str:
        return self._sistema

    @property
    def usuario(self) -> str:
        return self._usuario

    @property
    def base_usuario(self) -> str:
        return self._base_usuario

    def _detectar_sistema_servidor(self) -> str:
        if self._sistema == "Windows":
            return f"C:\\Users\\{self._usuario}"
        if self._sistema == "Darwin":
            return f"/Users/{self._usuario}"
        if self._sistema == "Linux":
            return f"/home/{self._usuario}"
        raise ValueError(f"Sistema operacional desconhecido: '{self._sistema}'")

    def _normalizar_caminho(self, caminho_bruto: str) -> Path:
        caminho_normal = caminho_bruto.strip()
        caminho_normal = re.sub(r"[\\]+", "/", caminho_normal)
        caminho_normal = re.sub(r"\s*/\s*", "/", caminho_normal)
        caminho_normal = re.sub(r"/{2,}", "/", caminho_normal)
        caminho_normal = re.sub(r"[<>:\"|?*]", "", caminho_normal)
        while caminho_normal.startswith("../"):
            caminho_normal = caminho_normal[3:]
        return Path(caminho_normal)

    def _tentar_corrigir_caminho(self, caminho_com_erro: Path) -> Optional[Path]:
        partes = caminho_com_erro.parts
        caminho_atual = [Path(partes[0]) if caminho_com_erro.is_absolute() else Path()]
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

    def server_analisar_caminhos(
        self, caminho_entrada: str, extensao_arquivo: str = ""
    ) -> ResultadoAnalise:
        resultado = ResultadoAnalise()
        caminho_normalizado = self._normalizar_caminho(caminho_entrada)
        if not caminho_normalizado.is_absolute():
            caminho_normalizado = (Path(self.base_usuario) / caminho_normalizado).resolve()
            resultado.tipo_caminho = "absoluto_convertido"
        else:
            caminho_normalizado = caminho_normalizado.resolve()
            resultado.tipo_caminho = "absoluto_natural"

        resultado.caminho_tratado = str(caminho_normalizado)

        if caminho_normalizado.exists():
            resultado.sucesso = True
            if caminho_normalizado.is_dir():
                resultado.mensagem = "Pasta identificada com sucesso."
                resultado.objetos_coletados = ObjetoPasta(
                    subitens=[
                        p.name
                        for p in caminho_normalizado.iterdir()
                        if p.is_file() and p.suffix == extensao_arquivo
                    ],
                    caminho_pasta=str(caminho_normalizado),
                )
            elif caminho_normalizado.is_file():
                resultado.mensagem = "Arquivo identificado com sucesso."
                resultado.objetos_coletados = ObjetoArquivo(
                    extensao_arquivo=caminho_normalizado.suffix,
                    tamanho_bytes=caminho_normalizado.stat().st_size,
                    ultima_modificacao=caminho_normalizado.stat().st_mtime,
                    caminho_arquivo=str(caminho_normalizado),
                )
            return resultado

        # Tentativa de corrigir caminho
        if caminho_corrigido := self._tentar_corrigir_caminho(caminho_normalizado):
            resultado.sucesso = True
            resultado.caminho_corrigido = str(caminho_corrigido)
            return resultado

        resultado.mensagem = "Caminho não encontrado ou não corrigido."
        return resultado
