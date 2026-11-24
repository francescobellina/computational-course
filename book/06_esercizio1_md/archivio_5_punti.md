(sec:es1-archivio)=
# Archivio: versione a 5 punti

:::{important} Non è la consegna d'esame
Questa versione dell'esercizio (`Exercise-MD.pdf`) è arrivata per errore il 24
novembre 2026, al posto della consegna *PART 1 + 2*, che è nella pagina
[Consegna e piano](intro.md). Ha temperature diverse, 5000 passi per prova e
due punti in più sull'adatomo in superficie. I punti 1–3 sono stati risolti e
restano qui; i punti 4–5 potrebbero servire per una parte successiva
dell'esercizio. Le parti di metodo utili anche per la consegna vera (numerica
del raccordo, robustezza del passo, energia «ombra», momento angolare) sono
state riportate nel notebook PART 1 + 2 e nelle [Note tecniche](note_tecniche.md).
:::

## Il testo

In tutte le simulazioni le interazioni tra gli atomi di Ag sono descritte dal
potenziale LJ ($\varepsilon=0.345$ eV, $\sigma=2.644$ Å) con raggio di taglio
$r_c=4.5$ Å. Si assume $t_{th}=3$ ps come tempo di termalizzazione e si usa la
cella di 256 atomi (file `fcc100a256.txt`), salvo indicazione diversa.

1. **Taglio netto.** Con un taglio netto, trovare il passo temporale ottimale
   (il più grande con $\delta E/|\langle E\rangle|<10^{-5}$) per
   $T_\text{ini}=50$ K, provando l'intervallo $[1,25]$ fs con 5000 passi per
   prova. Ripetere a $T_\text{ini}=500$ K e mostrare che il criterio non si
   può rispettare, comunque si riduca il passo.
2. **Raccordo polinomiale.** Implementare il raccordo di grado 7 per
   $r_p<r<r_c$, con $r_p=4.2$ Å e i coefficienti A…H di `poly7.py`, e adattare
   le forze. Verificare che a $T_\text{ini}=50$ K la simulazione sia coerente
   con quella a taglio netto, e trovare il passo ottimale per
   $T_\text{ini}=500$, 1000 e 2000 K.

*Per i punti seguenti, partire da un minimo trovato con steepest descent
($C=0.005$, stop a $F_\text{max}<0.001$ eV/Å).*

3. **Temperatura ed equipartizione.** Con i passi ottimali del punto 2, run da
   10 ps a $T_\text{ini}=50$, 500, 1000 e 2000 K. Tracciare $\langle T\rangle$
   contro $T_\text{ini}$, verificare $\langle T\rangle=T_\text{ini}/2$ e
   spiegarlo. Visualizzare le traiettorie degli atomi al centro e ai vertici
   del cubo, alla temperatura più bassa e a quella più alta.
4. **Adatomo su (100).** Lastra infinita ($L_x=L_y=16.6416$ Å) con superfici
   libere lungo $z$; un adatomo al centro della superficie superiore, 2.4 Å
   sopra la $z$ massima. Run da 300 ps dalla configurazione minimizzata, con
   $T_\text{ini}$ scelta per avere $T=850\pm30$ K e un passo appropriato.
   Tracciare la traiettoria dell'adatomo.
5. **Adatomo su (111).** Ripetere il punto 4 con la cella (111) di
   `fcc111a336+1.txt` ($L_x=L_y=20.3817$ Å) e confrontare le due orientazioni.
   È probabile che, a temperatura ambiente e nello stesso intervallo di tempo,
   l'adatomo diffonda su una sola superficie o su entrambe?

## Stato

| | Cosa | Risultato | Dove |
|---|---|---|---|
| **1** | Taglio netto a 50 e 500 K | 50 K: ottimale 20 fs; 500 K: nessun passo, $\delta E/\lvert\langle E\rangle\rvert\approx1.6\times10^{-4}$ anche a 0.25 fs | [punti 1–2](../../notebooks/06_esercizio1_md/punti_1_2_passo_temporale.ipynb), [soluzione 1–3](../../notebooks/06_esercizio1_md/esercizio1_soluzione.ipynb) |
| **2** | $P_7$: coerenza a 50 K; passo a 500, 1000, 2000 K | stesse medie del taglio netto; 6, 4, 3 fs | idem |
| **3** | 10 ps dal minimo; traiettorie | $\langle T\rangle/(T_\text{ini}/2)=1.01$, 1.03, 1.00, 0.91 | [soluzione 1–3](../../notebooks/06_esercizio1_md/esercizio1_soluzione.ipynb) |
| **4** | Adatomo su (100), PBC solo in $x$ e $y$ | | da fare |
| **5** | Adatomo su (111) e confronto | | da fare (manca `fcc111a336+1.txt`) |

## Note specifiche di questa versione

- **5000 passi fissi:** 5 ps a 1 fs (2 ps di statistica dopo $t_{th}$), 125 ps
  a 25 fs.
- **«From point 3,».** Nel PDF questa frase resta in sospeso dopo il preambolo;
  il paragrafo sulla *steepest descent* chiarisce che dal punto 3 si parte da un
  minimo.
- **Potenziale nei punti 3–5:** il testo non lo ripete, ma chiede i passi del
  punto 2, quindi si usa il $P_7$.
- **Punti 4–5:** il lato $L_x=16.6416$ Å è proprio $4a$ con $a=4.1604$ Å. Il
  modulo `md_p7` gestisce già le PBC solo in $x$ e $y$
  (`periodic=(True, True, False)`, con un test dedicato), e `steepest_descent`
  accetta qualunque modello, quindi anche la lastra.
