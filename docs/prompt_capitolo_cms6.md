# Prompt per l'agente — Capitolo Jupyter Book: «Simulazioni MD: dal potenziale alla statistica» (CMS_6)

## 0. Istruzioni per l'agente

Scrivi un capitolo di Jupyter Book (MyST Markdown, eseguibile in VS Code) **in italiano**, basato sui contenuti della sezione 3 di questo file (derivati dalle slide CMS_6 del corso *Computational Materials Science*, R. Bergamaschini).

**Stile**
- Intuitivo e completo, ma **non ridondante**: ogni concetto si spiega una volta, poi si richiama con riferimenti (`{eq}`, `{ref}`). Non rispiegare ciò che appartiene ai capitoli precedenti (liste dei vicini, forze, integrazione di Verlet): richiamalo in una riga e rimanda.
- Prima l'idea fisica in 2–3 frasi, poi la formula, poi il codice (solo dove serve). Spiegazioni più estese per ciò che è meno scontato (PBC, convenzione dell'immagine minima, JIT/Numba, formato xyz); sintetiche su ciò che un fisico dà per noto (ergodicità, medie, varianza).
- Termini inglesi tra parentesi solo alla prima occorrenza (es. «passo temporale (*time step*)»). Mantieni `steepest descent`, `velocity Verlet`, `cutoff` → «raggio di taglio» dopo la prima volta.
- Formule in LaTeX, etichettate (`$$ ... $$ (eq:nome)`) quando richiamate più avanti. I numeri (1)…(19) e i `\tag` di questo file sono solo indicativi: sostituiscili con le label MyST.
- I blocchi `:::{warning}` / `:::{note}` / `:::{tip}` sono già in sintassi MyST.
- Usa callout MyST (`{note}`, `{tip}`, `{warning}`) per intuizioni e avvertenze. I punti marcati con ⚠️ **correggono imprecisioni delle slide**: usa la versione corretta.

**Figure**
- Copia la cartella `immagini_CMS6/` nella cartella delle figure del book e inseriscile con la direttiva `{figure}` (con `:name:` e didascalia in italiano), nella posizione indicata dalla mappa della sezione 1.
- Se una figura si può **rigenerare** con il codice del capitolo (g(r), E_tot(t), δE/⟨E⟩ vs Δt, μ(N), E e F_max durante lo steepest descent), preferisci quella prodotta dal notebook e tieni l'immagine delle slide solo come riferimento/confronto. Le figure concettuali (schemi, PBC, workflow) si tengono così come sono.

**Codice**
- Celle brevi ed eseguibili. Se nel repository esistono già `calc_nbrs`, `calc_force`, `calc_epot` (o un pacchetto di utilità del corso), **riusale**; altrimenti implementale una volta sola nel capitolo.
- **Non inventare valori numerici**: calcolali eseguendo il codice. Quelli riportati qui sono parametri di input o riferimenti da verificare.
- Unità: eV, Å, u. Argento: $m = 107.87$ u. Il tempo naturale è $\sqrt{u\,Å^2/\text{eV}} \approx 10.18$ fs (quindi 1 fs ≈ 0.0982 unità), $k_B = 8.617333\times10^{-5}$ eV/K. (Salta se già gestito dal pacchetto.)

**Chiusura del capitolo**: esempio guidato end-to-end + 5 esercizi (sezione 3.10).

---

## 1. Mappa delle figure (`immagini_CMS6/`)

| File | Sezione | Cosa mostra / didascalia suggerita |
|---|---|---|
| `01_workflow_md.png` | 3.1 | Schema completo di una simulazione MD: parametri, condizioni iniziali, ciclo velocity Verlet, output |
| `02_gr_definizione_cristallo.png` | 3.2 | Definizione di g(r) e g(r) del cristallo ideale (picchi = vicini successivi) |
| `03_vibrazioni_reticolo.png` | 3.2 | Si a 500 K e 1500 K: traiettorie di atomi che vibrano attorno ai siti (fononi) |
| `04_liquido_gr_temperature.png` | 3.2 | Si a 2500 K: traiettorie diffusive; g(r) a 500/1500/2500 K |
| `05_media_temporale_ergodicita.png` | 3.3 | Traiettoria nello spazio delle fasi, media temporale ↔ media d'insieme NVE |
| `06_termalizzazione_timestep.png` | 3.3 e 3.4 | E_tot(t) per Δt = 1, 5, 10 fs: transiente di termalizzazione e fluttuazioni (0.005 / 0.02 / 0.1 eV) |
| `07_timestep_ottimale.png` | 3.4 | δE/\|⟨E⟩\| vs Δt a varie T, con soglia 10⁻⁵ |
| `08_ovito_xyz.png` | 3.5 | Visualizzazione in OVITO di una sequenza di file `.xyz` |
| `09_lj_cutoff_netto.png` | 3.6 | LJ con taglio netto: discontinuità in energia, singolarità nelle forze |
| `10_lj_raccordo_polinomiale.png` | 3.6 | LJ con raccordo polinomiale P₇ tra r_p e r_c (con zoom) e condizioni sui coefficienti |
| `11_forza_raccordo_polinomiale.png` | 3.6 | Forza a tratti: LJ, −P₇′, 0 |
| `12_steepest_superficie_energia.png` | 3.7 | Superficie di energia potenziale e discesa verso il minimo locale più vicino |
| `13_steepest_passo_convergenza.png` | 3.7 | Effetto di C piccolo/grande e criterio di convergenza |
| `14_steepest_esempio_864_atomi.png` | 3.7 | E(iterazioni) e F_max(iterazioni) per cluster Ag da 864 atomi, C = 0.003 e 0.01 |
| `15_fcc_vicini_mu_bulk.png` | 3.8 | Cella fcc: 12 primi vicini ⟨110⟩, 6 secondi vicini ⟨100⟩, μ_bulk |
| `16_mu_vs_N_cluster.png` | 3.8 | μ = E/N vs N per cluster finiti, confrontato con μ_bulk |
| `17_pbc_immagini_cutoff.png` | 3.8 | Cella replicata periodicamente; un atomo interagisce attraverso i bordi |
| `18_pbc_distanza_1D.png` | 3.8 | Distanza a immagine minima in 1D e formula con `round` |
| `19_pbc_cella_minima_2rc.png` | 3.8 | L < 2r_c (no) vs L > 2r_c (ok) |
| `20_pbc_array_di_difetti.png` | 3.8 | Un difetto in PBC = array periodico di difetti |
| `21_pbc_traiettorie.png` | 3.8 | Coordinate non limitate vs riportate in cella |
| `22_pbc_particelle_interagenti.png` | 3.8 | Due particelle in cella finita con PBC: incontri favoriti |
| `23_pbc_vuoto_superfici.png` | 3.8 | Cella con vuoto Δ > r_c: PBC «spente» lungo x → superfici libere |
| `24_wrapup_file_python.png` | 3.10 | Organizzazione dei moduli: potential, steepest, main, statistics |

---

## 2. Struttura del capitolo

1. Il ciclo di una simulazione MD
2. Cosa produce una MD: g(r) e fasi della materia
3. Medie, ergodicità, termalizzazione e fluttuazioni
4. Fluttuazioni fisiche vs errori numerici; scelta del passo temporale
5. Output e post-processing
6. Il potenziale di Lennard-Jones con raccordo polinomiale
7. Partire da una configurazione sensata: steepest descent
8. Dal cluster al bulk: condizioni periodiche al contorno (PBC)
9. Efficienza del codice
10. Workflow completo, esempio guidato ed esercizi

(La numerazione 3.x nella mappa delle figure e nel resto del file corrisponde a queste sezioni.)

---

## 3. Contenuti da sviluppare

### 3.1 Il ciclo di una simulazione MD

*Figura:* `01_workflow_md.png`.

Una MD si divide in **preparazione** e **ciclo temporale**.

Prima del ciclo si fissano tre cose:

- **Parametri**: potenziale interatomico, dominio (cella di simulazione), ensemble statistico (NVE, NVT, NPT…; fuori da NVE servono termostato/barostato).
- **Posizioni iniziali** $\mathbf x_i(0)$: importate o generate (es. reticolo cristallino), poi **rilassate con steepest descent** (sez. 3.7); infine si calcolano le forze iniziali $\mathbf F_i(0)=-\nabla_i\phi$.
- **Velocità iniziali** $\mathbf v_i(0)$: estratte a caso (distribuzione di Maxwell–Boltzmann a $T_{ini}$), poi corrette con $\mathbf v_{cm}=0$ (niente moto globale) e riscalate per ottenere esattamente $T_{ini}$.

Poi, finché $t<t_{end}$, si ripete il **velocity Verlet** (derivazione già vista nel capitolo precedente: qui solo il richiamo operativo):

$$\mathbf x_i(t+\Delta t)=\mathbf x_i(t)+\mathbf v_i(t)\,\Delta t+\frac{1}{2m}\mathbf F_i(t)\,\Delta t^2 \tag{1}$$

$$\mathbf F_i(t+\Delta t)=-\sum_{j\neq i}\nabla_i\,\phi(r_{ij}) \tag{2}$$

$$\mathbf v_i(t+\Delta t)=\mathbf v_i(t)+\frac{\Delta t}{2m}\left[\mathbf F_i(t)+\mathbf F_i(t+\Delta t)\right] \tag{3}$$

:::{warning}
L'**ordine** conta: (1) posizioni → (2) nuove forze **senza sovrascrivere** $\mathbf F(t)$, perché serve in (3) → (3) velocità. Solo alla fine $\mathbf F(t+\Delta t)$ diventa la $\mathbf F(t)$ del passo successivo (così le forze si calcolano una sola volta per passo).
:::
A ogni passo (o ogni tanti passi) si registrano: energia potenziale $\phi(t)$, cinetica $K(t)$, totale $E=\phi+K$ e temperatura. Con $K=\tfrac12\sum_i m v_i^2$:

$$T=\frac{2K}{3N k_B}$$

(con $\mathbf v_{cm}=0$ i gradi di libertà sono $3N-3$: differenza trascurabile per $N$ grande).

---

### 3.2 Cosa produce una MD: g(r) e fasi della materia

**Due tipi di risultati**: la **configurazione** (posizioni e velocità $\{\mathbf x_i(t)\},\{\mathbf v_i(t)\}$) e le **grandezze scalari** da monitorare nel tempo ($\phi,K,E,T$). Dal post-processing si ricavano cambiamenti qualitativi (nuove configurazioni, temperature critiche, velocità di transizione) e grandezze statistiche (spostamento quadratico medio, pressione, funzioni di correlazione).

:::{tip}
**Regola d'oro**: la simulazione è costosa, quindi **non analizzare dentro il codice di simulazione**. Salva su file tutto ciò che servirà e analizza dopo con script indipendenti: così puoi cambiare analisi senza rifare la simulazione.
:::
**Funzione di correlazione di coppia g(r).** Fissato un atomo di riferimento, il numero medio di atomi entro la distanza $R$ è

$$N(R)=\rho_0\int_0^R 4\pi r^2\, g(r)\,dr,\qquad \rho_0=\frac{N}{V}\ \text{(densità atomica media)} \tag{4}$$

Derivando: $dN=\rho_0\,g(r)\,4\pi r^2dr$. Quindi **g(r) = densità locale a distanza r / densità media**: $g=1$ significa «nessuna struttura» (distribuzione casuale), picchi $g>1$ significano distanze preferite.

Stima numerica (istogramma con passo $\Delta r$, $n_k$ = numero di coppie ordinate $i\ne j$ con distanza in $[r_k,r_k+\Delta r)$, mediato su più configurazioni **dopo** la termalizzazione):

$$g(r_k)\simeq\frac{n_k}{N\,\rho_0\,4\pi r_k^2\,\Delta r}$$

*Figure:* `02_gr_definizione_cristallo.png`, `03_vibrazioni_reticolo.png`, `04_liquido_gr_temperature.png`.

Esempio delle slide (Si, 8×8×8 celle = 2048 atomi, potenziale Stillinger–Weber, NVT, LAMMPS; è un esempio illustrativo, non da riprodurre):

- **Cristallo ideale**: g(r) è una serie di picchi sottilissimi, uno per shell di vicini (1°, 2°, 3°…).
- **$T<T_m$**: gli atomi vibrano attorno ai siti (fononi). I picchi si allargano al crescere di T ma le shell della struttura a diamante restano riconoscibili.
- **$T>T_m$ (2500 K)**: le traiettorie diventano diffusive. Il liquido **non è** una distribuzione casuale ($g\ne1$ ovunque): ha un primo picco largo e poi $g\to1$, cioè **ordine a corto raggio** dovuto ai legami.

*Approfondimento (una riga):* la differenza vibrazione/diffusione si quantifica con lo spostamento quadratico medio $\langle|\mathbf r(t)-\mathbf r(0)|^2\rangle$: limitato nel solido, crescente $\propto t$ nel liquido ($=6Dt$).

---

### 3.3 Medie, ergodicità, termalizzazione e fluttuazioni

*Figura:* `05_media_temporale_ergodicita.png`.

La MD genera **una traiettoria** nello spazio delle fasi; in NVE resta sull'ipersuperficie iso-energetica $H(\mathbf x,\mathbf p)=E$. Per un'osservabile $A$:

$$\langle A\rangle_{MD}\approx\langle A\rangle_t=\lim_{t\to\infty}\frac1t\int_0^t A\big(\mathbf x(t'),\mathbf p(t')\big)dt'
\;\;\overset{\text{ergodicità}}{\longleftrightarrow}\;\;
\langle A\rangle_{NVE}=\frac{\int_{E<H<E+dE}A\,d\mathbf x\,d\mathbf p}{\int_{E<H<E+dE}d\mathbf x\,d\mathbf p} \tag{5}$$

Per il **teorema ergodico** una traiettoria abbastanza lunga esplora tutto lo spazio delle fasi accessibile, quindi media temporale = media d'insieme microcanonica. La NVE è comoda perché traduce direttamente la legge di Newton e descrive correttamente i sistemi isolati.

**Termalizzazione.** Lo stato iniziale non è di equilibrio (es. atomi sui siti del reticolo con velocità casuali): il sistema deve prima rilassare verso l'equilibrio, tramite vibrazioni che avvengono su scale di frazioni di ps. Quel transiente, di durata $t_{th}$ (da pochi ps in su, da verificare su $E_{tot}(t)$ e $T(t)$), va **escluso** dalle medie. La figura `06_termalizzazione_timestep.png` mostra la zona grigia scartata.

**Medie e fluttuazioni dopo la termalizzazione** (con $N$ = numero di passi usati):

$$\langle A\rangle_t=\frac{1}{t-t_{th}}\int_{t_{th}}^{t}A(t')dt'\;\approx\;\frac1N\sum_{i=i_{th}}^{N}A_i \tag{6}$$

$$\delta A=\sqrt{\langle(A-\langle A\rangle)^2\rangle}=\sqrt{\frac1N\sum_{i=i_{th}}^N(A_i-\langle A\rangle)^2}=\sqrt{\langle A^2\rangle-\langle A\rangle^2} \tag{7}$$

(l'ultima uguaglianza: $\langle(A-\langle A\rangle)^2\rangle=\langle A^2\rangle-2\langle A\rangle\langle A\rangle+\langle A\rangle^2=\langle A^2\rangle-\langle A\rangle^2$).

:::{warning}
La temperatura della simulazione **non è** quella con cui hai inizializzato le velocità ($T_{ini}$), ma quella misurata all'equilibrio: $\langle T\rangle\pm\delta T$. Medie e fluttuazioni hanno senso solo dopo la termalizzazione.
:::
:::{note}
**Intuizione (equipartizione, approssimazione armonica).** Se parti dai siti del reticolo (energia potenziale minima) con energia cinetica corrispondente a $T_{ini}$, circa metà dell'energia cinetica si trasferisce in energia potenziale: ci si aspetta $\langle T\rangle\approx T_{ini}/2$. Nel notebook **verificalo numericamente**, e mostra come scegliere $T_{ini}\approx2\,T_{target}$ per ottenere la temperatura voluta.
:::
---

### 3.4 Fluttuazioni fisiche vs errori numerici; scelta del passo temporale

*Figure:* `06_termalizzazione_timestep.png` (se già usata in 3.3, richiamala con `{numref}`), `07_timestep_ottimale.png`.

In NVE due grandezze si comportano in modo opposto, ed è l'idea chiave della sezione:

| | Energia totale $E$ | Temperatura $T$ |
|---|---|---|
| Conservata? | **Sì**, esattamente (Newton, sistema isolato) | **No**: scambio continuo $K\leftrightarrow\phi$ |
| Fluttuazioni | $\delta E$ è **artefatto numerico** (errore di troncamento del velocity Verlet: $\mathrm{err}(\mathbf x)\sim O(\Delta t^4)$, $\mathrm{err}(\mathbf v)\sim O(\Delta t^3)$ per passo) → **da ridurre** diminuendo $\Delta t$ | $\delta T$ è **fisica**, **non dipende** da $\Delta t$ |

Come leggere la figura 06: a 1600 K, con $\Delta t$ = 10, 5, 1 fs la banda di fluttuazione di $E_{tot}$ è ≈ 0.1, 0.02, 0.005 eV. Nella stessa figura si vede il transiente di termalizzazione.

Le fluttuazioni fisiche dipendono dalla **taglia** del sistema:

$$\frac{\delta T}{\langle T\rangle}\approx\frac{1}{\sqrt N} \tag{8}$$

Per $N=256$ atomi è circa il 6 %. Nel limite termodinamico $N\to\infty$ tutti gli ensemble coincidono e le fluttuazioni spariscono ($\delta T\to0$).

**Passo temporale ottimale.** Compromesso: $\Delta t$ piccolo → errori di troncamento bassi ma simulazione lenta (tempi fisici raggiunti troppo corti); $\Delta t$ grande → veloce ma $E$ non conservata. Criterio euristico: il **più grande $\Delta t$** che soddisfa la conservazione dell'energia

$$\frac{\delta E}{|\langle E\rangle|}\le10^{-5} \tag{9}$$

La figura 07 (scala log) mostra che $\delta E/|\langle E\rangle|$ cresce con $\Delta t$ **e con la temperatura**: a T più alta gli atomi si muovono più velocemente, quindi serve un $\Delta t$ più piccolo. Procedura pratica: brevi run NVE per diversi $\Delta t$, grafico di (9) in scala log, scelta dell'intersezione con $10^{-5}$ (da fare nel notebook, vedi esercizio 4).

---

### 3.5 Output e post-processing

*Figura:* `08_ovito_xyz.png`.

Tre principi:

1. Scrivere i dati su **file** per il post-processing (utilizzabili in qualsiasi momento).
2. Stampare a **schermo** solo ogni `nPrint` passi (100, 1000…): stampare è costoso, serve solo a verificare che il codice giri.
3. **Non** salvare le posizioni a ogni passo: da un passo al successivo gli atomi si spostano pochissimo e file numerosi saturano disco e memoria. Salvare ogni `nOut` passi.

```python
with open('output.txt', 'w') as fout:
    for iStep in range(totStep):
        # ... passo di velocity Verlet ...
        fout.write(f'{time}\t{eTot}\t{ePot}\t{eKin}\t{Temp}\n')   # ⚠️ \n a fine riga
        if iStep % nPrint == 0:
            print(f'Time={time} - Energy={eTot}')                  # solo controllo
        if iStep % nOut == 0:
            fname = f'conf{str(iOut).zfill(5)}.xyz'                # zfill: numero fisso di cifre
            np.savetxt(fname, pos, header=f'{nAt}\ntime={time}', comments='')
            iOut += 1
```

**Formato `.xyz` per OVITO** (apre direttamente la sequenza e crea animazioni; con un pattern tipo `conf*.xyz`):

- riga 1: numero di atomi `nAt`;
- riga 2: commento libero (es. `time`, `eTot`, `Temp`);
- righe 3…`nAt`+2: coordinate `x y z` (eventualmente colonne aggiuntive, es. velocità).

:::{warning}
⚠️ Nelle slide l'header è scritto `'f{nAt}\n time={time}'` (la `f` dentro gli apici): è un errore, la f-string è `f'{nAt}\ntime={time}'`. `comments=''` serve a evitare il `#` che `np.savetxt` antepone all'header.
:::
Rilettura (saltando le 2 righe di intestazione): `pos = np.loadtxt(fname, skiprows=2)`. Per un controllo rapido si può usare un `scatter` 3D di Matplotlib; per le animazioni, OVITO o VMD.

**Analisi statistica** (script indipendente, es. `statistics.py`): carica `output.txt`, individua il primo istante dopo la termalizzazione e calcola medie e fluttuazioni con (6)–(7):

```python
data = np.loadtxt('output.txt')
time, eTot, temp = data[:,0], data[:,1], data[:,4]
iTh  = np.searchsorted(time, thTime)        # primo indice con time >= thTime
avgE, dE = eTot[iTh:].mean(), eTot[iTh:].std()   # std con 1/N = formula (7)
```

:::{note}
⚠️ L'approccio «compatto» delle slide usa `eTot[iTh:-1]`, che scarta l'ultimo punto senza motivo; e il ciclo esplicito `for t in Time: ... eTot[t]` confonde tempo e indice. Il blocco sopra è l'equivalente corretto: mostra a parole che un ciclo esplicito con contatore darebbe lo stesso risultato, ma `mean`/`std` sono più brevi e veloci.
:::
---

### 3.6 Il potenziale di Lennard-Jones con raccordo polinomiale

*Figure:* `09_lj_cutoff_netto.png`, `10_lj_raccordo_polinomiale.png`, `11_forza_raccordo_polinomiale.png`.

$$\phi_{LJ}(r)=4\varepsilon\left[\left(\frac{\sigma}{r}\right)^{12}-\left(\frac{\sigma}{r}\right)^{6}\right],\qquad \varepsilon=0.345\ \text{eV},\ \sigma=2.644\ \text{Å (Ag)} \tag{10}$$

Il minimo è in $r=2^{1/6}\sigma\approx2.97$ Å. I vicini successivi dell'fcc con $a\approx4.16$ Å cadono a 2.94 Å (1°, $a\sqrt2/2$), 4.16 Å (2°, $a$), 5.09 Å (3°, $a\sqrt{3/2}$).

**Problema del taglio netto.** Per rendere il calcolo finito si pone $\phi=0$ oltre $r_c=4.5$ Å (tra 2° e 3° vicini). Ma $\phi_{LJ}(r_c)\ne0$: l'energia ha un **salto** e la forza una **singolarità** (delta) in $r_c$. Ogni coppia che attraversa $r_c$ aggiunge o toglie energia: $E$ non si conserva **anche per $\Delta t\to0$**. È un errore del modello, non del integratore.

**Soluzione: raccordo polinomiale.** Si segue LJ fino a $r_p=4.2$ Å, poi un polinomio di grado 7 che porta a zero in $r_c$:

$$\phi(r)=\begin{cases}\phi_{LJ}(r)& r\le r_p\\ P_7(r)=A+Br+Cr^2+Dr^3+Er^4+Fr^5+Gr^6+Hr^7 & r_p<r\le r_c\\ 0 & r>r_c\end{cases}$$

Gli 8 coefficienti si fissano con 8 condizioni, 4 in $r_p$ e 4 in $r_c$ ($k=0,1,2,3$):

$$P_7^{(k)}(r_p)=\phi_{LJ}^{(k)}(r_p),\qquad P_7^{(k)}(r_c)=0 \tag{11}$$

Significato: $k=0$ continuità dell'energia, $k=1$ continuità della forza, $k=2,3$ continuità della derivata prima e seconda della forza. Sono 8 equazioni lineari in 8 incognite, quindi un sistema $8\times8$ ($\tfrac{d^k}{dr^k}r^n=\tfrac{n!}{(n-k)!}r^{n-k}$):

```python
from math import perm   # perm(n,k) = n!/(n-k)!

def poly7_coeffs(phi_derivs_rp, rp, rc):
    """phi_derivs_rp = [phi, phi', phi'', phi'''] di LJ in rp (derivate con sympy)."""
    M, b = np.zeros((8, 8)), np.zeros(8)
    for k in range(4):
        for n in range(k, 8):
            M[k,   n] = perm(n, k) * rp**(n - k)
            M[4+k, n] = perm(n, k) * rc**(n - k)
        b[k] = phi_derivs_rp[k]
    return np.linalg.solve(M, b)          # [A, B, ..., H]
```

:::{warning}
Il sistema è mal condizionato (potenze fino a $r^7$). Verifica sempre che $P_7$ e le sue derivate riproducano le (11) in $r_p$ e $r_c$ (test), oppure lavora con la variabile traslata $r-r_p$. Se il corso fornisce già un `poly7.py`, usa quello e confronta i coefficienti.
:::
**Forza** ($f=-d\phi/dr$, scalare lungo la congiungente):

$$f(r)=\begin{cases}24\,\varepsilon\,\sigma^6\,\dfrac{2\sigma^6/r^6-1}{r^7}& r\le r_p\\[2mm] -P_7'(r)=-\left(B+2Cr+3Dr^2+4Er^3+5Fr^4+6Gr^5+7Hr^6\right)& r_p<r\le r_c\\[1mm] 0&r>r_c\end{cases} \tag{12}$$

La figura 11 mostra che la forza ha un picco nella zona di raccordo: è il prezzo per portare $\phi$ a zero con continuità. Intuitivamente, più stretto è l'intervallo $[r_p,r_c]$, più marcato il picco.

**Forze su un cluster 3D.** Sull'atomo $k$ agiscono tutti gli altri:

$$\mathbf F(k)=\sum_{j\ne k}\big[-\nabla_k\phi(r_{kj})\big],\qquad r_{kj}=\sqrt{(x_k-x_j)^2+(y_k-y_j)^2+(z_k-z_j)^2}$$

$$f_{x,j}(k)=-\frac{\partial\phi(r_{kj})}{\partial r_{kj}}\cdot\frac{x_k-x_j}{r_{kj}}=f(r_{kj})\,\frac{x_k-x_j}{r_{kj}} \tag{13}$$

(idem per $y,z$): il modulo viene dalla $f(r)$ scalare, la direzione è il versore da $j$ a $k$; $f>0$ = repulsione.

**Implementazione**: dentro il doppio ciclo sui vicini scegli il ramo in base alla distanza (`dist < rp` → LJ; altrimenti polinomio).

:::{warning}
⚠️ Due cose da correggere rispetto alle slide: (i) il doppio ciclo sulle liste dei vicini conta **ogni coppia due volte**: l'energia va divisa per 2 (o sommata solo per $j>i$). (ii) `force[i] += f(dist) * dx` richiede che `f` sia già divisa per `dist` (cioè $f(r)/r$), altrimenti usa `dx/dist`. Passa i coefficienti $A\dots H$ come **argomenti** delle funzioni (non come attributi di un oggetto): serve per la compilazione JIT della sez. 3.9.
:::
---

### 3.7 Partire da una configurazione sensata: steepest descent

*Figure:* `12_steepest_superficie_energia.png`, `13_steepest_passo_convergenza.png`, `14_steepest_esempio_864_atomi.png`.

**Perché**: una configurazione generata o importata (come condizione iniziale della MD) in generale **non è un minimo** di energia potenziale: ha forze non nulle. Lanciare subito la MD trasformerebbe l'energia potenziale in cinetica spuria (surriscaldamento). All'equilibrio invece $\mathbf F(k)=0\ \forall k$.

**Idea.** L'energia potenziale $\phi(\{\mathbf r\})$ è una superficie in $3N$ dimensioni (PES); la forza $\mathbf F=-\nabla\phi$ punta sempre verso la discesa più ripida, con modulo proporzionale alla pendenza. Spostando **ogni atomo di poco lungo $\mathbf F$** si scende; ripetendo si arriva al minimo:

$$\delta\mathbf r(k)=C\,\mathbf F(k)\quad\Rightarrow\quad\mathbf r_k\leftarrow\mathbf r_k+C\,\mathbf F(k) \tag{14}$$

($C$ in Å²/eV: spostamento = C × forza.)

- **C piccolo** → passi minuscoli, moltissime iterazioni. **C grande** → si rimbalza attorno al minimo, o l'algoritmo diverge. Strategia semplice per un **C adattivo**: se l'energia sale, rifiuta il passo e dimezza $C$; se scende, aumentalo leggermente.
- **Convergenza**: si ferma quando la forza massima è trascurabile:

$$\max_k\|\mathbf F(k)\|=\max_{k=1..N}\sqrt{F_x^2(k)+F_y^2(k)+F_z^2(k)}\le F_{tol} \tag{15}$$

con $F_{tol}\sim10^{-5}$ eV/Å (nel codice di esempio delle slide $10^{-3}$ con $C=0.005$, più rapido).

```python
for iStep in range(maxStep):                       # maxStep: evita cicli infiniti
    nNbrs, whichNbrs = calc_nbrs(pos, ...)         # liste aggiornate: le posizioni cambiano
    forces = calc_forces(pos, nNbrs, whichNbrs, ...)
    maxf = np.max(np.linalg.norm(forces, axis=1))
    if maxf < ftol:
        break                                      # convergenza raggiunta
    pos = pos + Csteep * forces
```

**Controlli di sanità**: l'energia potenziale deve **decrescere monotonamente** (se no, $C$ troppo grande); $F_{max}$ in generale diminuisce ma può **aumentare localmente** (si minimizza l'energia, non la forza). Nell'esempio delle slide (cluster fcc di Ag, 864 atomi) con $C=0.003$ e $0.01$ le due curve $E(\text{iter})$ convergono allo stesso valore, ma $C$ più grande ci arriva in meno iterazioni (riprodurre con il codice).

:::{note}
Si converge **solo al minimo locale più vicino**. Per trovarne altri bisogna cambiare la configurazione di partenza. Esistono alternative per la minimizzazione multidimensionale, es. gradienti coniugati.
:::
---

### 3.8 Dal cluster al bulk: condizioni periodiche al contorno (PBC)

**3.8.1 Perché un cluster non basta.**

*Figure:* `16_mu_vs_N_cluster.png`, `15_fcc_vicini_mu_bulk.png`.

Un cluster ha molti atomi sotto-coordinati in superficie. Con $V\propto N$ e $S\propto N^{2/3}$:

$$\frac{S}{V}\propto N^{-1/3}$$

decresce lentamente. Se si guarda l'energia per atomo $\mu=E/N$ (dopo minimizzazione), per cluster da $N=4$ a $4000$ atomi $\mu$ scende da ≈ −0.5 eV verso valori più negativi, ma a $N=4000$ è ancora lontana dal bulk.

**Energia del bulk perfetto fcc.** Si prende l'atomo centrale di due celle convenzionali sovrapposte. Con $r_c=4.5$ Å entrano solo 1° e 2° vicini:

- 12 primi vicini lungo $\langle110\rangle$, $r_1=\tfrac{\sqrt2}{2}a$;
- 6 secondi vicini lungo $\langle100\rangle$, $r_2=a$.

$$\mu_{bulk}=\frac12\left[12\,\phi_{LJ}(r_1)+6\,\phi_{LJ}(r_2)\right]\approx-2.32\ \text{eV} \tag{16}$$

Il fattore $\tfrac12$ evita di contare due volte l'energia di ogni coppia; $r_2<r_p$, quindi qui il raccordo non interviene. Verifica il valore numericamente e mettilo nel grafico di $\mu(N)$ come linea orizzontale (fig. 16).

**3.8.2 L'idea delle PBC.**

*Figura:* `17_pbc_immagini_cutoff.png`.

Si assume che la cella $L_x\times L_y\times L_z$ sia una porzione **rappresentativa** di un bulk infinito: ciò che accade in una cella accade in tutte. Quindi si riempie lo spazio replicando la cella:

$$(x,y,z)\to(x+n_xL_x,\ y+n_yL_y,\ z+n_zL_z),\qquad n_x,n_y,n_z\in\mathbb Z$$

Conseguenza: atomi lontani nella cella ($r_{kj}>r_c$) possono interagire **attraverso le immagini** (un atomo vicino al bordo «vede» gli atomi del bordo opposto). La distanza che conta è la minima fra $j$ e **tutte** le immagini di $k$: $r_{kj}^{pbc}$.

*Figura:* `18_pbc_distanza_1D.png`.

Come calcolarla (idea in 1D): sia $\Delta x=x_k-x_j$. Le immagini di $k$ stanno a $\Delta x$, $\Delta x-L_x$, $\Delta x+L_x$. Se $|\Delta x|<L_x/2$ la più vicina è l'originale; altrimenti è l'immagine traslata di $\mp L_x$. Una formula unica copre tutti i casi (anche $x_k<x_j$):

$$\Delta x^{pbc}=\Delta x-L_x\,\mathrm{round}\!\left(\frac{\Delta x}{L_x}\right) \tag{17}$$

($\mathrm{round}$ = intero più vicino: vale 0 se $|\Delta x|<L_x/2$, ±1 altrimenti.) In 3D si applica **componente per componente**:

$$r^{pbc}_{kj}=\sqrt{(\Delta x^{pbc}_{kj})^2+(\Delta y^{pbc}_{kj})^2+(\Delta z^{pbc}_{kj})^2}$$

```python
dx = pos[k, 0] - pos[j, 0]
dx = dx - Lx * np.round(dx / Lx)        # idem dy (Ly), dz (Lz)
```

Va applicato **in tutte le funzioni che calcolano distanze**: assegnazione delle liste dei vicini, energia, forze. Nelle forze il `dx` da usare in (13) è quello già corretto ($\Delta x^{pbc}$), altrimenti la direzione è sbagliata.

**Convenzione dell'immagine minima.** La (17) sceglie una sola immagine per coppia. Perché sia giusto (nessun atomo interagisce con due immagini dello stesso atomo, né con sé stesso) serve

$$L_{min}>2\,r_c \tag{18}$$

*Figura:* `19_pbc_cella_minima_2rc.png` (a sinistra il caso sbagliato, a destra quello corretto). Per Ag con $r_c=4.5$ Å serve $L>9$ Å: una cella fcc di $2\times2\times2$ celle convenzionali ($\approx8.3$ Å) **non basta**; $3\times3\times3$ ($\approx12.5$ Å, 108 atomi) sì.

**3.8.3 Seguire le traiettorie con le PBC.**

*Figura:* `21_pbc_traiettorie.png`.

Una particella che diffonde esce da un lato della cella e rientra dall'altro. Due rappresentazioni, da scegliere in base all'analisi:

- **(a) coordinate non limitate**: si seguono $(x,y,z)$ senza mai riportarle in cella, e le PBC servono solo per le distanze. Necessaria per la **distanza percorsa**, la diffusione, lo spostamento quadratico medio.
- **(b) coordinate riportate in cella**: 

$$x^{pbc}=x-L_x\,\mathrm{floor}\!\left(\frac{x}{L_x}\right)\in[0,L_x) \tag{19}$$

(idem $y,z$; $\mathrm{floor}$ = intero inferiore). Utile per visualizzare **quali atomi interagiscono** con la particella; si perde la misura del percorso reale.

:::{tip}
Due funzioni per due scopi: `round` serve a trovare la **distanza** più corta (17), `floor` a **riportare** un punto dentro la cella (19).
:::
**3.8.4 PBC non è lo stesso del bulk reale.** Per un cristallo ordinato le PBC restituiscono il bulk perfetto, ma restano effetti da tenere presenti:

- Sistema «infinito» → nessuna rotazione; $\mathbf v_{cm}=0$ → nessuna traslazione globale.
- I siti del reticolo sono già il **minimo** di energia: lo steepest descent non cambia nulla (e vale l'equipartizione di sez. 3.3). Per vedere l'effetto del rilassamento, perturba prima le posizioni.
- Il **volume della cella è fisso**: niente dilatazione termica (gli atomi non possono allargare la spaziatura senza premere sulle repliche). Per includerla servirebbe un ensemble NPT.
- Le immagini si comportano tutte **identicamente**: correlazione totale oltre $L_x,L_y,L_z$; da qui la condizione (18).
- Gli effetti a lungo raggio sono riprodotti male se la cella è piccola. Un **difetto puntuale** (vacanza, interstiziale, inclusione) in PBC è in realtà un **array periodico di difetti** con densità $1/(L_xL_yL_z)$, non un difetto isolato (`20_pbc_array_di_difetti.png`).
- Con **due particelle che diffondono** (es. per formare un cluster, o annichilazione vacanza-interstiziale), cella finita + PBC **aumentano la probabilità di incontro** rispetto al sistema reale (`22_pbc_particelle_interagenti.png`): la cella deve essere molto più grande della lunghezza di diffusione caratteristica.

**3.8.5 Un solo codice per bulk, superfici e cluster.**

*Figura:* `23_pbc_vuoto_superfici.png`.

Invece di scrivere due versioni (con `if` che sceglie la definizione di distanza), si tiene **sempre** l'implementazione PBC e si controlla il bordo con le dimensioni della cella:

- **bulk lungo $x$**: $L_x=Na$ ($N$ celle del cristallo) → PBC lungo $x$;
- **superficie libera lungo $x$** (o cluster isolato nelle tre direzioni): $L_x=Na+\Delta$ con $\Delta>r_c$ (meglio $\Delta\gg r_c$) → il vuoto impedisce l'interazione con le repliche, le PBC sono «spente» di fatto.

---

### 3.9 Efficienza del codice

**Operazioni vettoriali.** Su array lunghi (le $N$ posizioni) conviene delegare il ciclo a NumPy:

```python
# lento: doppio ciclo su atomi e componenti
for i in range(natoms):
    for j in range(3):
        pos[i, j] = pos[i, j] + vel[i, j]*dt + 0.5*(force[i, j]/mass)*dt**2

# veloce: un'unica operazione su tutto l'array
pos = pos + vel*dt + 0.5*force/mass*dt**2
```

Ma la vettorializzazione ha un **overhead** (allocazione di array, chiamate a funzioni NumPy): conviene solo su array lunghi. Per la distanza fra due atomi (3 componenti), l'aritmetica scalare è **più veloce**:

```python
dx = pos[i,0]-pos[j,0]; dy = pos[i,1]-pos[j,1]; dz = pos[i,2]-pos[j,2]
dis = (dx*dx + dy*dy + dz*dz)**0.5          # più rapido di np.sqrt(np.sum(dxyz**2))
```

**Interpretato vs compilato.** Python traduce il codice riga per riga a ogni esecuzione: i cicli espliciti sono lenti, mentre C/C++/Fortran, compilati, li gestirebbero molto più velocemente. La compilazione **just-in-time** di Numba converte in codice macchina una funzione decorata, con grande accelerazione dei cicli:

```python
from numba import njit        # njit = jit(nopython=True)

@njit
def calc_nbrs(natoms, pos, rc): ...
@njit
def calc_energy(...): ...
@njit
def calc_forces(...): ...
```

:::{note}
- La **prima chiamata** compila (più lenta); dalle successive la funzione è veloce: misura i tempi dopo un «riscaldamento».
- Dentro le funzioni compilate si usano solo array NumPy, scalari e tuple: per questo i coefficienti del polinomio si passano come **argomenti** (sez. 3.6) e non come attributi di un oggetto `poly7`.
- `calc_nbrs` ha un doppio ciclo su tutte le coppie ($\propto N^2$): va bene per il corso, e proprio per questo è il primo candidato a `@njit`.
:::
Includi una mini-cella di benchmark: tempo di `calc_forces` con e senza `@njit` per $N$ crescente.

---

### 3.10 Workflow completo, esempio guidato ed esercizi

*Figura:* `24_wrapup_file_python.png`.

Il codice si organizza in moduli che condividono il potenziale:

- `potential.py`: energia e forze LJ (con raccordo e PBC), usato sia da `steepest.py` sia da `main.py`;
- `steepest.py`: configurazione `xyz` generica → configurazione `xyz` di minimo di energia;
- `main.py` (MD): legge la configurazione `xyz`, parametri del materiale (massa), temperatura/velocità iniziali, tempo di simulazione; produce $E(t)$, $T(t)$ (e altre osservabili), configurazioni `xyz` a vari tempi, posizioni nel tempo di atomi specifici;
- `statistics.py`: analisi dei file di output (sez. 3.5), anche g(r).

**Esempio guidato** (una cella di codice per passo, ogni passo con 2–3 righe di commento fisico):

1. Costruire un cristallo fcc di Ag $4\times4\times4$ celle convenzionali (256 atomi, $L\approx16.6$ Å $>2r_c$) e perturbare leggermente le posizioni.
2. Rilassare con steepest descent (sez. 3.7), con PBC e LJ raccordato.
3. Assegnare velocità a $T_{ini}$ (Maxwell–Boltzmann, $\mathbf v_{cm}=0$, riscalamento).
4. Evolvere in NVE con velocity Verlet, scrivendo `output.txt` e qualche `.xyz`.
5. Analizzare: scartare la termalizzazione, calcolare $\langle T\rangle\pm\delta T$, $\langle E\rangle$, $\delta E/|\langle E\rangle|$ e g(r).
6. Ripetere per vari $\Delta t$ e scegliere il passo con il criterio (9).

**Esercizi** (breve traccia ciascuno, con soluzione commentata in un blocco `:::{dropdown}`):

1. g(r) dell'Ag a due temperature: riconoscere i picchi di 1°, 2°, 3° vicini e confrontarli con 2.94, 4.16, 5.09 Å.
2. Verificare $\langle T\rangle\approx T_{ini}/2$ e studiare $\delta T/\langle T\rangle$ in funzione di $1/\sqrt N$ con $N=108,\,256,\,500,\,864$ (nota: $N=32$ viola la condizione (18)).
3. A parità di $\Delta t$, confrontare la deriva/fluttuazione di $E_{tot}$ con taglio netto e con raccordo polinomiale.
4. Scansione di $\Delta t$ a due temperature e confronto con la soglia (9).
5. Calcolare $\mu(N)$ con PBC in tutte le direzioni (cristallo perfetto) e con vuoto $\Delta>r_c$ in tutte le direzioni (cluster): mostrare che il primo dà subito $\mu_{bulk}$ mentre il secondo ci arriva lentamente (confrontare con la fig. 16).
