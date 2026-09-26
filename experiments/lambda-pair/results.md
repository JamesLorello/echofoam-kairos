# Results: λ=0 vs λ=0.5 quench pair ("memory deepens wells")

**Date:** 2026-09-25. **Preregistration:** `../lam_pair_prereg.md` (written before any run).
**Code:** `sim_vcf1_1/vcf1_1_quench.py` sha256 `27bd296f…` (diff vs `ee8b9a72…`: filename/saved-scalar
bookkeeping only — adds `lam` and `seed` to output name and `.npz`; no model change).
**Driver:** `sim_vcf1_1/run_lam_pair.py` (`03b13cc8…`). **Log:** `sim_vcf1_1/lam_pair_run.log` (exit 0).

## Paired results (primary metric D = mean|Ψ| over t∈[60,70]; settling check walls=0 passed in all 10 runs)

| seed | D(λ=0) | D(λ=0.5) | d = D(0.5)−D(0) | ⟨χ⟩ λ=0 → 0.5 |
|------|--------|----------|-----------------|----------------|
| 7    | 0.3832 | 0.3674   | −0.0158         | +0.0145 → +0.0132 |
| 8    | 0.3617 | 0.3689   | +0.0072         | +0.0138 → +0.0136 |
| 9    | 0.3827 | 0.3906   | +0.0078         | +0.0146 → +0.0155 |
| 10   | 0.3666 | 0.3716   | +0.0050         | +0.0143 → +0.0145 |
| 11   | 0.3453 | 0.3110   | −0.0343         | +0.0145 → +0.0142 |

Effect estimate: **mean(d) = −0.0060, SD = 0.0186, SE = 0.0083, 2·SE = 0.0166.**

## Verdict under the preregistered rule

**INCONCLUSIVE** — |mean(d)| = 0.0060 < 2·SE = 0.0166 ("too uncertain"). Signs mixed (3+/2−);
seed-to-seed variation (±0.019) dwarfs the mean effect. This is neither support nor failure
of the scoped prediction; the assay as designed cannot resolve the effect.

## Observations (TOY, not preregistered — hypothesis-generating only)

1. Wells are deepened relative to bare (0.316) in **both** arms (0.31–0.39): the deepening seen
   previously is real in the data, but this assay attributes it to the amplitude-driven (C/2)Ψ²
   χ channel, not the memory-mismatch channel.
2. Final ⟨χ⟩ is nearly identical across λ arms: the memory term (λ/2)(τ/τ_m) contributes little
   at late times — expected in hindsight, since τ=Ψ−Ψ′→0 as the echo catches up after settling.
   The memory channel is self-extinguishing in the settled phase; if it acts, it acts in the transient.

## Limits

n=5 seeds; seed 11 is a large negative outlier (−0.034) with no preregistered outlier rule —
it stays in. Deterministic runs: uncertainty is seed variation only. Metric window was late-time
by preregistration; the transient phase was not assayed.
