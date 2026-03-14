from __future__ import annotations

import html
import json
from pathlib import Path

from paths import CAMINHO_CSS, CAMINHO_DADOS, CAMINHO_TEMPLATE, DIR_DIST, garantir_dist


def _escapar(texto: str) -> str:
    return html.escape(str(texto), quote=True)


def _ul(itens: list[str]) -> str:
    return (
        '<ul class="bullets">'
        + "".join(f"<li>{_escapar(i)}</li>" for i in itens)
        + "</ul>"
    )


def _comp_grupos(grupos: list[dict]) -> str:
    return "\n".join(
        f"<div class=\"item\"><div class=\"item-title\">{_escapar(g['grupo'])}:</div> {_escapar(', '.join(g['itens']))}</div>"
        for g in grupos
    )


def _projetos(projetos: list[dict]) -> str:
    blocos = []
    for p in projetos:
        links = "".join(
            f"<li>{_escapar(l['rotulo'])}: <a href=\"{l['url']}\" target=\"_blank\" rel=\"noopener noreferrer\">{_escapar(l['url'])}</a></li>"
            for l in p.get("links", [])
        )
        blocos.append(
            '\n<div class="item">'
            f"<div class=\"item-title\">{_escapar(p['titulo'])}</div>"
            f"<div class=\"tech-line\">Tecnologias: {_escapar(p['tecnologias'])}</div>"
            f"{_ul(p['pontos'])}"
            f"{'<ul class=\"bullets\">' + links + '</ul>' if links else ''}"
            "</div>"
        )
    return "\n".join(blocos)


def _experiencias(exps: list[dict]) -> str:
    blocos = []
    for e in exps:
        blocos.append(
            '\n<div class="item">'
            '<div class="item-header">'
            "<div>"
            f"<div class=\"item-title\">{_escapar(e['cargo'])}</div>"
            f"<div class=\"item-subtitle\">{_escapar(e['empresa'])}</div>"
            "</div>"
            f"<div class=\"item-date\">{_escapar(e['periodo'])}</div>"
            "</div>"
            f"{_ul(e['pontos'])}"
            "</div>"
        )
    return "\n".join(blocos)


def _formacoes(formacoes: list[dict]) -> str:
    blocos = []
    for f in formacoes:
        blocos.append(
            '\n<div class="item">'
            '<div class="item-header">'
            "<div>"
            f"<div class=\"item-title\">{_escapar(f['titulo'])}</div>"
            f"<div class=\"item-subtitle\">{_escapar(f['instituicao'])}</div>"
            "</div>"
            f"<div class=\"item-date\">{_escapar(f['periodo'])}</div>"
            "</div>"
            "</div>"
        )
    return "\n".join(blocos)


def _idiomas(idiomas: list[dict]) -> str:
    blocos = []
    for l in idiomas:
        blocos.append(
            '\n<div class="item">'
            '<div class="item-header">'
            f"<div class=\"item-title\">{_escapar(l['nome'])} — {_escapar(l['nivel'])}</div>"
            f"<div class=\"item-date\">{_escapar(l.get('observacao', ''))}</div>"
            "</div>"
            "</div>"
        )
    return "\n".join(blocos)


def _links_contato(dados: dict) -> str:
    links = [
        {"url": dados.get("linkedin_url"), "rotulo": "LinkedIn"},
        {"url": dados.get("github_url"), "rotulo": "GitHub"},
        {"url": dados.get("site_url"), "rotulo": "Portfólio"},
    ]
    ativos = [l for l in links if l["url"] and str(l["url"]).strip()]
    return " | ".join(
        f"{_escapar(l['rotulo'])}: <a href=\"{_escapar(l['url'])}\" target=\"_blank\" rel=\"noopener noreferrer\">"
        f"{_escapar(str(l['url']).removeprefix('https://').removeprefix('http://').rstrip('/'))}</a>"
        for l in ativos
    )


def _secao(titulo: str, conteudo: str) -> str:
    if not conteudo:
        return ""
    return f'<section class="section"><h2 class="section-title">{_escapar(titulo)}</h2>{conteudo}</section>'


def gerar_html(destino: Path | None = None) -> Path:
    garantir_dist()
    tpl = CAMINHO_TEMPLATE.read_text(encoding="utf8")
    css = CAMINHO_CSS.read_text(encoding="utf8")
    dados = json.loads(CAMINHO_DADOS.read_text(encoding="utf8"))

    html_out = (
        tpl.replace(
            '<link rel="stylesheet" href="./estilos.css" />', f"<style>{css}</style>"
        )
        .replace("{{NOME}}", _escapar(dados["nome"]))
        .replace("{{TITULO}}", _escapar(dados["titulo"]))
        .replace("{{EMAIL}}", _escapar(dados["email"]))
        .replace("{{TELEFONE_E164}}", _escapar(dados["telefone_e164"]))
        .replace("{{TELEFONE_EXIBICAO}}", _escapar(dados["telefone_exibicao"]))
        .replace("{{LOCALIZACAO}}", _escapar(dados["localizacao"]))
        .replace("{{LINKS_CONTATO_HTML}}", _links_contato(dados))
        .replace("{{RESUMO}}", _escapar(dados["resumo"]).replace("\n", "<br />"))
        .replace(
            "{{COMPETENCIAS_HTML}}",
            _comp_grupos(dados.get("competencias_tecnicas", [])),
        )
        .replace("{{PROJETOS_HTML}}", _projetos(dados.get("projetos", [])))
        .replace("{{IDIOMAS_HTML}}", _idiomas(dados.get("idiomas", [])))
        .replace(
            "{{SECAO_EXPERIENCIAS_HTML}}",
            _secao("Experiência", _experiencias(dados.get("experiencias", []))),
        )
        .replace("{{FORMACAO_HTML}}", _formacoes(dados.get("formacao", [])))
        .replace(
            "{{SECAO_CURSOS_HTML}}",
            _secao("Cursos Complementares", _formacoes(dados.get("cursos", []))),
        )
        .replace(
            "{{SECAO_FERRAMENTAS_HTML}}",
            _secao("Ferramentas", _ul(dados.get("ferramentas", []))),
        )
    )

    destino = destino or (DIR_DIST / "cv.html")
    destino.write_text(html_out, encoding="utf8")
    return destino
