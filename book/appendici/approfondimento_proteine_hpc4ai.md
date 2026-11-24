(sec:es1-approfondimento)=
# Approfondimento: MD di proteine e HPC4AI

Questa pagina non fa parte della consegna. Raccoglie le **assonanze** tra
l'Esercizio 1 e due altri lavori:

- la MD di proteine dei progetti `p2-simulazioni` e `md-macromolecules`
  (GROMACS, peptidi in acqua);
- l'[Esercizio 6 di HPC4AI](https://francescobellina.github.io/hpc4ai/content/esercizi/es06-image-denoising/)
  (*image denoising*) e i capitoli su MPI dello stesso libro.

Per ognuno ci sono due parti: cosa è già verificato, con la fonte, e la
lista delle cose **da fare**.

## 1. MD di proteine (`p2-simulazioni`, `md-macromolecules`)

In entrambi i progetti la catena GROMACS è la stessa: minimizzazione con
`integrator = steep`, poi equilibrazione NVT e NPT, poi produzione. Il
sistema principale di `p2-simulazioni` è Ace-(Ala)₄-NMe in acqua TIP3P, con
CHARMM36m; la prova del tutorial del lisozima è il run L1 del registro. In
`md-macromolecules` lo stesso flusso serve alla tetra-alanina. I parametri
qui sotto vengono da `sim/01-minimizzazione/minim.mdp` e
`sim/02-nvt/nvt.mdp` di `p2-simulazioni`, e da `config/mdp/em.mdp` di
`md-macromolecules`, che per la minimizzazione ha gli stessi valori.

| | Esercizio 1 (LJ-Ag) | MD di proteine (GROMACS) |
|---|---|---|
| Algoritmo di minimizzazione | $\mathbf r\leftarrow\mathbf r+C\,\mathbf F$, $C$ costante | $\mathbf r_{n+1}=\mathbf r_n+h_n\,\mathbf F_n/\max\lvert\mathbf F_n\rvert$: il passo è normalizzato sulla forza massima, quindi $h_n$ è lo spostamento massimo {cite}`gromacs2022em` |
| Adattamento del passo | facoltativo (×1.1 se $E$ scende, ×0.5 se sale) | sempre: ×1.2 se l'energia scende, ×0.2 (passo rifiutato) se sale {cite}`gromacs2022em` |
| Passo iniziale | $C=0.005$ Å²/eV | `emstep = 0.01` nm, cioè 0.1 Å di spostamento massimo |
| Soglia sulle forze | $F_\text{tol}=10^{-3}$ eV/Å $\approx0.96$ kJ mol⁻¹ nm⁻¹ | `emtol = 1000` kJ mol⁻¹ nm⁻¹ $\approx1.04$ eV/Å, **mille volte più larga** (il valore predefinito di GROMACS è 10) |
| Numero massimo di passi | `max_iter` | `nsteps = 50000` |
| Passi per convergere | 598 (cluster di 256 atomi) | 96–157 per i peptidi (prove P1–P4), 457 per il lisozima (L1) |
| Taglio delle interazioni | raccordo $P_7$ tra 4.2 e 4.5 Å ($\phi$ e tre derivate continue) | `vdw-modifier = force-switch` tra `rvdw-switch = 1.0` e `rvdw = 1.2` nm in NVT e produzione, PME per l'elettrostatica |
| Passo temporale | dal criterio $\delta E/\lvert\langle E\rangle\rvert<10^{-5}$: 3–20 fs | 2 fs, con i legami con H vincolati (`constraints = h-bonds`, LINCS) |
| Temperatura | NVE: velocità a $T_\text{ini}$, poi $\langle T\rangle\approx T_\text{ini}/2$ | NVT con termostato V-rescale, velocità generate alla temperatura bersaglio (`gen_temp = 298`) |
| Condizioni al contorno | cluster isolato, senza PBC | PBC in $x$, $y$, $z$; scatola cubica a 1.2 nm dal peptide |

:::{important} La stessa fisica del punto 2, vista in GROMACS
Nel registro dei run di `p2-simulazioni` (run L1, lisozima, riga «T, NVT») è
annotato: «nel primo ps T scende a ~217 K (l'energia cinetica passa alla
potenziale dopo la minimizzazione) e poi risale con τ_T = 1 ps».

È lo stesso meccanismo per cui, nell'Esercizio 1, si ha
$\langle T\rangle\approx T_\text{ini}/2$. Partendo da un minimo, le velocità
iniziali portano energia solo nella parte cinetica, e l'equilibrio la divide
con quella potenziale. Nella MD di proteine il termostato restituisce
l'energia in circa $\tau_T$; nella NVE dell'esercizio nessuno la restituisce,
e per questo si parte da $T_\text{ini}=2T$.
:::

### Da fare

- [ ] **Perché 217 K e non 149 K?** Con un solido armonico in NVE ci si
  aspetterebbe la metà di 298 K. Possibili cause, da verificare: il termostato
  agisce già durante la discesa; l'acqua è un liquido, non un solido armonico;
  i vincoli LINCS tolgono gradi di libertà. Si può riprodurre con l'NVT del
  registro, leggendo $T(t)$ nel primo ps dal file `.edr`.
- [ ] **Che cosa cambia con `emtol = 1000`.** La soglia è mille volte più
  larga di quella dell'esercizio. Va capito a cosa serve, in un sistema con
  acqua che poi si equilibra per 600 ps: probabilmente solo a togliere gli
  scontri iniziali, ma va confermato con il tutorial o il manuale.
- [ ] **Il passo normalizzato di GROMACS sul cluster di Ag.** Implementare in
  `md_p7.py` la variante con $h_n$ e il fattore ×1.2/×0.2, e confrontarla con
  il $C$ costante e con il $C$ adattivo
  ([notebook](../../notebooks/laboratori/steepest_descent.ipynb), §4).
  Il manuale citato è quello del 2022, mentre i progetti usano GROMACS 2026.1:
  verificare che l'algoritmo sia rimasto lo stesso.
- [ ] **`force-switch` e $P_7$.** Il force-switch di CHARMM porta a zero la
  forza tra 1.0 e 1.2 nm, il $P_7$ porta a zero energia e tre derivate tra 4.2 e
  4.5 Å. Confrontare le due ricette, con la forma esatta presa dal manuale di
  GROMACS: quante derivate restano continue, e che effetto ha ciascuna sulla
  conservazione dell'energia.
- [ ] **Passo temporale e vincoli.** Nell'esercizio il passo è limitato dalle
  vibrazioni più veloci del cristallo (7.6 THz, periodo 131 fs). Nelle
  proteine si vincolano i legami con H: verificare con una fonte quanto
  permette di allungare il passo, e se il criterio $\delta E/|\langle E\rangle|$
  ha un equivalente in GROMACS (la deriva dell'energia in NVE).
- [ ] **Medie temporali e PMF.** `md-macromolecules` calcola il potenziale di
  forza media $F(x)=-k_BT\ln p(x)$, per esempio in funzione del raggio di
  girazione. Collegarlo all'ergodicità e alle medie temporali del capitolo
  [CMS 6](../teoria/05_simulazioni_md.md): quanto deve durare un run perché $p(x)$ sia
  affidabile? `p2-simulazioni` sceglie la durata dal $\tau_\text{int}$
  misurato.

## 2. HPC4AI: Esercizio 6 (*image denoising*) e capitoli su MPI

L'[Esercizio 6](https://francescobellina.github.io/hpc4ai/content/esercizi/es06-image-denoising/)
ripulisce un'immagine rumorosa $f$ cercando la $u$ che minimizza

$$
E(u)=\frac12\sum_{i,j}(u_{i,j}-f_{i,j})^2+\frac\lambda2\sum_{\{a,b\}}(u_a-u_b)^2,
$$

con la seconda somma sulle coppie di pixel adiacenti. Il problema è lo stesso
della *steepest descent*: minimizzare un'energia con un'iterazione locale. Le
corrispondenze sono strette.

- **Jacobi è una *steepest descent* con un passo per pixel.** Il gradiente è
  $\partial E/\partial u_{i,j}=(1+\lambda d_{i,j})\,u_{i,j}-f_{i,j}-\lambda\sum_{N(i,j)}u_{k,l}$,
  con $d_{i,j}$ il numero di vicini. Un passo di discesa con
  $C_{i,j}=1/(1+\lambda d_{i,j})$ dà
  $u_{i,j}-C_{i,j}\,\partial E/\partial u_{i,j}=\bigl(f_{i,j}+\lambda\sum_N u_{k,l}\bigr)/(1+\lambda d_{i,j})$,
  che è esattamente l'aggiornamento di Jacobi dell'Esercizio 6. È una
  *steepest descent* con il passo scalato sulla diagonale dell'Hessiana.
- **Stessa analisi di convergenza.** L'Hessiana è $A=I+\lambda L$, con $L$ il
  laplaciano della griglia, i cui autovalori stanno in $[0,8)$. Con un $C$
  uguale per tutti i pixel vale il limite
  [](#eq:es1-sd-stabilita), $C<2/\lambda_\text{max}(A)$. Per una griglia
  $12\times9$ con $\lambda=1$, ad esempio, $\lambda_\text{max}(A)=8.81$ e
  $C_\text{crit}=0.227$. Il Jacobi dei pixel interni usa $1/(1+4\lambda)=0.2$,
  appena sotto. Le componenti lisce dell'errore, lente per Jacobi (Esercizio 6,
  «Perché converge e quanto in fretta»), corrispondono ai modi morbidi che
  rallentano la discesa nel cluster di Ag.
- **Stesso criterio di arresto.** L'Esercizio 6 si ferma su
  $\max|u^{(t+1)}-u^{(t)}|$; con $C$ costante,
  $\max_k|\delta\mathbf r(k)|=C\,F_\text{max}$, cioè il criterio
  [](#eq:es1-sd-ftol).
- **Una differenza importante: la convessità.** $E(u)$ è strettamente
  convessa, quindi ha un solo minimo, indipendente dal punto di partenza. La
  PES di Lennard-Jones ha molti minimi, e la discesa trova quello del bacino
  di partenza ([teoria](../teoria/06_steepest_descent.md), §6).
- **Jacobi e Gauss–Seidel.** La *steepest descent* sposta tutti gli atomi con
  le forze della stessa configurazione, come Jacobi. Spostare un atomo alla
  volta con le forze già aggiornate sarebbe l'analogo di Gauss–Seidel.
- **Halo e raggio di taglio.** Lo stencil del denoising arriva ai primi vicini,
  quindi ogni processo MPI deve ricevere un halo di una riga. Il
  [capitolo 6 di HPC4AI](https://francescobellina.github.io/hpc4ai/content/teoria/mpi/)
  osserva che lo stesso schema, halo e celle fantasma, è il più comune anche
  nei codici di dinamica molecolare. In MD l'equivalente dello stencil è
  $r_c$: con una decomposizione in domini, l'halo deve contenere gli atomi
  entro $r_c$ dal bordo. La decisione di arresto dell'Esercizio 6
  (`MPI_Allreduce`) corrisponde, in MD, alla riduzione di $F_\text{max}$ e
  dell'energia totale su tutti i processi.

### Da fare

- [ ] **Chiudere la riga lasciata aperta in HPC4AI.** La tabella
  dell'Esercizio 6 elenca un «confronto con convoluzione e steepest descent»
  come approfondimento personale non ancora fatto. Ripetere sul denoising i
  controlli del [notebook](../../notebooks/laboratori/steepest_descent.ipynb):
  *steepest descent* a $C$ costante contro Jacobi, $C_\text{crit}$ misurato
  contro $2/\lambda_\text{max}(A)$, e numero di iterazioni contro $\lambda$.
- [ ] **Gauss–Seidel per atomi.** Provare sul cluster di 256 atomi una
  discesa che aggiorna un atomo alla volta, e confrontare il numero di
  iterazioni con quello della *steepest descent*.
- [ ] **Decomposizione in domini per la MD.** Leggere la parte su
  decomposizione a blocchi e scambio degli halo del
  [capitolo 7 di HPC4AI](https://francescobellina.github.io/hpc4ai/content/teoria/mpi-programmazione/)
  e stimare per una lastra (come quella dei punti 4–5 della
  [versione a 5 punti](archivio_esercizio1_5_punti.md)) quanto sarebbe spesso l'halo ($r_c$)
  rispetto a un dominio. Per 256 atomi non conviene, ma serve a capire perché
  i codici MD scalano.
- [ ] **Parallelizzare il calcolo delle forze.** Il ciclo sulle coppie di
  `md_p7` è compilato con Numba ma seriale. Provare `numba.prange` (thread,
  come OpenMP nel capitolo 5 di HPC4AI) e misurare lo *speed-up*, con la
  stessa metodologia degli esercizi di HPC4AI.
