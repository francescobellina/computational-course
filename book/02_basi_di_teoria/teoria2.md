
# TEORIA 2 

<div style="background-color:#00a6ff2e; border-left:2px solid #00a6ff2e; padding:12px 16px; border-radius:6px;">
qui si introducono concetti di base della teoria dei solidi, come potenziali interatomici, packing fraction, nearest neighbors, strutture cristalline e potenziali di coppia, lennard-jones, ecc.
E sopratutto metodo di CUTOFF RADIUS sul potenziale per il calcolo efficiente delle interazioni.

</div>




## 1: Potenziali interatomici

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

## 2: Strutture cristalline

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



### NELLA PRATICA:



## 4: LENNARD JONES --- IGNORE ---


## 5: CUTOFF METHOD --- IGNORE ---