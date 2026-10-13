# Introduzione all'esercizio

Questo capitolo raccoglie il materiale dell'esercitazione sul calcolo del cutoff per l'argento (Ag).

## 1. Teoria

I concetti di base necessari per l'esercizio sono:

- **Potenziali a coppie e many-body** — differenze tra potenziali descritti da interazioni binarie e potenziali che dipendono dall'intorno (many-body).
- **Neighbor lists** — come elencare i vicini di ogni atomo in modo efficiente.
- **Potenziali, Lennard-Jones (LJ)** — forma analitica del potenziale e sue proprietà.
- **Cutoff radius** — raggio oltre il quale le interazioni vengono troncate.
- **Packing fraction** — frazione di volume occupata dagli atomi.

## 2. Algoritmo

Come calcolare le quantità dell'esercizio (procedura operativa).

## 3. Continuazione

Prosecuzione del lavoro, in sintesi:

- Lista dei vicini (`nnbrs`, `whichnbr`) costruita una volta e riusata per energia e forze.
- Energia di Lennard-Jones con cutoff.
- **Forze** per atomo: $\vec F_i = \sum_j K_{ij}(\vec r_i - \vec r_j)$, con $K_{ij} = 24\varepsilon\,(2s_6^2 - s_6)/r_{ij}^2$ e $s_6 = (\sigma/r_{ij})^6$.
- Forza netta **nulla** nel bulk (ambiente simmetrico), **non nulla** su superficie, spigoli e angoli.
- Forze raggruppate per numero di primi vicini (NNBR), scomposte in $|f|$ (coppia) e $|\sum \hat u|$ (geometrico): $|\vec F| = |f|\,|\sum \hat u|$.


## TEORIA DELLA STRUTTURA CRISTALLINA (...)