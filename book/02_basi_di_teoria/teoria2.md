
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

---

## 6: Struttura cristallina

*Basato sulle note del corso di Struttura della Materia (Prof. M. Bernasconi, Univ. Milano-Bicocca) {cite}`bonetti2022struttura`, Parte 4 (Fisica dello Stato Cristallino), §2 Reticoli.*

### Solidi e ordine a lungo raggio

- **Cristallino**: disposizione periodica degli atomi che si ripete indefinitamente nello spazio — il *reticolo di Bravais*. Mono-cristalli rari; quasi tutti i minerali sono policristalli (aggregati di micro-cristalliti).
- **Amorfo**: nessun ordine a lungo raggio; corrisponde a un liquido sottoraffreddato (vetri, gomme).
- **Policristallino**: molti cristalliti di orientazione diversa.

La struttura governa proprietà meccaniche (moduli, sfaldatura), elettriche e ottiche: queste sono in genere **anisotrope**, cioè dipendono dall'orientamento.

### Reticolo di Bravais e cella unitaria

La struttura di un cristallo si scompone in due ingredienti:

$$
\text{struttura cristallina} = \text{reticolo di Bravais} + \text{base}.
$$

Il reticolo è l'insieme dei punti

$$
\mathbf{R} = n_1 \mathbf{a}_1 + n_2 \mathbf{a}_2 + n_3 \mathbf{a}_3,
\qquad n_i \in \mathbb{Z}
$$

(eq. 4.1–4.2 delle note); la **base** è l'insieme di uno o più atomi (ioni, molecole) associato a ogni punto. La **cella primitiva** è il parallelepipedo sotteso dai vettori primitivi $\mathbf{a}_1,\mathbf{a}_2,\mathbf{a}_3$: ripetuto per traslazioni reticolari riempie tutto lo spazio, con volume

$$
V_{\mathrm{cella}} = (\mathbf{a}_1 \wedge \mathbf{a}_2)\cdot \mathbf{a}_3
$$

(eq. 4.3). La scelta dei vettori non è univoca, ma il volume è sempre lo stesso. I lati della cella sono le **costanti reticolari** $a,b,c$, in Ångström ($10^{-10}$ m).

```{figure} ../../figures/reticoli_bravais_14.png
:label: reticoli-14
:width: 45%
:align: center

I 14 reticoli di Bravais, classificati nei 7 sistemi cristallini. Immagine: Wikimedia Commons, CC BY-SA 4.0.
```

### I 7 sistemi cristallini e i 14 reticoli

La teoria dei gruppi impone che nello spazio tridimensionale esistano solo **14 reticoli di Bravais**, in **7 sistemi cristallini** (7 reticoli semplici + 7 centrati). Furono confermati sperimentalmente dalla diffrazione dei raggi X (von Laue, Bragg); per l'idrogeno, povero di elettroni, si usa la diffrazione neutronica.

| Sistema | Vincoli | Reticoli | Esempio |
|---|---|---|---|
| Cubico | $a=b=c$, tutti $90^\circ$ | P, I, F (3) | Cu, Ag, Fe $\alpha$ |
| Tetragonale | $a=b\neq c$, tutti $90^\circ$ | P, I (2) | Sn bianco |
| Ortorombico | $a\neq b\neq c$, tutti $90^\circ$ | P, C, I, F (4) | FeS$_2$ (pirite) |
| Trigonale | $a=b=c$, $\alpha=\beta=\gamma\neq90^\circ$ | P (1) | CaCO$_3$ (calcite) |
| Esagonale | $a=b\neq c$, $\alpha=\beta=90^\circ$, $\gamma=120^\circ$ | P (1) | Mg, Zn, Ti, grafite |
| Monoclino | $\alpha=\gamma=90^\circ\neq\beta$ | P, C (2) | Gesso |
| Triclino | tutti gli angoli $\neq90^\circ$ | P (1) | Turchese |

### Il sistema cubico: SC, BCC, FCC

Il sistema cubico (a massima simmetria) contiene i tre reticoli usati in simulazione: cubico semplice (SC/*cP*), a corpo centrato (BCC/*cI*), a facce centrate (FCC/*cF*). Contando le frazioni di atomo nella cella (un vertice è condiviso da 8 celle, un centro di faccia da 2):

$$
N_{SC} = 8\cdot\tfrac18 = 1,
\quad
N_{BCC} = 8\cdot\tfrac18 + 1 = 2,
\quad
N_{FCC} = 8\cdot\tfrac18 + 6\cdot\tfrac12 = 4.
$$

```{figure} ../../figures/cella_unitaria_sc.png
:label: cella-sc
:width: 30%
:align: center

Cubico semplice: 1 atomo/cella, $Z=6$, $r=a/2$. Immagine: Wikimedia Commons, CC0.
```

```{figure} ../../figures/cella_unitaria_bcc.png
:label: cella-bcc
:width: 30%
:align: center

Cubo a corpo centrato: 2 atomi/cella, $Z=8$, $r=\sqrt{3}\,a/4$. Immagine: Wikimedia Commons, CC0.
```

```{figure} ../../figures/cella_unitaria_fcc.png
:label: cella-fcc
:width: 30%
:align: center

Cubo a facce centrate: 4 atomi/cella, $Z=12$, $r=\sqrt{2}\,a/4$. Immagine: Wikimedia Commons, CC0.
```

Il rapporto $r(a)$ viene dalla direzione di contatto tra sfere: spigolo in SC, diagonale del corpo in BCC, diagonale di faccia in FCC. Il **numero di coordinazione** $Z$ è il numero di primi vicini.

| Struttura | Contatto | $r(a)$ | $Z$ | $d_{nn}$ | APF | Esempi: $a$ (Å) |
|---|---|---|---:|---|---:|---|
| SC | spigolo | $a/2$ | 6 | $a$ | 0.524 | Po (unico elemento) |
| BCC | diagonale corpo | $\sqrt{3}\,a/4$ | 8 | $\sqrt{3}\,a/2$ | 0.680 | Fe 2.87, Cr 2.88, W 3.16, Mo 3.15, Na 4.23 |
| FCC | diagonale faccia | $\sqrt{2}\,a/4$ | 12 | $\sqrt{2}\,a/2$ | 0.740 | Al 4.05, Cu 3.61, Ni 3.52, **Ag 4.09**, Au 4.08, Pt 3.92 |

Valori da tabelle 9–10 delle note: elementi della stessa colonna della tavola periodica spesso cristallizzano allo stesso modo. L'**Ag FCC (a = 4.09 Å)** è il sistema dell'esercitazione hands-on di questo corso.

### Fattore di impacchettamento atomico (APF)

Con gli atomi come sfere rigide di raggio $r$,

$$
\mathrm{APF} = \frac{N_{\mathrm{atomi}}\,\frac{4}{3}\pi r^3}{V_{\mathrm{cella}}},
$$

e le relazioni $r(a)$ della tabella:

$$
\mathrm{APF}_{SC} = \frac{\pi}{6} \approx 0.524,
\qquad
\mathrm{APF}_{BCC} = \frac{\sqrt{3}\,\pi}{8} \approx 0.680,
\qquad
\mathrm{APF}_{FCC} = \frac{\pi}{\sqrt{18}} \approx 0.740.
$$

**0.740 è il massimo per sfere rigide identiche**, raggiunto anche dall'esagonale compatto (HCP): le due strutture impilano i piani densi come ABAB... (HCP) invece che ABCABC... (FCC).

```{figure} ../../figures/impacchettamento_compatto.png
:label: close-packing
:width: 70%
:align: center

Impacchettamento compatto di sfere: a sinistra HCP (impilamento ABAB...), a destra FCC (ABCABC...). Immagine: Wikimedia Commons, pubblico dominio.
```

Come già anticipato in §1: **PF alto e $Z$ alto** → potenziale di coppia sufficiente (gas nobili, metalli); **PF e $Z$ bassi** → strutture aperte con legami direzionali, servono termini many-body (Si, diamante).

### Strutture con base: diamante, NaCl, CsCl

Con basi di atomi diversi si ottengono strutture composte, leggibili come sottoreticoli interpenetranti:

| Struttura | Reticolo | Atomi/cella | $Z$ | Esempi |
|---|---|---:|---:|---|
| Diamante | FCC + base 2 atomi | 8 | 4 | C 3.57, Si 5.43, Ge 5.66 |
| Zincoblenda (ZnS) | come diamante, sottoreticoli diversi | 8 | 4 | ZnS, GaAs, InP |
| NaCl | due FCC traslati di $a/2$ | 8 | 6 | alogenuri alcalini |
| CsCl | due cubici semplici | 2 | 8 | CsCl, CsBr, CsI |

Nel diamante i due vettori di base sono $\mathbf{0}$ e $\frac{a}{4}(1,1,1)$ (eq. 4.4): due FCC compenetrati, legami $sp^3$ tetraedrici $\theta\approx109.5^\circ$ (dettagli in §2). Il rapporto $r_+/r_-$ sceglie la struttura: NaCl per $0.414 < r_+/r_- < 0.732$, CsCl per ioni di taglia simile.

### Simmetrie e cella di Wigner-Seitz

Le operazioni di simmetria puntuale (rotazioni, riflessioni, inversioni) compatibili con i 14 reticoli sono **32 gruppi puntuali**; combinandoli con i reticoli si ottengono i **230 gruppi spaziali**: ogni cristallo periodico appartiene a esattamente uno (§2.2 delle note).

La cella elementare non è univoca, ma la scelta più naturale è la **cella di Wigner-Seitz** (§2.2.1): regione di spazio più vicina a un nodo reticolare che a ogni altro nodo, costruita con i piani che bisecano i segmenti verso i primi vicini. È una cella primitiva che conserva tutte le simmetrie del reticolo (poliedro di Voronoi del reticolo).

```{figure} ../../figures/cella_wigner_seitz_fcc.jpg
:label: wigner-seitz
:width: 30%
:align: center

Costruzione della cella di Wigner-Seitz (tridimensionale) per un reticolo cubico a facce centrate. Immagine: Wikimedia Commons, pubblico dominio.
```

### Reticolo reciproco e zona di Brillouin

Poiché la densità elettronica di un cristallo è periodica, $\rho(\mathbf{x}+\mathbf{r})=\rho(\mathbf{x})$ per ogni $\mathbf{r}$ del reticolo (eq. 4.5), la si può sviluppare in serie di Fourier su un reticolo duale detto **reticolo reciproco**:

$$
\rho(\mathbf{x}) = \sum_{\mathbf{G}} \tilde{\rho}(\mathbf{G})\,e^{i\mathbf{G}\cdot\mathbf{x}},
\qquad
\mathbf{G} = m_1\mathbf{b}_1 + m_2\mathbf{b}_2 + m_3\mathbf{b}_3,
\qquad m_i \in \mathbb{Z},
$$

dove i vettori primitivi reciproci $\mathbf{b}_i$ si costruiscono da quelli diretti $\mathbf{a}_i$ (eq. 4.10–4.12):

$$
\mathbf{b}_1 = 2\pi\frac{\mathbf{a}_2\wedge\mathbf{a}_3}{(\mathbf{a}_1\wedge\mathbf{a}_2)\cdot\mathbf{a}_3},
\qquad
\mathbf{b}_2 = 2\pi\frac{\mathbf{a}_3\wedge\mathbf{a}_1}{(\mathbf{a}_1\wedge\mathbf{a}_2)\cdot\mathbf{a}_3},
\qquad
\mathbf{b}_3 = 2\pi\frac{\mathbf{a}_1\wedge\mathbf{a}_2}{(\mathbf{a}_1\wedge\mathbf{a}_2)\cdot\mathbf{a}_3}.
$$

I due reticoli soddisfano $\mathbf{G}\cdot\mathbf{R} = 2\pi n$ (eq. 4.14) e hanno le dimensioni di un vettore d'onda. Il reciproco del reciproco è il reticolo diretto; in particolare **FCC e BCC sono uno il reciproco dell'altro**, mentre il reciproco del cubico semplice è ancora cubico semplice.

La cella di Wigner-Seitz del reticolo reciproco è la **prima zona di Brillouin**: è l'insieme dei punti raggiungibili dall'origine senza attraversare alcun piano di Bragg, e gode della periodicità $\varepsilon(\mathbf{k}+\mathbf{G})=\varepsilon(\mathbf{k})$ (eq. 4.31). La si usa per descrivere gli stati elettronici a bande e i fononi [§2.3 delle note {cite}`bonetti2022struttura`]; per un reticolo reciproco FCC (cioè un cristallo BCC) la prima zona di Brillouin è un dodecaedro rombico, per un reticolo BCC è un ottaedro troncato.

### Per il corso: condizioni al contorno periodiche

Nelle simulazioni (MD, Monte Carlo) la cella unitaria — spesso cubica — è replicata con **condizioni al contorno periodiche**. Due vincoli usati in tutto il corso:

1. il **raggio di cutoff** deve stare entro metà del lato: $r_c \le L/2$, altrimenti la sfera delle interazioni è contata due volte;
2. $L$ deve contenere più periodi della struttura, altrimenti il sistema si ordina artificialmente.

Esempio: per Ag FCC ($a=4.09$ Å) una cella $2\times2\times2$ ha $L\approx8.2$ Å e ammette $r_c\le4.1$ Å — scelta del cutoff ripresa nel hands-on dedicato.

---

