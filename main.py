from __future__ import annotations

import argparse

from gerador_html import gerar_html
from pdf import gerar_pdf


def main():
  parser = argparse.ArgumentParser(description="Gerador de currículo ATS em Python")
  parser.add_argument("--pdf", action="store_true", help="Também gerar dist/cv.pdf")
  args = parser.parse_args()

  html_path = gerar_html()
  print(f"Gerado HTML: {html_path}")

  if args.pdf:
    pdf_path = gerar_pdf(html_path=html_path)
    print(f"Gerado PDF: {pdf_path}")


if __name__ == "__main__":
  main()
