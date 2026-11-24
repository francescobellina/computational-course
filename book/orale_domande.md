(sec:orale-domande)=
# Domande per l'orale

All'orale si presentano con delle slide i risultati dei tre esercizi d'esame.
Questa pagina raccoglie le domande che è ragionevole aspettarsi, una sezione
per esercizio. Ogni risposta è nascosta, così ci si può esercitare: si apre
con un clic. Le risposte riportano i numeri delle simulazioni e il punto in
cui si trovano (notebook o capitolo), così ogni affermazione si può
ritrovare su una slide.

:::{tip} Come rispondere
1. **La fisica:** il principio o la condizione in gioco.
2. **Il dato:** il numero o il grafico che lo mostra.
3. **La verifica:** il controllo fatto per escludere le altre spiegazioni.

Ad esempio: «il taglio netto non conserva l'energia (fisica); a 300 K
$\delta E/|\langle E\rangle|$ resta a $7\times10^{-5}$ anche a 1 fs
(dato); gli attraversamenti di $r_c$ non dipendono da $\Delta t$, e con il
$P_7$ il problema sparisce (verifica)».
:::

## Esercizio 1 — MD di Ag con Lennard-Jones

Riferimenti principali: il notebook della consegna
[Exercise 1 (PART 1 + 2)](../notebooks/06_esercizio1_md/esercizio1_part1_2.ipynb),
la [teoria della steepest descent](06_esercizio1_md/steepest_descent.md) e il
riquadro sulle [condizioni di $T_f=T(0)/2$](#sec:tini-mezzi).

### Domanda tipo

:::{important} «Lei osserva che per alcune temperature la regola $\langle T\rangle=T_\text{ini}/2$ non vale. Come mai? Quali condizioni sono venute meno?»
**Da dove viene la regola.** Si parte da un minimo, quindi tutta l'energia in
eccesso è cinetica, $K_0=\tfrac32Nk_BT_\text{ini}$. L'energia si conserva,
$K_0=\langle K\rangle+\langle V-V_\text{min}\rangle$, e per oscillazioni
armoniche vale l'equipartizione $\langle K\rangle=\langle V-V_\text{min}\rangle$.
Quindi $\langle K\rangle=K_0/2$ e $\langle T\rangle=T_\text{ini}/2$.

**Le tre condizioni:** (1) partenza da un minimo; (2) approssimazione armonica,
cioè $k_BT\ll\varepsilon$ e oscillazioni piccole rispetto alla distanza tra
primi vicini; (3) equilibrio, con la media presa dopo il transiente $t_{th}$.

**Quale viene meno, e dove:**

- **Condizione 1, nel punto 1.** Il reticolo del file non è un minimo: il
  rilassamento libera $\Delta U=0.22$ eV, e $\langle T\rangle$ sale di
  $\Delta U/(3Nk_B)=3.4$ K. A 30 K il rapporto è $1.21$, a 2500 K l'effetto
  non si vede. La previsione coincide con la misura entro 3 K.
- **Condizione 2, al primo ordine, ad alta $T$.** Sviluppando il potenziale
  di un legame, $V=\tfrac12kx^2+cx^3+dx^4$, si ottiene
  $\langle T\rangle/(T_\text{ini}/2)\simeq1-A\,k_B\langle T\rangle$, con
  $A=15c^2/(2k^3)-3d/k^2$. Per LJ $A\varepsilon=0.63>0$: il legame si allunga
  più facilmente di quanto si comprima, il potenziale prende più della metà
  dell'energia e $\langle T\rangle$ scende **linearmente**. Nel cluster con
  LJ senza taglio la pendenza è circa la metà di quella di un singolo legame.
- **Condizione 2, del tutto, sopra circa 1000 K.** Gli atomi di superficie
  lasciano il sito (39 a 2500 K) e il sistema esce dal bacino del minimo.
  Minimizzando la configurazione finale si trova un minimo **più alto** del
  cubo di $+1.9$ eV: si sono formati difetti, che trattengono energia
  potenziale. Il rapporto scende a $0.86$.
- **Un effetto del modello, tra 100 e 900 K.** Il rapporto supera 1 (fino a
  $1.033$) solo con il raccordo $P_7$, che è molto curvo tra 4.2 e 4.5 Å e si
  comporta come un irrigidimento ($A<0$). Il controllo a 500 K dà $0.976$ con
  il taglio netto e $0.983$ con LJ senza taglio.
- **La condizione 3 è rispettata:** si scartano i primi 3 ps. $T(t)$ dimezza in
  25–40 fs e poi fluttua del 4%, come previsto per un solido armonico in NVE.

**In una frase:** la regola vale a bassa temperatura ($1.002$ a 30 K).
Peggiora linearmente per l'anarmonicità e perde significato quando gli atomi
escono dal bacino di partenza.

*Dove:* notebook PART 1 + 2, §3 e §4.
:::

### A. Il modello

**A1. Perché serve un raggio di taglio, e perché proprio 4.5 Å?**

:::{dropdown} Risposta
- Senza taglio ogni atomo interagisce con tutti gli altri: costo $O(N^2)$, e
  con le PBC infinite immagini. Il potenziale LJ decade come $r^{-6}$, quindi
  i contributi lontani sono piccoli.
- 4.5 Å cade tra i secondi vicini ($r_2=a=4.16$ Å) e i terzi
  ($r_3=a\sqrt{3/2}=5.09$ Å): si tengono primi e secondi vicini, si
  trascurano gli altri.
:::

**A2. Perché il taglio netto non conserva l'energia?**

:::{dropdown} Risposta
- $\phi_{LJ}(r_c)=-0.054$ eV $\neq0$: quando una coppia attraversa $r_c$,
  l'energia salta di 0.054 eV, e la forza ha una delta (impulso) che
  l'integratore non può seguire.
- È un errore del **modello**, non dell'integratore: ridurre $\Delta t$ non
  lo elimina. Nel grafico di $E_\text{tot}(t)$ si vedono i gradini.
:::

**A3. Perché un polinomio di grado 7, e come ha verificato il raccordo?**

:::{dropdown} Risposta
- Le condizioni sono 8: $\phi$, $\phi'$, $\phi''$ e $\phi'''$ uguali a LJ in
  $r_p$ e nulli in $r_c$. Servono quindi 8 coefficienti, cioè grado 7.
- Ho calcolato $P_7^{(k)}$ in $r_p$ e $r_c$ per $k=0\dots3$ con i
  coefficienti di `poly7.py`: le condizioni valgono fino a qualche $10^{-6}$.
:::

**A4. Perché le condizioni valgono solo fino a $10^{-6}$ e non alla precisione di macchina?**

:::{dropdown} Risposta
- I coefficienti arrivano a $10^8$ con segni alterni, mentre $P_7$ vale meno
  di 0.1 eV: nella somma si perdono cifre per cancellazione. Il residuo è
  10 000 volte più piccolo del salto del taglio netto.
- C'è un effetto visibile: a 30 K, con 1–2 fs, $\delta E/|\langle E\rangle|$
  si ferma a circa $10^{-7}$. Lo causa lo scalino di $-3.9\times10^{-6}$ eV
  in $r_p$. Correggendo solo il coefficiente A, il pavimento scende da
  $1.0\times10^{-7}$ a $3.0\times10^{-8}$. È comunque 100 volte sotto la
  soglia.
- *Dove:* [punti 1–2](../notebooks/06_esercizio1_md/punti_1_2_passo_temporale.ipynb), §3.1.
:::

**A5. Come calcola le forze? Come evita il doppio conteggio?**

:::{dropdown} Risposta
- $\mathbf F(k)=\sum_j f(r_{kj})(\mathbf r_k-\mathbf r_j)/r_{kj}$ con
  $f=-\mathrm d\phi/\mathrm dr$: LJ fino a $r_p$, $-P_7'$ tra $r_p$ e $r_c$,
  zero oltre.
- Con le liste dei vicini complete ogni coppia compare due volte: l'energia
  va divisa per 2, le forze no. Con un ciclo su $j>i$ si aggiunge $+\mathbf f$
  a $i$ e $-\mathbf f$ a $j$ (terza legge di Newton).
- **Verifiche:** le forze coincidono con le differenze finite dell'energia,
  $\sum_k\mathbf F(k)=0$ e il momento totale è nullo (test in
  `tests/test_md_p7.py`). La versione in chiaro (`calcForces`) coincide con
  quella compilata entro $10^{-13}$.
:::

**A6. Perché un cluster senza PBC? Cosa cambierebbe con le PBC?**

:::{dropdown} Risposta
- Il testo parla di centro del cluster e di vertici del cubo: è un oggetto
  finito, con le superfici.
- Con le PBC non ci sarebbero superfici. In un cristallo periodico a 500 K,
  con il taglio netto, nessuna coppia attraversa $r_c$ e il criterio si
  rispetta fino a 6 fs. Nel cluster sono gli atomi di superficie, meno
  legati, a portare le coppie oltre $r_c$.
- *Dove:* [Esercizi CMS 6](../notebooks/05_molecular_dynamics/esercizi_cms6.ipynb), Parte 2.
:::

**A7. Perché nella cella solo 4 degli 8 vertici del cubo sono occupati?**

:::{dropdown} Risposta
La cella è $4\times4\times4$ celle fcc, con i siti $(i,j,k)\,a/2$ e
$i+j+k$ pari, $i,j,k=0\dots7$. Il vertice $(0,0,0)$ è occupato, mentre
$(7,7,7)$ ha somma dispari e non lo è: i vertici occupati sono 4, alternati.
Ho verificato che la stessa costruzione riproduce esattamente
`fcc100a108.txt`.
:::

**A8. Lennard-Jones è un buon potenziale per l'argento?**

:::{dropdown} Risposta
È un potenziale **a coppie**: l'energia di un legame non dipende
dall'intorno. Nei metalli il legame è collettivo, e l'energia di un atomo
dipende da quanti vicini ha: è un effetto *many-body*. Per i metalli si usano
quindi potenziali many-body. LJ va bene per studiare i metodi (integratore,
passo, equipartizione), non per previsioni quantitative sull'Ag.
:::

### B. Integratore e passo temporale (punto 1)

**B1. Perché velocity Verlet?**

:::{dropdown} Risposta
- È reversibile nel tempo e simplettico: l'energia non deriva, ma oscilla
  attorno a un valore costante, con un errore $O(\Delta t^2)$.
- Per un oscillatore armonico conserva **esattamente** una quantità vicina
  all'energia, $\tfrac12p^2+\tfrac12\omega^2q^2(1-\omega^2\Delta t^2/4)$
  (energia «ombra»). L'ho verificato numericamente.
- Richiede una sola valutazione delle forze per passo.
:::

**B2. Come definisce il criterio sul passo? Che cosa non vede?**

:::{dropdown} Risposta
- $\delta E/|\langle E\rangle|<10^{-5}$, con $\delta E$ la deviazione
  standard di $E_\text{tot}$ dopo $t_{th}$: misura le **fluttuazioni**
  dell'energia attorno alla sua media.
- Non vede uno spostamento costante della media. A 50 K con 20 fs la media
  è più alta di $E_0$ del 5% di $K_0$ (energia ombra, $\omega\Delta t\approx1$
  per il modo più veloce), ma $\langle T\rangle$ cambia meno dello 0.2%
  rispetto a 2 fs.
- *Dove:* [soluzione 1–3](../notebooks/06_esercizio1_md/esercizio1_soluzione.ipynb), nota del §3.
:::

**B3. Perché il passo ottimale scende con la temperatura?**

:::{dropdown} Risposta
- Con il $P_7$ si ottengono 20 fs a 30 K, 8 fs a 300 K, 3 fs a 1200 K e 2 fs
  a 2500 K.
- Ad alta $T$ gli atomi sono più veloci e le oscillazioni più ampie: in un
  passo percorrono più strada e incontrano zone del potenziale più ripide
  (la parete repulsiva) e più anarmoniche. L'errore per passo cresce, quindi
  il passo va accorciato.
:::

**B4. Perché l'errore cresce come $\Delta t^2$, e come lo si vede?**

:::{dropdown} Risposta
Velocity Verlet è del secondo ordine: l'errore globale sull'energia va come
$\Delta t^2$. In scala log-log le curve sono rette di pendenza 2, quasi
parallele tra loro, finché la simulazione è stabile.
:::

**B5. Perché con il taglio netto a 30 K un passo valido esiste e a 300 K no?**

:::{dropdown} Risposta
- A 30 K nessuna coppia attraversa $r_c$: i due potenziali coincidono, e sono
  validi tutti i passi fino a 25 fs.
- A 300 K ci sono già 46 attraversamenti in 8 ps, e
  $\delta E/|\langle E\rangle|\approx7\times10^{-5}$ anche a 1 fs: la curva è
  **piatta**. A 2500 K gli attraversamenti sono circa 14 500.
- Gli attraversamenti dipendono dalla temperatura, non dal passo: ridurre
  $\Delta t$ non aiuta.
:::

**B6. Che cosa limita il passo massimo? Perché le simulazioni divergono?**

:::{dropdown} Risposta
- Per un oscillatore, Verlet è stabile solo se $\omega\Delta t<2$. Il modo più
  veloce del cluster ha frequenza 7.6 THz (periodo 131 fs), quindi il limite
  lineare è circa 42 fs.
- Molto prima di questo limite l'accuratezza peggiora. Ad alta $T$ gli urti
  sulla parete repulsiva sono più violenti, e la simulazione diverge già da
  circa 18 fs (a 2500 K; a 300 K da 25 fs).
:::

**B7. Perché almeno 8000 passi? Quanto dura una prova?**

:::{dropdown} Risposta
La durata dipende da $\Delta t$: 8 ps a 1 fs, di cui 5 ps di statistica
dopo $t_{th}=3$ ps; 200 ps a 25 fs. Con meno passi, ai passi piccoli resterebbe
troppo poco tempo dopo la termalizzazione per una media affidabile.
:::

**B8. Il passo ottimale è robusto?**

:::{dropdown} Risposta
$\delta E$ viene da una sola traiettoria, quindi cambia di qualche punto
percentuale con il seme delle velocità. L'ho controllato con 4 semi: i passi
ottimali reggono, ma a volte con un margine di pochi punti percentuali sulla
soglia. Dove il margine è stretto, il passo immediatamente più piccolo è la
scelta prudente.

*Dove:* [punti 1–2](../notebooks/06_esercizio1_md/punti_1_2_passo_temporale.ipynb), §4.
:::

**B9. Come ha scelto il passo per le temperature intermedie del punto 2?**

:::{dropdown} Risposta
Ho usato il passo della prima temperatura del punto 1 **non inferiore**, ad
esempio 700 K → passo di 1200 K (3 fs). È prudente perché il passo valido
scende con $T$. In tutti i run da 50 ps $\delta E/|\langle E\rangle|$ resta
sotto $10^{-5}$.
:::

### C. Traiettorie (punto 1)

**C1. Perché l'atomo al vertice oscilla più di quello al centro?**

:::{dropdown} Risposta
Il vertice ha 3 primi vicini invece di 12, quindi è trattenuto da meno legami
e il potenziale attorno a lui è più morbido: a parità di energia, l'ampiezza è
maggiore. A 30 K l'rms è $0.075$ Å contro $0.025$ Å, circa 3 volte.
:::

**C2. Che cosa cambia a 2500 K?**

:::{dropdown} Risposta
Il centro vibra ancora attorno al sito: rms $0.19$ Å, al massimo $0.5$ Å,
molto meno della distanza tra primi vicini (2.94 Å). Il vertice si allontana
fino a $2.6$ Å e vaga sulla superficie: l'interno resta solido, la superficie
diventa mobile.
:::

**C3. Perché a 30 K la nuvola del vertice è spostata rispetto al sito iniziale?**

:::{dropdown} Risposta
Nel punto 1 si parte dal reticolo del file, che non è un minimo. Il vertice
si rilassa verso l'interno del cluster mentre oscilla. Lo spostamento,
qualche centesimo di Å verso $+x,+y$, coincide con quello trovato dalla
*steepest descent* (0.05 Å verso il centro).
:::

**C4. Perché ha tolto il momento angolare dalle velocità iniziali?**

:::{dropdown} Risposta
In un cluster isolato il momento angolare si conserva. Se non è nullo, il
cluster **ruota rigidamente** per tutto il run: a 2500 K i vertici, a 12.6 Å
dal centro, si sposterebbero di circa 4 Å in 10 ps per la sola rotazione, e
la traiettoria non mostrerebbe più le vibrazioni. `assign_vel` toglie solo la
quantità di moto; poi le velocità si riscalano a $T_\text{ini}$.
:::

### D. Steepest descent

**D1. Come funziona? Quali sono le unità di $C$?**

:::{dropdown} Risposta
- Ogni atomo si sposta lungo la propria forza,
  $\mathbf r(k)\leftarrow\mathbf r(k)+C\,\mathbf F(k)$, finché
  $\max_k|\mathbf F(k)|<F_\text{tol}$. Le forze sono quelle della MD.
- È il flusso di gradiente discretizzato, cioè un moto in un mezzo molto
  viscoso: l'energia viene dissipata e il sistema si ferma nel minimo.
- $[C]=\text{Å}/(\text{eV/Å})=$ **Å²/eV**. Il testo scrive «Å/eV»: il valore
  è 0.005, l'unità corretta è Å²/eV.
:::

**D2. Come si sceglie $C$? Cosa succede se è troppo grande?**

:::{dropdown} Risposta
- Vicino al minimo, ogni modo normale si moltiplica per $(1-C\lambda)$ a ogni
  passo: si converge solo se $C<2/\lambda_\text{max}$. Dall'Hessiana del
  cluster, $\lambda_\text{max}=25.8$ eV/Å² e quindi $C_\text{crit}=0.078$
  Å²/eV. Il $C=0.005$ del testo è circa 1/15 del limite: sicuro, ma lento.
- Con $C=1.05\,C_\text{crit}$ il cluster **esplode**: l'energia sale fino a
  $-275$ eV (il minimo è $-453.67$ eV) e 56 atomi restano senza vicini.
- Il numero di iterazioni va come $1/C$: $n\cdot C\approx3$ Å²/eV.
- *Dove:* [steepest descent](../notebooks/06_esercizio1_md/steepest_descent.ipynb), §4.
:::

**D3. Perché $F_\text{max}$ può crescere mentre l'energia scende?**

:::{dropdown} Risposta
L'algoritmo minimizza l'energia, che è una somma su tutti gli atomi.
$F_\text{max}$ guarda un solo atomo, che può peggiorare per un passo mentre il
resto del cluster migliora. L'energia invece deve scendere sempre: è il
controllo che conta.
:::

**D4. Perché il criterio usa la forza massima? $10^{-3}$ o $10^{-5}$ eV/Å?**

:::{dropdown} Risposta
- Il massimo garantisce che **ogni** atomo sia in equilibrio; una media
  nasconderebbe un atomo fuori posto.
- Con $10^{-3}$ eV/Å l'energia resta sopra il minimo di
  $1.6\times10^{-5}$ eV, e le posizioni ne distano meno di $10^{-3}$ Å.
  L'errore scende come $F^2$. $10^{-5}$ eV/Å (valore della slide 37)
  raddoppia le iterazioni per una differenza irrilevante nella MD.
:::

**D5. Attenzione: $F_\text{max}<F_\text{tol}$ basta per dire che si è al minimo?**

:::{dropdown} Risposta
No. Nell'esempio con $C$ troppo grande gli atomi si allontanano finché non
sentono più forze, e il criterio è «soddisfatto» con un cluster distrutto.
Serve sempre anche il controllo che l'energia scenda.
:::

**D6. La steepest descent trova il minimo globale? È un minimo o una sella?**

:::{dropdown} Risposta
- Trova solo il minimo **locale** del bacino di partenza, perché non sale mai.
  Per un altro minimo bisogna cambiare la configurazione iniziale.
- Partendo da una configurazione simmetrica, la discesa conserva la simmetria
  e potrebbe fermarsi su una sella. L'Hessiana nel punto finale esclude questo
  caso: a parte 6 autovalori nulli (3 traslazioni e 3 rotazioni), sono tutti
  positivi ($\ge0.12$ eV/Å²).
:::

**D7. Durante la minimizzazione il cluster trasla o ruota? Come cambia la sua forma?**

:::{dropdown} Risposta
- Non trasla né ruota: con forze di coppia centrali $\sum_k\mathbf F(k)=0$ e
  il momento totale è nullo, quindi $C\mathbf F$ non contiene moti rigidi
  (zero entro $10^{-13}$).
- Si contrae di poco: 598 iterazioni, $\Delta E=-0.22$ eV, spostamento
  massimo 0.05 Å ai vertici, verso l'interno.
:::

**D8. Come ha verificato il suo codice di minimizzazione?**

:::{dropdown} Risposta
Ho riprodotto l'esempio della slide 39 con il file da 864 atomi: $E$ passa da
$-1681.86$ a $-1682.39$ eV, e servono 1802 iterazioni con $C=0.003$ e 540 con
$C=0.01$.
:::

**D9. Esistono metodi migliori?**

:::{dropdown} Risposta
Il gradiente coniugato evita lo zig-zag nelle valli strette; i metodi
quasi-Newton (L-BFGS) stimano l'Hessiana; FIRE, molto usato nelle simulazioni
atomistiche, è una MD con velocità modificate e passo adattivo. Per 256 atomi
la steepest descent converge in meno di un secondo.
:::

### E. Temperatura ed equipartizione (punto 2)

**E1. Perché nel confronto con il punto 1 $\langle T\rangle$ è più alto? Di quanto?**

:::{dropdown} Risposta
Il reticolo del file non è un minimo: c'è un'energia potenziale in eccesso
$\Delta U=0.22$ eV, che si divide anch'essa a metà. Quindi
$\langle T\rangle_1=\langle T\rangle_2+\Delta U/(3Nk_B)$, cioè $+3.4$ K a
tutte le temperature, verificato entro 3 K. In proporzione pesa molto a
bassa $T$: a 30 K il rapporto è $1.21$ invece di $1.00$.
:::

**E2. Perché ad alta temperatura $\langle T\rangle<T_\text{ini}/2$? Perché lo scarto cresce linearmente?**

:::{dropdown} Risposta
- Al primo ordine nell'anarmonicità,
  $\langle T\rangle/(T_\text{ini}/2)\simeq1-A\,k_B\langle T\rangle$, con
  $A=15c^2/(2k^3)-3d/k^2$.
- Per un legame LJ il termine cubico prevale, $A\varepsilon=0.63$: un legame
  asimmetrico (facile da allungare, difficile da comprimere) mette più energia
  nel potenziale. Per questo lo scarto è negativo e lineare in $T$.
- Nel cluster con LJ senza taglio la pendenza è circa la metà
  ($A_\text{eff}/A=0.45$–$0.57$): ogni atomo è tenuto da molti legami in
  direzioni diverse.
- *Dove:* PART 1 + 2, §4.3.
:::

**E3. Perché tra 100 e 900 K $\langle T\rangle$ è invece **sopra** $T_\text{ini}/2$?**

:::{dropdown} Risposta
È un effetto del raccordo. Tra 4.2 e 4.5 Å il $P_7$ deve annullare energia e
tre derivate in 0.3 Å, quindi è molto curvo: fino a 5.9 eV/Å², contro 0.16 di
LJ in $r_p$. Si comporta come un irrigidimento ($A<0$). Controllo a 500 K: il
rapporto è $1.033$ con il $P_7$, $0.976$ con il taglio netto e $0.983$ con LJ
senza taglio.
:::

**E4. Che cosa succede sopra circa 1000 K?**

:::{dropdown} Risposta
Gli atomi di superficie lasciano il sito (da 1 a 900 K a 39 a 2500 K), e la
loro ampiezza di oscillazione arriva al 25% della distanza tra primi vicini.
Il sistema esce dal bacino. Minimizzando la configurazione finale si trova un
minimo più alto del cubo di $+1.9$ eV: sono difetti che immagazzinano energia
potenziale, come un calore latente. Per questo $\langle T\rangle$ scende più
del previsto.
:::

**E5. Con LJ senza taglio, a 2000 K, il rapporto torna vicino a 1. La regola torna a valere?**

:::{dropdown} Risposta
No. La configurazione finale minimizzata è 8–11 eV **sotto** il cubo: il
cluster si è riorganizzato in una forma più stabile (il cubo con spigoli non è
la forma di minima energia). L'energia liberata lo scalda di oltre 100 K e
compensa per caso l'anarmonicità. Fuori dal bacino il rapporto non ha un
valore definito.
:::

**E6. A che cosa serve $t_{th}$? Cosa succede se non si scarta il transiente?**

:::{dropdown} Risposta
Partendo dal minimo, $T(t)$ dimezza in 25–40 fs (circa un quarto del periodo
di vibrazione più breve) e poi oscilla. Se la media includesse i primi
istanti, in cui $T\approx T_\text{ini}$, sarebbe spostata verso l'alto e
servirebbero diversi ps per diluirli. Con $t_{th}=3$ ps si media solo lo stato
di equilibrio.
:::

**E7. Perché la temperatura istantanea fluttua? Di quanto?**

:::{dropdown} Risposta
Il sistema è finito: $T=2K/(3Nk_B)$ è una somma su $3N$ termini e fluttua
come $1/\sqrt N$. In NVE, per un solido armonico,
$\delta T/\langle T\rangle=\sqrt{1/3N}=0.036$ per $N=256$ (Lebowitz, Percus e
Verlet). Misuro circa 0.04. Il valore canonico, $\sqrt{2/3N}=0.051$, è più
grande, perché in NVE l'energia totale è fissata.
:::

**E8. La regola $T_\text{ini}/2$ richiede l'ergodicità?**

:::{dropdown} Risposta
Nel caso armonico no: ogni modo normale, da solo, divide in media a metà la
propria energia tra cinetica e potenziale. Basta mediare su tempi lunghi
rispetto ai periodi. L'equipartizione **tra** modi diversi (e quindi la
distribuzione di Maxwell) richiede invece che l'energia si scambi, cosa che
l'anarmonicità permette.
:::

**E9. In pratica, come si fissa la temperatura di una simulazione NVE?**

:::{dropdown} Risposta
Si parte dal minimo con $T_\text{ini}=2T$ e si scarta il transiente. Ad alta
$T$ serve una correzione, perché la regola non è più esatta: ad esempio, per
$\langle T\rangle\approx1000$ K servono circa 2300 K. In alternativa si usa un
termostato (NVT), come nella MD di proteine con GROMACS
([approfondimento](06_esercizio1_md/approfondimento.md)).
:::

### F. Domande generali e di metodo

**F1. Quale ensemble simula? Come definisce la temperatura?**

:::{dropdown} Risposta
NVE (microcanonico): velocity Verlet conserva l'energia. La temperatura è
quella cinetica, $T=2K/(3Nk_B)$. Togliere quantità di moto e momento angolare
rimuove 6 gradi di libertà: è un effetto dello 0.8% sul valore assoluto di
$T$, che però si cancella nel rapporto $\langle T\rangle/(T_\text{ini}/2)$
perché $T_\text{ini}$ è calcolata nello stesso modo.
:::

**F2. Quali unità usa il codice?**

:::{dropdown} Risposta
eV, Å e s. La massa è in eV·s²/Å², dove 1 unità = 16 kg, perché
1 eV·s²/Å² $=1.602\times10^{-19}$ J s² / $10^{-20}$ m². $k_B=1/11603$ eV/K.
:::

**F3. Come sa che il codice è corretto?**

:::{dropdown} Risposta
Con test automatici:
- forze uguali alle differenze finite dell'energia;
- forza totale e momento nulli;
- conservazione dell'energia in NVE;
- convergenza della steepest descent;
- PBC per direzione.

Più l'esempio della slide 39 riprodotto, e la versione in chiaro che coincide
con quella compilata.
:::

**F4. Quanto costa una simulazione? Come scalerebbe con $N$?**

:::{dropdown} Risposta
Il calcolo delle forze scorre tutte le coppie, quindi costa $O(N^2)$: per 256
atomi, circa 0.1 ms per passo con Numba (10 volte più veloce di NumPy). Per
sistemi grandi si usano liste di celle ($O(N)$) e, in parallelo, la
decomposizione in domini con un «halo» di spessore $r_c$ (vedi HPC4AI,
capitolo MPI, nell'[approfondimento](06_esercizio1_md/approfondimento.md)).
:::

**F5. Quanto sono affidabili i numeri? Ha stimato gli errori?**

:::{dropdown} Risposta
I semi delle velocità sono fissi, quindi i risultati sono riproducibili. Per
le grandezze vicine a una soglia, o mediate nel tempo, ho ripetuto i run con
semi diversi:
- 4 semi per il passo ottimale;
- 3 semi per $\langle T\rangle$ nel punto 2, con deviazioni standard tra
  0.0 e 5.7 K.
:::

## Esercizio 2 — Monte Carlo cinetico

*Da completare quando l'esercizio sarà svolto.*

## Esercizio 3 — Metropolis Monte Carlo

*Da completare quando l'esercizio sarà svolto.*
