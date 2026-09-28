# Computational Course

Repository per seguire un corso computazionale/numerico con **Jupyter Book 2**, notebook
Jupyter, codice Python riutilizzabile, test automatici, VS Code, Git e pubblicazione
automatica su GitHub Pages.

Repository prevista: `francescobellina/computational-course`  
URL Pages atteso dopo il deployment: `https://francescobellina.github.io/computational-course/`

> Jupyter Book 2 usa `myst.yml`. I vecchi file `_config.yml` e `_toc.yml` appartengono al
> workflow Jupyter Book 1 e non vengono usati qui.

## Struttura

```text
computational-course/
├── README.md
├── LICENSE
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock                 # generato dal primo `uv sync` e poi versionato
├── myst.yml
├── .vscode/
│   ├── settings.json
│   └── extensions.json
├── book/
│   ├── intro.md
│   ├── 01_workflow.md
│   ├── 02_root_finding/
│   │   └── newton.md
│   └── references.bib
├── notebooks/
│   └── 02_root_finding/
│       └── newton_experiment.ipynb
├── src/
│   └── computational_course/
│       ├── __init__.py
│       └── root_finding.py
├── tests/
│   └── test_root_finding.py
├── data/
│   ├── raw/
│   └── processed/
├── figures/
├── scripts/
│   └── check_project.py
└── .github/
    └── workflows/
        └── pages.yml
```

## Perché questa separazione

- **`book/`**: teoria, formule LaTeX, appunti, interpretazioni, risultati, esercizi.
- **`notebooks/`**: esperimenti, simulazioni, grafici, analisi numeriche ed esplorazione.
- **`src/computational_course/`**: algoritmi, funzioni e classi riutilizzabili.
- **`tests/`**: controlli automatici sul codice del package.

`uv sync` installa il package in modalità progetto dentro `.venv`, quindi notebook e test
possono importare direttamente:

```python
from computational_course.root_finding import newton
```

senza modificare `sys.path`.

---

# Setup from scratch

## 1. Prerequisiti

Installa:

1. Git
2. VS Code
3. `uv` (gestisce Python, `.venv`, dipendenze e lockfile)
4. un account GitHub

Python 3.12.14 viene installato da `uv`, quindi non serve installarlo separatamente se usi
il workflow qui sotto.

### macOS / Linux: installare uv

```bash
curl -LsSf https://astral.sh/uv/0.12.19/install.sh | sh
uv --version
```

### Windows PowerShell: installare uv

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.12.19/install.ps1 | iex"
uv --version
```

Se il comando `uv` non viene trovato subito, chiudi e riapri il terminale.

## 2. Entrare nel progetto e creare l'ambiente

Da questa cartella:

```bash
uv python install 3.12.14
uv sync
```

Questo crea `.venv/`, risolve le dipendenze esattamente pinnate in `pyproject.toml` e genera `uv.lock`. **Non ignorare `uv.lock`**: al momento dell'inizializzazione Git verrà incluso dal normale `git add .` e dovrà essere presente già nel primo push. Dalle esecuzioni successive puoi usare `uv sync --locked` per chiedere a `uv` di fallire se `pyproject.toml` e lockfile non sono coerenti.

### Attivazione manuale opzionale

Con `uv run ...` non è necessario attivare la virtualenv. Se però vuoi entrare esplicitamente nell'ambiente:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

Per uscire, su entrambi:

```text
deactivate
```

## 3. Aprire in VS Code

```bash
code .
```

Installa le estensioni raccomandate quando VS Code lo propone:

- Python — `ms-python.python`
- Pylance — `ms-python.vscode-pylance`
- Jupyter — `ms-toolsai.jupyter`
- Ruff — `charliermarsh.ruff`

Poi esegui **Python: Select Interpreter** e scegli `.venv` se non è già selezionato.

## 4. Test Python e package

```bash
uv run python scripts/check_project.py
uv run pytest
```

## 5. Test Jupyter

Verifica i kernel disponibili:

```bash
uv run jupyter kernelspec list
```

Apri `notebooks/02_root_finding/newton_experiment.ipynb` in VS Code e seleziona il kernel
Python della `.venv`.

## 6. Preview locale del Jupyter Book

```bash
uv run jupyter book start --execute
```

Il server usa normalmente:

```text
http://localhost:3000
```

Se la porta 3000 è occupata, il terminale mostra la porta alternativa scelta. Salva un file
Markdown o notebook e il sito viene ricostruito. Ferma il server con `Ctrl+C`.

## 7. Build statica locale

```bash
uv run jupyter book build --html --execute --strict
```

L'HTML statico viene scritto in:

```text
_build/html/
```

## 8. Inizializzare Git

Se questa cartella non è ancora un repository:

```bash
git init -b main
git status
git add .
git commit -m "Initial computational course setup"
```

## 9. Creare la repository GitHub

Nel browser:

1. apri GitHub;
2. crea una nuova repository sotto l'account `francescobellina`;
3. nome: `computational-course`;
4. scegli Public o Private in base alle tue esigenze;
5. **non** aggiungere README, `.gitignore` o licenza dal sito, perché sono già locali.

Dopo la creazione, collega il remote:

```bash
git remote add origin https://github.com/francescobellina/computational-course.git
git remote -v
git push -u origin main
```

In alternativa, se hai già GitHub CLI installato e autenticato:

```bash
gh auth login
gh repo create francescobellina/computational-course --public --source=. --remote=origin --push
```

Non inserire token nel repository e non salvarli in file versionati.

## 10. Configurare GitHub Pages

Dopo il primo push:

1. repository GitHub → **Settings**;
2. **Pages**;
3. in **Build and deployment**, imposta **Source = GitHub Actions**;
4. non scegliere branch/directory per il contenuto pubblicato: il workflow carica direttamente
   l'artifact `_build/html` con le Actions ufficiali di Pages.

Il workflow `.github/workflows/pages.yml` parte a ogni push su `main` e:

1. fa checkout;
2. installa `uv` e Python 3.12.14;
3. ricrea l'ambiente dal lockfile con `uv sync --locked`;
4. esegue `pytest`;
5. costruisce il Book con notebook rieseguiti e modalità strict;
6. carica `_build/html` come artifact Pages;
7. lo pubblica nell'environment `github-pages`.

Per un project site GitHub Pages, `BASE_URL` deve includere il nome repository. Il workflow
usa automaticamente:

```yaml
BASE_URL: /${{ github.event.repository.name }}
```

Con il nome scelto, l'URL atteso è:

```text
https://francescobellina.github.io/computational-course/
```

Controlla **Actions → Build and deploy Jupyter Book** per log ed errori. A deployment
completato, GitHub mostra anche l'URL nella pagina del job `deploy` e in **Settings → Pages**.

---

# Workflow quotidiano

Da terminale nella root:

```bash
# verifica/sincronizza l'ambiente dal lockfile
uv sync --locked

# test
uv run pytest

# preview locale con notebook rieseguiti
uv run jupyter book start --execute
```

Dopo le modifiche:

```bash
git status
git add book notebooks src tests myst.yml
git commit -m "Add notes and numerical experiment"
git push
```

Il push su `main` attiva GitHub Actions e aggiorna GitHub Pages se test e build passano.

---

# Aggiungere un nuovo argomento: esempio 03_ode

Una struttura coerente è:

```text
book/03_ode/
└── intro.md
notebooks/03_ode/
└── euler_experiment.ipynb
src/computational_course/
└── ode.py
figures/03_ode/
└── ...
tests/
└── test_ode.py
```

Aggiungi le pagine a `project.toc` in `myst.yml`:

```yaml
- title: Equazioni differenziali ordinarie
  children:
    - file: book/03_ode/intro.md
    - file: notebooks/03_ode/euler_experiment.ipynb
```

Poi:

```bash
uv run pytest
uv run jupyter book start --execute
```

---

# Git e notebook

I file `.ipynb` **vanno versionati** quando costituiscono materiale didattico o esperimenti
riproducibili del corso: contengono celle, metadati e — se salvati — output. Evita però
output enormi e dati incorporati inutilmente. Le directory `.ipynb_checkpoints/` sono ignorate.

Per dataset grandi:

- non committare file pesanti in `data/raw/` (la cartella li ignora di default);
- usa una fonte esterna o un archivio dati con versione;
- usa Git LFS solo se hai davvero bisogno di versionare file binari grandi nel repository.

---

# Troubleshooting

| Problema | Soluzione concreta |
|---|---|
| `python` / `python3` non trovato | usa `uv run python ...`; se necessario `uv python install 3.12.14` |
| `pip` non trovato | con questo progetto non serve invocarlo direttamente; usa `uv sync` |
| `.venv` non esiste | `uv sync` |
| VS Code usa l'interprete sbagliato | Command Palette → `Python: Select Interpreter` → `.venv` |
| Jupyter non trova il kernel | `uv run jupyter kernelspec list`; riapri VS Code e seleziona il kernel `.venv` |
| notebook non eseguibile | verifica che `uv run python -c "import numpy"` funzioni e seleziona il kernel corretto |
| import del package fallisce | esegui `uv sync` dalla root; importa `computational_course`, non `src` |
| `jupyter book` non trovato | `uv sync`, poi `uv run jupyter book --version` |
| build fallisce | `uv run jupyter book build --html --execute --strict` e leggi il primo errore/warning |
| preview non parte sulla 3000 | usa l'URL/porta stampata dal terminale; la 3000 potrebbe essere occupata |
| immagini mancanti | usa percorsi relativi al file Markdown e versiona le immagini necessarie |
| formule LaTeX non renderizzate | usa sintassi MyST/Markdown valida, ad es. `$$ ... $$` |
| notebook fallisce in CI | assicurati che tutte le dipendenze siano in `pyproject.toml` e aggiorna `uv.lock` |
| GitHub Actions fallisce | apri il run in **Actions**, espandi lo step rosso e riproduci localmente il comando |
| Pages mostra 404/asset rotti | Pages deve avere Source=`GitHub Actions`; verifica `BASE_URL` e il job `deploy` |
| dati raw troppo grandi | tienili fuori da Git o usa storage dedicato / Git LFS |

---

# Aggiornare le dipendenze

Modifica `pyproject.toml`, quindi:

```bash
uv lock --upgrade
uv sync --locked
uv run pytest
uv run jupyter book build --html --execute --strict
git add pyproject.toml uv.lock
git commit -m "Update dependencies"
```

---

# Cheat sheet

```bash
# ambiente (senza attivazione manuale)
uv sync --locked

# attivazione opzionale macOS/Linux
source .venv/bin/activate

# attivazione opzionale Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Python
uv run python

# Jupyter
uv run jupyter lab

# preview Jupyter Book
uv run jupyter book start --execute

# build Jupyter Book
uv run jupyter book build --html --execute --strict

# test
uv run pytest

# Git
git status
git add .
git commit -m "Messaggio"
git push
```
