(sec:mappa-concetti)=
# Mappa dei concetti

Per ogni concetto del corso, dove si trovano la **teoria**, la **verifica
numerica** (notebook) e le **domande d'orale** che lo riguardano. Serve per
ripassare e per ritrovare in fretta un risultato da mettere su una slide.

| Concetto | Teoria | Verifica numerica | Orale |
|---|---|---|---|
| Ensemble NVE e NVT, medie, ergodicità | [meccanica statistica](#sec:ms-meccanica-statistica); [medie e termalizzazione](#sec:md-medie) | [CMS 5](../notebooks/laboratori/cms5/equazioni_del_moto.ipynb), §12 | [F](#sec:orale-metodo), E8 |
| $T_f=T(0)/2$: le tre condizioni | [quando vale](#sec:tini-mezzi) | [PART 1 + 2](../notebooks/esame/esercizio1_part1_2.ipynb), §3–4 | [domanda tipo](#sec:orale-tipo), [E](#sec:orale-temperatura) |
| Partenza fuori dal minimo, $\Delta U/(3Nk_B)$ | [quando vale](#sec:tini-mezzi), caso 1 | PART 1 + 2, §3 (confronto con il punto 1) | E1 |
| Anarmonicità, coefficiente $A$ | [quando vale](#sec:tini-mezzi), caso 3 | PART 1 + 2, §4.3 | E2–E5 |
| Transiente, $t_{th}$, fluttuazioni $\propto1/\sqrt N$ | [quando vale](#sec:tini-mezzi), caso 2; [fluttuazioni e passo](#sec:md-passo) | PART 1 + 2, §4.2; [CMS 6](../notebooks/laboratori/cms6/esercizi_cms6.ipynb), Es. 2 | E6, E7 |
| Potenziale LJ, taglio netto, raccordo $P_7$ | [raccordo polinomiale](#sec:md-raccordo) | PART 1 + 2, §0–1; [note tecniche](#sec:es1-note-tecniche), §2 | [A](#sec:orale-modello) |
| Velocity Verlet, criterio sul passo | [dinamica molecolare](../notebooks/teoria/04_dinamica_molecolare.ipynb); [scelta del passo](#sec:md-passo) | [CMS 5](../notebooks/laboratori/cms5/equazioni_del_moto.ipynb), §3; PART 1 + 2, §1 | [B](#sec:orale-passo) |
| Energia «ombra», robustezza del passo | [note tecniche](#sec:es1-note-tecniche), §3–4 | PART 1 + 2, §1 (controlli sul passo) | B2, B8 |
| Steepest descent: $C$, $C_\text{crit}$, $F_\text{tol}$ | [steepest descent](#sec:es1-sd-teoria); [quanto vale $C$](#sec:es1-sd-passo) | [steepest descent](../notebooks/laboratori/steepest_descent.ipynb) | [D](#sec:orale-sd) |
| Traiettorie: centro e superficie, momento angolare | [note tecniche](#sec:es1-note-tecniche), §5 | PART 1 + 2, §1 | [C](#sec:orale-traiettorie) |
| Coordinazione, liste dei vicini, forze | [potenziali e cristalli](teoria/03_potenziali_e_cristalli.md) | [CMS 4](laboratori/cms4_intro.md) | A5 |
| Funzione di distribuzione radiale $g(r)$ | [g(r) e fasi](#sec:md-gr) | [CMS 5](../notebooks/laboratori/cms5/equazioni_del_moto.ipynb), §13; CMS 6, Es. 1 | — |
| Condizioni periodiche (PBC), immagine minima | [PBC](#sec:md-pbc) | CMS 6, Es. 5 e Parte 2 | A6 |
| Efficienza: NumPy, Numba, $O(N^2)$ | [efficienza del codice](#sec:md-efficienza) | CMS 6, Parte 3 | F4 |
| MD di proteine e calcolo parallelo | [approfondimento](#sec:es1-approfondimento) | — | — |

:::{tip} Come leggere la tabella
Le lettere della colonna «Orale» sono i gruppi di domande della pagina
[Domande per l'orale](#sec:orale-domande); le sigle come E2 indicano una
singola domanda dentro il gruppo.
:::
