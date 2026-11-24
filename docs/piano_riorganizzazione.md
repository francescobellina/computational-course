# Piano di riorganizzazione del progetto

Analisi del 24 novembre 2026. Il file è escluso dal book (`docs/**` in `myst.yml`).
Si spunta una casella quando il passo è fatto e verificato (test, build del book).

## Stato di partenza (24/11)

- 19 pagine in un indice piatto (8 Markdown, 11 notebook); titoli poco descrittivi.
- Notebook: 4.8 MB; `esercizi_cms6` 980 KB con una cella da 7 minuti.
- Figure: 23 MB, di cui 13 MB duplicati identici in `materials/CMS6_immagini`.
- Codice: due implementazioni di LJ (`lennard_jones.py` cubico, `md_p7.py` P7) e due
  integratori (`md.run_md` in Python puro, `md_p7.run_nve` con Numba).
- Build su GitHub: 20–29 minuti (una volta fallita dopo 42); i notebook nuovi aggiungono
  circa 5 minuti.

## Fase 1 — Pulizia rapida

- [x] Eliminati i file inutili: `CODICE_PER_JUPYTERBOOK.md`, `schema.png` (radice),
      `_site/primary_sidebar_footer.md`, `src/computational_course/run_Ag_cutoff.py` e
      `tests/test_handson_Ag_cutoff.py` (vuoti).
- [x] Eliminato il duplicato `materials/CMS6_immagini/` (identico a `figures/CMS6_immagini/`).
- [x] Eliminate le figure non usate da nessuna pagina né script: `figures/fcc_unit_cell.png`,
      `figures/fcc_lattice.png`, `figures/coordinazione_grid_raggi_uguali.png`,
      `imm4book/logoo_original.png`. Tenuta `figures/fcc_pattern_ptm.png`, prodotta da
      `notebooks/04_handson_Ag_cutoff/fcc_pattern_ptm.py`.
- [x] `generated/` nella radice tolta da git e aggiunta al `.gitignore` (output di
      `convert_to_xyz` lanciato dalla radice, non letto da nessuno).
- [x] Note di lavoro spostate in `docs/`: `revisione_equazioni_del_moto.md` (era
      `outputs/REVISIONE.md`) e `prompt_capitolo_cms6.md` (era in `materials/`).
- [x] Link rotto in `book/intro.md` (pagina su Newton inesistente) e riga spuria
      `:jupyter book start` tolti.
- [x] Titoli vuoti `--- IGNORE ---` e `NELLA PRATICA` tolti da `teoria2.md`.
- [x] Id di cella condivisi tra notebook resi unici (`forze-md`, `7d416f4b`, `6f575974`):
      spariti gli avvisi «Duplicate identifier» della build.
- [x] `myst.yml`: tolte le esclusioni di notebook inesistenti, aggiunta `docs/**`.
- [x] `AGENTS.md`: elenco dei moduli aggiornato.
- [x] PDF del corso fuori dal repository: `materials/*.pdf` nel `.gitignore`, file tenuti in
      locale. Le due consegne tolte anche dal commit dell'Esercizio 1 (non ancora pubblicato).
      Le slide `CMS.6-MD.pdf` restano nella storia già pubblicata (dal commit `6543ed3`):
      toglierle da lì richiederebbe di riscrivere la storia remota.
- [x] `root_finding.py` e il suo test tolti; aggiornati `__init__.py`,
      `scripts/check_project.py`, `01_workflow.md` e `AGENTS.md`.
- [x] `materials/CMS.6-MD.pdf` sostituito con la versione annotata (solo in locale).

## Fase 2 — Esercizio 1

- [x] Nuova `book/06_esercizio1_md/intro.md` («Consegna e piano») sul testo giusto
      (PART 1 + 2): testo tradotto, sotto-esercizi con risultati e stato, note di lettura.
- [x] Testo a 5 punti (`Exercise-MD.pdf`) spostato in `archivio_5_punti.md`, con il suo
      stato (punti 1–3 fatti, 4–5 da fare: potrebbero servire per una parte successiva).
- [x] Parti utili travasate:
      - robustezza del passo con 4 semi e energia «ombra» di Verlet **ricalcolate** per le
        temperature della consegna, nel notebook PART 1 + 2 (§1, «Controlli sul passo»);
      - spostamento dovuto alla sola rotazione stampato nel §1 (7.3 Å in 16 ps a 2500 K);
      - nuova pagina `note_tecniche.md`: unità, numerica del P7 (scalino in r_p, correzione
        di A), criterio ed energia ombra, robustezza, momento angolare, cella, test,
        prestazioni.
- [x] `esercizio1_soluzione.ipynb` e `punti_1_2_passo_temporale.ipynb` archiviati: avviso in
      testa, link ripuntati all'archivio, sottosezione «Archivio» nell'indice. I file restano
      nella cartella attuale fino alla rinomina della fase 3.
- [x] PART 1 + 2, §4 alleggerita: riquadro delle condizioni più corto, derivazioni (caso 1 e
      calcolo di A) sostituite da un rimando a `intro_teoria1` (`sec:tini-mezzi`); restano
      tabella dei casi, dati e figure.
- [x] Riferimenti alla versione a 5 punti tolti da `steepest_descent.md`, dal suo notebook e
      da `approfondimento.md`.
- [x] `orale_domande.md`: link ripuntati a PART 1 + 2 e alle note tecniche; numeri aggiornati
      (energia ombra 4% di K₀ e −1.3% su ⟨T⟩ a 30 K; robustezza con 4 semi; rotazione 7.3 Å) e
      verificati sugli output rieseguiti.
- [ ] Generare i numeri delle domande d'orale da un file di risultati scritto dai notebook:
      rimandato. Oggi il controllo è manuale, dopo ogni riesecuzione di PART 1 + 2.

## Fase 3 — Nuovo indice e cartelle

- [x] Indice in `myst.yml` diviso in parti: Introduzione e Mappa dei concetti; Parte I — Teoria;
      Parte II — Laboratori del corso; Parte III — Esame; Appendici. Differenze dalla proposta:
      le note tecniche restano dentro l'Esercizio 1 (sono specifiche), la mappa dei concetti è
      subito dopo l'introduzione, gli esercizi 2 e 3 entrano quando saranno assegnati.
- [x] Cartelle rinominate con `git mv` e link relativi ricalcolati da uno script (16 file):

```text
book/teoria/              01_meccanica_statistica, 02_approssimazione_adiabatica,
                          03_potenziali_e_cristalli, 05_simulazioni_md, 06_steepest_descent
book/laboratori/          cms4_intro
book/esame/               orale_domande; esercizio1/{consegna, note_tecniche}
book/appendici/           workflow, approfondimento_proteine_hpc4ai, archivio_esercizio1_5_punti
notebooks/teoria/         04_dinamica_molecolare (era 00_molecular_dynamics)
notebooks/laboratori/     cms4/, cms5/equazioni_del_moto, cms6/esercizi_cms6, steepest_descent
notebooks/esame/          esercizio1_part1_2
notebooks/archivio/       esercizio1_soluzione, punti_1_2_passo_temporale
```

- [x] Percorsi nel codice aggiornati: cartelle `generated` di `04_dinamica_molecolare` e
      `equazioni_del_moto`, radice di `fcc_pattern_ptm.py`. Entrambi i notebook rieseguiti in
      una copia dalla nuova posizione.
- [x] «TEORIA 1» divisa in due capitoli (meccanica statistica; approssimazione adiabatica e
      $T_f=T(0)/2$); titoli descrittivi al posto di «TEORIA 2», «MOLECULAR DYNAMICS»,
      «Introduzione all'esercizio», «forze e statica molecolare».
- [x] `book/intro.md` riscritta: tabella delle parti con i link, programma numerato 1–7.
- [x] `01_workflow.md` in appendice; un solo schema (`schema_workflow.jpg`, 320 KB, era 1.4 MB);
      tolti `schema1.png` e `schema3.png` (descrivevano una struttura superata) e
      `imm4book/1.png` (identica a `figures/hero.png`).
- [x] `README.md` riscritto; `AGENTS.md` con la nuova struttura e la convenzione sulle etichette.
- [x] Pagina `book/mappa_concetti.md`: per ogni concetto teoria, verifica numerica e domande.
      Aggiunte le etichette `sec:md-gr`, `sec:md-medie`, `sec:md-passo`, `sec:md-raccordo`,
      `sec:md-efficienza` e `sec:orale-*` per collegarla.
- [x] Convenzione sulle etichette (`sec:`/`eq:`/`fig:` + prefisso di capitolo) scritta in
      `AGENTS.md` e usata per le etichette nuove.
- [ ] Rinominare le etichette esistenti non conformi (per esempio `eq:sd-step`, `eq:ftol`):
      rimandato, perché vanno aggiornati tutti i rimandi e il guadagno è piccolo.
- [ ] Gli URL del sito sono cambiati con le cartelle: eventuali link esterni alle pagine vecchie
      non funzionano più.

## Fase 4 — Teoria senza duplicati

- [x] `03_potenziali_e_cristalli.md`: le due sezioni sulle strutture cristalline unite (tenuta la
      più completa; distanza tra primi vicini e PF del diamante portati dentro); sezioni numerate
      1–4; via il riquadro e la frase in maiuscolo.
- [x] `02_approssimazione_adiabatica.md`: appunti in maiuscolo («B.O.A.», «PANORAMICA», «NELLA
      PRATICA») riscritti in prosa, senza cambiare il contenuto. La separazione dei due capitoli
      era già fatta nella fase 3.
- [x] `04_dinamica_molecolare`: da notebook a pagina Markdown (`book/teoria/`). L'unica cella di
      codice stampava unità e costanti, già riportate nel testo; non va più eseguita in CI.
- [x] `05_simulazioni_md.md` (725 → 631 righe): §7 (steepest descent) ridotta a un rimando al
      capitolo dedicato; §9 (Numba) spostata nella nuova appendice; etichette tenute.
- [x] Una sola spiegazione di ⟨T⟩ = T_ini/2 (`sec:tini-mezzi`): la nota del capitolo 5 e il §6 del
      notebook della steepest descent ora rimandano lì.
- [x] `cms4_intro.md`: segnaposto sostituiti da una procedura in 5 passi e dai link ai notebook.
- [x] CMS 5: sezioni rinumerate (12→4, 13→5, 14→6) e 17 rimandi interni corretti, compresi quelli
      al vecchio «notebook Molecular Dynamics», ora capitolo.
- [x] `esercizi_cms6`: tolte la Parte 2 (P7 con PBC, la cella da 7 minuti) e la Parte 3 (Numba),
      con una nota che dice dove sono finite:
      - confronto cluster/cristallo periodico **ricalcolato** nel §1 di PART 1 + 2 (300 K: 46
        attraversamenti nel cluster, nessuno nel cristallo; 1200 K: 4939 contro 410);
      - curvatura del P7 ricalcolata nel §4.4 di PART 1 + 2 (5.87 eV/Å²);
      - prove di velocità nella nuova appendice `notebooks/appendici/efficienza_codice.ipynb`,
        insieme al testo della vecchia §9 (eseguita: ~10× sulle forze, ~6× sulla MD).
- [x] Rimandi aggiornati in consegna, domande d'orale (A6, F4), note tecniche, mappa dei concetti,
      introduzione e indice.
- [x] Tabelle lunghe: tolta quella da 112 run di CMS 6; l'unica rimasta (110 righe, CMS 4) è già in
      un riquadro a scomparsa.

## Fase 5 — Codice

- [x] `_setup_path` tolto dai 9 notebook: il pacchetto è installato in modalità editable (anche in
      CI, con `uv sync --locked`). Al suo posto `find_project_root`, spostata nel nuovo modulo
      leggero `paths.py` (prima stava in `ovito_visualization.py`, che importa OVITO), con test.
      Celle iniziali dei 9 notebook eseguite dalla loro cartella: tutte OK.
- [x] `poly7.py` spostato da `materials/` a `src/computational_course/` con `git mv`, identico
      byte per byte al file del corso; escluso sia da `ruff check` sia da `ruff format`
      (`pyproject.toml`). Import ovunque `from computational_course.poly7 import poly7`;
      `test_md_p7.py`, consegna, `README.md` e `AGENTS.md` aggiornati.
- [x] Errori di ruff in `ovito_visualization.py` corretti (`ovito` non usato, annotazioni
      `py3Dmol` sotto `TYPE_CHECKING`); `ruff check` e `ruff format --check` su `src/` e
      `tests/` puliti. Negli import dei notebook corretto solo l'ordine (`--select I`).
- [x] **Non fatto, di proposito:** un solo modulo LJ e un solo integratore. `lennard_jones.py` e
      `md.run_md` (liste dei vicini, coda cubica, cicli espliciti come nelle slide) servono ai
      laboratori CMS 4–6, e i numeri citati nel loro testo vengono da lì: unirli a `md_p7.py`
      vorrebbe dire rieseguire quei notebook e ricontrollare il testo. La divisione dei compiti
      è scritta nelle docstring dei tre moduli.
- [x] **Non fatto, di proposito:** modulo `esercizio1.py`. `calcNbrs`, `calcEnergy` e
      `calcForces` sono le funzioni che l'esercizio chiede di scrivere e restano in chiaro nel
      notebook PART 1 + 2 (le note tecniche lo dicono, §7); le altre copie sono solo nei notebook
      d'archivio, che non si toccano più. `prova`, `velocita` e `assi_dt` hanno firme diverse
      nelle tre versioni.
- [ ] Avvisi di ruff rimasti nei notebook (32, quasi tutti `int(round(...))` e `dict()`): fuori
      dal controllo del progetto (`src/`, `tests/`), lasciati.

## Fase 6 — Build e CI

- [x] Meccanismo di MyST verificato nel codice di `jupyter-book` 2.1.7: la chiave di pagina
      `execute.skip` (la vecchia `skip_execution` è deprecata) si può mettere nei metadati del
      notebook, che MyST legge come frontmatter. Con `skip` la build usa gli output salvati.
- [x] Tutti i 9 notebook rieseguiti in locale (24 novembre) e confrontati con gli output salvati:
      numeri identici, a parte i tempi misurati e un'ultima cifra a 1e-10 in CMS 4. Fa
      eccezione `equazioni_del_moto`, i cui output salvati erano vecchi (un `NameError` nella
      cella 4 e il percorso `notebooks/05_molecular_dynamics`): sostituiti con quelli nuovi.
      Tempi in locale: `equazioni_del_moto` 849 s, `esercizio1_part1_2` 136 s,
      `punti_1_2_passo_temporale` 85 s, `esercizi_cms6` 81 s, `esercizio1_soluzione` 34 s,
      gli altri meno di 10 s.
- [x] `execute: {skip: true}` in 7 notebook: i quattro pesanti, l'altro d'archivio e i due di
      CMS 4 con OVITO. In CI restano eseguiti `steepest_descent` e `efficienza_codice` (13 s),
      come prova che il codice del pacchetto gira dentro un notebook.
- [x] `scripts/riesegui_notebook.py` riesegue in locale i notebook esclusi (tutti o filtrati per
      nome); documentato in `README.md`, `AGENTS.md` e nell'appendice «Workflow».
- [x] Build locale con cache di esecuzione vuota (`jupyter book build --html --execute
      --strict`): 12 s, nessun errore, output presenti in tutte le pagine dei notebook esclusi.
      Prima: 21 min 16 s per il passo di build nell'ultima esecuzione su GitHub (`06bfca5`).
      Su GitHub, dopo il push di `0b74d3a`: 23 s per il passo di build, run riuscito.
- [x] Tolto dal workflow il passo che installava Vulkan (`mesa-vulkan-drivers`): serviva solo a
      OVITO per disegnare le immagini dei notebook di CMS 4, che non vengono più eseguiti in CI.
      L'unico test che usa OVITO (`test_lennard_jones.py`) importa `load_structure`, che non
      disegna. Se un notebook con OVITO torna a essere eseguito in CI, il passo va rimesso.
- [ ] Rischio da tenere presente: un notebook escluso non segnala più in CI se il codice
      cambia sotto di lui. Va rieseguito a mano con lo script.
