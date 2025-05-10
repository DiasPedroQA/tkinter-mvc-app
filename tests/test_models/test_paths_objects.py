"""
Testes para o módulo paths_objects.
"""

from datetime import datetime, timedelta
from src.models.paths_objects import ObjetoArquivo, ObjetoPasta


def test_objeto_arquivo_formatacao_datas() -> None:
    """Testa a formatação de datas no ObjetoArquivo."""
    timestamp = datetime.now().timestamp()
    arquivo = ObjetoArquivo(
        ultima_modificacao=timestamp,
        data_acesso=timestamp,
        data_criacao=timestamp,
    )

    assert arquivo.ultima_modificacao_formatada == datetime.fromtimestamp(
        timestamp
    ).strftime("%Y-%m-%d %H:%M:%S")
    assert arquivo.data_acesso_formatada == datetime.fromtimestamp(timestamp).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    assert arquivo.data_criacao_formatada == datetime.fromtimestamp(timestamp).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def test_objeto_arquivo_tamanho_formatado() -> None:
    """Testa a formatação do tamanho do arquivo."""
    arquivo = ObjetoArquivo(tamanho_bytes=1048576)  # 1 MB
    assert arquivo.tamanho_formatado == "1.00 MB"

    arquivo.tamanho_bytes = 1024  # 1 KB
    assert arquivo.tamanho_formatado == "1.00 KB"

    arquivo.tamanho_bytes = 123  # Bytes
    assert arquivo.tamanho_formatado == "123.00 B"


def test_objeto_arquivo_eh_arquivo_grande() -> None:
    """Testa se o arquivo é considerado grande."""
    arquivo = ObjetoArquivo(tamanho_bytes=150 * 1024 * 1024)  # 150 MB
    assert arquivo.eh_arquivo_grande(limite_mb=100) is True

    arquivo.tamanho_bytes = 50 * 1024 * 1024  # 50 MB
    assert arquivo.eh_arquivo_grande(limite_mb=100) is False


def test_objeto_arquivo_eh_recente() -> None:
    """Testa se o arquivo foi modificado recentemente."""
    timestamp_recente = (datetime.now() - timedelta(days=3)).timestamp()
    timestamp_antigo = (datetime.now() - timedelta(days=10)).timestamp()

    arquivo = ObjetoArquivo(ultima_modificacao=timestamp_recente)
    assert arquivo.eh_recente(dias=7) is True

    arquivo.ultima_modificacao = timestamp_antigo
    assert arquivo.eh_recente(dias=7) is False


def test_objeto_pasta_quantidade_subitens() -> None:
    """Testa a contagem de subitens na pasta."""
    pasta = ObjetoPasta(subitens=["arquivo1.txt", "arquivo2.txt", "subpasta"])
    assert pasta.quantidade_subitens == 3

    pasta.subitens = []
    assert pasta.quantidade_subitens == 0


def test_objeto_pasta_tamanho_total_formatado() -> None:
    """Testa a formatação do tamanho total da pasta."""
    pasta = ObjetoPasta(tamanho_total_bytes=10485760)  # 10 MB
    assert pasta.tamanho_total_formatado == "10.00 MB"

    pasta.tamanho_total_bytes = 512  # Bytes
    assert pasta.tamanho_total_formatado == "512.00 B"


def test_objeto_pasta_esta_vazia() -> None:
    """Testa se a pasta está vazia."""
    pasta = ObjetoPasta(subitens=[])
    assert pasta.esta_vazia() is True

    pasta.subitens = ["arquivo1.txt"]
    assert pasta.esta_vazia() is False


def test_objeto_pasta_contem_arquivos_com_extensao() -> None:
    """Testa se a pasta contém arquivos com uma extensão específica."""
    pasta = ObjetoPasta(
        subitens=["arquivo1.txt", "arquivo2.csv", "arquivo3.txt", "subpasta"]
    )
    arquivos_txt = pasta.contem_arquivos_com_extensao(".txt")
    assert arquivos_txt == ["arquivo1.txt", "arquivo3.txt"]

    arquivos_csv = pasta.contem_arquivos_com_extensao(".csv")
    assert arquivos_csv == ["arquivo2.csv"]

    arquivos_png = pasta.contem_arquivos_com_extensao(".png")
    assert arquivos_png == []
