# Link 2 results — causal ablation assay

**Chain:** mech-chain-2026-09-26 · **Prereg:** `mechanism_chain_prereg.md`
**Run date:** 2026-09-26 · **Model sha256:**
`4af60c8c6629fe48257c9ae88582a0b25216c4c1cbb5ee304888a8e8f74774f0`
**Driver sha256:**
`54f9f38d6d6135842df9ca31a6bdd80b601ed8c7157d7054434fdf8b140c6198`
**Log:** `mech_chain/link2_run.log` (83 .npz outputs preserved)

**Design.** 40 seeds (100–139). Branch A: intact dynamics. Branch B: identical
until t0=11.0, then the chi channel removed (chi/chi_dot zeroed, chi updates
skipped). Deterministic (T_noise=0), so A(t)=B(t) for t≤t0 by construction.

## Findings

**Primary — D_sign** (fraction of grid points with sign(psi) disagreement at
t_end, mean over seeds):
- mean = 0.0250, SD = 0.1581, bootstrap 95% CI = [0.0000, 0.0750]
  (10k replicates, seed 20260926)
- 39/40 seeds: D_sign = 0 (ablating the entire history channel changed
  nothing about the final domain pattern)
- 1/40 seeds (107): D_sign = 1.0 — whole-domain flip (A settled −, B
  settled +; both branches clean single domains, min|psi| 0.337 vs 0.286)
- Preregistered H0 (mean ≤ 0.05): **not rejected** — point estimate and most
  of the interval sit below 0.05.

**Secondary — ΔD** (late-window t∈[60,70] ⟨|psi|⟩ difference, margin 0.02):
- mean = 0.0510, max = 0.1168 → **margin exceeded**
- Direction: 36/40 seeds positive (intact runs have DEEPER wells); 4 near
  zero/negative (−0.023 to −0.001).
- The chi channel systematically deepens wells by ~0.05.

**Tertiary — walls at t_end:** all 40 seeds end walls=0 in both branches
(descriptive; ablation did not change the coarsening outcome).

**Controls.**
- Sham forks (machinery armed, no ablation), seeds 100–102:
  max|psi_sham − psi_A| = 0.000e+00 — bit-identical. Fork machinery verified.
- Repeated A-run, seed 100: output hash identical — rng discipline verified.

## Verdict vs preregistration

The preregistered break rule required H0-holds AND secondaries-within-margins
for a strong break. H0 was not rejected on the primary, but the amplitude
secondary exceeded its margin. **Neither preregistered branch fires cleanly —
ambiguous case.** Per stopping rule 3, the chain stops here pending James's
read; no further link runs on momentum.

## Cross-assay dissociation (clean side result)

- λ-pair assay (2026-09-25): λ=0 vs 0.5 → late amplitude ΔD mean −0.0060 ±
  0.0083 — no detectable effect of the memory-mismatch (λ·tau) channel.
- Link 2: removing ALL chi → amplitude drops 0.051 mean.
- Joint reading: the well-deepening is caused by the **amplitude-driven
  (psi²) chi channel**, not the λ memory-mismatch channel. The specifically
  *mnemonic* content of M (psi_prime, tau, λ) is inert for both observables
  tested; the *integrator* content (psi² → chi accumulation) deepens wells but
  does not select them (39/40).

## Ledger mapping (ChatGPT stop-point rubric)

- Domain-choice observable → rubric row 3: "F-only stays within the margin —
  no material history advantage shown for the tested observable and regime."
- Amplitude observable → no clean rubric row: real causal effect (M modulates
  magnitude), but the rubric does not distinguish modulation from selection.
  Recorded as its own finding, not forced into a row.
