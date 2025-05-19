# pylint: disable=unknown-option-value, missing-module-docstring, missing-docstring-class, missing-function-docstring

import json
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path


# === MODEL ===
@dataclass
class CaminhoModel:
    """Modelo de dados para representar um caminho no sistema de arquivos."""

    nome: str
    tipo: str
    caminho: str
    existe: bool

    @classmethod
    def from_path(cls, caminho_str: str) -> "CaminhoModel":
        """Cria modelo a partir de um caminho do sistema de arquivos."""
        try:
            caminho = Path(caminho_str).expanduser().resolve()
            tipo = (
                "diretório"
                if caminho.is_dir()
                else "arquivo"
                if caminho.is_file()
                else "desconhecido"
            )
            return cls(
                nome=caminho.name,
                tipo=tipo,
                caminho=str(caminho),
                existe=caminho.exists(),
            )
        except ValueError:
            return cls(
                nome=Path(caminho_str).name,
                tipo="erro",
                caminho=caminho_str,
                existe=False,
            )

    def to_dict(self) -> dict[str, str | bool]:
        """Converte o modelo para dicionário."""
        return asdict(self)


# === TOOLS ===
def validar_caminho(caminho: str) -> bool:
    """Verifica se o caminho existe no sistema."""
    return Path(caminho).expanduser().resolve().exists()


def gerar_id_para_path(caminho: str) -> str:
    """Gera um UUID baseado no caminho."""
    return str(uuid.uuid5(namespace=uuid.NAMESPACE_URL, name=caminho))


def ler_conteudo(caminho: str) -> str:
    """Lê o conteúdo de um arquivo, se existir."""
    caminho_atual: Path = Path(caminho).expanduser().resolve()
    if caminho_atual.is_file():
        return caminho_atual.read_text(encoding="utf-8")
    return ""


def criar_novo_arquivo(caminho: str, conteudo: str) -> str:
    """Cria um novo arquivo com o conteúdo especificado."""
    caminho_atual: Path = Path(caminho).expanduser().resolve()
    caminho_atual.parent.mkdir(parents=True, exist_ok=True)
    caminho_atual.write_text(conteudo, encoding="utf-8")
    return str(caminho_atual)


def atualizar_arquivo(caminho: str, novo_conteudo: str) -> str:
    """Atualiza um arquivo existente com novo conteúdo."""
    caminho_atual: Path = Path(caminho).expanduser().resolve()
    if caminho_atual.is_file():
        caminho_atual.write_text(data=novo_conteudo, encoding="utf-8")
        return str(caminho_atual)
    raise FileNotFoundError(f"Caminho {caminho} não encontrado.")


# === CONTROLLER ===
class PathController:
    """Controlador principal de caminhos, responsável por ações CRUD e validação."""

    def __init__(self, caminhos: list[str]) -> None:
        self.caminhos: list[str] = caminhos

    def ler_caminhos(self) -> list[dict[str, str | bool]]:
        """Cria modelos para todos os caminhos, válidos ou não."""
        return [CaminhoModel.from_path(c).to_dict() for c in self.caminhos]

    def gerar_id(self, caminho: str) -> str:
        """Retorna o ID gerado para um caminho."""
        return gerar_id_para_path(caminho=caminho)

    def adicionar_caminho(self, caminho: str) -> None:
        """Adiciona um novo caminho à lista."""
        if caminho not in self.caminhos:
            self.caminhos.append(caminho)

    def remover_caminho(self, caminho: str) -> bool:
        """Remove um caminho da lista, se existir."""
        if caminho in self.caminhos:
            self.caminhos.remove(caminho)
            return True
        return False

    def listar_todos_os_caminhos(self) -> list[str]:
        """Retorna todos os caminhos armazenados (válidos ou não)."""
        return self.caminhos

    def caminhos_invalidos(self) -> list[str]:
        """Retorna os caminhos que não existem no sistema."""
        return [c for c in self.caminhos if not validar_caminho(c)]

    def obter_conteudo(self, caminho: str) -> str:
        """Obtém o conteúdo de um arquivo, se possível."""
        return ler_conteudo(caminho=caminho)

    def criar_arquivo(self, caminho: str, conteudo: str) -> str:
        """Cria um novo arquivo."""
        return criar_novo_arquivo(caminho=caminho, conteudo=conteudo)

    def atualizar_arquivo(self, caminho: str, conteudo: str) -> str:
        """Atualiza um arquivo existente."""
        return atualizar_arquivo(caminho=caminho, novo_conteudo=conteudo)


# === VIEW ===
class PathView:
    """Responsável por exibir os dados no terminal de forma legível."""

    @staticmethod
    def exibir_em_json(lista_modelos: list[dict[str, str | bool]]) -> None:
        """Exibe os dados convertidos em JSON."""
        print("\n🧾 Dados em JSON:")
        print(json.dumps(lista_modelos, ensure_ascii=False, indent=2))

    @staticmethod
    def exibir_em_tabela(lista_modelos: list[dict[str, str | bool]]) -> None:
        """Exibe os dados em formato de tabela no terminal."""
        if not lista_modelos:
            print("Nenhum caminho válido encontrado.")
            return

        colunas = list(lista_modelos[0].keys())
        larguras: dict[str, int] = {
            coluna: max(
                len(coluna), max(len(str(item[coluna])) for item in lista_modelos)
            )
            for coluna in colunas
        }

        def formatar_linha(valores: list[str]) -> str:
            return " | ".join(f"{v:<{larguras[c]}}" for v, c in zip(valores, colunas))

        separador: str = "-+-".join("-" * larguras[c] for c in colunas)

        print("\n📁 Tabela de Caminhos:\n")
        print(formatar_linha(valores=colunas))
        print(separador)

        for item in lista_modelos:
            valores: list[str] = [str(item[c]) for c in colunas]
            print(formatar_linha(valores=valores))
        print()


# === MAIN ===
def main() -> None:
    caminhos: list[str] = [
        "~/Documentos",
        "~/Downloads/Firefox/bookmarks.html",
        "~/Downloads/Firefox/",
        "~/Downloads/Firefox/nao_existe",
    ]

    controller = PathController(caminhos=caminhos)

    # Teste de leitura geral
    resultados = controller.ler_caminhos()

    # Teste de ID
    print("\n🆔 Exemplo de ID gerado:")
    print(controller.gerar_id(caminhos[0]))

    # Teste de caminhos inválidos
    print("\n❌ Caminhos inválidos:")
    for invalido in controller.caminhos_invalidos():
        print(f"- {invalido}")

    # Teste de listagem
    print("\n📄 Caminhos registrados:")
    for c in controller.listar_todos_os_caminhos():
        print(f"- {c}")

    # Adicionando novo caminho
    controller.adicionar_caminho("~/NovoDiretorioDeTeste")
    print("\n➕ Novo caminho adicionado:")
    print(controller.listar_todos_os_caminhos()[-1])

    # Exibição dos resultados
    view = PathView()
    view.exibir_em_tabela(lista_modelos=resultados)
    view.exibir_em_json(lista_modelos=resultados)


if __name__ == "__main__":
    main()
