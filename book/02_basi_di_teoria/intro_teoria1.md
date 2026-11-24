# TEORIA 1

In questa prima parte del corso vengono introdotti i concetti di base della meccanica statistica classica, dell'approssimazione adiabatica e del moto nucleare, E poi dei potenziali interatomici, della dinamica molecolare e dei metodi Monte Carlo. L'approssimazione adiabatica viene anche chiamata **approssimazione di Born-Oppenheimer (B.O.A.)**.

# 1. Classical Statistical Mechanics

## Ensemble NVE e formalismo microcanonico

Nell'ensemble microcanonico l'energia totale del sistema è costante.

```{figure} ../../figures/energy_surface.png
:label: energy-surface
:width: 80%
:align: center

Superficie di energia nello spazio delle fasi per un sistema a energia totale fissata.
```

L'ensemble microcanonico descrive un sistema isolato:

- **Ensemble:** $(N,V,E)$
- **Sistema:** isolato

Indichiamo con $(q,p)$ un punto nello spazio delle fasi, con $H(q,p)$ l'Hamiltoniana e con $W$ il valore fissato dell'energia totale, cioè $E=W$.

Per un sistema con $N$ particelle in tre dimensioni, tutti gli integrali nello spazio delle fasi sono $6N$-dimensionali. In particolare, $dq\,dp$ rappresenta l'elemento di volume nello spazio delle fasi.

### Media di un'osservabile

Data una densità di probabilità $\rho(q,p)$, la media di un'osservabile $A(q,p)$ è

$$
\langle A\rangle_{\rho}
=
C\iint A(q,p)\,\rho(q,p)\,dq\,dp,
$$

dove la costante di normalizzazione è

$$
C=
\frac{1}{\displaystyle \iint \rho(q',p')\,dq'\,dp'}.
$$

Se $\rho$ è già normalizzata, allora $C=1$.

### Distribuzione microcanonica

Nell'ensemble microcanonico sono accessibili soltanto i microstati la cui energia appartiene a un piccolo intervallo attorno a $W$:

$$
\rho_{\mathrm{mc}}(q,p)=
\begin{cases}
C, & W\le H(q,p)\le W+\delta W,\\[4pt]
0, & \text{altrimenti}.
\end{cases}
$$

Nel limite in cui l'energia è fissata esattamente, la distribuzione può essere espressa mediante la delta di Dirac:

$$
\boxed{
\rho_{\mathrm{mc}}(q,p)
=
C\,\delta\!\bigl(H(q,p)-W\bigr)
}
$$

dove $C$ è la costante di normalizzazione, che può essere pensata uguale a $1$ quando la distribuzione è già normalizzata.

### Media microcanonica

Per uno strato energetico finito $W\le H\le W+\delta W$, la media microcanonica di un'osservabile è

$$
\boxed{
\langle A(q,p)\rangle_{\mathrm{mc}}
=
\frac{
\displaystyle \iint_{W\le H(q,p)\le W+\delta W}
A(q,p)\,dq\,dp
}{
\displaystyle \iint_{W\le H(q,p)\le W+\delta W}
dq\,dp
}
}
$$

Equivalentemente, imponendo il vincolo $H=W$ mediante la delta di Dirac,

$$
\boxed{
\langle A\rangle_{\mathrm{mc}}
=
\frac{
\displaystyle \iint
A(q,p)\,\delta\!\bigl(H(q,p)-W\bigr)\,dq\,dp
}{
\displaystyle \iint
\delta\!\bigl(H(q,p)-W\bigr)\,dq\,dp
}
}
$$

Anche in questo caso la costante di normalizzazione $C$ si semplifica nel rapporto.

### Postulato di equiprobabilità di Gibbs

La distribuzione microcanonica è un'espressione diretta del **postulato di equiprobabilità di Gibbs**:

> Un sistema isolato all'equilibrio ha la stessa probabilità di trovarsi in ciascun microstato accessibile.

Un microstato è *accessibile* se soddisfa il vincolo sull'energia totale, cioè $H(q,p)=W$, oppure, nella descrizione mediante uno strato energetico finito,

$$
W\le H(q,p)\le W+\delta W.
$$

La media microcanonica valuta quindi l'osservabile $A$ su tutti i microstati accessibili, ossia su tutti i modi in cui le particelle possono disporsi e muoversi nello spazio delle fasi mantenendo la stessa energia totale.

In sintesi, la media d'ensemble nell'ensemble microcanonico è la media aritmetica o integrale dell'osservabile ristretta all'ipersuperficie dello spazio delle fasi sulla quale l'energia totale vale $W$.

## Ensemble NVT e formalismo canonico

Nell'ensemble canonico il sistema è a contatto termico con un bagno: $N$, $V$ e la temperatura $T$ sono fissati, mentre il sistema può scambiare energia con l'ambiente.

La densità di probabilità è proporzionale al **fattore di Boltzmann**:

$$
\rho_{\mathrm{can}}(q,p)
=
C\,e^{-\beta H(q,p)}.
$$

Di conseguenza,

$$
\boxed{
\langle A\rangle_{\mathrm{can}}
=
\frac{
\displaystyle \iint A(q,p)e^{-\beta H(q,p)}\,dq\,dp
}{
\displaystyle \iint e^{-\beta H(q,p)}\,dq\,dp
}
}
$$

poiché la costante di normalizzazione si semplifica nel rapporto.

Se gli stati sono discreti,

$$
\langle A\rangle_{\mathrm{can}}
=
\frac{
\displaystyle\sum_i A_i e^{-\beta E_i}
}{
\displaystyle\sum_i e^{-\beta E_i}
}.
$$

Se invece i livelli energetici possono essere trattati come continui, la somma viene sostituita dall'integrale sullo spazio delle fasi introdotto sopra.

### Caso di particelle non interagenti

Se l'Hamiltoniana dipende soltanto dagli impulsi ed è separabile,

$$
H(\mathbf q,\mathbf p)
=
H(\mathbf p)
=
\sum_{i=1}^{N}\frac{\mathbf p_i^2}{2m}
=
\sum_{i=1}^{N} h(\mathbf p_i),
$$

con

$$
\mathbf p_i=(p_{x_i},p_{y_i},p_{z_i}),
\qquad
h(\mathbf p_i)=\frac{\mathbf p_i^2}{2m},
$$

allora

$$
\langle H\rangle_{\mathrm{can}}
=
N\,
\frac{
\displaystyle\int d\mathbf p\;h(\mathbf p)e^{-\beta h(\mathbf p)}
}{
\displaystyle\int d\mathbf p'\;e^{-\beta h(\mathbf p')}
}.
$$

Per un sistema di particelle **non interagenti**, il problema a $N$ particelle si riduce quindi allo studio del problema a singola particella:

$$
\boxed{
\langle H\rangle_{\mathrm{can}}
=
N\langle h\rangle_{\mathrm{can}}
}
$$

Nel seguito saranno invece di interesse soprattutto le **particelle interagenti**, che costituiscono la maggior parte dei sistemi reali.

## Rappresentazione nello spazio delle fasi degli ensemble NVE e NVT

Consideriamo un sistema classico di $N$ particelle, descritto nello spazio delle fasi dalle coordinate collettive

$$
(Q,P)
=
(q_1,\ldots,q_{3N},p_1,\ldots,p_{3N}),
$$

e quindi da uno spazio di dimensione $6N$.

### Ensemble microcanonico

L'ensemble **microcanonico** descrive un **sistema isolato**: il numero di particelle $N$, il volume $V$ e l'energia $E$ sono fissati.

I microstati accessibili appartengono a un sottile strato energetico dello spazio delle fasi:

$$
W \le H(Q,P) \le W+\delta W.
$$

METTERE IMMAGINE

Per il postulato di equiprobabilità, tutti i microstati accessibili hanno lo stesso peso. La media microcanonica di un'osservabile $A(Q,P)$ è quindi

$$
\langle A\rangle_{\mathrm{mc}}
=
\frac{
\displaystyle \int_{W\le H(Q,P)\le W+\delta W}
A(Q,P)\,dQ\,dP
}{
\displaystyle \int_{W\le H(Q,P)\le W+\delta W}
dQ\,dP
}.
$$

In questo ensemble l'**energia è fissata**, mentre grandezze derivate come la temperatura possono mostrare fluttuazioni microscopiche.

### Ensemble canonico

Nell'ensemble **canonico**, poiché il sistema può scambiare energia con il bagno termico, i microstati possono avere energie differenti e non sono equiprobabili. (Si parla di microstati perchè in teoria si formalizza il tutto partendo da un sistema S e un grande resevoir R (o termostato) per cui il sistema totale è isolato, per cui globalmente il sistema è microcanonico quindi si parla di microstati e si usa il formalismo microcanonico studiando però la ripartizione dell'energia in S ecc.) 

Il loro peso è determinato dal **fattore di Boltzmann**

$$
e^{-\beta H(Q,P)},
\qquad
\beta=\frac{1}{k_B T}.
$$

METTERE IMMAGINE

La media canonica di $A$ è

$$
\boxed{
\langle A\rangle_{\mathrm{can}}
=
\frac{
\displaystyle \int A(Q,P)e^{-\beta H(Q,P)}\,dQ\,dP
}{
\displaystyle \int e^{-\beta H(Q,P)}\,dQ\,dP
}
}
$$

Il denominatore coincide, a eventuali fattori di normalizzazione vicino, con la funzione di partizione classica:

$$
Z
=
\int e^{-\beta H(Q,P)}\,dQ\,dP.
$$

A temperatura fissata, gli stati a energia minore hanno peso maggiore e l'**energia del sistema fluttua** attorno al proprio valore medio.

### Differenza essenziale

| Ensemble | Grandezze fissate | Energia | Peso dei microstati |
|---|---|---|---|
| Microcanonico | $N,V,E$ | fissata | uniforme nella regione accessibile |
| Canonico | $N,V,T$ | fluttua | $\propto e^{-\beta H(Q,P)}$ |


```{figure} ../../figures/energy_temp_fluct.png
:label: energy-temp-fluct
:width: 80%
:align: center

Confronto qualitativo delle fluttuazioni di energia e temperatura.
```

Nel microcanonico $E$ è costante; nel canonico è invece $T$ a essere imposta dal bagno termico, mentre $E$ fluttua.

## Ensemble statistici e limite termodinamico

La scelta dell'ensemble dipende dai vincoli fisici imposti al sistema:

- **microcanonico**: sistema isolato, con $N$, $V$ ed energia $E$ fissati;
- **canonico**: sistema a contatto con un bagno termico, con $N$, $V$ e temperatura $T$ fissati; l'energia può fluttuare;
- **gran canonico**: il sistema può scambiare sia energia sia particelle, quindi si fissano tipicamente $T$, $V$ e potenziale chimico $\mu$.

### Limite termodinamico ed equivalenza degli ensemble

Nel limite termodinamico

$$
N,V\to\infty,
\qquad
\frac{N}{V}=\text{costante},
$$

le fluttuazioni relative delle grandezze estensive diventano trascurabili. In particolare, per l'energia nell'ensemble canonico,

$$
\frac{\sigma_E}{\langle E\rangle_{\mathrm{can}}}
\longrightarrow 0.
$$

Per quantità estensive, tipicamente,

$$
\frac{\sigma_E}{\langle E\rangle}
\sim N^{-1/2}.
$$

Per questo motivo, sotto le usuali ipotesi di equivalenza degli ensemble, nel limite termodinamico le medie ottenute nei diversi ensemble coincidono e i diversi ensemble forniscono gli stessi risultati per le osservabili macroscopiche.

<span style="color:red">-&gt;</span>Ciò permette di scegliere, a seconda del problema, il formalismo più conveniente. In particolare, per molti **calcoli analitici** è conveniente lavorare nell'ensemble canonico.

<span style="color:red">-&gt;</span>Dal punto di vista dinamico, tuttavia, una traiettoria hamiltoniana di un sistema isolato conserva l'energia; per questo motivo la descrizione naturale della traiettoria è quella **microcanonica**.

## Media microcanonica e superficie di energia

Per un'osservabile $A(q,p)$, la media microcanonica può essere interpretata come una media uniforme sulla regione dello spazio delle fasi compatibile con una stretta finestra energetica:

$$
\langle A\rangle_{\mu\mathrm{can}}
=
\frac{1}{\Omega(E,\Delta E)}
\int_{E\le H(q,p)\le E+\Delta E}
dq\,dp\,A(q,p),
$$

dove $\Omega(E,\Delta E)$ è il volume della stessa regione energetica e serve a normalizzare la media.

Per un sistema con $N$ particelle in tre dimensioni, lo spazio delle fasi ha dimensione $6N$. La condizione

$$
H(q,p)=E
$$

<div style="background-color:#fff3cd; border-left:2px solid #ff9900bb; padding:12px 16px; border-radius:6px;">vincola il moto alla superficie di energia, che ha dimensione 6N-1.
</div>

## Traiettoria e media temporale

L'evoluzione dinamica genera una traiettoria sulla superficie di energia:

$$
(q(t),p(t)).
$$

Lungo questa traiettoria si può definire la media temporale dell'osservabile:

$$
\langle A\rangle_T
=
\lim_{T\to\infty}
\frac{1}{T}
\int_0^T
A(q(t),p(t))\,dt.
$$

Dal punto di vista numerico, questa quantità viene approssimata seguendo la traiettoria per un tempo finito e campionandola a intervalli temporali discreti.

## Ergodicità

Il **postulato ergodico** collega la media d'ensemble alla media temporale. Se la dinamica esplora in modo rappresentativo tutti i microstati accessibili, allora

$$
\boxed{
\langle A\rangle_{\mathrm{ens}}
=
\lim_{\tau\to\infty}
\frac{1}{\tau}
\int_0^\tau
A(Q(t),P(t))\,dt
}
$$

In particolare, se il sistema è **ergodico** sulla superficie di energia, una traiettoria sufficientemente lunga esplora in modo rappresentativo la regione accessibile dello spazio delle fasi. In tal caso, per quasi tutte le condizioni iniziali,

$$
\langle A\rangle_T
=
\langle A\rangle_{\mu\mathrm{can}}.
$$

Questa relazione collega una simulazione dinamica, basata su una singola traiettoria, alle medie statistiche dell'ensemble microcanonico.

Le medie statistiche richiedono in generale integrali in uno spazio di dimensione $6N$ e, per sistemi realistici, non sono quasi mai calcolabili direttamente. Due strategie numeriche fondamentali sono:

- **Molecular Dynamics (MD):** genera una traiettoria dinamica e stima una **media temporale**;
- **Monte Carlo (MC):** campiona direttamente la distribuzione dell'ensemble e stima una **media d'ensemble**.

In presenza di ergodicità e di un campionamento sufficientemente lungo, le due procedure devono fornire la stessa media di equilibrio.

## Teorema KAM

Il [teorema di Kolmogorov-Arnol'd-Moser (KAM)](https://it.wikipedia.org/wiki/Teorema_di_Kolmogorov-Arnol%27d-Moser) riguarda sistemi hamiltoniani quasi integrabili.

Per perturbazioni sufficientemente piccole, molti tori invarianti del sistema integrabile sopravvivono. Su questi tori il moto può essere quasi-periodico e, nel caso di frequenze incommensurabili, la traiettoria può essere densa **sul toro invariante**, ma non necessariamente sull'intera superficie di energia.

Il teorema KAM non garantisce quindi l'ergodicità globale; al contrario, mostra come possano esistere regioni invarianti dello spazio delle fasi che impediscono a una singola traiettoria di esplorare tutta la superficie microcanonica.

<div style="background-color:#fff3cd; border-left:2px solid #ff9900bb; padding:12px 16px; border-radius:6px;">

<b>IN BREVE:</b> la traiettoria <b>"is infinite dense on the energy phase-space surface"</b>.<br><br>

<b>COMPUTAZIONALMENTE:</b> avremo dei <b>TIME STEP</b>, se la traiettoria è densa abbastanza.

</div>

## Quadro complessivo

Il collegamento tra descrizione dinamica e statistica può essere riassunto come

$$
\text{traiettoria hamiltoniana}
\;\xrightarrow[\text{se ergodica}]{}\;
\langle A\rangle_T
=
\langle A\rangle_{\mu\mathrm{can}}
$$

e, nel limite termodinamico e sotto le usuali condizioni di equivalenza degli ensemble,

$$
\langle A\rangle_{\mu\mathrm{can}}
\simeq
\langle A\rangle_{\mathrm{can}}
\simeq
\langle A\rangle_{\mathrm{gran\,can}}.
$$

In sintesi,

$$
\boxed{
\text{Microcanonico: } E\ \text{fissata}
\qquad\Longleftrightarrow\qquad
\text{Canonico: } T\ \text{fissata, }E\ \text{fluttua}
}
$$

La differenza tra i due ensemble è importante a scala microscopica; per sistemi molto grandi, le fluttuazioni relative diventano piccole e gli ensemble risultano termodinamicamente equivalenti nelle condizioni usuali.

In pratica: **la dinamica conserva l'energia e suggerisce il microcanonico; il limite termodinamico rende spesso equivalenti gli ensemble e consente di usare quello più conveniente per il calcolo.**
In laboratorio spesso è piu facile avere T costante, quindi ensemble canonico, ma in simulazioni numeriche spesso si lavora con l'ensemble microcanonico ecc.

---
---

# 2:ADIABATIC APPROXIMATION AND NUCLEAR MOTION
B.O.A.
GS of electrons (...)
quindi ELECTRONIC HAMITLONIAN AND WAVEFUNCTION AT GS + KNOWN GUESS OF POTENTIAL (INTERTOMIC)

PANORAMICA:
1) SOLVING SCHRODINGER EQUATION FOR ELECTRONS (GS)--> DFT (difficile)
2) NEWTON EQUATION FOR NUCLEI (classical)--> MOLECULAR DYNAMICS (piu facile, ma molte simulazioni richiedono molto tempo, molte particelle ecc)
3) AB INIT IO MOLECULAR DYNAMICS (AIMD)-->  CAR-PARRINELLO ( 1+2 .molto accurato) 

## NELLA PRATICA: 
scegliere un potenziale interatomico, risolvere NUMERICAMENTE le equazioni di Newton per i nuclei (moto atomico), campionare la traiettoria e calcolare le medie temporali delle osservabili di interesse, traiettorie ecc.

### TEMPERATURA E POTENZIALE
- t=0. suppongo che la posizione iniziale q(0) sia un minimo locale del mio (guess) potenziale V(q). Ho fissato l'energia totale a t=0.
- Al tempo t=tau, la traiettoria hamiltoniana esplora la superficie di energia. La temperatura è legata all'energia cinetica media dei nuclei.

se mi metto vicino al minimo: parabola approx, harmonic potential). 
L'energia totale è sempre conservata, avrò quindi:

## Energia totale costante

Al tempo iniziale:

$$
E_{\mathrm{tot}}(0)=E_{\mathrm{kin}}(0)+V(q(0))
$$

In una simulazione **NVE**:

$$
E_{\mathrm{tot}}(t)=E_{\mathrm{kin}}(t)+V(q(t))=\text{costante}
$$

Se il sistema parte da un minimo del potenziale $q_0$, vicino al minimo posso usare:

$$
V(q)\simeq V_0+\frac{1}{2}kx^2
$$

Inizialmente:

$$
E_{\mathrm{tot}}(0)=V_0+\frac{3}{2}Nk_BT(0)
$$

All'equilibrio, per equipartizione:

$$
\langle E_{\mathrm{kin}}\rangle
=
\langle V-V_0\rangle
=
\frac{3}{2}Nk_BT_f
$$

Per conservazione dell'energia:

$$
\frac{3}{2}Nk_BT(0)=3Nk_BT_f
$$

quindi:

$$
\boxed{T_f=\frac{T(0)}{2}}
$$

> **Esempio:** se $T(0)=100\,\mathrm{K}$, dopo il transiente la temperatura oscilla attorno a $50\,\mathrm{K}$. Quindi dopo un certo tempo la temperatura si stabilizza a $50\,\mathrm{K}$.

```{figure} ../../figures/check.png
:label: check_forsimulations
:width: 80%
:align: center

...Nel tempo perdo energia cinetica che è uguale a 3Nk_BT_f; Questo trick sarà un check utile nelle simulazioni!. quindi T(t)=50%T(0) dopo un certo t.
```

(sec:tini-mezzi)=
### Quando vale $T_f=T(0)/2$

:::{important} Le tre condizioni
La regola $T_f=T(0)/2$ vale se, **tutte insieme**:

1. **il sistema parte da un minimo**: $q(0)$ è un minimo di $V$, quindi
   $V(q(0))=V_0$ e all'inizio l'energia in eccesso è tutta cinetica;
2. **l'approssimazione armonica è valida**: le oscillazioni attorno al minimo
   sono piccole, $V\simeq V_0+\tfrac12kx^2$, il che richiede $k_BT$ molto
   minore delle energie di legame;
3. **il sistema raggiunge l'equilibrio**: si media su tempi lunghi rispetto ai
   periodi di vibrazione e, **nella simulazione, si trascurano i primi istanti**,
   in cui il sistema non è ancora in equilibrio. Dopo, la temperatura oscilla
   attorno a $T_f$.

Con queste tre condizioni vale l'**equipartizione** tra energia cinetica e
potenziale, $\langle E_\text{kin}\rangle=\langle V-V_0\rangle$, e da qui
$T_f=T(0)/2$.
:::

Ognuna delle tre condizioni, se viene meno, sposta $T_f$ in un modo
riconoscibile. I numeri qui sotto vengono dal cluster di 256 atomi di Ag
dell'Esercizio 1
([notebook PART 1 + 2](../../notebooks/06_esercizio1_md/esercizio1_part1_2.ipynb), §4).

**1. Partenza fuori dal minimo.** Se $V(q(0))=V_0+\Delta U$, l'energia in
eccesso è $\tfrac32Nk_BT(0)+\Delta U$. In regime armonico si divide ancora a
metà, quindi $3Nk_BT_f=\tfrac32Nk_BT(0)+\Delta U$, cioè

$$
T_f=\frac{T(0)}2+\frac{\Delta U}{3Nk_B}.
$$

Lo spostamento assoluto non dipende dalla temperatura, ma il suo peso relativo
va come $1/T(0)$. Nel cluster di Ag non rilassato, $\Delta U=0.22$ eV porta il
rapporto $T_f/(T(0)/2)$ a $1.21$ a 30 K, mentre a 2500 K non lo cambia. Per
questo si parte da un minimo trovato con la *steepest descent*.

**2. Equilibrio e transiente.** Partendo dal minimo, $T(t)$ scende a circa
$T(0)/2$ in un quarto del periodo di vibrazione più breve (alcune decine di fs),
poi oscilla e si assesta. Se la media includesse questi primi istanti, in cui
$T\approx T(0)$, risulterebbe spostata verso l'alto: per questo si scarta il
tempo di termalizzazione $t_{th}$. Anche all'equilibrio la temperatura
istantanea fluttua, perché il sistema è finito: in NVE, per un solido armonico,
$\delta T/\langle T\rangle=\sqrt{1/3N}$ {cite}`lebowitz1967ensemble`, circa il
4% per $N=256$. Conta quindi la **media** su molti periodi. Nel caso armonico
non serve nemmeno che l'energia passi da un modo all'altro: ogni modo, da solo,
divide in media a metà la propria energia tra cinetica e potenziale.

**3. Anarmonicità.** Oltre la parabola, il potenziale di un legame è
$V(x)=\tfrac12kx^2+c\,x^3+d\,x^4+\dots$. All'equilibrio a temperatura $T$, al
primo ordine in $k_BT$ (momenti gaussiani $\langle x^4\rangle_0=3\sigma^4$,
$\langle x^6\rangle_0=15\sigma^6$, $\sigma^2=k_BT/k$):

$$
\langle E_\text{kin}\rangle=\tfrac12k_BT,\qquad
\langle V-V_0\rangle=\tfrac12k_BT+A\,(k_BT)^2,\qquad
A=\frac{15c^2}{2k^3}-\frac{3d}{k^2},
$$

e in NVE, a energia fissata,

$$
\frac{T_f}{T(0)/2}\simeq1-A\,k_BT_f .
$$

- **Termine cubico** (asimmetria del legame). Entra come $c^2$, quindi spinge
  sempre $A>0$: l'energia potenziale prende più della metà e $T_f<T(0)/2$.
- **Termine quartico** (irrigidimento, $d>0$). Spinge $A<0$, e $T_f>T(0)/2$.

Per un legame di Lennard-Jones il cubico prevale, $A=0.63/\varepsilon$: lo
scarto è negativo e cresce linearmente con la temperatura. La regola vale
quindi finché $k_BT\ll\varepsilon$, cioè finché l'ampiezza delle oscillazioni
resta molto minore della distanza tra primi vicini. Un raccordo molto curvo,
come il $P_7$ tra $r_p$ e $r_c$, agisce invece come un irrigidimento e porta
$T_f$ leggermente sopra $T(0)/2$: è un effetto del modello.

**4. Fuori dal bacino.** Ad alta temperatura alcuni atomi, per primi quelli di
superficie, lasciano il loro sito e il sistema visita altri minimi:
l'approssimazione armonica cade del tutto. Se i nuovi minimi sono più alti
(difetti), l'energia resta immagazzinata nel potenziale e $T_f$ scende ancora
di più, come accade al calore latente in una fusione. Se invece il sistema
trova un minimo più profondo (una struttura più stabile), l'energia liberata lo
scalda. In entrambi i casi $T_f/(T(0)/2)$ non ha più un valore definito, e il
risultato dipende da quali minimi vengono visitati.
