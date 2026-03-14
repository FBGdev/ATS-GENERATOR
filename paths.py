from __future__ import annotations

from pathlib import Path


REPO = Path(__file__).resolve().parent
CAMINHO_TEMPLATE = REPO / "templates" / "curriculo-ats.html"
CAMINHO_CSS = REPO / "templates" / "estilos.css"
CAMINHO_DADOS = REPO / "data" / "curriculo.exemplo.json"
DIR_DIST = REPO / "dist"


def garantir_dist() -> Path:
  DIR_DIST.mkdir(parents=True, exist_ok=True)
  return DIR_DIST
