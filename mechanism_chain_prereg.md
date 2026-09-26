# Mechanism chain preregistration

**Chain ID:** mech-chain-2026-09-26
**Question (James, 2026-09-25):** does retained history M add predictive value
beyond the present predictive state F? Assay: match F, vary M, test whether
P(F′|F,M) beats P(F′|F) on held-out futures — and per protocol, M must beat
*ordinary* explanations (enlarged Markov states, AR models, delay terms,
generic internal variables), not just F-only.
**Authorization:** James, 2026-09-26 — "continue the simulation experiment
chain until our mechanism breaks"; may stop and ask for help/definitions.
**Scope:** toy-only (vcf1_1 quench simulator). No physical inference.

## Link 1 — minimal fair state from the equations of motion (DONE, analysis only)

Stepping the code (`vcf1_1_quench.py::run`), the Markov state is:

- `psi`, `psi_dot` — second-order field EOM; both required to step.
- `chi`, `chi_dot` — second-order, driven oscillator for surviving history.
- `psi_prime` — first-order recursive echo (memory) variable.
- `phi` — deterministic functional of `chi` via Poisson (not independent).
- `tau = psi − psi_prime` — derived (not independent).

Split (per James's correction — derived from the EOMs, not assumed):

- **F (fair instantaneous state)** = `(psi, psi_dot)`.
- **M (retained history)** = `(chi, chi_dot, psi_prime)`.

Rationale: in Echofoam's own ontology `chi` *is* surviving history density and
`psi_prime` the echo; the mechanism claim is precisely that these add
predictive value beyond the instantaneous field. `psi_prime` reaches `psi`'s
EOM only through `chi` (via `tau` in the chi source: λ term + anti-windup
cap), so ablating the chi channel removes all of M's influence on `psi`.
Considered and set aside: treating `chi` as "just a coupled field" — the
theory defines it as history, so the mechanism must defend that reading.
(James may overrule this split; it is flagged, not buried.)

## Link 2 — causal ablation assay (PREREGISTERED, not yet run)

**Design.** N=40 runs, seeds 100–139 (fresh; no overlap with λ-pair seeds
7–11), baseline params, λ=0.5 (theory default), T_noise=0, chi_source="psi2".
Each seed runs twice from t=0:

- **Branch A (intact):** full dynamics to t_end=70.
- **Branch B (M-ablated):** identical until fork time t0=11.0 (1.0 after the
  quench at t=10; kick absorbed into F, memory mismatch tau large, domains
  not yet settled); for t>t0 the chi channel is removed — `(C·chi·psi)/A`
  dropped from `a_cons`, chi dynamics skipped (chi ≡ 0 in psi's EOM).
  Deterministic (T_noise=0), so A(t)=B(t) for t≤t0 by construction.

**Primary observable.** D_sign = mean over runs of (fraction of grid points
where sign(psi) at t_end differs between A and B).
**Null H0:** mean D_sign ≤ 0.05.
**Secondaries.** ΔD = |⟨|psi|⟩_A − ⟨|psi|⟩_B| over t∈[60,70], margin 0.02
(consistent with lam_pair_prereg.md); wall-count difference at t_end
(descriptive only).
**Controls.** (i) Sham fork: same fork machinery, ablation off → must match
A bit-identically (verifies fork code). (ii) One A-run repeated → bit-identical
(verifies rng discipline).
**Uncertainty.** Bootstrap over the 40 runs, 10,000 replicates; report mean,
SD, 95% interval for D_sign.
**Break rule.** If H0 holds (interval consistent with ≤0.05) AND secondaries
within margins → M causally inert for domain outcomes in this toy/regime →
mechanism BREAKS (strong sense) → chain ends, FAIL recorded. If H0 rejected
→ proceed to Link 3.
**Provenance.** Driver + two-line ablation diff (reviewable), per-seed .npz
for A and B, run log, seeds/config/commands recorded.

## Link 3 — distinctness vs ordinary internal variable (CONDITIONAL sketch)

If Link 2 rejects H0: fit a *conventional* one-mode internal variable
(Maxwell-like, relaxing toward psi² — NO anti-windup bound, NO λ
memory-mismatch term) on training forks; branch C starts from F(t0) only
(IV initialized from F, not from true chi(t0)) and predicts A's trajectory.
If C closes the A−B gap within the Link-2 margins → the history effect is
real but *ordinary* → mechanism BREAKS (distinctness sense). If C cannot
close it → Echofoam-specific structure (bound, λ-channel) is doing work no
ordinary IV captures → mechanism survives as distinct. Full prereg before
running.

## Link 4 — boundary mapping (CONDITIONAL sketch)

If the mechanism survives Link 3: vary λ ∈ {0, 0.5}, T_noise ∈ {0, 3e-4},
kick_amp, and fork time t0 ∈ {11, 20} to map where M's contribution is
largest/smallest. Characterize the domain of the effect; look for the regime
where it vanishes (the breaking point). Full prereg before running.

## Stopping rules

1. **Clean break:** any link preregistered as a falsification test returns its
   break verdict → chain ends; the FAIL (or qualified survival) is recorded
   with evidence, limits, uncertainties, and no further links run on momentum.
2. **Link budget:** at most 4 links. If none breaks the mechanism, the chain
   ends with "survives in tested regimes" + characterization of where M
   matters most. Survival is not validation.
3. **Stop-and-ask:** if a link's result is ambiguous and the next design needs
   a judgment call (observable choice, F/M redefinition, margin change), stop
   and ask James before proceeding. A margin or design change is never made
   post hoc to rescue a result.
4. **Inconclusive handling:** an inconclusive link (like the λ-pair assay)
   does not end the chain by itself; the next link must be designed to
   resolve the specific ambiguity, or the ambiguity is recorded and the chain
   ends.

## What "breaks" means

Two distinct break senses, kept separate: (a) **strong** — M adds no
causal/predictive value beyond F at all (Link 2); (b) **distinctness** — M
adds value but a conventional internal variable adds the same (Link 3).
Either ends the chain with the mechanism shelved for this toy class, pending
a new observable or regime proposed with fresh preregistration.
