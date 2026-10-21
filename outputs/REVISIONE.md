# Revisione di `equazioni_del_moto.ipynb` (CMS 5)

Notebook: `notebooks/05_molecular_dynamics/equazioni_del_moto.ipynb` (64 celle, eseguito end-to-end).
Nessuna modifica a `src/`: il codice di scansione e di analisi sta nelle celle del notebook.
## A. Struttura, coerenza dei numeri
- Stessa struttura (sezioni 1-14 + riepilogo), nessun argomento nuovo.
- Ogni numero nel markdown è ora stampato da una cella di codice (controllo automatico
  sui 43 testi markdown: nessun numero senza riscontro negli output).
- Rimossi i numeri non prodotti dal codice: periodo di vibrazione "0.1 ps" (ora stimato
  dalla curvatura LJ: 0.353 ps), "11603/400 K" (ora 290 K), "56 meV" (ora -54.441 meV),
  "20.4 kJ/mol" e altre stime non stampate.
## B. Sezione 11 - scelta di dt
- Protocollo cambiato: durata fisica fissa (2 ps di equilibrazione + 10 ps di produzione)
  invece di 1000+1500 passi uguali per ogni dt.
- Tre semi a 600 K, uno a 1200 e 150 K; la divergenza è gestita (blocchi da 200 passi,
  ricalcolo passo-passo, distanza minima fra atomi).
- Risultati: dt_max = 4 fs (600 K), 2 fs (1200 K), 7 fs (150 K); errore ~ dt^2
  (pendenza 2.03 +- 0.01). A 1200 K e dt = 20 fs la simulazione diverge (min_r = 0.095 A).
## C. Sezione 12.1 - fluttuazioni di T
- Aggiunta la giustificazione: dT/T = sqrt(2/(3N)) * sqrt(c_V/C_V), che nel limite
  armonico (c_V ~ c_K) dà 1/sqrt(3N): la potenza è N^{-1/2}, il prefattore dipende dal
  sistema. Non è una dimostrazione per il LJ, e il testo lo dice.
- Cinque box (3^3, 4^3, 6x3x6, 5^3, 6^3) x 3 semi, errore via bootstrap (2000 estrazioni).
- Pendenza -0.504 +- 0.047; il punto non cubico (N = 432) cade sulla retta dei cubici;
  fit ristretto ai cubici -0.500. Si spiega perché un cubo FCC esatto con 432 atomi
  non esiste e si aggiunge il punto cubico 5^3 (500 atomi).
## D. Sezione 13 - g(r), solido e liquido
- Il reticolo a rho* = 1 non fonda a 4000 K (MSD piatta, terzo guscio FCC ancora a
  1.84): era un solido caldo, non un liquido. Ora il liquido è preparato in una scatola
  espansa (rho* = 0.85, T* = 0.97), punto che cade nella regione liquida.
- Il termostato di riscalamento è descritto come soluzione semplice per lo stato
  iniziale, non come ensemble canonico.
- Aggiunti MSD e coefficiente di diffusione come prova dello stato: D = 0.621 A^2/ps nel
  liquido, 0.0000 nel solido; il terzo guscio scende da 4.19 a 1.21.
## E. Sezione 10 - equilibrio
- Il transitorio è misurato, non dichiarato: minimo 226.5 K a 0.044 ps, ultimo passo
  fuori banda +-20% a 0.060 ps, rientro in banda a 0.064 ps.
## F. Sezione 8.1 - velocità iniziali
- Corretto: la regola T_f ~ T_i/2 è verificata a T_i = 1200 K (rapporto 0.503,
  errore 0.6%), non a 600 K.
## G. Sezione 9 - potenziale
- Salto al cutoff stampato: -54.441 meV con cutoff sharp, -9.948e-10 meV con il
  raccordo polinomiale.
## H. Refusi e formattazione
- "del second'ordine" -> "del secondo ordine"; "il scaling" -> "lo scaling";
  "le gusci" -> "i gusci"; "sistemazioni FCC" -> "configurazioni FCC";
  "del programma" riformulato in 13.3.
- Rimossi i path assoluti dagli output (il notebook funziona da qualsiasi directory);
  i file generati restano in `notebooks/05_molecular_dynamics/generated/`.
## Verifica
- Esecuzione completa del notebook senza errori (24 celle di codice, ~15 min); controllo
  automatico: ogni numero del markdown compare in un output.
- Consegna: `outputs/equazioni_del_moto.ipynb` + `outputs/REVISIONE.md`.
  `/mnt/user-data/outputs` non è scrivibile in questo ambiente (read-only), quindi i due
  file sono stati depositati in `outputs/` nel repository.
