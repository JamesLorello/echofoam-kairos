# Preregistration: λ=0 vs λ=0.5 quench pair ("memory deepens wells")

**Date:** 2026-09-25. **Status:** preregistered BEFORE any run. No simulations executed yet.

## What λ controls (established by code inspection, `vcf1_1_quench.py`)

λ appears exactly once in the dynamics (line 119):

```
source = gain * (base + 0.5 * p.lam * tau / p.tau_m + p.D_tau * laplacian(tau_s, dx)) * bound
```

where `tau = psi - psi_prime` (line 103) and ψ′ is the exponential memory echo,
`psi_prime += (dt/tau_m)*(psi - psi_prime)` (line 125, λ-independent).

- λ scales **only** the memory-mismatch → χ channel: the term (λ/2)·(Ψ−Ψ′)/τ_m in the χ source.
- λ does **not** touch: the potential (m2, D in `a_cons`), the Ψ EOM otherwise, initialization
  (RNG draws at lines 71/73/84 — order identical, so ICs are bit-identical across the pair),
  the Ψ′ update, or the bound's form. T_noise=0 → no exogenous noise; runs are deterministic given seed.
- With λ=0 the memory echo Ψ′ still exists and evolves; what is removed is its *coupling into χ*.
  Scope of the test: the memory-driven component of χ and its downstream effect on Ψ via CχΨ.

**Confound check: PASS.** The pair isolates the memory contribution. No model change required;
only a bookkeeping change (output filename + saved scalar include λ) to avoid overwriting
the existing `echofoam_quench_d0_Dt0_gphi0_output.npz` baseline.

## Scoped hypothesis

Within `vcf1_1_quench.py` (1D, default Params), the memory-mismatch term increases the settled
well depth through χ accumulation feeding back via CχΨ. I.e., D(λ=0.5) > D(λ=0).

## Metric and window

- **Primary metric:** D = mean over t∈[60,70] of spatial-mean|Ψ(t)| (settled well depth; |·| handles sign).
- **Settling check:** require walls=0 for all snapshots in [60,70] in every run; violation = reported protocol deviation.
- **Secondary (mechanism only, not pass/fail):** mean χ over t∈[60,70] per run — expect higher at λ=0.5 if the memory channel adds χ.

## Design

- Seeds: [7, 8, 9, 10, 11]; paired within seed: λ∈{0, 0.5}.
- All other settings: Params defaults (δ=0, D_tau=0, g_phi=0, T_noise=0, chi_source="psi2", kick_amp=0.25, t_quench=10, t_end=70).
- Effect: d_i = D_i(0.5) − D_i(0). Report each d_i, mean, sample SD, SE=SD/√5.

## Decision rule (bare well = 0.316; previously observed deepening Δ≈0.07)

- **INCONCLUSIVE:** |mean(d)| < 2·SE (too uncertain) OR |mean(d)| < 0.005 (near zero).
- **SUPPORT** ("memory deepens wells" in this toy/regime): mean(d) ≥ +0.02 (≈6% of well depth, well above numerical noise).
- **FAIL** (scoped prediction fails): 0.005 ≤ mean(d) < 0.02 (resolved but below meaningful threshold), or mean(d) ≤ −0.005 (opposite direction — memory shallows wells).

A positive result is support **only** within this specified toy model and parameter regime.
No inference to physical memory, dark matter, or any bridge is licensed by this assay.

## Provenance to preserve

Config (this file), command, `sha256sum` of `vcf1_1_quench.py` before/after the filename diff,
the diff itself, full stdout log, and all 10 `.npz` outputs.
