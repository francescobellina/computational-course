(sec:es1-sd-teoria)=
# Steepest descent: teoria

Nel punto 2 dell'[Esercizio 1](intro.md) ogni simulazione parte da un
**minimo locale** dell'energia potenziale. Se si partisse dal reticolo ideale
del file, gli atomi non sarebbero in equilibrio: in MD l'energia potenziale in
eccesso diventerebbe energia cinetica e scalderebbe il sistema. Nel cluster
di 256 atomi a $T_\text{ini}=50$ K si ottiene infatti
$\langle T\rangle\approx28$ K invece di 25 K (vedi il
[notebook](../../notebooks/06_esercizio1_md/steepest_descent.ipynb), §6).

Questa pagina segue le slide 30–39 di CMS.6 {cite}`bergamaschini2026cms6`,
con le note prese a lezione, e integra due cose: l'analisi del passo $C$
vicino al minimo, standard nell'ottimizzazione numerica
{cite}`nocedal2006numerical`, e i metodi alternativi
{cite}`bitzek2006fire`. I numeri citati vengono dal notebook
[Steepest descent: implementazione e verifiche](../../notebooks/06_esercizio1_md/steepest_descent.ipynb).

## 1. La superficie di energia potenziale

:::{figure} ../../figures/CMS6_immagini/12_steepest_superficie_energia.png
:name: fig:es1-pes
:width: 80%

La superficie di energia potenziale (PES), disegnata in 2D; in realtà è
un'ipersuperficie in $3N$ dimensioni. La discesa lungo la forza porta al
minimo locale più vicino (slide 31–36).
:::

Una configurazione di $N$ atomi è un punto $\{\mathbf r_i\}$ in uno spazio a
$3N$ dimensioni, e l'energia potenziale $\phi(\{\mathbf r_i\})$ ne è una
funzione: la **superficie di energia potenziale** (*potential energy surface*,
PES). La forza sull'atomo $k$ è

$$
\mathbf F(k)=\sum_{j\neq k}\left[-\nabla_k\,\phi(r_{kj})\right].
$$ (eq:es1-sd-forza)

$\mathbf F(k)$ punta nel verso in cui l'energia scende più rapidamente, e il
suo modulo è tanto più grande quanto più ripida è la PES nel punto
$\mathbf r_k$.

Una configurazione di **equilibrio** è un punto in cui la forza è nulla su
tutti gli atomi: $\mathbf F(k)=0$ per ogni $k$. Trovare un minimo vuol dire
quindi trovare il punto della PES in cui non agisce più nessuna forza. La
condizione però non basta: le forze sono nulle anche nei massimi e nei
**punti di sella**. La PES ha molti minimi, separati da selle. L'obiettivo
non è il minimo assoluto, ma il minimo locale nel cui **bacino**
(*basin*) si trova la configurazione di partenza. Il bacino è l'insieme delle
configurazioni da cui la discesa porta a quel minimo.

:::{note} Le domande delle note alla slide 31
**«Cosa succede ai primi vicini e al cluster?»** Gli atomi di superficie
hanno meno vicini degli atomi interni e, rilassando, si avvicinano a quelli
che restano: il cluster si contrae. Nel cluster di 256 atomi lo spostamento
più grande è quello dei vertici, $0.05$ Å verso il centro, meno del 2% della
distanza tra primi vicini.

**«E alle rotazioni?»** L'energia dipende solo dalle distanze tra gli atomi,
quindi non cambia se il cluster trasla o ruota rigidamente. Il minimo non è
un punto isolato, ma una famiglia di configurazioni equivalenti, e
l'Hessiana ha 6 autovalori nulli: 3 traslazioni e 3 rotazioni. La discesa non
si muove però lungo queste direzioni. Con forze di coppia centrali,
$\mathbf F_{kj}=f(r_{kj})\,(\mathbf r_k-\mathbf r_j)/r_{kj}=-\mathbf F_{jk}$,
quindi

$$
\sum_k\mathbf F(k)=0,\qquad
\sum_k\mathbf r_k\times\mathbf F(k)=\sum_{k<j}(\mathbf r_k-\mathbf r_j)\times\mathbf F_{kj}=0,
$$

e lo spostamento $C\,\mathbf F(k)$ non contiene né traslazioni né rotazioni
rigide. Il notebook lo verifica: centro di massa e rotazione restano fermi a
meno di $10^{-12}$. Con le PBC, anche solo in $x$ e $y$ come per una lastra,
la cella rompe l'invarianza per rotazione e restano solo le 3 traslazioni.

**«E a proposito delle posizioni iniziali? E quelle di equilibrio?»** Le
posizioni iniziali sono quelle del file, cioè il reticolo ideale con
$a=4.1604$ Å, che **non** è un equilibrio per il cluster con questo
potenziale. Le posizioni di equilibrio sono quelle trovate dalla
minimizzazione, e diventano l'array delle posizioni iniziali della MD.
:::

## 2. L'algoritmo

L'idea è semplice. Si sposta ogni atomo «un po'» nella direzione della sua
forza; si arriva così in un punto a energia più bassa, e si ripete finché si è
«abbastanza vicini» al minimo (slide 32–35):

$$
\delta\mathbf r(k)=C\,\mathbf F(k),\qquad
\mathbf r_k\leftarrow\mathbf r_k+C\,\mathbf F(k).
$$ (eq:es1-sd-passo)

:::{warning} Unità di $C$
Dall'equazione {eq}`eq:es1-sd-passo`, $[C]=[\delta r]/[F]=\text{Å}/(\text{eV/Å})=\text{Å}^2/\text{eV}$.
Il testo d'esame scrive «$C=0.005$ Å/eV»: il valore è quello, l'unità
corretta è Å²/eV.
:::

L'equazione {eq}`eq:es1-sd-passo` è la discretizzazione, con il metodo di
Eulero esplicito, del **flusso di gradiente** $\mathrm d\mathbf r_k/\mathrm d\tau=\mathbf F(k)$.
Fisicamente è il moto di atomi immersi in un mezzo molto viscoso, dove l'attrito
annulla l'inerzia e la velocità è proporzionale alla forza. La MD conserva
l'energia e fa oscillare gli atomi attorno al minimo; la *steepest descent*
invece la **dissipa**, ed è per questo che si ferma nel minimo.

Lo pseudocodice della slide 38 usa $C=0.005$ Å²/eV e $F_\text{tol}=10^{-3}$
eV/Å, come il testo d'esame:

```python
# configurazione iniziale pos
Csteep = 0.005
ftoll = 1.e-3

for iStep in range(0, maxStep):  # non si cicla all'infinito se non converge
    # liste dei vicini
    forces = calcForces(pos, nNbrs, whichNbrs)  # la stessa funzione della MD (con il P7)
    maxf = np.max(np.sqrt(forces[:, 0]**2 + forces[:, 1]**2 + forces[:, 2]**2))
    if maxf < ftoll:
        break  # convergenza: si esce dal ciclo
    else:
        pos = pos + Csteep * forces
```

Le forze vengono dalla **stessa funzione** usata nella MD e nel raccordo
polinomiale. Nel progetto l'algoritmo è `steepest_descent` del modulo
`computational_course.md_p7`.

(sec:es1-sd-passo)=
## 3. Quanto vale $C$?

:::{figure} ../../figures/CMS6_immagini/13_steepest_passo_convergenza.png
:name: fig:es1-passo
:width: 85%

Effetto di $C$ piccolo e grande, e criterio di convergenza (slide 37).
:::

La slide dà la risposta qualitativa:

- **$C$ piccolo:** moltissimi passi minuscoli;
- **$C$ grande:** se non si va in crash, si può non convergere o rimbalzare
  avanti e indietro attorno al minimo.

Vicino al minimo questa intuizione diventa un criterio preciso. Si chiamino
$\mathbf r^*$ il minimo e $\mathbf u=\mathbf r-\mathbf r^*$ lo scostamento
(vettore a $3N$ componenti). Al secondo ordine

$$
\phi\simeq\phi^*+\tfrac12\,\mathbf u^{\mathsf T}H\,\mathbf u,\qquad
\mathbf F=-H\,\mathbf u,
$$

dove $H$ è l'**Hessiana**, la matrice delle derivate seconde dell'energia.
Un passo {eq}`eq:es1-sd-passo` dà $\mathbf u_{n+1}=(1-CH)\,\mathbf u_n$.
Nella base dei modi normali di $H$, cioè gli autovettori con curvatura
$\lambda_i\ge0$, ogni componente evolve per conto suo:

$$
q_i^{(n)}=(1-C\lambda_i)^n\,q_i^{(0)}.
$$ (eq:es1-sd-modi)

Da {eq}`eq:es1-sd-modi` seguono quattro conseguenze.

1. **Stabilità.** Si converge solo se $|1-C\lambda_i|<1$ per tutti i modi,
   cioè

   $$
   0<C<C_\text{crit}=\frac{2}{\lambda_\text{max}}.
   $$ (eq:es1-sd-stabilita)

   Per $1<C\lambda_i<2$ il fattore è negativo: la componente cambia segno a
   ogni passo, e questo è il «rimbalzo» della slide. Per $C\lambda_i>2$
   cresce in modo esponenziale, e il sistema va in crash.
2. **Velocità.** Ogni modo si riduce di un fattore fisso a ogni passo: la
   convergenza è **lineare** (geometrica), e in scala semilogaritmica
   l'errore scende lungo una retta. Il modo più lento è quello di curvatura
   minima, che richiede $n\approx\ln(q^{(0)}/q^{(n)})/(C\lambda_\text{min})$
   passi. Il miglior $C$ costante è $C^*=2/(\lambda_\text{min}+\lambda_\text{max})$,
   che riduce l'errore di $(\kappa-1)/(\kappa+1)$ a passo, con
   $\kappa=\lambda_\text{max}/\lambda_\text{min}$ (numero di condizionamento).
   Se $\kappa$ è grande, cioè se la PES è una valle stretta, la *steepest
   descent* è lenta **qualunque** $C$ si scelga. È il suo limite noto: anche
   scegliendo a ogni passo il $C$ ottimale lungo la direzione della forza
   (ricerca in linea esatta), il fattore per passo sull'energia resta
   $\left[(\kappa-1)/(\kappa+1)\right]^2$ ({cite}`nocedal2006numerical`,
   cap. 3).
3. **Modi nulli.** Con $\lambda=0$ il fattore è 1: lungo traslazioni e
   rotazioni non succede nulla, ed è innocuo, perché le forze non hanno
   componenti lungo quei modi (§1).
4. **L'energia scende sempre.** L'energia sopra il minimo vale
   $\sum_i\frac12\lambda_i q_i^2$, e ogni termine si riduce di
   $(1-C\lambda_i)^2<1$ a ogni passo. Con $C<C_\text{crit}$ l'energia cala
   quindi in modo monotono, come richiesto a un algoritmo di minimizzazione.
   Non vale invece per $F_\text{max}$: è il massimo su **un** atomo, e può
   crescere quando la forza si ridistribuisce tra gli atomi (§5).

:::{note} I numeri del cluster dell'esercizio (256 atomi, LJ + $P_7$)
Dall'Hessiana calcolata nel minimo:

- **Spettro:** 6 autovalori nulli, poi da $\lambda_\text{min}=0.12$ a
  $\lambda_\text{max}=25.8$ eV/Å², quindi $\kappa\approx215$.
- **Limite su $C$:** $C_\text{crit}=2/\lambda_\text{max}\approx0.078$ Å²/eV;
  il $C=0.005$ del testo ne è circa 1/15. Con $C=1.05\,C_\text{crit}$ il
  cluster esplode.
- **Modi coinvolti:** partendo dal reticolo ideale si muovono solo 40 modi
  su 768, per la simmetria della configurazione di partenza. Il più morbido
  ha $\lambda\approx1.39$ eV/Å², e da lui dipende il numero di passi:
  $n\cdot C\approx3$ Å²/eV per tutti i $C$ provati.
- **Legame con la MD:** la curvatura massima fissa anche la frequenza di
  vibrazione più alta, $7.6$ THz (periodo 131 fs). I passi temporali della
  MD del punto 1 (2–20 fs) ne sono una piccola frazione.
:::

**$C$ adattivo.** Una ricetta pragmatica, evidenziata nella slide, è far
variare $C$: se il passo fa scendere l'energia lo si accetta e si aumenta
$C$ (×1.1), se la fa salire lo si rifiuta e si dimezza $C$. L'energia non
sale mai, e $C$ si porta da solo vicino al limite. Nel cluster di 256 atomi
bastano circa 40 iterazioni invece di 598, anche partendo da un $C$ sopra
$C_\text{crit}$. Il limite {eq}`eq:es1-sd-stabilita` vale per $C$
**costante**. Con $C$ variabile ogni modo viene moltiplicato per
$\prod_k|1-C_k\lambda_i|$, e $C$ può superare $C_\text{crit}$ per qualche
passo senza danni, se i modi rigidi sono già stati smorzati. Il testo d'esame
chiede però $C$ costante.

## 4. Criterio di convergenza

Ci si ferma quando la forza più grande è sotto una soglia:

$$
\max_{k=1,\dots,N}\sqrt{F_x^2(k)+F_y^2(k)+F_z^2(k)}\;\le\;F_\text{tol}.
$$ (eq:es1-sd-ftol)

Si usa il **massimo**, non la media, perché il criterio deve garantire che
**ogni** atomo sia in equilibrio. Un solo atomo fuori posto, ad esempio
un adatomo in superficie, sparirebbe in una media su centinaia di atomi.

:::{warning} Quale $F_\text{tol}$?
La slide 37 indica $F_\text{tol}\sim10^{-5}$ eV/Å, mentre il codice della
slide 38 e il testo d'esame usano $10^{-3}$ eV/Å. **Per l'esercizio vale
$10^{-3}$ eV/Å.**
:::

**Quanto si è vicini al minimo?** Nel modello quadratico una forza residua
$F$ su un modo di curvatura $\lambda$ corrisponde a uno scostamento $F/\lambda$
e a un'energia in eccesso $F^2/(2\lambda)$. Le forze residue sono quindi
trascurabili? Per il cluster dell'esercizio sì:

- con $F_\text{tol}=10^{-3}$ eV/Å l'energia resta sopra il minimo di
  $1.6\times10^{-5}$ eV **in tutto**, e le posizioni ne distano meno di
  $10^{-3}$ Å;
- l'energia cinetica a 25 K vale $0.83$ eV, 50 000 volte di più;
- stringere a $10^{-5}$ eV/Å raddoppia le iterazioni, per una differenza
  di energia che nella MD è irrilevante;
- come previsto, l'errore sull'energia scende di 100 volte per ogni decade
  di $F_\text{tol}$.

:::{important}
$F_\text{max}<F_\text{tol}$ è necessario, ma **non** sufficiente. Con
$C$ sopra il limite il cluster esplode: gli atomi si allontanano finché non
sentono più forze, e il criterio risulta «soddisfatto» con un'energia di
$-275$ eV invece di $-453.67$ eV. Serve sempre anche il controllo
sull'energia (§5). Inoltre il ciclo va limitato a un numero massimo di passi
(`maxStep`), nel caso la convergenza non arrivi mai.
:::

## 5. Funziona? Le verifiche

:::{figure} ../../figures/CMS6_immagini/14_steepest_esempio_864_atomi.png
:name: fig:es1-864
:width: 85%

Esempio della slide 39: cluster di Ag di 864 atomi, $E$ e $F_\text{max}$ in
funzione delle iterazioni per $C=0.003$ e $C=0.01$ Å²/eV.
:::

La slide 38 propone due controlli:

1. **L'energia potenziale deve scendere sempre**: è ciò che si chiede a un
   algoritmo di minimizzazione.
2. **Anche $F_\text{max}$ deve scendere**, nel complesso; aumenti locali sono
   ammessi, perché si minimizza l'energia e non la forza.

Il notebook ripete l'esempio della slide 39 con il file `fcc100a864.txt` e
ottiene gli stessi valori: $E$ passa da $-1681.86$ a $-1682.39$ eV,
$F_\text{max}$ parte da circa $0.2$ eV/Å, e servono 1802 iterazioni con
$C=0.003$ e 540 con $C=0.01$. L'energia scende a ogni iterazione, mentre
$F_\text{max}$ cresce qualche volta (13 e 4 volte), come mostra anche la
slide. Le coordinate cambiano pochissimo: lo spostamento massimo è $0.07$ Å,
quello medio $0.02$ Å.

## 6. Limiti e alternative

**Solo il minimo locale più vicino.** La *steepest descent* non sale mai,
quindi non attraversa le barriere tra un bacino e l'altro: converge al
minimo del bacino in cui parte (slide 36). Per trovare un minimo diverso
bisogna cambiare la configurazione di partenza, ad esempio perturbandola o
facendola evolvere prima con una MD.

**Simmetria e punti di sella.** Se la configurazione di partenza è simmetrica,
anche le forze lo sono, e la discesa conserva la simmetria. Nel cluster
dell'esercizio, infatti, si muovono solo 40 modi su 768. Una discesa
simmetrica potrebbe in principio fermarsi su un punto di sella, dove le forze
sono nulle per simmetria. Per escluderlo si guarda l'Hessiana nel punto
finale: nel cluster dell'esercizio, a parte i 6 modi nulli, tutti gli
autovalori sono positivi ($\lambda\ge0.12$ eV/Å²), quindi il punto trovato è
un minimo vero.

**Metodi più efficienti.** La slide 36 cita ad esempio il **gradiente
coniugato**, che combina la forza con la direzione del passo precedente ed
evita lo zig-zag nelle valli strette ({cite}`nocedal2006numerical`, cap. 5).
I metodi quasi-Newton come L-BFGS costruiscono invece un'approssimazione
dell'Hessiana durante la discesa. Nelle simulazioni atomistiche è molto usato
anche **FIRE** (*Fast Inertial Relaxation Engine*): è una MD con modifiche
alle velocità e passo temporale adattivo, semplice da inserire in un codice
MD già esistente; secondo i suoi autori è più veloce del gradiente coniugato
e competitivo con L-BFGS {cite}`bitzek2006fire`. Per i sistemi di questo
esercizio (qualche centinaio di atomi) la *steepest descent* converge in
meno di un secondo ed è più che sufficiente.
