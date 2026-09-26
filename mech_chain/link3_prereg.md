# Link 3 preregistration — is the anti-windup bound load-bearing?

**Chain:** mech-chain-2026-09-26 · **Authorized:** James, 2026-09-26
("one run of Link 3, don't get too into the weeds, break the branch clean").
**Status when written:** Link 2 complete (mixed: domain-choice null 39/40,
amplitude effect +0.051 mean). No Link-3 data seen — this is preregistered.

## Rationale

Link 2 showed the chi channel deepens wells (+0.051) but does not select them
(39/40). The λ memory-mismatch channel is inert (λ-pair null). The only
remaining Echofoam-distinctive structure in M is the **anti-windup bound**
(source throttled by 1 − |chi|/(|tau|+eps)). If the bound does nothing, chi
is exactly a conventional linear internal variable (damped oscillator driven
by psi²) — the history effect is real but *ordinary*.

## Design

Branch C, 40 seeds (100–139, same as Link 2): identical to intact branch A
until fork t0=11.0, then the bound is forced to 1 (throttle off) for t>t0.
Everything else — coupling C=1, λ=0.5 kept, damping, EOMs — unchanged.
One code param (`no_bound=True`); reviewable diff.

**Primary observable.** Per-seed late-window (t∈[60,70])
|⟨|psi|⟩_C − ⟨|psi|⟩_A|, mean over seeds. Margin 0.02 (same as the Link-2
amplitude margin — this is the effect being tested).
**Descriptive.** D_sign(C vs A) at t_end — does bound removal change domain
choice (expect no, per Link 2).
**Uncertainty.** Bootstrap 10k over seeds for the mean; report 95% CI.
**Controls.** Sham/determinism already verified for the fork machinery in
Link 2 (bit-identical); the only new code path is the bound bypass, exercised
by construction in every C run.

## Verdict rule (decisive, one run)

- **Mean |C−A| ≤ 0.02** → the bound is inert → chi ≡ conventional linear
  internal variable (λ already inert) → **DISTINCTNESS BREAK**. The history
  effect is ordinary. Chain ends; mechanism shelved for this toy class.
- **Mean |C−A| > 0.02** → the bound is load-bearing (it quantitatively shapes
  the deepening) → mechanism **survives as structurally distinct** in this
  toy. Chain ends (one run only, per authorization); survival is not
  validation.

No fitting, no gain tuning, no follow-up links on momentum. Numerical
stability: without the throttle, chi's linear equilibrium is ~psi² ≈ 0.1
(damped oscillator, unconditionally stable); no blowup expected.
