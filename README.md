Currículo ATS em HTML
=====================

Gerador simples de currículo em HTML e PDF, totalmente em português e pensado para compatibilidade com sistemas de rastreamento de vagas (ATS). Agora apenas em Python.

Principais pontos
-----------------
- Dados ficam em `data/curriculo.exemplo.json`.
- Template único em `templates/curriculo-ats.html` com estilos em `templates/estilos.css`.
- Saída gerada em `dist/cv.html` e `dist/cv.pdf`.
- Dependência principal: Playwright Python.

Requisitos
----------
- Python 3.10+

Instalação
----------
```bash
pip install playwright
playwright install chromium
```

Como usar (Python)
------------------
1. Edite os dados em `data/curriculo.exemplo.json` (campos todos em português).
2. Gere o HTML:  
   ```bash
   python main.py
   ```
   O arquivo `dist/cv.html` será criado.
3. Exporte para PDF:  
   ```bash
   python main.py --pdf
   ```
   O arquivo `dist/cv.pdf` será criado com links clicáveis.

Campos do JSON
--------------
- Identificação: `nome`, `titulo`, `email`, `telefone_e164`, `telefone_exibicao`, `localizacao`.
- Links: `linkedin_url`, `github_url`, `site_url`.
- Seções:  
  - `resumo` (texto com quebras de linha opcionais)  
  - `competencias_tecnicas`: lista de grupos `{ grupo, itens[] }`  
  - `competencias_comportamentais`: lista simples de strings  
  - `diferenciais`: lista simples de strings  
  - `projetos`: `{ titulo, tecnologias, pontos[], links[{ rotulo, url }] }`  
  - `experiencias`: `{ cargo, empresa, periodo, pontos[] }`  
  - `formacao` e `cursos`: `{ titulo, instituicao, periodo }`  
  - `idiomas`: `{ nome, nivel, observacao }`

Estrutura do projeto
--------------------
- `data/` – JSON de exemplo e assets.
- `templates/` – HTML (`curriculo-ats.html`) e CSS (`estilos.css`).
- Arquivos Python na raiz: `paths.py`, `gerador_html.py`, `pdf.py`, `main.py`.
- `dist/` – Saída gerada (gitignored).

Personalização rápida
---------------------
- Cores e tipografia: edite `templates/estilos.css`.
- Layout/labels: ajuste `templates/curriculo-ats.html`.
- Formatação dos dados: adapte as funções em `gerador_html.py`.
