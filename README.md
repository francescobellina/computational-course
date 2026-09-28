# Computational Course

cd ~/Desktop/computational-course
git add .
git commit -m "Aggiorna corso"
git push

# Computational Course

Repository per gli appunti, gli esercizi e le simulazioni del corso di **statistical mechanics e computational methods**, organizzata come **Jupyter Book** e pubblicata automaticamente con GitHub Pages.

🌐 **Book online:** https://francescobellina.github.io/computational-course/  
📦 **Repository:** https://github.com/francescobellina/computational-course

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
   - potenziali a coppie e many-body
   - packing fraction
   - potenziale Lennard-Jones
   - cutoff radius e dipendenza delle quantità fisiche dal cutoff
   - neighbor lists

4. **Scientific coding**
   - implementazione numerica degli algoritmi del corso
   - esempi in MATLAB
   - calcolo dell'energia di un cristallo
   - costruzione delle liste dei vicini

5. **Molecular Dynamics**
   - Verlet configurazionale e velocity Verlet
   - velocità iniziali e scelta del timestep
   - calcolo delle forze
   - codice Molecular Dynamics completo con Lennard-Jones
   - termostati e velocity rescaling
   - thermal cycles / simulated annealing
   - cenni ai codici linear-scaling
   - esercizio d'esame 1/3

6. **Kinetic Monte Carlo**
   - problema delle scale temporali
   - transition state theory
   - first-escape times
   - catene di Markov, Master equation e detailed balance
   - algoritmo Bortz-Kalos-Lebowitz
   - simulazione della crescita cristallina
   - esercizio d'esame 2/3

7. **Metropolis Monte Carlo**
   - importance sampling
   - proprietà di equilibrio
   - algoritmo Metropolis
   - implementazione di un codice Monte Carlo
   - esercizio d'esame 3/3

## Struttura del repository

```text
computational-course/
├── book/                     # teoria e capitoli del Jupyter Book
├── notebooks/                # simulazioni ed esperimenti numerici
├── src/
│   └── computational_course/ # codice Python riutilizzabile
├── data/
│   ├── raw/                  # dati originali
│   └── processed/            # dati elaborati
├── figures/                  # figure da conservare nel repository
├── tests/                    # test del codice Python
├── myst.yml                  # indice e configurazione del Jupyter Book
└── pyproject.toml            # ambiente Python e dipendenze
```

Una possibile organizzazione dei capitoli è:

```text
book/
├── 01_statistical_mechanics/
├── 02_adiabatic_approximation/
├── 03_interatomic_potentials/
├── 04_scientific_coding/
├── 05_molecular_dynamics/
├── 06_kinetic_monte_carlo/
└── 07_metropolis_monte_carlo/
```

Lo stesso numero può essere usato in `notebooks/` per tenere teoria ed esperimenti facilmente associabili.

## Dove mettere cosa

- **`book/`** → teoria, formule, derivazioni, spiegazioni, risultati e discussioni.
- **`notebooks/`** → simulazioni, grafici, prove numeriche ed esperimenti.
- **`src/computational_course/`** → funzioni e algoritmi Python riutilizzabili.
- **`data/raw/`** → dati originali, da non modificare.
- **`data/processed/`** → dati ottenuti elaborando quelli raw.
- **`figures/`** → immagini o grafici da conservare.
- **`tests/`** → test automatici del codice Python.

Per il codice MATLAB del corso si può aggiungere:

```text
matlab/
```

con file `.m` organizzati per argomento.

## Aggiungere un nuovo capitolo

Esempio: **Molecular Dynamics**.

Crea:

```text
book/05_molecular_dynamics/
└── intro.md
```

Poi aggiungi la pagina al `project.toc` di `myst.yml`:

```yaml
- title: Molecular Dynamics
  children:
    - file: book/05_molecular_dynamics/intro.md
```

## Aggiungere un notebook

Crea il notebook nella cartella dello stesso argomento:

```text
notebooks/05_molecular_dynamics/
└── verlet.ipynb
```

Se vuoi che compaia anche nel sito, aggiungilo a `myst.yml`:

```yaml
- title: Molecular Dynamics
  children:
    - file: book/05_molecular_dynamics/intro.md
    - file: notebooks/05_molecular_dynamics/verlet.ipynb
```

Nel notebook puoi importare il codice riutilizzabile, ad esempio:

```python
from computational_course.qualcosa import funzione
```

## Aggiungere dati

Metti i dati originali in:

```text
data/raw/
```

e i dati generati o ripuliti in:

```text
data/processed/
```

Evita di caricare direttamente su Git file molto grandi; per dataset pesanti usa storage esterno o Git LFS.

## Lavorare sul progetto

Per vedere il Book in locale:

```bash
uv run jupyter book start --execute
```

Per pubblicare le modifiche:

```bash
git add .
git commit -m "Aggiorna corso"
git push
```

Il `push` su `main` avvia GitHub Actions e aggiorna automaticamente il sito su GitHub Pages.
