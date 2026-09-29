# Workflow del progetto

## Codice riutilizzabile

Il progetto è un vero package Python con layout `src`. Dopo `uv sync`, il package viene
installato nell'ambiente `.venv`, quindi notebook e test possono usare import normali:

```python
from computational_course.root_finding import newton
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

Per impostazione predefinita la preview viene servita su `http://localhost:3000`; se la
porta è occupata, Jupyter Book sceglie una porta libera e la stampa nel terminale.
Interrompi il server con `Ctrl+C`.


## SCHEMI 

```{figure} ../figures/schema1.png
:label: schema1
:width: 100%
:align: center

schema operativo
```

```{figure} ../figures/schema2.png
:label: schema2
:width: 100%
:align: center

schema operativo 2 (git/pull/push)  working in progress
```
