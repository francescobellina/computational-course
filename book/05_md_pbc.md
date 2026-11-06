# Simulazioni MD: dal potenziale alla statistica (CMS 6)

Questa sezione segue il materiale di CMS_6. Si va dal ciclo operativo di una simulazione di dinamica molecolare (MD) alla lettura statistica dei risultati, al raccordo del potenziale di Lennard-Jones, alla minimizzazione (*steepest descent*) e alle condizioni periodiche al contorno (PBC) per passare da un cluster isolato al cristallo bulk.

## 1. Il ciclo di una simulazione MD

:::{figure} ../figures/CMS6_immagini/01_workflow_md.png
:name: fig:md-workflow
:width: 90%

Schema completo di una simulazione MD: parametri, condizioni iniziali, ciclo *velocity Verlet*, output.
:::

Una simulazione MD si divide in **preparazione** e **ciclo temporale**.

### Preparazione

Prima di avviare il ciclo si fissano:

- **Parametri**: potenziale interatomico, dominio di simulazione, ensemble statistico (NVE, NVT, NPT, ...). Fuori da NVE servono termostato/barostato.
- **Posizioni iniziali** $\mathbf{x}_i(0)$: generate (ad esempio da un reticolo cristallino) o importate. Se non sono prossime ad un minimo di energia potenziale conviene rilassarle con *steepest descent* ({numref}`sec:md-steepest`). Si calcolano quindi le forze iniziali $\mathbf{F}_i(0) = -\nabla_i \phi$.
- **Velocità iniziali** $\mathbf{v}_i(0)$: estratte casualmente (distribuzione di Maxwell–Boltzmann alla $T_\text{ini}$), corrette per avere quantità di moto totale nulla ($\mathbf{v}_\text{cm}=0$) e riscalate per ottenere esattamente $T_\text{ini}$.

### Ciclo *velocity Verlet*

Una volta pronte le condizioni iniziali, si integra l'equazione del moto finché $t < t_\text{end}$ con l'algoritmo *velocity Verlet* (già introdotto nei capitoli precedenti; qui interessa l'ordine operativo):

$$
\mathbf{x}_i(t+\Delta t)=\mathbf{x}_i(t)+\mathbf{v}_i(t)\,\Delta t+\frac{1}{2m}\mathbf{F}_i(t)\,\Delta t^2 \,.
$$ (eq:vv-x)

$$
\mathbf{F}_i(t+\Delta t)= -\sum_{j\neq i}\nabla_i\,\phi(r_{ij}) \,.
$$ (eq:vv-f)

$$
\mathbf{v}_i(t+\Delta t)=\mathbf{v}_i(t)+\frac{\Delta t}{2m}\left(\mathbf{F}_i(t)+\mathbf{F}_i(t+\Delta t)\right) \,.
$$ (eq:vv-v)

:::{warning}
**Ordine fondamentale.** Si aggiornano le posizioni con {eq}`eq:vv-x`, si calcolano le **nuove** forze {eq}`eq:vv-f` **senza sovrascrivere** $\mathbf{F}(t)$ (serve per {eq}`eq:vv-v`), infine si aggiornano le velocità {eq}`eq:vv-v`. Solo a questo punto $\mathbf{F}(t+\Delta t)$ diventa $\mathbf{F}(t)$ del passo successivo (le forze vanno calcolate una sola volta per passo temporale).
:::

Ad ogni passo (o con cadenza prefissata) si registrano energia potenziale $\phi(t)$, energia cinetica $K(t)$, energia totale $E(t)=\phi(t)+K(t)$ e temperatura. Per $N$ atomi, con $\mathbf{v}_\text{cm}=0$,

$$
K=\frac{1}{2}\sum_i m v_i^2,\qquad T=\frac{2K}{3N k_B}\,,
$$ (eq:T-from-K)

essendo i gradi di libertà effettivi $3N-3$ trascurabili per $N$ grande.

## 2. Cosa produce una MD: g(r) e fasi della materia

Una simulazione MD produce essenzialmente due tipi di informazioni: **configurazioni** $\{\mathbf{x}_i(t), \mathbf{v}_i(t)\}$ e **grandezze scalari** nel tempo ($\phi, K, E, T$: rispettivamente energia potenziale totale $\sum_{i<j}\phi(r_{ij})$, energia cinetica totale $\frac{1}{2}\sum_i m v_i^2$, energia totale $E=K+\phi$ e temperatura istantanea $T=2K/(3Nk_B)$, un valore per ogni passo temporale). Dal post-processing si ottengono transizioni, spostamento quadratico medio, pressione, funzioni di correlazione, ecc.

:::{tip}
**Regola d'oro.** È costoso analizzare direttamente durante la simulazione: conviene salvare su file tutto ciò che serve e analizzare **dopo** con script indipendenti, così da poter cambiare l'analisi senza rifare la MD.
:::

### Funzione di correlazione di coppia g(r)

Fissato un atomo di riferimento, sia $N(R)$ il numero medio di atomi entro distanza $R$ da esso. Con densità atomica media $\rho_0 = N/V$,

$$
N(R)=\rho_0 \int_0^R 4\pi r^2\, g(r)\,dr,\qquad \rho_0=\frac{N}{V}\,.
$$ (eq:N-R-g)

Derivando,

$$
dN = \rho_0\, g(r)\, 4\pi r^2 dr \implies g(r)=\frac{1}{\rho_0}\frac{dN/dr}{4\pi r^2}\,.
$$ (eq:g-def)

In pratica $g(r)$ è il **rapporto tra densità locale a distanza $r$ e densità media**: $g(r)\to 1$ indica assenza di struttura (gas ideale in limite opportuno), mentre picchi con $g(r)>1$ corrispondono a distanze interatomiche favorite.

Stima numerica (istogramma con passo $\Delta r$), mediata su più configurazioni **dopo** la termalizzazione, con $n_k$ numero di coppie ordinate $i\neq j$ aventi distanza in $[r_k, r_k+\Delta r)$:

$$
g(r_k)\simeq \frac{n_k}{N\, \rho_0\, 4\pi r_k^2\, \Delta r}\,.
$$ (eq:g-histo)

:::{figure} ../figures/CMS6_immagini/02_gr_definizione_cristallo.png
:name: fig:gr-def
:width: 80%

Definizione di $g(r)$ e sua forma per un cristallo ideale (ogni picco corrisponde ad una shell di vicini successivi).
:::

:::{figure} ../figures/CMS6_immagini/03_vibrazioni_reticolo.png
:name: fig:gr-vib
:width: 80%

Si a 500 K e 1500 K: gli atomi vibrano attorno ai siti del reticolo (fononi).
:::

:::{figure} ../figures/CMS6_immagini/04_liquido_gr_temperature.png
:name: fig:gr-liq
:width: 80%

Si a 2500 K: traiettorie diffusive e confronto di $g(r)$ a 500/1500/2500 K (ordine a corto raggio nel liquido).
:::

A titolo illustrativo (potenziale Stillinger–Weber, Si, $8\times8\times8$ celle, NVT):

- **Cristallo ideale**: $g(r)$ è una serie di picchi molto stretti, uno per ogni shell di vicini (1°, 2°, 3°, ...).
- **$T < T_m$**: vibrazioni attorno ai siti → picchi si allargano al crescere della temperatura, ma la struttura resta riconoscibile.
- **$T > T_m$ (2500 K)**: traiettorie diffusive. Nel liquido **non** c'è distribuzione casuale ($g(r)\neq 1$): compare un primo picco largo seguito da oscillazioni smorzate e $g(r)\to 1$ a grandi $r$ (**ordine a corto raggio**).

Una distinzione quantitativa tra vibrazione e diffusione si può ottenere dallo spostamento quadratico medio $\langle |\mathbf{r}(t)-\mathbf{r}(0)|^2\rangle$ (limitato nel solido, $\propto t$ nel liquido con $\langle \Delta r^2\rangle = 6 D t$).

## 3. Medie, ergodicità, termalizzazione e fluttuazioni

:::{figure} ../figures/CMS6_immagini/05_media_temporale_ergodicita.png
:name: fig:ergodicity
:width: 80%

Traiettoria nello spazio delle fasi: media temporale ↔ media d'insieme NVE.
:::

In NVE la traiettoria resta sull'ipersuperficie isoenergetica $H(\mathbf{x},\mathbf{p})=E$. Per un'osservabile $A$,

$$
\langle A\rangle_{MD}\approx \langle A\rangle_t=\lim_{t\to\infty}\frac{1}{t}\int_{0}^{t} A(\mathbf{x}(t'),\mathbf{p}(t'))dt' \;\;\overset{\text{ergodicità}}{\longleftrightarrow}\;\; \langle A\rangle_{NVE}=\frac{\int_{E<H<E+dE}A\,d\mathbf{x}d\mathbf{p}}{\int_{E<H<E+dE}d\mathbf{x}d\mathbf{p}} \,.
$$ (eq:ergodic)

Se il sistema è ergodico e la simulazione è sufficientemente lunga, **media temporale = media microcanonica**.

### Termalizzazione

Lo stato iniziale (atomi sui siti reticolari, velocità casuali) **non** è generalmente uno stato di equilibrio: il sistema rilassa verso l'equilibrio su tempi di frazioni di ps. Il transiente di durata $t_\text{th}$ va **escluso** dalle medie statistiche. Per determinarlo conviene guardare $E_\text{tot}(t)$ e $T(t)$ (figura {numref}`fig:dt-term`).

Dopo la termalizzazione, con $N$ passi nella finestra di analisi,

$$
\langle A\rangle_t = \frac{1}{t-t_\text{th}}\int_{t_\text{th}}^{t} A(t')dt' \approx \frac{1}{N}\sum_{i=i_\text{th}}^{N} A_i \,,
$$ (eq:time-avg)

$$
\delta A = \sqrt{\langle (A-\langle A\rangle)^2\rangle_t} = \sqrt{\frac{1}{N}\sum_{i=i_\text{th}}^{N} (A_i-\langle A\rangle)^2} = \sqrt{\langle A^2\rangle_t - \langle A\rangle_t^2}\,.
$$ (eq:fluct)

:::{warning}
La temperatura misurata all'equilibrio $\langle T\rangle \pm \delta T$ **non** coincide in generale con $T_\text{ini}$ usata per assegnare le velocità iniziali.
:::

:::{note}
**Equipartizione (idea pratica).** Partendo dai siti di minima potenziale con energia cinetica corrispondente a $T_\text{ini}$, in un potenziale approssimativamente armonico circa metà dell'energia cinetica iniziale si trasferisce in energia potenziale: $\langle T\rangle \approx T_\text{ini}/2$. Per ottenere $\langle T\rangle \simeq T_\text{target}$ conviene spesso inizializzare a $T_\text{ini}\approx 2T_\text{target}$ (da verificare caso per caso).
:::

## 4. Fluttuazioni fisiche vs errori numerici; scelta del passo temporale

:::{figure} ../figures/CMS6_immagini/06_termalizzazione_timestep.png
:name: fig:dt-term
:width: 80%

$E_\text{tot}(t)$ per diversi $\Delta t$: transiente di termalizzazione (da scartare) e ampiezza delle fluttuazioni.
:::

:::{figure} ../figures/CMS6_immagini/07_timestep_ottimale.png
:name: fig:dt-opt
:width: 80%

$\delta E / |\langle E\rangle|$ in funzione di $\Delta t$ a diverse temperature (scala logaritmica).
:::

In NVE è fondamentale distinguere **due tipi di fluttuazioni**:

| Grandezza | Conservazione | Natura | Come agire |
|---|---|---|---|
| $E_\text{tot}=K+\phi$ | Conservata idealmente (sistema isolato) | Le fluttuazioni $\delta E$ sono **errori di troncamento** dell'integratore *velocity Verlet* ($\mathcal{O}(\Delta t^4)$ sulle posizioni, $\mathcal{O}(\Delta t^3)$ sulle velocità per passo) | **Ridurre** diminuendo $\Delta t$ |
| $T \propto K$ | **Non conservata** (scambio $K \leftrightarrow \phi$) | Le fluttuazioni $\delta T$ sono **fisiche** | **Non** dipendono criticamente da $\Delta t$ (per valori ragionevoli) |

### Dipendenza dalla taglia del sistema

Per grandi $N$ le fluttuazioni relative dell'energia cinetica (e quindi di $T$) scalano come

$$
\frac{\delta T}{\langle T\rangle} \approx \frac{1}{\sqrt{N}}\,.
$$ (eq:deltaT-scaling)

Per $N=256$ questo dà circa il 6%; nel limite termodinamico $N\to\infty$ le fluttuazioni relative svaniscono e gli ensemble diventano equivalenti.

### Scelta del passo temporale

Si cerca il **massimo** $\Delta t$ compatibile con una buona conservazione dell'energia. Un criterio euristico molto usato è

$$
\frac{\delta E}{\left|\langle E\rangle\right|} \le 10^{-5}\,.
$$ (eq:dt-criterion)

Come mostra {numref}`fig:dt-opt`, $\delta E/|\langle E\rangle|$ cresce al crescere di $\Delta t$ e **anche con la temperatura** (a temperatura più alta gli atomi sono più veloci, servono quindi passi temporali più piccoli). Nella pratica si eseguono brevi run NVE per diversi $\Delta t$, si calcola {eq}`eq:dt-criterion` nella finestra dopo termalizzazione e si sceglie il più grande $\Delta t$ che rispetti il criterio.

## 5. Output e post-processing

Per efficienza e flessibilità conviene seguire tre regole:

1. **Scrivere tutto su file** per l'analisi post-simulazione.
2. **Stampare a schermo solo di tanto in tanto** (ogni `nPrint` passi) per controllo.
3. **Non salvare le posizioni ad ogni passo**: salvare ogni `nOut` passi per limitare spazio su disco/memoria.

Esempio minimale (idea):

```python
with open('output.txt', 'w') as fout:
    for iStep in range(totStep):
        # 1) aggiorna posizioni/velocità/forze con velocity Verlet
        # ...
        # 2) scrivi grandezze scalari
        fout.write(f'{time}\t{eTot}\t{ePot}\t{eKin}\t{Temp}\n')
        if iStep % nPrint == 0:
            print(f'Time={time:.3f} ps - E_tot={eTot:.6f} eV')
        if iStep % nOut == 0:
            fname = f'conf{str(iOut).zfill(5)}.xyz'
            np.savetxt(fname, pos, header=f'{nAt}\ntime={time:.6f}', comments='')
            iOut += 1
```

### Formato `.xyz` per OVITO

Per visualizzare/animare con OVITO conviene il formato `.xyz`:

- Riga 1: numero di atomi `nAt`
- Riga 2: commento libero (es. `time=...`, `E_tot=...`, `T=...`)
- Righe 3..`nAt+2`: `x y z` per ogni atomo (si possono aggiungere altre colonne, ad esempio velocità/componenti)

:::{warning}
Nella forma scritta sopra si usa `comments=''` per evitare che `np.savetxt` anteponga `#` all'header; inoltre la stringa deve essere `f'{nAt}\ntime={time}'` (non `f'{nAt}\n time={time}'` con `f` interno agli apici).
:::

Per rileggere: `pos = np.loadtxt(fname, skiprows=2)`. Per una verifica rapida si può usare uno scatter 3D in Matplotlib; per animazioni sono più comodi OVITO o VMD.

:::{figure} ../figures/CMS6_immagini/08_ovito_xyz.png
:name: fig:ovito-xyz
:width: 80%

Visualizzazione in OVITO di una sequenza di file `.xyz`.
:::

### Analisi statistica (script indipendente)

L'analisi va fatta su `output.txt`, individuando il tempo/indice dopo la termalizzazione:

```python
import numpy as np

data = np.loadtxt('output.txt')
time, eTot, ePot, eKin, Temp = data[:,0], data[:,1], data[:,2], data[:,3], data[:,4]

# individua inizio finestra di analisi
thTime = 1.0  # ps, da verificare su T(t), E_tot(t)
iTh = np.searchsorted(time, thTime)

# medie e fluttuazioni nella finestra dopo termalizzazione
avgE, dE = eTot[iTh:].mean(), eTot[iTh:].std()
avgT, dT = Temp[iTh:].mean(), Temp[iTh:].std()

print(f'<E_tot> = {avgE:.6f} ± {dE:.6e} eV,  deltaE/|<E>| = {dE/abs(avgE):.2e}')
print(f'<T> = {avgT:.2f} ± {dT:.2f} K')
```

Per la finestra di analisi si usa `mean()`/`std()` su tutto l'intervallo $[t_\text{th}, t_\text{end}]$ (non serve un ciclo esplicito). `std()` calcolato così corrisponde a $\sqrt{\langle A^2\rangle - \langle A\rangle^2}$ con peso $1/N$ come in {eq}`eq:fluct`.

## 6. Il potenziale di Lennard-Jones con raccordo polinomiale

:::{figure} ../figures/CMS6_immagini/09_lj_cutoff_netto.png
:name: fig:lj-cutoff
:width: 80%

LJ con taglio netto: discontinuità in energia e singolarità nelle forze.
:::

Per l'Argento si usa il potenziale di Lennard-Jones

$$
\phi_{LJ}(r)=4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12}-\left(\frac{\sigma}{r}\right)^{6}\right],\qquad \varepsilon=0.345\,\text{eV},\qquad \sigma=2.644\,\text{Å}\,.
$$ (eq:lj)

Il minimo si trova a $r_\text{min}=2^{1/6}\sigma \approx 2.97\,\text{Å}$. Per una cella fcc di Ag ($a\approx4.16\,\text{Å}$) i primi vicini sono a $r_1=\frac{a\sqrt{2}}{2}\approx2.94\,\text{Å}$, i secondi a $r_2=a\approx4.16\,\text{Å}$, i terzi a $r_3=a\sqrt{3/2}\approx5.09\,\text{Å}$.

### Problema del taglio netto

Per limitare il numero di coppie interagenti si impone un **raggio di taglio** $r_c$: si considera $\phi=0$ per $r>r_c$. Spesso si sceglie $r_c=4.5\,\text{Å}$, compreso tra secondi e terzi vicini. Il problema è che $\phi_{LJ}(r_c)\neq 0$: ciò provoca una **discontinuità nell'energia** e una **singolarità (delta) nelle forze** ad ogni volta che una coppia attraversa $r_c$. Il risultato è che l'**energia totale non si conserva nemmeno idealmente**, un difetto del **modello** (non dell'integratore).

### Raccordo polinomiale

Si adotta una soluzione standard: si usa $\phi_{LJ}$ fino a $r_p$, poi un polinomio di grado 7 $P_7(r)$ che raccorda $\phi$ e le sue derivate fino al terzo ordine fino a portarla a 0 in $r_c$:

$$
\phi(r)=\begin{cases}
\phi_{LJ}(r),& r\le r_p,\\[4pt]
P_7(r)=\sum_{n=0}^{7} c_n r^n = A + B r + C r^2 + D r^3 + E r^4 + F r^5 + G r^6 + H r^7,& r_p < r \le r_c,\\[12pt]
0,& r > r_c\,.
\end{cases}
$$ (eq:lj-poly)

Gli 8 coefficienti sono determinati da 8 condizioni (continuità di energia, forza e prime due derivate della forza) in $r_p$ e in $r_c$:

$$
P_7^{(k)}(r_p)=\phi_{LJ}^{(k)}(r_p),\qquad P_7^{(k)}(r_c)=0,\qquad k=0,1,2,3\,.
$$ (eq:poly-conds)

Questo dà un sistema lineare $8\times8$:

```python
from math import perm
import numpy as np

def poly7_coeffs(phi_derivs_rp, rp, rc):
    """phi_derivs_rp = [phi, phi', phi'', phi'''] di LJ in rp"""
    M = np.zeros((8,8))
    b = np.zeros(8)
    for k in range(4):
        for n in range(k, 8):
            M[k,   n] = perm(n,k) * rp**(n-k)
            M[4+k, n] = perm(n,k) * rc**(n-k)
        b[k] = phi_derivs_rp[k]
        b[4+k] = 0.0
    return np.linalg.solve(M, b)  # [A,...,H]
```

:::{warning}
Il sistema può essere **mal condizionato**. È buona norma verificare numericamente che $P_7, P_7', P_7'', P_7'''$ riproducano le condizioni {eq}`eq:poly-conds` in $r_p$ e $r_c$. In alternativa si può lavorare con la variabile traslata $r-r_p$. Se il corso fornisce già `poly7.py` si consiglia di usarlo.
:::

:::{figure} ../figures/CMS6_immagini/10_lj_raccordo_polinomiale.png
:name: fig:lj-poly
:width: 80%

LJ con raccordo polinomiale $P_7$ tra $r_p$ e $r_c$ e relative condizioni di continuità.
:::

### Forze

La forza scalare (modulo lungo la congiungente, con segno per repulsione/attrazione secondo convenzione) è $f(r) = -\frac{d\phi}{dr}$:

$$
f(r)=\begin{cases}
24\varepsilon\sigma^6 \frac{2\sigma^6/r^6 - 1}{r^7},& r\le r_p,\\[10pt]
-P_7'(r)= -\left(B + 2C r + 3D r^2 + 4E r^3 + 5F r^4 + 6G r^5 + 7H r^6\right),& r_p < r \le r_c,\\[14pt]
0,& r>r_c\,.
\end{cases}
$$ (eq:lj-force)

:::{figure} ../figures/CMS6_immagini/11_forza_raccordo_polinomiale.png
:name: fig:lj-force-poly
:width: 80%

Andamento della forza: LJ, derivata del polinomio di raccordo, zero oltre $r_c$.
:::

Per un sistema 3D, la forza sull'atomo $k$ è

$$
\mathbf{F}(k)=\sum_{j\neq k} f(r_{kj})\frac{\mathbf{r}_k - \mathbf{r}_j}{r_{kj}},\qquad r_{kj}=\sqrt{(x_k-x_j)^2 + (y_k-y_j)^2 + (z_k-z_j)^2}\,.
$$ (eq:force-3d)

Nelle componenti,

$$
F_x(k)=\sum_{j\neq k} f(r_{kj})\frac{x_k - x_j}{r_{kj}}\,,
$$ (eq:force-x)

e analogamente per $y,z$. È importante notare: **se** in fase di calcolo si usa già $f(r)/r$ conviene passarlo direttamente; in ogni caso va usato il vettore che congiunge correttamente i due atomi.

### Piccoli accorgimenti implementativi

:::{warning}
- **Doppio conteggio.** Se si scorre tutte le coppie $(i,j)$ con $j>i$ l'energia va divisa per 2; se invece si somma su tutti $j\neq i$ va **evitato** il doppio conteggio (la forma {eq}`eq:force-3d` somma già correttamente $j\neq k$).
- **JIT/Numba.** Per usare `@njit` i coefficienti del polinomio vanno passati come **argomenti** alle funzioni (non come attributi di oggetti), come suggerito in {eq}`eq:poly-conds`/{eq}`eq:lj-force`.
- **Efficienza.** Calcolare `dx*dx+dy*dy+dz*dz` e poi `sqrt` (o confrontare i quadrati quando possibile) è spesso più efficiente che funzioni più generiche.
:::

(sec:md-steepest)=
## 7. Partire da una configurazione sensata: *steepest descent*

:::{figure} ../figures/CMS6_immagini/12_steepest_superficie_energia.png
:name: fig:steepest-surf
:width: 80%

Superficie di energia potenziale e discesa lungo il gradiente (*steepest descent*) verso il minimo locale.
:::

Lanciare direttamente una MD da una configurazione generata casualmente o da un reticolo "grezzo" è sbagliato: se gli atomi sono lontani dal loro minimo, le forze sono grandi e l'energia potenziale verrebbe convertita in energia cinetica spuria (surriscaldamento artificiale). Prima della MD conviene quindi **minimizzare** l'energia potenziale con *steepest descent* fino a ottenere forze prossime a zero.

### Algoritmo

L'energia potenziale $\phi(\{\mathbf{r}_i\})$ è una funzione in $3N$ dimensioni. La forza è $-\nabla\phi$, cioè diretta lungo la discesa più ripida. Si spostano gli atomi di poco lungo $\mathbf{F}$:

$$
\delta \mathbf{r}_i = C\, \mathbf{F}_i,\qquad \mathbf{r}_i \leftarrow \mathbf{r}_i + C\, \mathbf{F}_i \,,
$$ (eq:sd-step)

con $C>0$ opportunamente scelto (ha dimensioni Å²/eV).

:::{figure} ../figures/CMS6_immagini/13_steepest_passo_convergenza.png
:name: fig:steepest-step
:width: 80%

Effetto di $C$ troppo piccolo/grande e criterio di convergenza.
:::

- **$C$ troppo piccolo**: convergenza lenta (tante iterazioni).
- **$C$ troppo grande**: si "rimbalza" attorno al minimo o si diverge.
- **$C$ adattivo (pragmatico)**: se $\phi$ **diminuisce** si può aumentare leggermente $C$; se $\phi$ **aumenta** si rifiuta il passo e si dimezza $C$.

Il criterio di arresto è tipicamente sulla forza massima:

$$
F_\text{max} = \max_{i=1,\ldots,N} \sqrt{F_{x,i}^2 + F_{y,i}^2 + F_{z,i}^2} \le F_\text{tol}\,.
$$ (eq:ftol)

Un valore ragionevole per il corso può essere $F_\text{tol}\sim 10^{-3}\,\text{eV/Å}$ (più stringente se serve maggiore accuratezza). Nello schema di convergenza è importante notare: **minimizzare l'energia non implica necessariamente monotonicità stretta di $F_\text{max}$**, anche se spesso decresce.

Esempio minimale:

```python
for iStep in range(maxStep):
    # aggiorna liste di vicini se necessario (posizioni cambiate)
    nNbrs, whichNbrs = calc_nbrs(pos, box_or_pbc, rc)
    forces = calc_forces(pos, nNbrs, whichNbrs, coeff_poly, ...)
    Fmax = np.max(np.linalg.norm(forces, axis=1))
    if Fmax < ftol:
        break
    pos = pos + Csteep * forces
```

:::{figure} ../figures/CMS6_immagini/14_steepest_esempio_864_atomi.png
:name: fig:steepest-864
:width: 80%

Cluster Ag da 864 atomi: $E(\text{iter})$ e $F_\text{max}(\text{iter})$ per $C=0.003$ e $C=0.01$.
:::

:::{note}
*Steepest descent* converge **solo al minimo locale più vicino** alla configurazione di partenza. Per esplorare minimi diversi serve variare le condizioni iniziali. Esistono metodi più efficienti (*conjugate gradients*, etc.), ma per il corso questo approccio è più che sufficiente.
:::

(sec:md-pbc)=
## 8. Dal cluster al bulk: condizioni periodiche al contorno (PBC)

### 8.1 Perché un cluster non basta

:::{figure} ../figures/CMS6_immagini/16_mu_vs_N_cluster.png
:name: fig:mu-cluster
:width: 80%

Energia per atomo $\mu = E/N$ in funzione di $N$ per cluster finiti, confronto con $\mu_\text{bulk}$.
:::

In un cluster molti atomi sono **sotto-coordinati** sulla superficie. Poiché $S/V \propto N^{-1/3}$ decresce lentamente, anche per cluster relativamente grandi $\mu(N)=E/N$ è ancora lontano dal valore di bulk (fig. {numref}`fig:mu-cluster`).

### Energia per atomo del bulk perfetto

Considerando l'atomo centrale di due celle convenzionali fcc sovrapposte e $r_c=4.5\,\text{Å}$, interagiscono solo primi e secondi vicini:

- 12 primi vicini lungo $\langle 110\rangle$, $r_1 = \frac{a\sqrt{2}}{2}$
- 6 secondi vicini lungo $\langle 100\rangle$, $r_2 = a$

Per evitare il doppio conteggio di ogni coppia,

$$
\mu_\text{bulk} = \frac{1}{2}\left(12\,\phi_{LJ}(r_1) + 6\,\phi_{LJ}(r_2)\right)\,.
$$ (eq:mu-bulk)

Con i parametri usati nel corso si ottiene $\mu_\text{bulk}\approx -2.32\,\text{eV}$. Per $r_2 < r_p$ il raccordo polinomiale non interviene. Vale la pena verificare numericamente questo valore e riportarlo come linea orizzontale nel grafico $\mu(N)$.

:::{figure} ../figures/CMS6_immagini/15_fcc_vicini_mu_bulk.png
:name: fig:fcc-vicini
:width: 80%

Cella fcc, primi/secondi vicini e calcolo di $\mu_\text{bulk}$.
:::

### 8.2 L'idea delle PBC

:::{figure} ../figures/CMS6_immagini/17_pbc_immagini_cutoff.png
:name: fig:pbc-img
:width: 80%

Cella replicata periodicamente: un atomo interagisce anche con immagini di atomi nel bordo opposto.
:::

Si replica la cella di simulazione periodicamente nello spazio:

$$
(x,y,z) \mapsto (x + n_x L_x, y + n_y L_y, z + n_z L_z),\qquad n_x,n_y,n_z \in \mathbb{Z}\,.
$$ (eq:pbc-rep)

L'idea è simulare una **porzione rappresentativa** di un sistema infinito: ciò che accade nella cella si ripete identicamente. Di conseguenza, per calcolare distanze e interazioni si deve usare la **distanza all'immagine più vicina**.

:::{figure} ../figures/CMS6_immagini/18_pbc_distanza_1D.png
:name: fig:pbc-1d
:width: 70%

Distanza all'immagine minima in 1D.
:::

In 1D, data la distanza $\Delta x = x_k - x_j$, le immagini sono $\Delta x, \Delta x - L_x, \Delta x + L_x,\ldots$ La più vicina si ottiene con

$$
\Delta x^\text{pbc} = \Delta x - L_x\,\operatorname{round}\!\left(\frac{\Delta x}{L_x}\right)\,.
$$ (eq:pbc-min)

($\operatorname{round}$ restituisce l'intero più vicino a 0, +1 o -1 a seconda del caso). In 3D si applica componente per componente:

$$
r_{kj}^\text{pbc} = \sqrt{(\Delta x_{kj}^\text{pbc})^2 + (\Delta y_{kj}^\text{pbc})^2 + (\Delta z_{kj}^\text{pbc})^2}\,.
$$ (eq:pbc-r3d)

```python
dx = pos[k,0] - pos[j,0]
dx = dx - Lx * np.round(dx/Lx)
# idem per dy, dz
```

**Tutte** le funzioni che usano distanze (liste dei vicini, energia potenziale, forze) devono utilizzare $r_{kj}^\text{pbc}$. Nelle forze, il vettore da usare in {eq}`eq:force-3d` deve essere quello corrispondente all'immagine minima (altrimenti la direzione della forza è sbagliata).

### Condizione minima per l'immagine unica

Per garantire che ogni coppia interagisca **al massimo una volta** (con la propria immagine più vicina) e che un atomo non interagisca con un'immagine di sé stesso, è necessario

$$
L_\text{min} > 2r_c\,.
$$ (eq:pbc-lmin)

:::{figure} ../figures/CMS6_immagini/19_pbc_cella_minima_2rc.png
:name: fig:pbc-2rc
:width: 80%

$L < 2r_c$ (non valido) vs $L > 2r_c$ (valido): condizione per l'immagine minima.
:::

Per Ag con $r_c=4.5\,\text{Å}$ serve $L > 9\,\text{Å}$. Una cella fcc $2\times2\times2$ celle convenzionali ha $L \approx 8.3\,\text{Å}$ (troppo piccola), una $3\times3\times3$ ha $L \approx 12.5\,\text{Å}$ e $N=108$ atomi (sufficiente). Più in generale è bene verificare sempre {eq}`eq:pbc-lmin`.

### Seguire le traiettorie con PBC

:::{figure} ../figures/CMS6_immagini/21_pbc_traiettorie.png
:name: fig:pbc-traj
:width: 80%

Coordinate non limitate (per MSD/diffusione) vs coordinate riportate nella cella (per visualizzazione).
:::

Quando un atomo esce da un lato della cella entra da quello opposto. A seconda dell'analisi si usano due rappresentazioni diverse:

- **Coordinate non limitate** (mantenute senza *wrap*): necessarie per calcolare spostamento percorso, **spostamento quadratico medio** $\langle |\Delta \mathbf{r}(t)|^2\rangle$ e coefficiente di diffusione. Per le distanze/interazioni si usano comunque le PBC.
- **Coordinate riportate nella cella** con

$$
x^\text{pbc} = x - L_x \lfloor x/L_x \rfloor \in [0, L_x)\,,
$$ (eq:pbc-wrap)

(idem per $y,z$, con $\lfloor \cdot \rfloor$ = parte intera inferiore): utili per visualizzare la configurazione e capire quali atomi interagiscono, ma **perdono l'informazione sul percorso reale**.

:::{tip}
**Regola pratica:** `round(...)` per la **distanza all'immagine minima** {eq}`eq:pbc-min`; `floor(...)` per **riportare** le coordinate dentro la cella {eq}`eq:pbc-wrap`.
:::

### Aspetti pratici delle PBC

:::{figure} ../figures/CMS6_immagini/20_pbc_array_di_difetti.png
:name: fig:pbc-defect
:width: 80%

Un difetto in PBC corrisponde ad un array periodico di difetti identici.
:::

:::{figure} ../figures/CMS6_immagini/22_pbc_particelle_interagenti.png
:name: fig:pbc-collision
:width: 80%

In cella finita con PBC aumenta la probabilità d'incontro tra particelle che diffondono.
:::

:::{figure} ../figures/CMS6_immagini/23_pbc_vuoto_superfici.png
:name: fig:pbc-surface
:width: 80%

Cella con vuoto: se $L_x = N a + \Delta$ con $\Delta > r_c$, le PBC lungo $x$ diventano effettivamente «spente» e si ottengono superfici libere.
:::

Alcuni punti da tenere a mente:

- **Nessuna superficie**: in una cella perfetta le PBC riproducono il bulk ideale. Lo *steepest descent* non modifica la configurazione (è già un minimo) a meno di perturbazioni.
- **Volume fisso**: le PBC con cella costante corrispondono a $NVE$ (o $NVT$ con termostato) a volume fisso. Per la dilatazione termica servirebbe $NPT$.
- **Effetti finiti**: oltre a $L/2$ non ci sono correlazioni fisiche nuove, ma le repliche sono correlate per costruzione.
- **Difetti**: una vacanza in PBC è in realtà un **array periodico** di vacanze con densità $1/V$ (fig. {numref}`fig:pbc-defect`). Per difetti isolati servono celle molto grandi.
- **Diffusione/reattività**: in cella finita la probabilità che due particelle diffondano l'una incontro all'altra è **sovrastimata** rispetto al sistema reale (fig. {numref}`fig:pbc-collision`).
- **Superfici e cluster**: basta usare lo **stesso codice** con PBC. Per ottenere superfici libere o un cluster isolato si introduce un vuoto $\Delta > r_c$ (meglio $\Delta \gg r_c$) nella direzione desiderata: le repliche non interagiscono più e le PBC sono di fatto disattivate lungo quella direzione (fig. {numref}`fig:pbc-surface`).

## 9. Efficienza del codice

### Vettorizzazione con NumPy

Quando possibile conviene evitare cicli espliciti su grandi array e usare operazioni vettoriali:

```python
# meno efficiente in generale su molti elementi (dipende dal caso)
for i in range(natoms):
    for j in range(3):
        pos[i,j] = pos[i,j] + vel[i,j]*dt + 0.5*force[i,j]/mass*dt**2

# più efficiente (vettorializzato)
pos = pos + vel*dt + 0.5*force/mass*dt**2
```

Per il calcolo scalare di una singola distanza, però, l'aritmetica esplicita a 3 componenti risulta spesso più veloce di costruzioni puramente vettorializzate:

```python
dx = pos[i,0]-pos[j,0]; dy = pos[i,1]-pos[j,1]; dz = pos[i,2]-pos[j,2]
dis = (dx*dx + dy*dy + dz*dz)**0.5
```

### JIT con Numba

Python è interpretato: cicli doppi su $N$ atomi sono lenti. Con [Numba](https://numba.pydata.org/) è possibile compilare *just-in-time* (JIT) le funzioni più pesanti con il decoratore `@njit` (*nopython mode*):

```python
from numba import njit

@njit
def calc_nbrs(natoms, pos, rc, Lx,Ly,Lz, use_pbc=True):
    ...
    return nNbrs, whichNbrs

@njit
def calc_energy(natoms, pos, nNbrs, whichNbrs, coeff_poly, rp, rc, eps, sig, Lx,Ly,Lz):
    ...
    return ePot

@njit
def calc_forces(natoms, pos, nNbrs, whichNbrs, coeff_poly, rp, rc, eps, sig, Lx,Ly,Lz):
    ...
    return forces
```

:::{note}
- **Prima chiamata**: compilazione (lenta). **Chiamate successive**: codice macchina veloce → misurare i tempi **dopo** il riscaldamento.
- **Vincoli nopython**: usare solo array NumPy, scalari, tuple. Per questo i **coefficienzi del polinomio** vanno passati direttamente come argomenti (sezione 6).
- **Candidato ideale**: `calc_nbrs` con doppio ciclo $N^2$.
:::

È utile includere una breve cella di *benchmark* confrontando `calc_forces` con e senza `@njit` per valori crescenti di $N$.

## 10. Workflow completo, esempio guidato ed esercizi

:::{figure} ../figures/CMS6_immagini/24_wrapup_file_python.png
:name: fig:workflow-files
:width: 90%

Organizzazione modulare del codice: `potential.py`, `steepest.py`, `main.py`, `statistics.py`.
:::

### Organizzazione dei moduli

Un'organizzazione pratica (coerente con quanto visto nel corso) è:

| File | Funzione |
|---|---|
| `potential.py` | Calcolo di energia e forze con LJ + raccordo polinomiale e PBC. Usato da `steepest.py` e `main.py`. |
| `steepest.py` | Partendo da una configurazione `.xyz` generica, esegue *steepest descent* fino al minimo locale di energia potenziale. |
| `main.py` | MD vera e propria: legge configurazione rilassata, assegna velocità, integra con *velocity Verlet* in NVE, produce `output.txt` e file `.xyz`. |
| `statistics.py` | Post-processing indipendente: termalizzazione, medie/fluttuazioni, $g(r)$, ecc. |

### Esempio guidato end-to-end

Si consiglia di procedere passo per paso:

1. **Costruzione**: creare un cristallo fcc di Ag $4\times4\times4$ celle convenzionali (256 atomi, $L \approx 16.6\,\text{Å}$, con $L > 2r_c$). Eventualmente perturbare leggermente le posizioni per evitare simmetrie eccessive.
2. **Rilassamento**: eseguire *steepest descent* ({numref}`sec:md-steepest`) con PBC, LJ con raccordo polinomiale, fino a $F_\text{max} \le F_\text{tol}$.
3. **Condizioni iniziali MD**: assegnare velocità da distribuzione Maxwell–Boltzmann a $T_\text{ini}$, correggere $\mathbf{v}_\text{cm}=0$, riscalare per ottenere esattamente $T_\text{ini}$.
4. **Integrazione**: evolvere in NVE con *velocity Verlet*, scrivendo `output.txt` ogni passo e file `.xyz` ogni `nOut` passi.
5. **Analisi**: identificare $t_\text{th}$ da $T(t)$ e $E_\text{tot(t)}$; calcolare $\langle T\rangle, \delta T, \langle E_\text{tot}\rangle, \delta E/|\langle E\rangle|$ nella finestra dopo termalizzazione; calcolare $g(r)$.
6. **Ottimizzazione del passo**: ripetere brevi run per diversi $\Delta t$ e scegliere quello conforme al criterio {eq}`eq:dt-criterion`.

### Esercizi

:::{exercise}
**1) g(r) a due temperature**
Calcolare $g(r)$ per Ag in due condizioni (ad esempio solido a bassa $T$ e liquido/sovracaldo) confrontando i picchi con le posizioni attese dei primi tre vicini: $r_1\approx2.94\,\text{Å}$, $r_2\approx4.16\,\text{Å}$, $r_3\approx5.09\,\text{Å}$. Commentare l'allargamento dei picchi e il passaggio all'ordine a corto raggio.
:::

:::{exercise}
**2) Equipartizione e fluttuazioni di $T$**
Verificare che $\langle T\rangle \approx T_\text{ini}/2$ dopo la termalizzazione. Studiare $\delta T/\langle T\rangle$ in funzione di $1/\sqrt{N}$ per $N=108, 256, 500, 864$ (attenzione: $N=32$ **non** soddisfa la condizione $L > 2r_c$, da evitare).
:::

:::{exercise}
**3) Taglio netto vs raccordo polinomiale**
A parità di $\Delta t$, confrontare conservazione dell'energia e fluttuazioni di $E_\text{tot}$ usando il potenziale LJ con **taglio netto** ($r_c=4.5\,\text{Å}$) e con **raccordo polinomiale**. Spiegare perché il taglio netto impedisce la conservazione anche per $\Delta t\to0$.
:::

:::{exercise}
**4) Scansione del passo temporale**
Eseguire una scansione di $\Delta t$ a due diverse temperatures. Tracciare $\delta E/|\langle E\rangle|$ in scala logaritmica e individuare il più grande $\Delta t$ conforme al criterio $\delta E/|\langle E\rangle| \le 10^{-5}$.
:::

:::{exercise}
**5) Cluster vs bulk (PBC)**
Calcolare $\mu(N)=E/N$ dopo minimizzazione per diverse taglie di cluster (senza PBC, in tutte le direzioni con vuoto $>\ r_c$) e confrontarlo con il caso **bulk perfetto** ottenuto usando PBC in tutte le direzione, per cellule sufficienti a soddisfare $L > 2r_c$. Mostrare che le PBC danno subito $\mu_\text{bulk}$ mentre il cluster ci arriva lentamente, confrontando qualitativamente con {numref}`fig:mu-cluster`.
:::
