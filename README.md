# Computational Course

Appunti, laboratori ed esercizi d'esame del corso di **Computational Material Science**
(meccanica statistica, potenziali interatomici, dinamica molecolare, metodi Monte Carlo),
organizzati come **Jupyter Book** e pubblicati automaticamente con GitHub Pages.

🌐 **Book online:** https://francescobellina.github.io/computational-course/
📦 **Repository:** https://github.com/francescobellina/computational-course

Il programma del corso e la struttura del book sono nella pagina iniziale del book
(`book/intro.md`).

## Struttura

```text
computational-course/
├── book/                      # pagine del book (Markdown)
│   ├── intro.md, mappa_concetti.md
│   ├── teoria/                # Parte I: capitoli di teoria
│   ├── laboratori/            # Parte II: laboratori del corso (CMS 4, 5, 6)
│   ├── esame/                 # Parte III: esercizi d'esame e domande per l'orale
│   ├── appendici/             # workflow, approfondimenti, archivio
│   └── references.bib
├── notebooks/                 # notebook, con le stesse parti del book
│   ├── teoria/, laboratori/, esame/
│   └── archivio/              # versioni superate, conservate
├── src/computational_course/  # codice Python riutilizzabile
├── tests/                     # test del codice
├── data/raw/, data/processed/ # dati originali e dati elaborati
├── figures/                   # figure usate dal book
├── materials/                 # file del corso (poly7.py); i PDF restano solo in locale
├── docs/                      # note di lavoro e piano di riorganizzazione (fuori dal book)
├── myst.yml                   # indice e configurazione del book
└── pyproject.toml             # ambiente Python e dipendenze
```

## Comandi

```bash
uv sync                                    # ambiente e pacchetto (modalità editable)
uv run pytest                              # test
uv run ruff check src/ tests/              # controllo dello stile
uv run jupyter book start                  # anteprima locale del book
uv run jupyter book build --html --execute --strict   # build come in CI
```

## Dove mettere cosa

- **Teoria:** una pagina in `book/teoria/`, aggiunta all'indice in `myst.yml`.
- **Simulazioni:** un notebook in `notebooks/laboratori/` o `notebooks/esame/`; i notebook
  importano il codice da `computational_course` senza modificare `sys.path`.
- **Codice riutilizzabile:** un modulo in `src/computational_course/`, esportato in
  `__init__.py`, con i test in `tests/`.
- **Collegamenti tra pagine:** con le etichette (`[](#sec:md-pbc)`), che non si rompono se
  un file cambia cartella.

## Pubblicazione

Il `push` su `main` avvia GitHub Actions, che esegue i test, riesegue i notebook,
ricostruisce il book e lo pubblica su GitHub Pages. Il workflow completo è nell'appendice
del book «Workflow del repository».
