(sec:ms-approssimazione-adiabatica)=
# Approssimazione adiabatica e moto dei nuclei

L'approssimazione adiabatica, detta anche **approssimazione di Born-Oppenheimer
(B.O.A.)**, separa il moto degli elettroni da quello dei nuclei: gli elettroni
restano nello stato fondamentale per ogni configurazione dei nuclei, che si muovono
in un potenziale interatomico. Il capitolo si chiude con la regola $T_f=T(0)/2$ e le
condizioni in cui vale.

## Elettroni e nuclei

L'Hamiltoniana elettronica e la sua funzione d'onda nello stato fondamentale
determinano l'energia in funzione delle posizioni dei nuclei, cioè il **potenziale
interatomico**. In questo corso il potenziale non si calcola: se ne assume una forma
approssimata (*guess*). Ci sono tre livelli di descrizione:

1. **equazione di Schrödinger per gli elettroni** nello stato fondamentale, ad
   esempio con la DFT: è il livello più difficile;
2. **equazioni di Newton per i nuclei**, classiche, con un potenziale dato: è la
   **dinamica molecolare**, più semplice, anche se molte simulazioni richiedono
   tempi lunghi e molte particelle;
3. **dinamica molecolare *ab initio*** (AIMD), ad esempio Car-Parrinello: unisce i
   due livelli precedenti ed è molto accurata.

## Nella pratica

Si sceglie un potenziale interatomico, si risolvono **numericamente** le equazioni
di Newton per i nuclei, si campiona la traiettoria e si calcolano le medie temporali
delle osservabili di interesse.

### Temperatura e potenziale

- A $t=0$ si suppone che la posizione iniziale $q(0)$ sia un minimo locale del
  potenziale $V(q)$; l'energia totale è fissata.
- Al tempo $t=\tau$ la traiettoria hamiltoniana esplora la superficie di energia, e
  la temperatura è legata all'energia cinetica media dei nuclei.

Vicino al minimo il potenziale è approssimativamente una parabola (potenziale
armonico). L'energia totale si conserva sempre, quindi:

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
([notebook PART 1 + 2](../../notebooks/esame/esercizio1_part1_2.ipynb), §4).

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
