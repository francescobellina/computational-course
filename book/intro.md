# Computational Course

Questo Jupyter Book raccoglie teoria, formule, risultati e interpretazioni del corso.
Gli esperimenti rimangono nei notebook, mentre gli algoritmi riutilizzabili vivono nel
package Python `computational_course` sotto `src/`.

Il flusso di lavoro è:

```text
VS Code -> Markdown / Notebook / Python -> test -> preview locale -> Git -> GitHub Actions -> GitHub Pages
```

## Separazione delle responsabilità

- `book/`: narrazione didattica, teoria, formule, risultati e riferimenti.
- `notebooks/`: esperimenti, simulazioni, visualizzazioni e analisi esplorative.
- `src/computational_course/`: algoritmi e funzioni riutilizzabili.
- `tests/`: test automatici del codice Python.

Il capitolo sul [metodo di Newton](02_root_finding/newton.md) mostra il pattern completo.
