# Audit: Kairos sim track (vCF-1.x toys)

**Audit date:** 2026-09-25. **Auditor role:** secondary analyst, read-only.
**Scope:** files, history, and results inspectable in the local workspace. No new simulations were run for this audit; `.npz` outputs were loaded and recomputed only to check reported figures.

## Repository, revision, coverage

- **Repository:** none. `~/workspace/echofoam/sim_vcf1_1/` is **not under version control** (no `.git`; `git rev-parse` fails). There is no branch, commit, or revision to cite.
- **Coverage examined:** 17 Python scripts, 45 `.npz` result files, 25 `.png` figures, `battery.sh`, two tune logs, `frames*/` snapshot dirs, 4 `.gif`s. All files dated **2026-09-24** (single working day).
- **Seeds (in code):** 42 (`vcf1_1.py`, `vcf1_1_logtau.py`, `vcf1_1_doublewell.py`), 7 (quench/probe/sweep scripts), 11 (merger battery via `battery.sh`). All use `np.random.default_rng(seed)`.
- **Labels below are the provisional working labels supplied 2026-09-25** (KNOWN, EQ, TOY, TOY-C, FAIL, BRIDGE, CONCEPT, META, PSQ). No project document defining them was found in the workspace; no canonical glossary exists locally.

## What this track is and is not

- **Direct dark-matter tests in this track: zero.** `grep -ri "dark matter"` over all 17 scripts returns nothing. No rotation-curve fit, no lensing comparison, no N-body or halo code exists here.
- **Adjacent work present:** gravity-loop toys (1D/2D), quench/domain-formation toys, bubble-chamber (grain) toys, kernel-merger battery. These are mechanism toys for χ/Ψ dynamics, not DM tests.
- **DM content lives elsewhere:** the "spacetime lock-step" hypothesis (2026-09-25) is CONCEPT with no toy; earlier "cohesive effect" permutations per the ChatGPT audit belong to the ChatGPT track, not this one.

## Evidence ledger

### A. Base model and anti-windup (EQ + TOY)

- **EQ:** `vcf1_1.py` encodes Ψ̈=(B/A)∇²Ψ+(C/A)χΨ−(2D/A)Ψ³; χ̈=[−Fχ+(C/2)Ψ²+(λ/2)(Ψ−Ψ′)/τ_m−γ_χχ̇]/E; Ψ̇′=(Ψ−Ψ′)/τ_m. Velocity-Verlet/leapfrog, periodic BCs, N=256, L=10, dt=1e-3, 50k steps, seed 42. Output: `echofoam_minimal_1d_output.npz`.
- **EQ (anti-windup):** implemented exactly as stated — `bound = max(0, 1−|χ|/(|τ|+ε))`, multiplicative on the χ source, in `vcf1_1_logtau.py:103-108`, `vcf1_1_doublewell.py`, `vcf1_1_quench.py:107-112`, `vcf1_3_probe.py:89-92`. Comment in code: "The repair cannot exceed the wound... This is integrator anti-windup."
- **TOY:** anti-windup ON is the validated baseline across quench/probe/gravity runs (all stable runs use it). `break1d.py` B1 contains the anti-windup-OFF comparison (code verified; numerical outputs were printed to stdout, not saved).
- **Gap:** the original "linear-tension blowup → stabilized" validation numbers are chat-reported; no pre/post-fix outputs are both saved. The stabilization claim rests on code + the stability of all subsequent runs, not on a saved A/B pair.

### B. Overcorrection δ sweep (TOY, partial)

- **Code verified:** `sweep_delta.py` sweeps δ∈{0, 0.3, 0.7, 1.5, 3.0} with pre-registered metrics (final walls, max|χ|/max|τ|, ring amplitude, blowup at max|Ψ|>10) and verdict logic. `vcf1_1_quench.py:37,104-112` implements gain=(1+δ), cap=(1+δ)|τ|; δ=0 recovers baseline.
- **Saved outputs found:** δ=0 variants only (`echofoam_quench_d0_Dt*.npz`). **No δ=0.3/0.7/1.5/3.0 outputs exist on disk.**
- **Verdict:** the δ_c∈(1.5,3.0) claim, the "δ=3.0 violent oscillation" and "δ=1.5 damped" characterizations are **unverified from files** (chat-reported). The sweep procedure is TOY-grade; its results are not in the record.

### C. Quench experiments (TOY + TOY-C + FAIL)

- **TOY (protocol):** `vcf1_1_quench.py` — Kibble-Zurek-style: single well (m²=−0.09) relaxes, quench at t=10 to double well (m²=0.04, wells ±0.316) + random kick (amp 0.25), seed 7. `vcf1_2_quench.py` is the 2D version (N×N grid, Langevin bath optional).
- **TOY (verified from `echofoam_quench_output.npz`):** walls 134→0 (single uniform domain); final E=0.0758; final ⟨Ψ⟩=−0.388 vs bare well minimum −0.316 — the field settles **deeper** than the bare well, consistent with the CχΨ coupling (final ⟨χ⟩=+0.0112 deepens the effective well).
- **TOY (wall/bulk):** recomputed from the saved npz: mean|χ| wall-zone/bulk ratios 0.98–1.16 across snapshots (undilated sign-change mask). Consistent with the reported ≈1.01; the exact figure's method is not saved. Qualitative finding stands: χ is **not** wall-localized (order-unity ratios, not ≫1).
- **TOY (Langevin):** 1D noise sweep `echofoam_quench_T{0,0.0003,0.001,0.003,0.01}_output.npz` — walls_f=0 at every T; no mosaic. Verified.
- **TOY-C (memory deepens wells):** the code contains the mechanism (CχΨ coupling; χ>0 deepens the effective quadratic coefficient), and the single-seed result (0.388 > 0.316) is consistent. But **no memory-off control run is saved** (no λ=0 or C=0 quench variant on disk). The isolated causal claim "memory deepens wells" is therefore TOY-C, not TOY. *This is the cleanest available mechanism-first test not yet run.*
- **Unverified under audit:** the sign-symmetry correction (10/10 → 3+/7−). No multi-seed quench ensemble is saved; the claim has no file evidence.
- **FAIL (2D mosaic):** the T=3e-4 "mosaic" was corrected to noise froth (field never reaches wells); recorded as a corrected misread, not a persisting claim. No persistent multi-domain mosaic exists in any saved run — an HONEST negative result for domain chemistry in this toy.

### D. Gravity loop (TOY + FAIL)

- **EQ/BRIDGE:** `poisson_phi` in `vcf1_1_quench.py:51-60` solves ∇²φ=4πG_eff(χ−⟨χ⟩) by FFT with k=0→0 ("uniform surviving history does not gravitate — the background goes into the scale factor"); back-reaction −g_φφΨ in the Ψ EOM. **The χ→Poisson step is BRIDGE (assumed)** — asserted in code comments, no derivation on disk.
- **TOY (1D, verified from `echofoam_quench_d0_Dt0_gphi{0,0.03,0.1,0.3}_output.npz`):** g_φ≤0.1 stable and near-identical (max|Ψ|=0.68); g_φ=0.3 runaway — max|Ψ|=**21.00**, low-k χ power share 0.19→**0.88** (reported 0.20→0.87; matches within rounding). Critical g_φ∈(0.1,0.3).
- **TOY (2D, verified from `echofoam_quench2d_T0_gphi{0,0.1,0.2}_output.npz`):** walls at t=40 = **1062→1476→1974** — gravity monotonically brakes coarsening; all runs stable (max|ψ|≈0.3), all end at one domain.
- **FAIL:** strong gravity has no saturation mechanism — the runaway is unbounded (Jeans-like collapse with no pressure term). Anti-windup does not prevent it (windup moved into Ψ). Open, recorded.

### E. Bubble-chamber / grain battery (TOY + TOY-C + FAIL)

- **TOY (protocol):** `vcf1_3_probe.py` — localized packet (coupling A) fired through a relaxed single-well medium; pre-registered metric (time-max of mean|χ| in traversed window minus background); artifact controls in the docstring (σ≫dx, damped medium, A=0 null, seed ensemble, Mach check). 2D version: `vcf2_3_probe.py`.
- **TOY (response curve):** numbers hardcoded in `analyze_probe.py:27-28` (from `sweep_probe.py` output): trail 9.7e-4 (A=0.02, below null bg 1.07e-3) → 5.3e-3 → 1.78e-2 → 4.73e-2 → 1.54e-1 → 3.56e-1 at A=1.0. Ratios consistent with ∼A² at small A saturating toward linear (anti-windup provides the saturation); τ wake ∼A (linear). A_c≈0.03 is a smooth crossover, not a sharp threshold (`break1d.py` A1 fine scan implements the check).
- **TOY (break-it battery):** `break1d.py` implements A1 (threshold fine scan), A2 (N=1024 resolution), A3 (detector params γ_ψ, F), B1 (anti-windup off), B2 (dose hypothesis A·σ/v — rejected in code comments), B3 (negative coupling/holes), B4 (stationary probe), C1 (90-time-unit sub-threshold leak), C2 (blind inversion), D1 (Mach vs c=√B). `followup1d.py` adds F1–F4 (A=2.0 with bound, D=0 saturator test, dose law at D=0, stationary-probe metric). Procedures verified; numerical outcomes printed to stdout, not saved.
- **TOY-C:** blind-inversion recovery (reported 10%/4%/2% for true A=0.035/0.15/0.7) — procedure in `break1d.py:74-81`, figures chat-reported, not on disk. Sign asymmetry (holes vs bumps) — B3 code exists; the **"λ=0 erases it"** follow-up has **no saved code or output** → unverified under audit.
- **FAIL (scope):** the battery tests *imposed* packets (grain), not emergent shattering of a kernel into quanta. Recorded as the honest limit.

### F. Merger battery (TOY-C + FAIL)

- **TOY (protocol):** `battery.sh` documents the 6-run battery exactly as executed (orbit g_φ=0.03/0.06/0.12, head-on, single control, no-gravity; seed 11; tend 80–100). `vcf2_4_merger.py` + `analyze_merger.py` (D1–D3c criteria pre-stated in the analyzer docstring).
- **TOY (verified from `echofoam_merger_*.npz`, seed 11):**
  - **D1 — FAIL (clean negative):** no orbital capture at any tested g_φ (t_merge=−1 for all three; min separations 6.70/3.60/6.92). No inspiral/deconfliction measurement was possible.
  - **D2 — contaminated:** head-on merged at t=31.5; high-k χ 0.11→0.57; total χ 5.9→8461 (runaway — the no-saturation collapse, same FAIL as §D). Excess inseparable from runaway.
  - **D3a — ambiguous:** head-on pre-merger aspect ratio max = 3.02, coinciding with overlap + runaway onset (possible tracker artifact).
  - **D3b — FAIL as discriminator:** post-merger banding fit τ=418 on a 100-unit run (fit longer than the data — unreliable by construction); single-kernel control shows banding too. Banding is a kernel property, not a sorting signature.
  - **D3c:** only head-on merged — supports "gentle gravity cannot capture" over "shear sorts."
  - g_φ=0.12 orbital ran away (χ 5.9→12730) without merging — same collapse FAIL.
- **Diagnostics on disk:** `merger_diagnostics.png`, `merger_banding.png`.

### G. Assay note: the minimal fair state (META)

From the model equations (`vcf1_1_quench.py`): Ψ is second-order in time → needs (Ψ, Ψ̇); χ is second-order → needs (χ, χ̇); Ψ′ (the exponential memory echo) is first-order → needs Ψ′. **Full Markov state: (Ψ, Ψ̇, χ, χ̇, Ψ′)** — the system is Markovian in this state by construction.

Consequences for P(F′|F,M) vs P(F′|F):

1. **F must not be Ψ alone.** The Ψ EOM contains χ (CχΨ term), so (Ψ, Ψ̇) is not dynamically adequate without χ. A reported "memory advantage" over F=Ψ alone would be trivially won by any M containing χ's present value — that is a missing-variable win, not a memory win.
2. **Minimal fair F: (Ψ, Ψ̇, χ, χ̇)** — the dynamically adequate present state excluding the echo. Then M={Ψ′}: does the exponential echo add predictive value beyond the present fields? This is the non-circular comparison the toy can actually run.
3. **Circularity warning:** the toy implements memory *as* an enlarged Markov state (Ψ′ is an auxiliary field). Any "memory effect" found here (e.g., well-deepening) is formally an internal-variable/delay-line effect. The toy can show that this history-dependence has dynamical consequences; it **cannot** establish irreducible or physical memory, and it cannot discriminate against ordinary explanations (enlarged Markov states, internal variables, hysteresis) because it *is* one.
4. **Non-trivial assay requires:** either (a) a toy variant where memory is purely a functional of Ψ-history with no independent χ dynamics, or (b) a Markovianized control — replace χ by an instantaneous functional of (Ψ, Ψ̇) and test whether the genuine history content adds anything. Neither exists on disk.

## Findings

1. The track is a coherent, well-instrumented set of mechanism toys with pre-registered metrics, artifact controls, seed discipline, and honestly recorded FAILs. Code matches described procedures throughout.
2. **Every quantitative claim re-checked against saved outputs reproduced** (gravity runaway 21.00; low-k 0.19→0.88; 2D walls 1062→1476→1974; merger t=31.5/aspect 3.02/band-τ 418; wall/bulk ≈1; 1D no-mosaic at all T).
3. **Gaps between chat-reported and file-evidenced:** δ-sweep verdicts (no δ≠0 outputs saved), blind-inversion percentages, sign-asymmetry λ=0 follow-up, multi-seed bias correction, anti-windup A/B validation pair. Procedures exist in code for most; numbers do not.
4. **No version control exists.** Findings rest on filesystem state of 2026-09-24; nothing is citable by commit.
5. **Zero direct dark-matter tests** in this track; the χ→Poisson bridge is assumed, not derived.

## Evidence and limits

- Evidence: 17 scripts + 45 `.npz` + figures listed above; recomputation from saved arrays for the figures quoted.
- Limits: read-only audit; stdout-only results (sweeps, break-it batteries) are unverifiable post-hoc; chat-reported numbers without saved artifacts are marked as such, not treated as findings.

## What remains uncertain

- Whether "memory deepens wells" survives a matched memory-off control (the λ=0 quench was never saved).
- The δ_c boundary (outputs missing).
- Whether any memory effect in this architecture is distinguishable from an enlarged Markov state (META: by construction, no).
- All physical bridges (χ→φ→gravity→mass; grain→particle; merger→astrophysics) are assumed mappings.

## One recommended next step

Run the **matched λ=0 vs λ=0.5 quench pair** (memory→χ coupling off/on, identical seeds/configs, pre-registered metric: effective well depth ⟨|Ψ|⟩_final and settling time): the smallest experiment that promotes "memory deepens wells" from TOY-C to TOY-or-FAIL, and the natural first assay of whether retained history does dynamical work beyond the present state.
