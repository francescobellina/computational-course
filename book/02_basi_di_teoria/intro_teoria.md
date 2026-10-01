# Introduzione al corso

In questa prima parte del corso vengono introdotti i concetti di base della meccanica statistica classica, dell'approssimazione adiabatica e del moto nucleare, dei potenziali interatomici, della dinamica molecolare e dei metodi Monte Carlo. L'approssimazione adiabatica viene anche chiamata **approssimazione di Born-Oppenheimer (B.O.A.)**.

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

![Regione accessibile nello spazio delle fasi per l'ensemble microcanonico](images/microcanonical_phase_space.png)

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

![Microstati dello spazio delle fasi pesati con il fattore di Boltzmann](images/canonical_phase_space.png)

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

> **Nota:** vale se il sistema parte da un minimo (V(q(0))), l'approssimazione armonica è valida e il sistema raggiunge l'equilibrio ma quindi nella simulazione trascureremo i punti iniziali in cui il sistema non è in equilibrio e la temperatura oscilla attorno a $T_f$.

> **Nota:** vale se il sistema parte da un minimo (V(q(0))), l'approssimazione armonica è valida e il sistema raggiunge l'equilibrio.

# 3: INTERATOMIC POTENTIALS

## Potenziali interatomici

L'energia potenziale di un sistema di \(N\) atomi può essere sviluppata come somma di contributi a uno, due, tre o più corpi:

$$
V (1,2,...,N) = \sum_i v_1(i) + \sum_{i<j} v_2(i,j) + \sum_{i<j<k} v_3(i,j,k) + \cdots
$$

qui abbiamo single particle (spesso 0), 2-body (pair potential), 3-body (bond), ecc.
La più semplice approssimazione è il **potenziale di coppia**, in cui l'energia dipende solo dalla distanza tra coppie di atomi:

$$
V(\mathbf R_1,\ldots,\mathbf R_N)
=
\frac{1}{2}\sum_{i\neq j}
\phi\left(|\mathbf R_i-\mathbf R_j|\right).
$$

Questi modelli funzionano bene quando l'interazione è poco direzionale, mentre diventano insufficienti quando sono importanti gli angoli di legame o effetti many-body.

QUANDO POSSO USARE IL PAIR POTENTAIL? devo guardare il PACKING FRACTION (PF) e il numero di coordinazione Z. Se PF è alto e Z è alto, allora posso usare il pair potential. Se PF è basso e Z è basso, allora devo usare un potenziale many-body.

**NOTA**: Tenere a mente il concetto di **Nearest Neighbors**: per ogni atomo, il numero di atomi più vicini (primi vicini) è il numero di coordinazione Z. Il **packing fraction** PF è la frazione di volume occupata dagli atomi rispetto al volume della cella.

---

## Strutture cristalline

Per confrontare la compattezza dei reticoli si usa il **packing fraction**

$$
PF = \frac{V_{\mathrm{atomi}}}{V_{\mathrm{cella}}}.
$$

Assumendo gli atomi come sfere rigide tangenti:

$$
r = \frac{d_{nn}}{2}.
$$

### Simple Cubic (SC)

- Atomi per cella: \(1\)
- Primi vicini: \(Z=6\)
- Distanza tra primi vicini:

$$
d_{nn}=a
$$

- Packing fraction:

$$
PF_{SC}=\frac{\pi}{6}\approx 0.52
$$

La struttura è relativamente poco compatta.

### Body-Centered Cubic (BCC)

- Atomi per cella: \(2\)
- Primi vicini: \(Z=8\)

$$
d_{nn}=\frac{\sqrt{3}}{2}a
$$

$$
PF_{BCC}=\frac{\sqrt{3}\pi}{8}\approx 0.68
$$

È più compatta della struttura SC.

### Face-Centered Cubic (FCC)

- Atomi per cella: \(4\)
- Primi vicini: \(Z=12\)

$$
d_{nn}=\frac{\sqrt{2}}{2}a
$$

$$
PF_{FCC}=\frac{\sqrt{2}\pi}{6}\approx 0.74
$$

L'FCC è una struttura **close-packed**: ogni atomo ha il massimo numero di primi vicini possibile per un impacchettamento di sfere identiche.

### Struttura del diamante

La struttura del diamante può essere vista come due reticoli FCC traslati di

$$
\frac{1}{4}(1,1,1).
$$

- Atomi per cella convenzionale: \(8\)
- Primi vicini: \(Z=4\)

$$
d_{nn}=\frac{\sqrt{3}}{4}a
$$

$$
PF_{dia}=\frac{\sqrt{3}\pi}{16}\approx 0.34
$$

Ogni atomo forma quattro legami tetraedrici con angolo circa

$$
\theta \approx 109.5^\circ.
$$

Il diamante è quindi molto meno compatto dell'FCC, ma possiede legami covalenti fortemente direzionali.

| Struttura | Coordinazione \(Z\) | Packing fraction |
|---|---:|---:|
| SC | 6 | 0.52 |
| BCC | 8 | 0.68 |
| FCC | 12 | 0.74 |
| Diamante | 4 | 0.34 |

---

## Potenziali di coppia e struttura cristallina

Un potenziale di coppia assegna energia favorevole a ogni vicino posto vicino alla distanza di equilibrio. Di conseguenza tende a favorire strutture con elevato numero di coordinazione, come l'FCC.

Per questo motivo:

- nei **gas nobili** i potenziali di coppia funzionano molto bene;
- nei **metalli** possono descrivere qualitativamente la struttura, ma trascurano importanti effetti many-body;
- nei **solidi covalenti**, come Si e diamante, non sono sufficienti perché non descrivono la direzionalità dei legami.

Per materiali covalenti occorrono quindi termini angolari a tre corpi, come nel potenziale di Stillinger-Weber.

---

## Potenziale di Lennard-Jones

Il modello più noto di potenziale di coppia è il **Lennard-Jones 12-6**:

$$
\phi(r)
=
4\epsilon
\left[
\left(\frac{\sigma}{r}\right)^{12}
-
\left(\frac{\sigma}{r}\right)^6
\right].
$$

Il termine

$$
\left(\frac{\sigma}{r}\right)^{12}
$$

descrive la forte repulsione a corta distanza, mentre

$$
-\left(\frac{\sigma}{r}\right)^6
$$

rappresenta l'attrazione di van der Waals.

I due parametri principali sono:

- \(\epsilon\): profondità della buca di potenziale;
- \(\sigma\): distanza alla quale il potenziale si annulla.

Il minimo del potenziale si trova a

$$
r_{min}=2^{1/6}\sigma
$$

e vale

$$
\phi(r_{min})=-\epsilon.
$$

Il Lennard-Jones descrive particolarmente bene solidi di gas nobili come Ar e Kr, perché le loro interazioni sono deboli, isotrope e dominate dalle forze di van der Waals.

Poiché un potenziale di coppia favorisce un alto numero di vicini, il modello Lennard-Jones porta naturalmente a strutture compatte, in particolare FCC.



## NELLA PRATICA: