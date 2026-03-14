from __future__ import annotations

from pathlib import Path

from paths import DIR_DIST
from gerador_html import gerar_html


def gerar_pdf(html_path: Path | None = None, destino_pdf: Path | None = None):
  try:
    from playwright.sync_api import sync_playwright
  except ImportError:
    raise SystemExit("Instale o Playwright Python: pip install playwright && playwright install chromium")

  html_path = html_path or (DIR_DIST / "cv.html")
  destino_pdf = destino_pdf or (DIR_DIST / "cv.pdf")

  if not html_path.exists():
    html_path = gerar_html()

  with sync_playwright() as p:
    navegador = p.chromium.launch(
      headless=True,
      chromium_sandbox=False,
      args=["--no-sandbox", "--disable-setuid-sandbox"],
    )
    pagina = navegador.new_page()
    pagina.set_content(html_path.read_text(encoding="utf8"), wait_until="load")
    pagina.pdf(
      path=str(destino_pdf),
      format="A4",
      print_background=True,
      margin={"top": "0.5in", "right": "0.5in", "bottom": "0.5in", "left": "0.5in"},
    )
    navegador.close()
  return destino_pdf
