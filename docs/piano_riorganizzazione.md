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

- [ ] Nuova `book/06_esercizio1_md/intro.md` sul testo giusto (PART 1 + 2); il testo a 5 punti
      (`Exercise-MD.pdf`) va in archivio.
- [ ] Travasare in PART 1 + 2 (o in «Note tecniche») le parti utili delle pagine superate:
      scalino del P7 in r_p (correzione di A), robustezza del passo con 4 semi, energia
      «ombra» di Verlet, momento angolare.
- [ ] Archiviare `esercizio1_soluzione.ipynb` e `punti_1_2_passo_temporale.ipynb` in una
      sottosezione «Archivio: versione a 5 punti» (i punti 4–5 sull'adatomo potrebbero
      servire per la PART 3).
- [ ] PART 1 + 2, §4: lasciare tabella dei casi e dati, rimandare la teoria a
      `intro_teoria1` (`sec:tini-mezzi`).
- [ ] `orale_domande.md`: verificare i numeri dopo ogni riesecuzione; valutare di generarli
      da un file di risultati scritto dai notebook.

## Fase 3 — Nuovo indice e cartelle

- [ ] Riorganizzare `myst.yml` in parti:

```text
Introduzione
  Il corso, il programma e come usare il book       (intro.md, riscritto)
Parte I — Teoria
  1. Meccanica statistica classica                  (intro_teoria1 §1)
  2. Approssimazione adiabatica; T_f = T(0)/2       (intro_teoria1 §2 + riquadro)
  3. Potenziali interatomici e cristalli            (teoria2, senza duplicati)
  4. Integrare le equazioni del moto                (00_molecular_dynamics → .md)
  5. Simulazioni MD: dal potenziale alla statistica (05_md_pbc, senza §7 e §9)
     5.1 Steepest descent: teoria                   (da 06_esercizio1_md)
Parte II — Laboratori del corso
  CMS 4 — Ag: coordinazione, forze, statica         (notebook 04 + intro completata)
  CMS 5 — Equazioni del moto                        (equazioni_del_moto)
  CMS 6 — Esercizi                                  (esercizi_cms6, solo Es. 1–5)
  Steepest descent: implementazione e verifiche     (notebook)
Parte III — Esame
  Esercizio 1 — MD di LJ-Ag (PART 1 + 2)
    Consegna e piano
    Soluzione                                       (esercizio1_part1_2)
  Esercizio 2 — Monte Carlo cinetico                (da fare)
  Esercizio 3 — Metropolis Monte Carlo              (da fare)
  Domande per l'orale
Appendici
  Note tecniche (unità, numerica del P7, energia ombra, momento angolare, test)
  Efficienza del codice (NumPy e Numba)
  Approfondimento: MD di proteine e HPC4AI
  Workflow del repository                           (01_workflow)
  Archivio: Exercise-MD.pdf, versione a 5 punti
```

- [ ] Rinominare le cartelle (`book/teoria/`, `book/laboratori/`, `book/esame/`, …) in un solo
      passaggio, aggiornando tutti i link relativi.
- [ ] Titoli descrittivi al posto di «TEORIA 1», «TEORIA 2», «MOLECULAR DYNAMICS»,
      «Introduzione all'esercizio».
- [ ] Riscrivere `book/intro.md` (ordine dei titoli, programma, come usare il book).
- [ ] Spostare `01_workflow.md` in appendice; un solo schema, compresso (oggi 3 PNG da
      1.4–2 MB; `schema3.png` fa scattare l'avviso «Image is too large»).
- [ ] Aggiornare `README.md` (intestazione doppia, comandi git in cima) e `AGENTS.md`
      (struttura delle cartelle).
- [ ] Pagina «Mappa dei concetti»: per ogni concetto, dove sono teoria, verifica numerica e
      domanda d'orale.
- [ ] Etichette coerenti con un prefisso per capitolo (`sec:`, `eq:`, `fig:`).

## Fase 4 — Teoria senza duplicati

- [ ] `teoria2.md`: unire le due sezioni sulle strutture cristalline (§2 e §6).
- [ ] `intro_teoria1.md`: separare meccanica statistica e approssimazione adiabatica; titoli
      non in maiuscolo.
- [ ] `00_molecular_dynamics.ipynb` → pagina Markdown.
- [ ] `05_md_pbc.md`: §7 (steepest descent) ridotta a un rimando; §9 (Numba) spostata in
      appendice.
- [ ] Una sola spiegazione di ⟨T⟩ = T_ini/2 (in `intro_teoria1`); altrove una riga di rimando.
- [ ] `book/04_handson_Ag_cutoff/intro.md`: riempire o togliere i segnaposto.
- [ ] `equazioni_del_moto`: numerazione delle sezioni (oggi salta da §3 a §12).
- [ ] `esercizi_cms6`: togliere la Parte 2 (P7 con PBC, superata dalla versione sul cluster;
      tenere una tabella sul confronto PBC/cluster) e la Parte 3 (Numba, in appendice).
- [ ] Tabelle lunghe (scansioni Δt × T, 112 run) ridotte a un riassunto, con la tabella completa
      in un riquadro a scomparsa.

## Fase 5 — Codice

- [ ] Un solo modulo per il potenziale LJ, con la coda a scelta (nessuna, cubica, P7) e PBC per
      direzione; `lennard_jones.py` e `md_p7.py` uniti, test aggiornati.
- [ ] Un solo integratore: `md.run_md` come involucro di `run_nve`.
- [ ] Togliere `_setup_path` dai 9 notebook: il pacchetto è già installato in modalità editable.
      Dare a `poly7.py` un posto stabile nel pacchetto, citando la fonte.
- [ ] Modulo `esercizio1.py` per le funzioni oggi duplicate nei notebook (`calcForces`,
      `calcEnergy`, `calcNbrs`, `prova`, `velocita`, `assi_dt`).
- [ ] Correggere i 3 errori di ruff in `ovito_visualization.py`.

## Fase 6 — Build e CI

- [ ] Salvare gli output dei notebook pesanti (`esercizi_cms6`, `equazioni_del_moto`,
      `esercizio1_part1_2`, notebook con OVITO) ed escluderli dall'esecuzione in CI: verificare
      il meccanismo di MyST.
- [ ] Misurare di nuovo il tempo della build dopo le fasi 4–6.
