# Codice PRONTO DA COPIARE: py3Dmol per Jupyter Book

## Situazione Attuale

- ✅ `py3dmol>=2.5.5` è già in `pyproject.toml`
- ✅ Le funzioni `create_py3dmol_view()` e `create_py3dmol_view_with_highlight()` sono già in `ovito_visualization.py`
- ✅ L'esportazione XYZ è già implementata in `convert_to_xyz()`

**Cosa fare:** Aggiungere celle ai tuoi notebook per esportare i risultati OVITO e visualizzarli in Jupyter Book.

---

## 1. MODULO PYTHON PER L'ESPORTAZIONE (GIÀ PRESENTE)

Le funzioni sono già in `/src/computational_course/ovito_visualization.py`. Niente da aggiungere.

**Funzioni disponibili:**

```python
# Visualizzazione semplice
create_py3dmol_view(
    xyz_path: Path,
    width: int = 600,
    height: int = 400,
    style: str = "cartoon",  # "cartoon", "sphere", "stick"
    colorscheme: str = "Jmol"
)

# Visualizzazione con highlight (come OVITO)
create_py3dmol_view_with_highlight(
    xyz_path: Path,
    neighbor_indices: np.ndarray | None = None,
    reference_index: int | None = None,
    width: int = 600,
    height: int = 400
)
```

---

## 2. MODIFICHE AL NOTEBOOK: Celle da Aggiungere

### Cella A: Importazione (dopo la cella di import standard)

```python
# Visualizzazione interattiva per Jupyter Book
from src.computational_course.ovito_visualization import (
    create_py3dmol_view,
    create_py3dmol_view_with_highlight
)
```

### Cella B: Dopo l'analisi OVITO (esportazione semplice)

Aggiungi questa cella DOPO aver calcolato i risultati OVITO:

```python
# Esportare la visualizzazione semplice per il book
viewer_simple = create_py3dmol_view(
    xyz_path,
    width=700,
    height=500,
    style="sphere",
    colorscheme="Jmol"
)
viewer_simple._make_html()  # Renderizza nel notebook e nel book
```

### Cella C: Dopo l'analisi OVITO (esportazione con highlight)

Se hai i risultati dell'analisi geometrica (neighbor_indices, reference_index):

```python
# Esportare la visualizzazione con highlight per il book
results = compute_neighbor_distances(
    coords=coords,
    reference_atom=1,  # Indice human-readable (1-based)
    r_min=2.0,
    r_max=3.0
)

viewer_highlight = create_py3dmol_view_with_highlight(
    xyz_path,
    neighbor_indices=results["neighbor_indices"],
    reference_index=0,  # Indice 0-based per la reference
    width=700,
    height=500
)
viewer_highlight._make_html()  # Renderizza nel notebook e nel book
```

### Cella D: Visualizzazione multipla (facoltativa)

```python
# Confronto: tre stili diversi
from IPython.display import HTML

viewers = {
    "Sphere": create_py3dmol_view(xyz_path, style="sphere"),
    "Stick": create_py3dmol_view(xyz_path, style="stick"),
    "Highlight": create_py3dmol_view_with_highlight(
        xyz_path,
        neighbor_indices=results["neighbor_indices"],
        reference_index=0
    )
}

# Renderizza tutti
for name, viewer in viewers.items():
    print(f"\n=== {name} ===")
    viewer._make_html()
```

---

## 3. TEMPLATE MARKDOWN PER IL BOOK

### Opzione A: File `.md` nel book

Se usi un file `.md` nel book (es. `book/03_visualizations.md`):

```markdown
# Visualizzazioni 3D Interattive

Questo capitolo mostra le strutture atomiche analizzate con OVITO,
visualizzate in modo interattivo usando py3Dmol.

## Struttura FCC - Visualizzazione Semplice

Puoi ruotare, zoommare e pannare con il mouse:

```{code-cell} ipynb
:tags: [remove-input]

from pathlib import Path
from src.computational_course.ovito_visualization import create_py3dmol_view

xyz_path = Path("generated/fcc100a864.xyz")
viewer = create_py3dmol_view(xyz_path, width=700, height=500, style="sphere")
viewer._make_html()
```

## Struttura FCC - Con Highlight dei Vicini

Giallo: atomo di riferimento | Rosso: vicini nel primo guscio | Grigio: sfondo

```{code-cell} ipynb
:tags: [remove-input]

from pathlib import Path
import numpy as np
from src.computational_course.ovito_visualization import (
    create_py3dmol_view_with_highlight,
    compute_neighbor_distances,
    load_structure,
    convert_to_xyz
)

# Carica dati
txt_path, coords = load_structure("fcc100a864.txt")
xyz_path = convert_to_xyz(coords, "fcc100a864")

# Analizza
results = compute_neighbor_distances(coords, reference_atom=1, r_min=2.0, r_max=3.0)

# Visualizza
viewer = create_py3dmol_view_with_highlight(
    xyz_path,
    neighbor_indices=results["neighbor_indices"],
    reference_index=0,
    width=700,
    height=500
)
viewer._make_html()
```

**Analisi:**
- Numero di vicini: {results['coordination_number']}
- d_nn: {results['d_nn']:.4f} Å
- a_fcc: {results['a_fcc']:.4f} Å
- Ambiente: {results['environment']}
```

### Opzione B: Integrare direttamente nel notebook esistente

Se il tuo book include il notebook `04_handson_Ag_cutoff.ipynb`, aggiungi le celle B, C, D come descritto sopra.

---

## 4. WORKFLOW COMPLETO: Passo a Passo

### Fase 1: Preparazione locale (nel tuo ambiente)

1. Apri il notebook `/notebooks/04_handson_Ag_cutoff/analysis.ipynb`
2. Aggiungi le **Celle A, B, C** come descritto
3. Verifica che le visualizzazioni py3dmol funzionino in locale:
   ```bash
   jupyter notebook /Users/francesco/Desktop/computational-course/notebooks/04_handson_Ag_cutoff/analysis.ipynb
   ```

### Fase 2: Build del book

```bash
# Dalla root del progetto
jupyter-book build book/
```

Controlla l'output in `book/_build/html/` — i viewer py3dmol renderizzeranno come HTML interattivo.

### Fase 3: Deploy

Il book con i viewer interattivi è pronto per l'hosting:
- GitHub Pages: Push `book/_build/html/` su `gh-pages` branch
- Netlify: Connetti il repo e deploya `book/_build/html/`
- Vercel: Come Netlify

---

## 5. DIPENDENZE IN `pyproject.toml`

**Già presente** (niente da aggiungere):

```toml
dependencies = [
    "ipykernel>=7.3.0",
    "ipywidgets>=8.1.9",
    "ovito>=3.16.1.post1",
    "py3dmol>=2.5.5",  # ← py3Dmol incluso
]
```

Se necessario (per il book):
```toml
dev = [
    # ... altri package ...
    "jupyter-book==2.1.7",  # ← Già presente
]
```

---

## 6. TROUBLESHOOTING

### Il viewer non appare nel notebook locale
**Soluzione:**
```python
# Aggiungi questa riga PRIMA della cella con py3dmol:
import py3Dmol
print(f"py3Dmol version: {py3Dmol.__version__}")
```

Se py3Dmol non è installato:
```bash
pip install py3dmol>=2.5.5
```

### Il viewer non appare nel book pubblicato
**Soluzione:**
1. Verifica che le celle abbiano il tag `remove-input` se vuoi nascondere il codice
2. Verifica che `_make_html()` sia chiamato (non solo il `view` creato)
3. Controlla che i file XYZ siano nel path corretto

### Errore "File not found" per XYZ
**Soluzione:**
```python
# Usa path assoluto:
from pathlib import Path
xyz_path = Path("/Users/francesco/Desktop/computational-course/generated/fcc100a864.xyz")

# Oppure relativo dalla root del progetto:
from src.computational_course.ovito_visualization import find_project_root
root = find_project_root()
xyz_path = root / "generated" / "fcc100a864.xyz"
```

---

## 7. ESEMPIO COMPLETO: Notebook Minimo

```python
# ==== CELLA 1: Import ====
import numpy as np
from pathlib import Path
from src.computational_course.ovito_visualization import (
    find_project_root,
    load_structure,
    convert_to_xyz,
    compute_neighbor_distances,
    create_py3dmol_view,
    create_py3dmol_view_with_highlight,
)

# ==== CELLA 2: Carica e analizza ====
root = find_project_root()
txt_path, coords = load_structure("fcc100a864.txt", project_root=root)
xyz_path = convert_to_xyz(coords, "fcc100a864_export")
results = compute_neighbor_distances(coords, reference_atom=1, r_min=2.0, r_max=3.0)

print(f"Atomi: {len(coords)}")
print(f"Vicini: {results['coordination_number']}")
print(f"d_nn: {results['d_nn']:.4f} Å")

# ==== CELLA 3: Visualizza semplice ====
viewer_simple = create_py3dmol_view(xyz_path, width=700, height=500)
viewer_simple._make_html()

# ==== CELLA 4: Visualizza con highlight ====
viewer_hl = create_py3dmol_view_with_highlight(
    xyz_path,
    neighbor_indices=results["neighbor_indices"],
    reference_index=0,
    width=700,
    height=500
)
viewer_hl._make_html()
```

---

## 8. PROSSIMI PASSI

1. **Copia le Celle A-D** nel tuo notebook
2. **Verifica localmente** che i viewer appaiano
3. **Aggiungi il notebook al book** (o crea una nuova pagina `.md`)
4. **Build il book**: `jupyter-book build book/`
5. **Verifica l'HTML**: Apri `book/_build/html/` nel browser
6. **Deploy**: Push su GitHub, Netlify, o Vercel

Il viewer py3dmol sarà **completamente interattivo** nel browser, accessibile a tutti coloro che visiteranno il tuo book!

---

**Note finali:**
- py3Dmol non richiede installazioni aggiuntive nel server (è JavaScript puro)
- OVITO rimane solo per l'analisi locale (non serve sul server)
- XYZ è il formato universale per strutture atomiche
- Il viewer si sincronizza automaticamente tra notebook e book
