# import json
# from dataclasses import asdict, dataclass
# from pathlib import Path


# @dataclass
# class CaminhoModel:
#     """Preencher depois"""
#     nome: str
#     tipo: str
#     caminho: str
#     existe: bool

#     @classmethod
#     def from_path(cls, caminho_str: str) -> "CaminhoModel":
#         caminho: Path = Path(caminho_str).expanduser().resolve()
#         tipo: str = (
#             "diretório"
#             if caminho.is_dir()
#             else "arquivo"
#             if caminho.is_file()
#             else "desconhecido"
#         )
#         return cls(
#             nome=caminho.name,
#             tipo=tipo,
#             caminho=str(caminho),
#             existe=caminho.exists(),
#         )

#     def to_json(self) -> str:
#         return json.dumps(asdict(self), ensure_ascii=False, indent=2)
