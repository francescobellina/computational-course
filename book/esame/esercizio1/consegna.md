(sec:es1-intro)=
# Consegna e piano (PART 1 + 2)

L'**Esercizio 1** (*MD simulations of LJ-Ag*) è il primo dei tre esercizi
d'esame. Riguarda la dinamica molecolare; il secondo e il terzo riguarderanno
il Monte Carlo cinetico e il Metropolis Monte Carlo. Questa pagina riporta la
consegna del 24 novembre 2026, *Exercise 1 (PART 1 + 2)*, con la divisione in
sotto-esercizi e lo stato del lavoro. La soluzione è nel notebook
[Exercise 1 (PART 1 + 2)](../../../notebooks/esame/esercizio1_part1_2.ipynb).

## Parametri comuni

| Grandezza | Valore |
|---|---|
| Potenziale | Lennard-Jones, $\varepsilon=0.345$ eV, $\sigma=2.644$ Å |
| Raggio di taglio e raccordo | $r_c=4.5$ Å; polinomio di grado 7 per $r_p<r<r_c$, $r_p=4.2$ Å, coefficienti A…H di `poly7.py` (**in tutte le simulazioni**) |
| Tempo di termalizzazione | $t_{th}=3$ ps, scartato dalle medie |
| Cella | 256 atomi, file `fcc100a256.txt` (elearning), salvo indicazione diversa |
| Criterio sul passo temporale | $\delta E/\lvert\langle E\rangle\rvert<10^{-5}$ ([](#eq:dt-criterion)) |
| *Steepest descent* (dal punto 2) | $C=0.005$ Å²/eV, stop quando $F_\text{max}<10^{-3}$ eV/Å |

## Il testo

In tutte le simulazioni le interazioni tra gli atomi di Ag sono descritte dal
potenziale LJ ($\varepsilon=0.345$ eV, $\sigma=2.644$ Å) con raggio di taglio
$r_c=4.5$ Å e un raccordo polinomiale di grado 7 per $r_p<r<r_c$, con
$r_p=4.2$ Å. Si usano i coefficienti A, B, …, H per i termini di grado
0, 1, …, 7, come forniti nel file `poly7.py` sulla pagina elearning. Si assume
$t_{th}=3$ ps come tempo di termalizzazione e si usa la cella di 256 atomi
(file `fcc100a256.txt`), salvo indicazione diversa.

1. **Passo temporale ottimale.** Trovare il passo ottimale, cioè il più grande
   che dà $\delta E/|\langle E\rangle|<10^{-5}$, per simulazioni con
   temperatura iniziale $T_\text{ini}=30$, 300, 1200 e 2500 K. Considerare
   l'intervallo $[1,25]$ fs ed eseguire almeno 8000 passi di integrazione per
   ogni prova. Verificare se alle stesse temperature esisterebbe un passo
   valido usando un potenziale con **taglio netto**. Visualizzare la
   traiettoria di un atomo al **centro** del cluster e di uno a un **vertice**
   del cubo, alla temperatura più bassa e a quella più alta, e confrontarle.

*Per i punti seguenti, usare sempre i passi ottimali trovati nel punto 1 e
implementare una procedura di steepest descent per far partire la simulazione
da una configurazione di minimo dell'energia (usare $C=0.005$ e fermarsi quando
la forza massima scende sotto $0.001$ eV/Å).*

2. **Temperatura ed equipartizione.** Eseguire simulazioni lunghe 50 ps per
   $T_\text{ini}$ nell'intervallo $[30,2500]$ K e tracciare $\langle T\rangle$ in
   funzione di $T_\text{ini}$. Confrontare i risultati con quelli trovati nel
   punto 2 [*sic*, vedi le note] e verificare quando vale la condizione
   $\langle T\rangle=T_\text{ini}/2$, e perché non vale per ogni $T_\text{ini}$.

## Sotto-esercizi e stato

| | Cosa fare | Risultato | Stato |
|---|---|---|---|
| **1a** | $\Delta t$ ottimale con il $P_7$ a 30, 300, 1200, 2500 K ($[1,25]$ fs, 8000 passi) | 20, 8, 3, 2 fs; validi con 4 semi su 4 | fatto (§1) |
| **1b** | Stesse temperature con il taglio netto | valido solo a 30 K; da 300 K nessun passo, per gli attraversamenti di $r_c$ | fatto (§1) |
| **1c** | Traiettorie di un atomo al centro e di uno al vertice, a 30 e 2500 K | a 30 K il vertice oscilla 3 volte più del centro; a 2500 K lascia il sito, il centro no | fatto (§1) |
| **SD** | *Steepest descent* con $C=0.005$ Å²/eV e $F_\text{tol}=10^{-3}$ eV/Å | 598 iterazioni, $\Delta E=-0.22$ eV | fatto (§2; [teoria](../../teoria/06_steepest_descent.md), [verifiche](../../../notebooks/laboratori/steepest_descent.ipynb)) |
| **2a** | 50 ps dal minimo per $T_\text{ini}$ in $[30,2500]$ K, $\langle T\rangle$ contro $T_\text{ini}$ | 12 temperature, 3 semi ciascuna | fatto (§3) |
| **2b** | Confronto con il punto 1 (partenza non minimizzata) | $+\Delta U/(3Nk_B)=+3.4$ K a ogni $T$: rapporto 1.21 a 30 K | fatto (§3) |
| **2c** | Quando vale $\langle T\rangle=T_\text{ini}/2$, e perché non sempre | 1.00 a 30 K; sopra 1 fino a +3% (effetto del $P_7$); 0.86 a 2500 K (anarmonicità, atomi fuori dal bacino) | fatto (§4) |
| *extra* | [Domande per l'orale](../orale_domande.md), [approfondimento](../../appendici/approfondimento_proteine_hpc4ai.md) su MD di proteine e HPC4AI | | in corso |

## Note di lettura

:::{warning} Un cluster, non un cristallo periodico
Il punto 1 parla di «centro del cluster» e di «vertici del cubo»: i 256 atomi
formano un **cluster isolato**, senza condizioni periodiche. La differenza
conta. Con il taglio netto, già a 300 K le coppie attraversano $r_c$, perché gli
atomi di superficie sono meno legati, e il criterio fallisce. In un cristallo
periodico, senza superfici, a 500 K il taglio netto dava invece un passo valido
di 6 fs ([Esercizi CMS 6](../../../notebooks/laboratori/cms6/esercizi_cms6.ipynb),
Parte 2).
:::

- **«Compare with point 2».** Il punto 2 chiede di confrontare «con i
  risultati del punto 2»: è quasi certamente un refuso per **punto 1**, cioè
  i run che partono dal reticolo non minimizzato.
- **Il raccordo $P_7$ si usa sempre.** Il taglio netto serve solo come
  controllo nel punto 1.
- **Punto 1 senza minimizzazione.** La *steepest descent* è chiesta «per i
  punti seguenti», quindi nel punto 1 si parte dal reticolo del file.
- **Almeno 8000 passi.** La durata di una prova dipende da $\Delta t$: 8 ps a
  1 fs (5 ps di statistica dopo $t_{th}$), 200 ps a 25 fs.
- **Passo per le temperature intermedie del punto 2.** Si usa il passo della
  prima temperatura del punto 1 non inferiore (ad esempio 700 K → passo di
  1200 K). È la scelta prudente, perché il passo valido scende con $T$.
- **Unità di $C$.** Da $\delta\mathbf r=C\,\mathbf F$ si ha $[C]=$ Å²/eV, non
  Å/eV. Il valore resta 0.005.
- **Soglia sulle forze.** La slide 37 indica $F_\text{tol}\sim10^{-5}$ eV/Å,
  mentre il testo d'esame (e il codice della slide 38) usa $10^{-3}$ eV/Å.
  Vale il testo d'esame.
- **Momento angolare.** `assign_vel` annulla la quantità di moto, ma non il
  momento angolare. Un cluster isolato ruoterebbe rigidamente per tutto il run,
  e la rotazione nasconderebbe la traiettoria del vertice. Lo si toglie
  (`remove_angular_momentum`) prima di riscalare a $T_\text{ini}$.
- **Vertici del cubo.** Con la costruzione dei file del corso solo 4 degli 8
  vertici sono occupati da un atomo.
- **La cella.** `fcc100a256.txt` non è ancora in `data/raw/`. Finché manca, si
  ricostruisce con `fcc_supercell` ($4\times4\times4$ celle, $a=4.1604$ Å): la
  stessa costruzione con $3\times3\times3$ celle riproduce esattamente il file
  del corso `fcc100a108.txt`.

Per i dettagli numerici (unità del codice, numerica del raccordo, energia
«ombra» di Verlet, controlli sul codice) vedi le
[Note tecniche](note_tecniche.md).

## Il codice

- `src/computational_course/md_p7.py` contiene:
  - `lj_p7_model`: LJ con taglio netto o raccordo $P_7$, e PBC scelte per
    direzione (cluster, lastra o bulk);
  - `run_nve`: *velocity Verlet* in NVE, con il conteggio degli
    attraversamenti di $r_c$;
  - `production_stats`: le medie dopo $t_{th}$;
  - `remove_angular_momentum`: toglie la rotazione rigida dalle velocità;
  - `steepest_descent`.

  I test sono in `tests/test_md_p7.py`.
- `materials/poly7.py` è il file dei coefficienti del corso, usato così com'è.
- Le consegne in PDF stanno solo in locale (`materials/*.pdf` è nel
  `.gitignore`).

:::{note} Un'altra versione del testo
Il 24 novembre è arrivata per errore anche una versione dell'esercizio a 5
punti (`Exercise-MD.pdf`), con temperature diverse e due punti sull'adatomo in
superficie. I punti 1–3 sono stati risolti comunque, e sono conservati
nell'[archivio](../../appendici/archivio_esercizio1_5_punti.md): i punti 4–5 potrebbero servire per una
parte successiva.
:::
