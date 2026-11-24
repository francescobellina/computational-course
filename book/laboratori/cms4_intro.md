# CMS 4 — argento: coordinazione, cutoff e forze

Questo capitolo raccoglie il materiale dell'esercitazione sul calcolo del cutoff per
l'argento (Ag), in due notebook:
[coordinazione ed energia di Lennard-Jones](../../notebooks/laboratori/cms4/coordinazione_e_lennard_jones.ipynb)
e [forze e statica molecolare](../../notebooks/laboratori/cms4/forze_e_statica_molecolare.ipynb).
La teoria di riferimento è nel capitolo
[Potenziali interatomici e strutture cristalline](../teoria/03_potenziali_e_cristalli.md).

## 1. Teoria

I concetti di base necessari per l'esercizio sono:

- **Potenziali a coppie e many-body** — differenze tra potenziali descritti da interazioni binarie e potenziali che dipendono dall'intorno (many-body).
- **Neighbor lists** — come elencare i vicini di ogni atomo in modo efficiente.
- **Potenziali, Lennard-Jones (LJ)** — forma analitica del potenziale e sue proprietà.
- **Cutoff radius** — raggio oltre il quale le interazioni vengono troncate.
- **Packing fraction** — frazione di volume occupata dagli atomi.

## 2. Algoritmo

1. Si legge la struttura, un cluster FCC di Ag dai file del corso (`data/raw/`).
2. Si calcola la coordinazione locale di ogni atomo e la si visualizza con OVITO.
3. Si costruiscono le liste dei vicini entro il raggio di taglio, una volta sola.
4. Con le stesse liste si calcolano l'energia di Lennard-Jones con il taglio e le
   forze su ogni atomo.
5. Nel secondo notebook si confronta il calcolo «brute force» con quello sulle liste,
   si minimizza l'energia con la *steepest descent* (statica molecolare) e si confronta
   il taglio netto con il raccordo polinomiale.

## 3. Continuazione

Prosecuzione del lavoro, in sintesi:

- Lista dei vicini (`nnbrs`, `whichnbr`) costruita una volta e riusata per energia e forze.
- Energia di Lennard-Jones con cutoff.
- **Forze** per atomo: $\vec F_i = \sum_j K_{ij}(\vec r_i - \vec r_j)$, con $K_{ij} = 24\varepsilon\,(2s_6^2 - s_6)/r_{ij}^2$ e $s_6 = (\sigma/r_{ij})^6$.
- Forza netta **nulla** nel bulk (ambiente simmetrico), **non nulla** su superficie, spigoli e angoli.
- Forze raggruppate per numero di primi vicini (NNBR), scomposte in $|f|$ (coppia) e $|\sum \hat u|$ (geometrico): $|\vec F| = |f|\,|\sum \hat u|$.
