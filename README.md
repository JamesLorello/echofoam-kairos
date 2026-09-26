# echofoam-kairos

Kairos's independent analysis track for the Echofoam research program.

**Roles:** James Lorello makes project decisions. ChatGPT is the primary
integrator and reviewer. Kairos (this track) works independently and
skeptically to clarify, test, critique, and document.

**Standing rules:**
- Echofoam is a speculative, falsification-oriented mechanism search —
  never presented as validated physics or a replacement for established theories.
- One well-defined test or audit at a time; preregister before running.
- Each test states its null, matched controls, observable, uncertainty method,
  and failure/abandonment criteria.
- Negative results and failed predictions stay in the record.
- Code and documentation changes land as reviewable branches, not unreviewed
  main-branch edits.
- Mapping is not claiming.

**Contents:**
- `docs/audit_kairos_sim_track.md` — read-only audit of the vcf1_1 simulation
  track (accepted as first pass 2026-09-25).
- `experiments/lambda-pair/` — preregistered λ=0 vs λ=0.5 quench comparison
  ("memory deepens wells" assay). Verdict: **inconclusive** under the
  preregistered rule. Includes preregistration, seed-level results, driver
  script, run log, and all ten `.npz` outputs.
- `src/` — simulation scripts plus the reviewable diff for the λ-pair run.
