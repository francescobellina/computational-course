(sec:md-dinamica-molecolare)=
# Dinamica molecolare: equazioni del moto e algoritmo di Verlet

Questo capitolo introduce la *molecular dynamics* partendo dalle equazioni di
Newton: la teoria (Taylor, Verlet, errori, ensemble microcanonico, condizioni
iniziali), il setup del sistema e le unità di misura. Il codice eseguito
commentato passo passo e la lettura dei risultati sono nel laboratorio
[CMS 5](../../notebooks/laboratori/cms5/equazioni_del_moto.ipynb). Il riferimento sono le slide CMS 5; dove le slide
citano risultati di altri codici (per esempio LAMMPS), il valore viene
presentato come **riferimento** e confrontato con quanto produce il nostro
codice.

Sistema studiato: argento con potenziale di Lennard-Jones (stessi parametri
del CMS 4: $\sigma = 2.644$ Å, $\varepsilon = 0.345$ eV, $r_c = 4.5$ Å),
reticolo FCC perfetto con condizioni periodiche, energie in eV, distanze in Å,
tempi in s (fs e ps nei grafici).

## 1. Il problema: integrare le equazioni di Newton

Per un sistema di $N$ particelle le equazioni di Newton sono

$$
m_i \ddot{\vec r}_i = -\vec\nabla_{\vec r_i} V(\vec r_1, \dots, \vec r_N),
\qquad i = 1, \dots, N .
$$

Sono $3N$ equazioni differenziali del secondo ordine **accoppiate**: la forza
sulla particella $i$ dipende da tutte le altre attraverso il potenziale
$V$. Non esiste soluzione analitica generale: non si cerca di integrare a
mano, si usa un **metodo alle differenze finite**.

L'idea è la seguente. Il tempo viene discretizzato in passi $\Delta t$; sia
$\{(x, v)\}_t$ la configurazione (posizioni e velocità) al tempo $t$. Un
*algoritmo di integrazione* è una regola che, data la configurazione a
$t$, produce la configurazione a $t + \Delta t$:

$$
\{(x, v)\}_t \;\xrightarrow{\ \Delta t \ }\; \{(x, v)\}_{t+\Delta t}
\;\xrightarrow{\ \Delta t \ }\; \{(x, v)\}_{t+2\Delta t} \;\to\; \dots
$$

Tutta la qualità del metodo dipende da quanto è buona questa regola: gli
errori si accumulano passo dopo passo, quindi a ogni passo devono essere
piccoli.

## 2. Idea di base e sviluppo di Taylor

La mossa naturale è lo sviluppo di Taylor della posizione attorno al tempo
$t$. Con $v$, $a$, $b$ derivate rispetto al tempo:

$$
x(t+\Delta t) = x(t) + v(t)\,\Delta t + \tfrac{1}{2}a(t)\,\Delta t^2
+ \tfrac{1}{6}b(t)\,\Delta t^3 + \dots
$$

Se conosco $x, v, a, b$ al tempo $t$ posso calcolare $x(t+\Delta t)$ e, con
gli sviluppi analoghi, anche le derivate nei tempi successivi: in linea di
principio **genero l'evoluzione completa** del sistema. Il limite dello
sviluppo è il suo errore di troncamento: voglio errori piccoli anche per
passi $\Delta t$ "lunghi", così che la dinamica resti affidabile.

Restano due domande aperte, che guidano la costruzione degli algoritmi:

1. **Dove sono le equazioni di Newton** (cioè il potenziale atomistico) in
   questo schema? Lo sviluppo di Taylor è pura cinematica: di fisica c'è
   solo $a = f/m$, e la forza va calcolata **ogni passo** dal potenziale.
2. **Quanto è grave** il vincolo che la derivata temporale di $a$ sia
   costante ($\dot b = 0$)? Implica che l'accelerazione varia linearmente
   nel tempo: valido per pochi passi, ma la costanza di $b$ è un'ipotesi
   restrittiva se la mantengo per troppo tempo.

## 3. Errori di troncamento e scelta del time step

La qualità di un algoritmo si misura con un **test standard**: un sistema
isolato deve conservare l'energia totale $E = K + V$. Regola empirica del
corso:

$$
\frac{dE}{E} < 10^{-5}.
$$

Due vincoli sulla scelta di $\Delta t$:

- $\Delta t$ deve essere **molto più piccolo** dei tempi caratteristici dei
  processi fondamentali. Dalla curvatura del potenziale LJ al suo minimo
  (sezione 9.1 del notebook sulle equazioni del moto) si stima un periodo di vibrazione di reticolo di **0.353 ps**:
  quindi $\Delta t \ll 0.353$ ps.
- In pratica il vincolo sulla conservazione dell'energia è **più stringente**
  di quello sui periodi: il range utile è $\Delta t \sim 1\text{–}10$ fs.

Attenzione: a temperature più alte gli atomi si muovono di più, le vibrazioni
sono più ampie e il potenziale più anarmonico; può servire un $\Delta t$ più
piccolo. Il capitolo verificherà numericamente entrambi gli effetti
(sezione 11 del notebook sulle equazioni del moto).

## 4. Schema "di ordine superiore" (solo teoria)

Per avere un'idea di cosa cerca uno schema migliore, estendo lo sviluppo fino
a $\Delta t^4$ usando $x, v, a, b$ e ponendo $\dot b = 0$:

$$
\begin{aligned}
x(t+\Delta t) &= x + v\,\Delta t + \tfrac{1}{2}a\,\Delta t^2
                 + \tfrac{1}{6}b\,\Delta t^3 \\[2pt]
v(t+\Delta t) &= v + a\,\Delta t + \tfrac{1}{2}b\,\Delta t^2 \\[2pt]
a(t+\Delta t) &= a + b\,\Delta t \\[2pt]
b(t+\Delta t) &= b
\end{aligned}
$$

Ottenengo un sistema di quattro equazioni accoppiate in cui, nota la
configurazione $(x, v, a, b)$ a $t$, calcolo $(x, v, a, b)$ a $t+\Delta t$.
È un passaggio **concettuale**, non un algoritmo da usare: mostra che
servono quattro "livelli" di derivate e che tenere $b$ costante è il punto
debole. La conclusione è che serve un modo più efficiente di usare le
derivate note — che è esattamente ciò che fa Verlet.

## 5. L'algoritmo di Verlet

### 5.1 Verlet standard

L'idea di Verlet è espandere $x(t+\Delta t)$ **e** $x(t-\Delta t)$ al terzo
ordine e **sommarle**. I termini dispari si cancellano:

$$
x(t+\Delta t) + x(t-\Delta t) = 2x(t) + a(t)\,\Delta t^2
+ \mathrm{err}(\Delta t^4).
$$

Con $a = f/m$ (per ciascuna componente: sono $3N$ equazioni), riordino:

$$
\vec r_i(t+\Delta t) = 2\vec r_i(t) - \vec r_i(t-\Delta t)
+ \frac{\vec f_i(t)}{m_i}\,\Delta t^2 + \mathrm{error}(\Delta t^4).
$$

Proprietà:

- schema **semplice**: a ogni passo serve una sola valutazione delle forze;
- **conserva molto bene l'energia** anche con passi "grandi";
- è **reversibile nel tempo**: invertendo il tempo (e le velocità) si
  ripercorre la traiettoria. Questa è una proprietà di simmetria molto
  rara e utile come test.

Svantaggi: servono **tre tempi diversi** ($t-\Delta t$, $t$, $t+\Delta t$)
e le velocità si conoscono solo indirettamente, come differenza finita
centrata tra le posizioni "future" e "passate":

$$
\vec v(t) = \frac{\vec r(t+\Delta t) - \vec r(t-\Delta t)}{2\Delta t}
+ \mathrm{error}(\Delta t^2).
$$

### 5.2 Velocity Verlet (quello usato nel corso)

Algoritmo equivalente — produce **le stesse traiettorie** — ma che tratta le
velocità in modo diretto:

$$
\begin{aligned}
x(t+\Delta t) &= x(t) + v(t)\,\Delta t
                 + \tfrac{1}{2}a(t)\,\Delta t^2 + \mathrm{err}(\Delta t^4) \\[2pt]
v(t+\Delta t) &= v(t) + \frac{a(t) + a(t+\Delta t)}{2}\,\Delta t
                 + \mathrm{err}(\Delta t^3).
\end{aligned}
$$

Il ciclo di un passo è il seguente:

1. Conosco $x(t)$, $v(t)$ e quindi $a(t) = f(t)/m$ (dalla funzione forze).
2. Con la prima equazione calcolo $x(t+\Delta t)$.
3. Con la funzione forze **sulle nuove posizioni** calcolo $a(t+\Delta t)$.
4. Con la seconda equazione calcolo $v(t+\Delta t)$.
5. Ripeto dal passo 1.

C'è un apparente paradosso: il passo richiede $a(t)$ **e** $a(t+\Delta t)$,
ma $a(t+\Delta t)$ nasce da $x(t+\Delta t)$. Non c'è ambiguità nell'ordine:
prima si aggiornano le posizioni con $a(t)$, poi si valutano le forze sulle
posizioni nuove, poi si aggiornano le velocità con la media delle due
accelerazioni.

> **Nota sul codice.** Gli indici $(i)$ delle particelle non hanno nulla a
> che fare con il tempo: $i = 1 \dots N$ è l'atomo, non il passo. Non si
> salvano posizioni e velocità a tutti i tempi (servirebbero $O(N \times
> N_{steps})$ dati): i vettori `pos`, `vel`, `force` vengono **sovrascritti**
> a ogni passo, tenendo solo le osservabili che ci interessano.

## 6. Unità di misura

Il codice lavora in **unità di codice**: le unità sono scelte in modo che i
numeri restino $O(1)$. Energia in eV, lunghezze in Å, tempi in s (fs = $10^{-15}$ s,
ps = $10^{-12}$ s). Qual è l'unità di massa coerente? Da $E = mc^2$:

$$
[m] = \frac{\text{eV}\cdot\text{s}^2}{\text{Å}^2}.
$$

Conversione in kg: $1\,\text{eV} = 1.6\times10^{-19}$ J e
$1\,\text{Å}^2 = 10^{-20}\ \text{m}^2$, quindi

$$
1\,\frac{\text{eV}\cdot\text{s}^2}{\text{Å}^2}
= \frac{1.6\times10^{-19}\ \text{J}\cdot\text{s}^2}{10^{-20}\ \text{m}^2}
= 16\ \text{kg}.
$$

Per l'argento ($^{108}$Ag): 108 g di argento contengono una mole,
$6.023\times10^{23}$ atomi, quindi la massa di un atomo è
$108\times1.66\times10^{-27}$ kg (il fattore $1.66\times10^{-27}$ kg è
$1/6.023\times10^{23}$ di grammo). In unità di codice:

$$
m = \frac{108 \times 1.66\times10^{-27}}{16}.
$$

La costante di Boltzmann in queste unità è $k_B = 8.618461\times10^{-5}$ eV/K
(= $1/11603$ eV/K). Ne seguono due numeri utili: a temperatura ambiente ($300$ K) l'energia
termica è $k_B T = 0.0259$ eV, cioè circa $1/40$ eV; e viceversa
$1/40$ eV corrisponde a $T \approx 290$ K.

## 7. Ensemble microcanonico (NVE) e temperatura istantanea

Il nostro sistema è **isolato**: non scambia energia con l'esterno, quindi
viviamo nell'ensemble **microcanonico** (NVE) e l'energia totale

$$
E = K + V = \text{costante}
$$

(a meno dell'errore di troncamento dell'algoritmo, che è artefatto e si
riduce con $\Delta t$).

Nel microcanonico la temperatura **non è un parametro imposto**: è una
grandezza *definita* attraverso l'energia cinetica istantanea, sfruttando il
teorema di equipartizione. Con

$$
K(t) = \frac{1}{2}\sum_i m_i |\vec v_i(t)|^2
\qquad\text{e}\qquad
K(t) \equiv \frac{N_{dof}\,k_B\,T(t)}{2},
\qquad N_{dof}\approx 3N,
$$

si definisce

$$
\boxed{\,T(t) = \frac{2K(t)}{N_{dof}\,k_B}\,}
$$

Punti da tenere a mente:

- $T(t)$ **fluttua** nel tempo: non è costante come nell'ensemble canonico.
  Le fluttuazioni della temperatura cinetica scalano come $1/\sqrt{N}$, come
  quelle dell'energia cinetica. Le slide, in un punto, scrivono $1/N$:
  il coefficiente corretto è $1/\sqrt{N}$ e la sezione 4 del laboratorio
  [CMS 5](../../notebooks/laboratori/cms5/equazioni_del_moto.ipynb) lo **verifica
  numericamente** variando $N$.
- Sulla media temporale lunga si recupera il teorema di equipartizione,
  tipico del comportamento canonico: la media di $T(t)$ coincide con la
  temperatura dell'ensemble.
- Con il momento totale azzerato i gradi di libertà effettivi sono $3N-3$.
  Per coerenza con le slide qui si usa $N_{dof} = 3N$; per $N$ grande la
  differenza è trascurabile ($3/3N$), ma va **segnalata**.

> Due fluttuazioni diverse, da non confondere:
>
> - le fluttuazioni di $E$ sono **artificiali** (dovute al troncamento): si
>   riducono diminuendo $\Delta t$;
> - le fluttuazioni di $T$ sono **fisiche**: non si riducono con $\Delta t$;
>   per diminuirle serve un sistema più grande (numero di particelle $N$
>   maggiore).

## 8. Condizioni iniziali e assegnazione delle velocità

### 8.1 Posizioni iniziali

Con condizioni periodiche in tutte e tre le direzioni, il **reticolo
perfetto** è una configurazione di forze nulle: corrisponde a un minimo
$U_0$ dell'energia potenziale. Le velocità iniziali portano un'energia
cinetica $K_0 = \tfrac{3}{2}N k_B T_0$, quindi $E_0 = U_0 + K_0$.

Se $T_0$ è sufficientemente bassa il sistema resta vicino al minimo e il
potenziale si può trattare in **approssimazione armonica**: gli atomi
oscillano attorno alle posizioni di equilibrio e l'energia cinetica iniziale
si ripartisce con l'energia potenziale, con la conseguenza

$$
T_f \cong \tfrac{1}{2} T_i .
$$

Quindi, per simulare a $T = 100$ K si assegnano velocità corrispondenti a
$T_i = 200$ K. Ma $T_i$ **non ha significato fisico**: è solo il valore di
partenza; l'unica grandezza significativa è $T_f$, quella misurata dopo
l'equilibrazione. Se le posizioni non sono al minimo (per esempio senza PBC)
o se si va oltre il regime armonico, $T_i$ va **tarato** sui risultati della
simulazione: l'esercizio 2 del notebook sulle equazioni del moto misura $T_f/T_i = 0.503$ per $T_i = 1200$ K
(regola armonica, errore dello 0.65%), mentre a temperature più alte
l'anarmonicità allinea $T_f$ leggermente sopra $T_i/2$.

### 8.2 Distribuzione di Boltzmann

All'equilibrio (ensemble canonico, o microcanonico nel limite
termodinamico) le velocità seguono la distribuzione di Maxwell-Boltzmann:

$$
f(v_x)\,dv_x = \frac{1}{\sqrt{2\pi}}\sqrt{\frac{m}{k_BT}}\,
e^{-\frac{m v_x^2}{2k_BT}}\,dv_x .
$$

Potremmo assegnare direttamente questa distribuzione, ma il codice parte da
una distribuzione **più semplice — uniforme in $[-C, C]$** — e l'obiettivo
didattico è **verificare** che il sistema, evolvendo con le forze, si
equilibri verso la distribuzione di Boltzmann (sezione 10 del notebook sulle equazioni del moto).

### 8.3 Come si assegnano le velocità

Per ogni componente di ogni atomo si estrae un numero casuale uniforme in
$[-C, C]$ con

$$
C = \sqrt{\frac{3 k_B T}{m}},
$$

che garantisce l'**energia cinetica media corretta** (la varianza della
distribuzione uniforme è $C^2/3 = k_BT/m$, esattamente il valore di
equipartizione per componente). Poi due correzioni, **in quest'ordine**:

1. **Azzerare il momento totale.** La media finita di estrazioni casuali non
   dà $\langle v \rangle = 0$: il centro di massa avrebbe una velocità
   residua. Le equazioni di Newton conservano il momento, quindi quella
   deriva resterebbe **per sempre** e l'intera cella traslerebbe durante
   l'evoluzione (esercizio 1 del notebook sulle equazioni del moto).
2. **Riscala la temperatura** a $T$ desiderata: si calcola la $T'$ della
   distribuzione estratta e si moltiplicano tutte le velocità per
   $\sqrt{T/T'}$.

L'ordine conta: la rimozione del momento cambia la $T'$ (toglie energia
cinetica), quindi se si riscala prima e poi si azzera il momento la
temperatura finale non è più quella richiesta. Il **seme casuale è fisso**
(`33282739`) per rendere la simulazione riproducibile.
