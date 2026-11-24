(sec:es1-intro)=
# Testo e piano dell'esercizio

:::{important} Consegna del 24 novembre: PART 1 + 2
La consegna di oggi è `materials/Exercise-MD-PART1+2.pdf`, risolta nel
notebook [Exercise 1 (PART 1 + 2)](../../notebooks/06_esercizio1_md/esercizio1_part1_2.ipynb).
Rispetto al testo di questa pagina (`Exercise-MD.pdf`) cambiano diverse cose:
il raccordo $P_7$ si usa sempre, le temperature sono 30, 300, 1200 e 2500 K,
servono almeno 8000 passi, e le traiettorie sono nel punto 1. Il punto 2
chiede $\langle T\rangle$ contro $T_\text{ini}$ su 50 ps, dal minimo.
:::

L'**Esercizio 1** (*MD simulations of LJ-Ag*) è il primo dei tre esercizi
d'esame. Riguarda la dinamica molecolare (MD); il secondo e il terzo
riguarderanno il Monte Carlo cinetico e il Metropolis Monte Carlo. Il testo
originale, in inglese, è in `materials/Exercise-MD.pdf`.

## Parametri comuni

| Grandezza | Valore |
|---|---|
| Potenziale | Lennard-Jones, $\varepsilon=0.345$ eV, $\sigma=2.644$ Å |
| Raggio di taglio | $r_c=4.5$ Å |
| Tempo di termalizzazione | $t_{th}=3$ ps (scartato dalle medie) |
| Cella | 256 atomi, file `fcc100a256.txt` (elearning), salvo indicazione diversa |
| Raccordo polinomiale (dal punto 2) | $P_7$ tra $r_p=4.2$ Å e $r_c$, coefficienti di `poly7.py` |
| *Steepest descent* (dal punto 3) | $C=0.005$ Å²/eV, stop quando $F_\text{max}<10^{-3}$ eV/Å |
| Criterio sul passo temporale | $\delta E/\lvert\langle E\rangle\rvert<10^{-5}$ ([](#eq:dt-criterion)) |

## Il testo

In tutte le simulazioni le interazioni tra gli atomi di Ag sono descritte dal
potenziale LJ ($\varepsilon=0.345$ eV, $\sigma=2.644$ Å) con raggio di taglio
$r_c=4.5$ Å. Si assume $t_{th}=3$ ps come tempo di termalizzazione e si usa
la cella di simulazione di 256 atomi (file `fcc100a256.txt` sulla pagina
elearning), salvo indicazione diversa.

1. **Taglio netto.** Usando un taglio netto (*sharp cutoff*), trovare il
   passo temporale ottimale per una simulazione con temperatura iniziale
   $T_\text{ini}=50$ K. Il passo ottimale è il più grande per cui
   $\delta E/|\langle E\rangle|<10^{-5}$. Considerare l'intervallo
   $[1,25]$ fs ed eseguire 5000 passi di integrazione per ogni prova.
   Ripetere l'analisi per $T_\text{ini}=500$ K e mostrare che il criterio
   non può essere soddisfatto, comunque si riduca il passo.
2. **Raccordo polinomiale.** Implementare un raccordo polinomiale di grado 7
   per $r_p<r<r_c$, con $r_p=4.2$ Å. Usare i coefficienti A, B, …, H per i
   termini di grado 0, 1, …, 7, come forniti nel file `poly7.py` sulla
   pagina elearning. Adattare di conseguenza la definizione delle forze.
   Verificare che per $T_\text{ini}=50$ K la simulazione sia coerente con
   quella a taglio netto, e trovare il passo ottimale per
   $T_\text{ini}=500$ K, $1000$ K e $2000$ K.

*Per i punti seguenti, implementare una procedura di steepest descent per far
partire la simulazione da una configurazione di minimo dell'energia (usare
$C=0.005$ e fermarsi quando la forza massima scende sotto $0.001$ eV/Å).*

3. **Temperatura ed equipartizione.** Usando i passi ottimali trovati nel
   punto 2, eseguire simulazioni lunghe 10 ps per $T_\text{ini}=50$, $500$,
   $1000$ e $2000$ K. Tracciare $\langle T\rangle$ in funzione di
   $T_\text{ini}$, verificare se vale la condizione
   $\langle T\rangle=T_\text{ini}/2$ e spiegare il risultato. Visualizzare
   le traiettorie degli atomi al centro del cluster e ai vertici del cubo, sia
   per la temperatura più bassa sia per la più alta, e commentarne la
   differenza.
4. **Adatomo su (100).** Considerare una lastra cristallina infinita
   ($L_x=L_y=16.6416$ Å) con superfici libere lungo $z$. Aggiungere un
   adatomo al centro della superficie superiore, con coordinata $z$ di
   $2.4$ Å sopra la $z$ massima degli atomi della cella. Eseguire una
   simulazione lunga 300 ps a partire dalla configurazione minimizzata.
   Scegliere $T_\text{ini}$ in modo da ottenere una temperatura di
   equilibrio $T=850\pm30$ K e usare un passo temporale appropriato.
   Tracciare la traiettoria dell'adatomo nel tempo.
5. **Adatomo su (111).** Ripetere l'analisi del punto 4 con una cella
   orientata (111), dal file `fcc111a336+1.txt` sulla pagina elearning, con
   $L_x=L_y=20.3817$ Å, e confrontare i risultati per le due orientazioni.
   È probabile che, a temperatura ambiente e nello stesso intervallo di
   tempo, l'adatomo diffonda su una sola superficie o su entrambe?

## Sotto-esercizi e stato

La soluzione dei punti 1–3 da presentare all'esame è nel notebook
[Esercizio 1 — soluzione dei punti 1–3](../../notebooks/06_esercizio1_md/esercizio1_soluzione.ipynb).

| | Cosa fare | Risultato | Stato |
|---|---|---|---|
| **1a** | Taglio netto, $T_\text{ini}=50$ K: scansione di $\Delta t$ in $[1,25]$ fs, 5000 passi per prova | $\Delta t$ ottimale $=20$ fs | fatto ([punti 1–2](../../notebooks/06_esercizio1_md/punti_1_2_passo_temporale.ipynb)) |
| **1b** | Taglio netto, $T_\text{ini}=500$ K: mostrare che nessun $\Delta t$ basta | $\delta E/\lvert\langle E\rangle\rvert\approx1.6\times10^{-4}$ anche a $0.25$ fs | fatto |
| **2a** | Raccordo $P_7$ con i coefficienti di `poly7.py`, forze adattate | modulo `md_p7`, con test | fatto |
| **2b** | Coerenza tra $P_7$ e taglio netto a 50 K | stesse medie e stesso passo ottimale | fatto |
| **2c** | $\Delta t$ ottimale con $P_7$ a 500, 1000, 2000 K | 6, 4, 3 fs (verificati con 4 semi) | fatto |
| **SD** | *Steepest descent* con $C=0.005$ Å²/eV e $F_\text{tol}=10^{-3}$ eV/Å | 598 iterazioni, $\Delta E=-0.22$ eV | fatto ([teoria](steepest_descent.md), [implementazione](../../notebooks/06_esercizio1_md/steepest_descent.ipynb)) |
| **3a** | 10 ps a 50/500/1000/2000 K dal minimo; $\langle T\rangle$ contro $T_\text{ini}$; spiegare $T_\text{ini}/2$ | $\langle T\rangle/(T_\text{ini}/2)=1.01$, 1.03, 1.00, 0.91: equipartizione armonica, anarmonicità ad alta $T$ | fatto ([soluzione](../../notebooks/06_esercizio1_md/esercizio1_soluzione.ipynb)) |
| **3b** | Traiettorie degli atomi al centro e ai vertici, alla $T$ più bassa e più alta | vertici circa 3 volte più mobili a 50 K; a 2000 K lasciano il sito, il centro no | fatto |
| **4a** | Lastra (100): PBC solo in $x$ e $y$, adatomo a $+2.4$ Å, minimizzazione | | da fare |
| **4b** | $T_\text{ini}$ per $T=850\pm30$ K, scelta di $\Delta t$, 300 ps, traiettoria dell'adatomo | | da fare |
| **5a** | Cella (111) da `fcc111a336+1.txt`, $L_x=L_y=20.3817$ Å: ripetere il punto 4 | | da fare (manca il file) |
| **5b** | Confronto (100)/(111) e diffusione a temperatura ambiente | | da fare |
| *extra* | Assonanze con la MD di proteine (`p2-simulazioni`, `md-macromolecules`) e con l'Esercizio 6 di HPC4AI | prime corrispondenze verificate | da fare ([approfondimento](approfondimento.md)) |

## Note di lettura

:::{warning} Punti 1–3: un cluster, non un cristallo periodico
Il punto 3 parla di «centro del cluster» e di «vertici del cubo»: nei punti
1–3 i 256 atomi formano un **cluster isolato**, senza condizioni periodiche.
Le PBC entrano solo nel punto 4, e solo lungo $x$ e $y$. La differenza conta.
A 500 K, con il taglio netto, le coppie attraversano $r_c$ solo nel cluster,
dove gli atomi di superficie sono meno legati, e il criterio fallisce come
chiede il testo. Nel cristallo periodico della
[Parte 2 di Esercizi CMS 6](../../notebooks/05_molecular_dynamics/esercizi_cms6.ipynb)
lo stesso caso dava invece un passo ottimale di 6 fs.
:::

- **Unità di $C$.** Il testo scrive «$C=0.005$ Å/eV», ma
  $\delta\mathbf r=C\,\mathbf F$ richiede $[C]=$ Å²/eV. Il valore resta
  quello.
- **«From point 3,».** Nel PDF questa frase resta in sospeso dopo il
  preambolo. Il senso lo chiarisce il paragrafo sulla *steepest descent*: dal
  punto 3 in poi si parte da una configurazione minimizzata.
- **Soglia sulle forze.** La slide 37 indica $F_\text{tol}\sim10^{-5}$ eV/Å,
  mentre il testo d'esame (e il codice della slide 38) usa $10^{-3}$ eV/Å.
  Vale il testo d'esame.
- **5000 passi fissi.** La durata di una prova dipende da $\Delta t$: 5 ps a
  1 fs (restano 2 ps dopo $t_{th}$), 125 ps a 25 fs.
- **Potenziale nei punti 3–5.** Il testo non lo ripete, ma chiede i passi
  ottimali del punto 2. Si usa quindi il raccordo $P_7$.
- **Vertici del cubo.** Con la costruzione dei file del corso solo 4 degli 8
  vertici del cubo sono occupati da un atomo.
- **Momento angolare (punto 3).** `assign_vel` annulla la quantità di moto,
  ma non il momento angolare. Un cluster isolato ruoterebbe rigidamente per
  tutto il run (a 2000 K i vertici si sposterebbero di circa 4 Å in 10 ps per
  la sola rotazione), quindi lo si toglie (`remove_angular_momentum`) prima
  di riscalare a $T_\text{ini}$.
- **File dall'elearning.** `fcc100a256.txt` non è ancora in `data/raw/`.
  Finché manca, la cella si ricostruisce con `fcc_supercell` ($4\times4\times4$
  celle, $a=4.1604$ Å). La stessa costruzione con $3\times3\times3$ celle
  riproduce esattamente il file del corso `fcc100a108.txt`, e $4a=16.6416$ Å
  è proprio il lato $L_x$ del punto 4. Per il punto 5 serve
  `fcc111a336+1.txt`.

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
