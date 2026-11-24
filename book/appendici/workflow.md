# Workflow del repository

## Codice riutilizzabile

Il progetto è un vero package Python con layout `src`. Dopo `uv sync`, il package viene
installato nell'ambiente `.venv`, quindi notebook e test possono usare import normali:

```python
from computational_course.md_p7 import lj_p7_model, run_nve
```

Non è necessario modificare `sys.path`.

## Notebook e Book

I notebook `.ipynb` possono comparire direttamente nel sommario di `myst.yml`. Per una
build riproducibile usa:

```bash
uv run jupyter book build --html --execute --strict
```

`--execute` riesegue il contenuto computazionale; `--strict` trasforma warning importanti
(inclusi riferimenti mancanti) in errori della build.

## Preview locale

```bash
uv run jupyter book start --execute
```


```bash
jupyter book start 
```

Per impostazione predefinita la preview viene servita su `http://localhost:3000`; se la
porta è occupata, Jupyter Book sceglie una porta libera e la stampa nel terminale.
Interrompi il server con `Ctrl+C`.


## Lo schema

```{figure} ../../figures/schema_workflow.jpg
:label: fig-workflow
:width: 100%
:align: center

Il workflow: si lavora in VS Code, si sincronizza con GitHub, GitHub Actions
ricostruisce il book e lo pubblica su GitHub Pages.
```
