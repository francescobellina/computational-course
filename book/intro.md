# Computational Course

Questo Jupyter Book raccoglie teoria, formule, risultati e interpretazioni del corso.
Gli esperimenti rimangono nei notebook, mentre gli algoritmi riutilizzabili vivono nel
package Python `computational_course` sotto `src/`.

Il flusso di lavoro è:

```text
VS Code -> Markdown / Notebook / Python -> test -> preview locale -> Git -> GitHub Actions -> GitHub Pages
```

## Separazione 

- `book/`: narrazione didattica, teoria, formule, risultati e riferimenti.
- `notebooks/`: esperimenti, simulazioni, visualizzazioni e analisi esplorative.
- `src/computational_course/`: algoritmi e funzioni riutilizzabili.
- `tests/`: test automatici del codice Python.

Il capitolo sul [metodo di Newton](02_root_finding/newton.md) mostra il pattern completo.

## Programma del corso

Il materiale seguirà principalmente questi argomenti:

1. **Classical Statistical Mechanics**
   - ensemble canonico e microcanonico
   - medie temporali e microcanoniche
   - teorema ergodico
   - limite termodinamico ed equivalenza degli ensemble

2. **Adiabatic approximation e moto nucleare**
   - scale temporali elettroniche e nucleari
   - Hamiltoniana elettronica
   - approssimazione classica del moto dei nuclei
   - dinamica molecolare *ab initio* e classica

3. **Interatomic potentials**
   - numenclatura cristallina e simmetria
   - potenziali a coppie e many-body
   - packing fraction
   - potenziale Lennard-Jones
   - cutoff radius e dipendenza delle quantità fisiche dal cutoff
   - neighbor lists
---------------------------------------------------------------------------
1. **Scientific coding**
   - implementazione numerica degli algoritmi del corso
   - esempi in MATLAB(no matlab quest'anno)
   - calcolo dell'energia di un cristallo
   - costruzione delle liste dei vicini

2. **Molecular Dynamics**
   - Verlet configurazionale e velocity Verlet
   - velocità iniziali e scelta del timestep
   - calcolo delle forze
   - codice Molecular Dynamics completo con Lennard-Jones
   - termostati e velocity rescaling
   - thermal cycles / simulated annealing
   - cenni ai codici linear-scaling
   - esercizio d'esame 1/3

3. **Kinetic Monte Carlo**
   - problema delle scale temporali
   - transition state theory
   - first-escape times
   - catene di Markov, Master equation e detailed balance
   - algoritmo Bortz-Kalos-Lebowitz
   - simulazione della crescita cristallina
   - esercizio d'esame 2/3

4. **Metropolis Monte Carlo** (da discutersi durante esame)
   - importance sampling
   - proprietà di equilibrio
   - algoritmo Metropolis
   - implementazione di un codice Monte Carlo
   - esercizio d'esame 3/3
