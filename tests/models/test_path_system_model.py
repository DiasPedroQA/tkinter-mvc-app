# pylint: disable=missing-function-docstring, missing-module-docstring, useless-suppression, use-set-for-membership

from pathlib import Path

import pytest

from models.path_system_model import CaminhoModel
from tools.path_definitions import PathData, PathStatus, PathType

# Caminhos de teste (modifique conforme necessário para o seu ambiente)
CAMINHOS_TESTE = [
    ("~/Downloads/Firefox", PathType.DIRECTORY, True, PathStatus.EXISTS),
    ("~/Downloads/Firefox/bookmarks.html", PathType.FILE, True, PathStatus.EXISTS),
    (
        "~/Downloads/Firefox/bookmark.html",
        PathType.UNKNOWN,
        False,
        PathStatus.NOT_EXISTS,
    ),
    ("~/Downloads/Chromium", PathType.UNKNOWN, False, PathStatus.NOT_EXISTS),
]


@pytest.mark.parametrize(
    "entrada,tipo_esperado,status_esperado", CAMINHOS_TESTE
)
def test_caminho_model_basico(
    entrada: str, tipo_esperado: str, status_esperado: str
) -> None:
    model = CaminhoModel.from_path(entrada)

    assert isinstance(model, CaminhoModel)
    assert model.nome == Path(entrada).expanduser().name
    assert model.tipo == tipo_esperado
    assert model.status == status_esperado
    assert isinstance(model.caminho, str)


def test_to_dict() -> None:
    model = CaminhoModel(
        nome="exemplo.txt",
        tipo=PathType.FILE,
        caminho="/caminho/fake/exemplo.txt",
        status=PathStatus.EXISTS,
    )

    resultado = model.to_dict()
    assert resultado == {
        "nome": "exemplo.txt",
        "tipo": "File",
        "caminho": "/caminho/fake/exemplo.txt",
        "status": "existe",
    }


def test_to_pathdata() -> None:
    model = CaminhoModel(
        nome="arquivo",
        tipo=PathType.FILE,
        caminho="/tmp/arquivo",
        status=PathStatus.EXISTS,
    )

    pathdata = model.to_pathdata()
    assert isinstance(pathdata, PathData)
    assert pathdata.nome == "arquivo"
    assert pathdata.tipo == PathType.FILE
    assert pathdata.caminho == "/tmp/arquivo"
    assert pathdata.status == PathStatus.EXISTS


def test_str_representation() -> None:
    model = CaminhoModel(
        nome="pasta",
        tipo=PathType.DIRECTORY,
        caminho="/tmp/pasta",
        status=PathStatus.NOT_EXISTS,
    )
    representacao = str(model)
    assert "DIRECTORY" in representacao
    assert "nao_existe" in representacao
