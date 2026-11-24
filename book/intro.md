:::{image} ../figures/hero.png
:class: intro-hero
:alt: Computational Material Science
:::

# Computational Material Science

Appunti, laboratori ed esercizi d'esame del corso di *Computational Material
Science*: meccanica statistica, potenziali interatomici, dinamica molecolare e
metodi Monte Carlo. La teoria sta nelle pagine del book, le simulazioni nei
notebook, il codice riutilizzabile nel pacchetto Python `computational_course`.

## Come è organizzato

| Parte | Contenuto |
|---|---|
| **[Mappa dei concetti](mappa_concetti.md)** | per ogni concetto, dove sono la teoria, la verifica numerica e la domanda d'orale |
| **Parte I — Teoria** | [meccanica statistica](teoria/01_meccanica_statistica.md), [approssimazione adiabatica e $T_f=T(0)/2$](teoria/02_approssimazione_adiabatica.md), [potenziali e cristalli](teoria/03_potenziali_e_cristalli.md), [dinamica molecolare](teoria/04_dinamica_molecolare.md), [simulazioni MD](teoria/05_simulazioni_md.md), [steepest descent](teoria/06_steepest_descent.md) |
| **Parte II — Laboratori del corso** | [CMS 4](laboratori/cms4_intro.md) (argento: coordinazione, cutoff e forze), [CMS 5](../notebooks/laboratori/cms5/equazioni_del_moto.ipynb) (equazioni del moto), [CMS 6](../notebooks/laboratori/cms6/esercizi_cms6.ipynb) (esercizi), [steepest descent](../notebooks/laboratori/steepest_descent.ipynb) |
| **Parte III — Esame** | [Esercizio 1](esame/esercizio1/consegna.md) (MD di LJ-Ag), [domande per l'orale](esame/orale_domande.md); esercizi 2 e 3 quando saranno assegnati |
| **Appendici** | [efficienza del codice](../notebooks/appendici/efficienza_codice.ipynb), [MD di proteine e HPC4AI](appendici/approfondimento_proteine_hpc4ai.md), [workflow del repository](appendici/workflow.md), [archivio](appendici/archivio_esercizio1_5_punti.md) |

## Programma del corso

1. **Meccanica statistica classica**
   - ensemble canonico e microcanonico
   - medie temporali e microcanoniche
   - teorema ergodico
   - limite termodinamico ed equivalenza degli ensemble
2. **Approssimazione adiabatica e moto dei nuclei**
   - scale temporali elettroniche e nucleari
   - Hamiltoniana elettronica
   - approssimazione classica del moto dei nuclei
   - dinamica molecolare *ab initio* e classica
3. **Potenziali interatomici**
   - nomenclatura cristallina e simmetria
   - potenziali a coppie e many-body
   - packing fraction
   - potenziale di Lennard-Jones
   - raggio di taglio e dipendenza delle grandezze fisiche dal taglio
   - liste dei vicini
4. **Scientific coding**
   - [implementazione numerica degli algoritmi del corso](../notebooks/laboratori/cms4/coordinazione_e_lennard_jones.ipynb)
   - [energia di un cristallo](../notebooks/laboratori/cms4/coordinazione_e_lennard_jones.ipynb#id-7-energia-di-lennard-jones-con-cutoff)
   - [liste dei vicini](../notebooks/laboratori/cms4/coordinazione_e_lennard_jones.ipynb#id-6-lista-dei-vicini-entro-il-cutoff)
   - esempi in MATLAB (quest'anno non in programma)
5. **Dinamica molecolare**
   - [teoria e algoritmo di Verlet](teoria/04_dinamica_molecolare.md)
   - [integrazione delle equazioni del moto](../notebooks/laboratori/cms5/equazioni_del_moto.ipynb)
   - Verlet configurazionale e velocity Verlet
   - velocità iniziali e scelta del passo temporale
   - calcolo delle forze
   - codice MD completo con Lennard-Jones
   - termostati e *velocity rescaling*
   - cicli termici e *simulated annealing*
   - cenni ai codici *linear-scaling*
   - [esercizio d'esame 1/3](esame/esercizio1/consegna.md)
6. **Monte Carlo cinetico**
   - problema delle scale temporali
   - teoria dello stato di transizione
   - tempi di prima fuga
   - catene di Markov, equazione maestra e bilancio dettagliato
   - algoritmo di Bortz-Kalos-Lebowitz
   - simulazione della crescita cristallina
   - esercizio d'esame 2/3
7. **Metropolis Monte Carlo** (da discutere durante l'esame)
   - *importance sampling*
   - proprietà di equilibrio
   - algoritmo di Metropolis
   - implementazione di un codice Monte Carlo
   - esercizio d'esame 3/3

## Il repository

- `book/`: teoria, consegne, risultati e riferimenti;
- `notebooks/`: simulazioni, figure e analisi;
- `src/computational_course/`: algoritmi riutilizzabili, con i test in `tests/`.

Comandi, anteprima locale e pubblicazione sono nell'appendice
[Workflow del repository](appendici/workflow.md).
