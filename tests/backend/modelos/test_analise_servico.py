from app.backend.modelos.objetos import ObjetoArquivo, ObjetoPasta, ResultadoAnalise


def test_objeto_arquivo_defaults() -> None:
    obj = ObjetoArquivo()
    assert obj.tipo_item == "Arquivo"
    assert obj.extensao_arquivo == ""
    assert obj.tamanho_bytes == 0
    assert obj.ultima_modificacao == 0.0
    assert obj.caminho_arquivo == ""


def test_objeto_arquivo_ultima_modificacao_formatada() -> None:
    timestamp = 1672531200  # Corresponds to 2023-01-01 00:00:00
    obj = ObjetoArquivo(ultima_modificacao=timestamp)
    assert obj.ultima_modificacao_formatada == "2023-01-01 00:00:00"


def test_objeto_pasta_defaults() -> None:
    obj = ObjetoPasta()
    assert obj.tipo_item == "Pasta"
    assert obj.subitens is []
    assert obj.caminho_pasta == ""


def test_objeto_pasta_custom_values() -> None:
    obj = ObjetoPasta(subitens=["file1.txt", "file2.txt"], caminho_pasta="/test/path")
    assert obj.subitens == ["file1.txt", "file2.txt"]
    assert obj.caminho_pasta == "/test/path"


def test_resultado_analise_defaults() -> None:
    obj = ResultadoAnalise()
    assert obj.sucesso is False
    assert obj.mensagem == ""
    assert obj.caminho_tratado == ""
    assert obj.tipo_caminho == ""
    assert obj.objetos_coletados is None
    assert obj.caminho_corrigido is None


def test_resultado_analise_custom_values() -> None:
    arquivo = ObjetoArquivo(caminho_arquivo="/test/file.txt")
    obj = ResultadoAnalise(
        sucesso=True,
        mensagem="Analysis successful",
        caminho_tratado="/test",
        tipo_caminho="Arquivo",
        objetos_coletados=arquivo,
        caminho_corrigido="/corrected/path",
    )
    assert obj.sucesso is True
    assert obj.mensagem == "Analysis successful"
    assert obj.caminho_tratado == "/test"
    assert obj.tipo_caminho == "Arquivo"
    assert obj.objetos_coletados == arquivo
    assert obj.caminho_corrigido == "/corrected/path"
