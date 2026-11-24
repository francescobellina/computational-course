(sec:es1-note-tecniche)=
# Note tecniche

Dettagli di metodo che non servono per seguire la soluzione, ma che spiegano
perché i numeri sono affidabili, e che all'orale possono servire per rispondere
a domande più tecniche. Ogni numero rimanda al notebook in cui è calcolato.

## 1. Unità del codice

| Grandezza | Unità |
|---|---|
| energia | eV |
| lunghezza | Å |
| tempo | s (nei grafici fs e ps) |
| massa | eV·s²/Å²: 1 unità $=1.602\times10^{-19}$ J s² / $10^{-20}$ m² $\approx16$ kg; per l'Ag $m=108\times1.66\times10^{-27}/16$ |
| temperatura | K, con $k_B=1/11603$ eV/K |

La temperatura istantanea è $T=2K/(3Nk_B)$. Togliere quantità di moto e momento
angolare rimuove 6 gradi di libertà su $3N=768$ (0.8%). L'effetto si cancella nel
rapporto $\langle T\rangle/(T_\text{ini}/2)$, perché $T_\text{ini}$ si calcola
nello stesso modo.

## 2. Il raccordo $P_7$ in doppia precisione

- **Cancellazione.** I coefficienti di `poly7.py` vanno da $6\times10^3$ a
  $2.8\times10^8$, con segni alterni, mentre $P_7$ vale meno di 0.1 eV. Valutare
  il polinomio in doppia precisione introduce un errore fino a $10^{-6}$ eV, e
  anche con un'aritmetica esatta il polinomio vale $-6\times10^{-6}$ eV in $r_c$
  invece di zero.
- **Lo scalino in $r_p$.** $P_7(r_p)-\phi_{LJ}(r_p)=-3.9\times10^{-6}$ eV: ogni
  coppia che attraversa $r_p$ fa un piccolissimo salto di energia. A bassa
  temperatura e con passi piccoli, questo pone un pavimento a
  $\delta E/|\langle E\rangle|\approx10^{-7}$, mentre il taglio netto scende più
  in basso. Correggendo solo il coefficiente A, il pavimento scende da
  $1.0\times10^{-7}$ a $3.0\times10^{-8}$ (7691 attraversamenti di $r_p$ in 5 ps
  a 50 K; [punti 1–2](../../notebooks/06_esercizio1_md/punti_1_2_passo_temporale.ipynb),
  §3.1). È 100 volte sotto la soglia, quindi per l'esercizio si usano i
  coefficienti così come sono.
- **Ordine di grandezza.** Entrambi i residui sono circa 10 000 volte più
  piccoli del salto del taglio netto, $|\phi_{LJ}(r_c)|=0.054$ eV.
- **Nei test.** Per confrontare le forze con le differenze finite dell'energia
  serve un passo $h\approx10^{-3}$ Å: con $h$ più piccolo il rumore della
  cancellazione, diviso per $h$, domina.
- **Curvatura.** Il $P_7$ deve annullare energia e tre derivate in 0.3 Å, quindi è
  molto curvo: fino a 5.9 eV/Å², contro 0.16 eV/Å² di LJ in $r_p$
  ([Esercizi CMS 6](../../notebooks/05_molecular_dynamics/esercizi_cms6.ipynb)).
  È la causa dell'eccesso di $\langle T\rangle$ tra 100 e 900 K nel punto 2.

## 3. Che cosa misura il criterio sul passo

$\delta E/|\langle E\rangle|$ è la deviazione standard di $E_\text{tot}$ dopo
$t_{th}$: misura le **fluttuazioni** dell'energia, non uno spostamento della sua
media. *Velocity Verlet* è simplettico: per un oscillatore armonico conserva
esattamente $\tfrac12p^2+\tfrac12\omega^2q^2(1-\omega^2\Delta t^2/4)$ (energia
«ombra»), che differisce dall'energia vera di una quantità che cresce con
$(\omega\Delta t)^2$. Per il modo più veloce del cluster (7.6 THz, periodo
131 fs) a 20 fs, $\omega\Delta t\approx1$.

Nel punto 1, a 30 K con 20 fs, il criterio è rispettato
($6\times10^{-6}$), ma la media di $E_\text{tot}$ è più alta di $E_0$ del 4% di
$K_0$. Con 2 fs lo spostamento sparisce. L'effetto su $\langle T\rangle$ è
$-1.3\%$ (18.16 K contro 18.40 K)
([PART 1 + 2](../../notebooks/06_esercizio1_md/esercizio1_part1_2.ipynb), §1).

## 4. Robustezza del passo ottimale

$\delta E$ viene da una sola traiettoria, e cambia di qualche punto percentuale
con il seme delle velocità iniziali. Nel punto 1 il passo ottimale e il
successivo sono stati ripetuti con 4 semi. I passi ottimali (20, 8, 3, 2 fs)
restano validi con tutti i semi, mentre il successivo fallisce con la maggior
parte. A 1200 K, 4 fs passa con 2 semi su 4: è al limite
([PART 1 + 2](../../notebooks/06_esercizio1_md/esercizio1_part1_2.ipynb), §1).

## 5. Momento angolare

In un cluster isolato il momento angolare $\mathbf L$ si conserva, e
`assign_vel` toglie solo la quantità di moto. Con $\mathbf L\neq0$ il cluster
ruota rigidamente con $\boldsymbol\omega=I^{-1}\mathbf L$ per tutto il run. A
2500 K il vertice, a 12.6 Å dal centro, si sposterebbe di 7.3 Å in 16 ps per la
sola rotazione, più del suo moto vero. `remove_angular_momentum` sottrae
$\boldsymbol\omega\times(\mathbf r-\mathbf r_\text{cm})$ dalle velocità, che poi
si riscalano a $T_\text{ini}$.

## 6. La cella

- `fcc100a256.txt` non è ancora in `data/raw/`: la cella si ricostruisce con
  `fcc_supercell` ($4\times4\times4$ celle, $a=4.1604$ Å). La stessa costruzione
  con $3\times3\times3$ celle riproduce esattamente il file del corso
  `fcc100a108.txt`.
- I siti sono $(i,j,k)\,a/2$ con $i+j+k$ pari, $i,j,k=0\dots7$. Il vertice
  $(0,0,0)$ è occupato, $(7,7,7)$ no: dei vertici del cubo ne sono occupati
  4 su 8.

## 7. Come è verificato il codice

- **Test automatici** (`tests/test_md_p7.py`):
  - le condizioni del $P_7$ in $r_p$ e $r_c$;
  - il taglio netto uguale al modulo `lennard_jones`;
  - le forze uguali alle differenze finite dell'energia;
  - forza totale e momento nulli nel cluster;
  - le PBC solo in $x$ e $y$ per la lastra;
  - la conservazione dell'energia in NVE e il riconoscimento delle divergenze;
  - la discesa monotona della *steepest descent*, anche nella versione
    adattiva;
  - la rimozione del momento angolare.
- **Due versioni del calcolo delle forze.** `calcForces`, scritta in chiaro
  nel notebook, coincide con la versione compilata entro $10^{-13}$ eV/Å.
- **Un risultato del corso riprodotto.** Sul cluster di 864 atomi la
  *steepest descent* dà $-1681.86\to-1682.39$ eV, come la slide 39
  ([notebook](../../notebooks/06_esercizio1_md/steepest_descent.ipynb), §2).

## 8. Prestazioni

Il calcolo di energia e forze scorre tutte le $N(N-1)/2$ coppie ($O(N^2)$),
compilato con Numba. Per 256 atomi costa circa 0.1 ms per chiamata, 10 volte
meno della versione NumPy
([Esercizi CMS 6](../../notebooks/05_molecular_dynamics/esercizi_cms6.ipynb),
Parte 3). L'intero notebook PART 1 + 2 gira in circa 2 minuti.
