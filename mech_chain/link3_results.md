# Link 3 results — is the anti-windup bound load-bearing?

**Chain:** mech-chain-2026-09-26 · **Prereg:** `mech_chain/link3_prereg.md`
(committed before the run) · **Run date:** 2026-09-26
**Model:** `mech_chain/vcf1_1_fork.py` (sha256 `9f6903c7...`; reviewable diff
vs the ChatGPT-side `vcf1_1_quench.py`)
**Log:** `mech_chain/link3_run.log` · **Driver:** `mech_chain/run_link3.py`
**Outputs:** 40 C-branch `.npz` files (local; SHA256 manifest
`mech_chain/output_manifest.sha256` — 69 MB total, not pushed to git)

**Design.** Branch C, 40 seeds (100–139): identical to intact branch A until
fork t0=11.0, then the anti-windup bound forced to 1 (throttle off) for t>t0.
λ=0.5 kept; coupling, damping, EOMs otherwise unchanged.

## Findings

**35/40 C-branch runs went non-finite** (psi NaN between t=49 and t=67;
max|chi| ~ 1e6 before blowup). The remaining 5 reached t=70 but were
mid-runaway (e.g. seed 107: ⟨|chi|⟩ 4.8e-3 at t=50 → 35.2 at t=70).

The preregistered primary — late-window |⟨|psi|⟩_C − ⟨|psi|⟩_A| against the
0.02 margin — is **undefined** on non-finite runs. **Neither preregistered
threshold branch fired.** An earlier version of this report claimed the
"load-bearing" branch had fired; that was an error (see Corrections). The
analysis script originally let NaNs flow into `mean <= 0.02` (NaN comparison
is False) and printed a verdict it had not earned; it now classifies NaN runs
explicitly as stability failures.

**Blowup mechanism (analytical, consistent with the data).** Linearizing
psi's EOM at the well bottom psi0=±0.316: effective curvature is
m2 − 6D·psi0² + C·chi = −0.08 + chi (C=1). The well bottom destabilizes when
chi ≳ 0.08. Without the throttle, chi drifts toward its linear equilibrium
~(C/2)⟨psi²⟩/F ≈ 0.1 — above threshold — the well ejects psi, psi² drives chi
harder: super-exponential runaway. The bound caps chi below the
destabilization threshold. This is genuine ODE-level positive feedback, not a
dt artifact.

## Corrected interpretation

- The bound **does something**: removing it destroys the simulation. That is
  a real, reproducible finding — the stability postulate's first direct
  ablation test, and it holds.
- It is a **post-hoc observation, not a preregistered verdict.** The planned
  amplitude test could not run. The distinctness question as framed — *can a
  stabilized ordinary internal variable reproduce the amplitude effect?* — is
  **not answered** by this link. Answering it needs a stabilized comparator
  (e.g. saturating coupling or fitted gain), which was not run.
- Skeptical caveat, unchanged: the instability is created by the theory's own
  +C·chi·psi coupling; the bound repairs what the architecture breaks. An
  ordinary modeler would choose a non-amplifying coupling and need no bespoke
  throttle. Load-bearing *within this architecture*.

## Corrections (review 2026-09-26)

1. The claim that the preregistered "load-bearing" rule "fired" is withdrawn:
   the rule's comparison was undefined. Reclassified as unexpected stability
   failure, separate from the planned amplitude test.
2. `analyze_link3.py` patched: NaN runs now halt with an explicit stability
   classification instead of falling through a NaN comparison into a verdict.
3. `analyze_link2.py` patched: the misleading `H0... REJECTED` label now
   reads "NOT established: upper CI exceeds 0.05."
4. Reproduction artifacts pushed to the branch: the model module
   (`vcf1_1_fork.py`), both run logs, both drivers/analyses, and a SHA256
   manifest of all 123 `.npz` outputs (regenerable from the pushed code; the
   69 MB of outputs themselves are not in git).

## Chain verdict, corrected (all three links)

- **Outcome selection: no reliable selection advantage detected.** 39/40
  seeds unchanged under full M ablation, but the 95% interval [0, 0.075]
  crosses the 0.05 margin — equivalence within the margin is *not*
  established. (An earlier chat summary overstated this as "broken";
  corrected.)
- **Mnemonic content (psi_prime, tau, λ): inert** everywhere tested
  (λ-pair null + Link 2).
- **Amplitude modulation: real toy-model effect** (Link 2: chi deepens wells
  by +0.051 mean — separate from the selection question).
- **Anti-windup bound: load-bearing for stability** (Link 3, post-hoc:
  removal → finite-time runaway in 35/40 seeds). The distinctness question
  remains open.

Net, stated carefully: the selection claim finds no support in this assay;
the specifically mnemonic machinery is inert; what the history channel
demonstrably does is modulate amplitude, and the bound demonstrably keeps the
toy finite. No physical validation follows from any of this.
