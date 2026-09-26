# Link 3 results — is the anti-windup bound load-bearing?

**Chain:** mech-chain-2026-09-26 · **Prereg:** `mech_chain/link3_prereg.md`
(committed before the run) · **Run date:** 2026-09-26
**Model sha256:** `9f6903c7b51545ee...` (adds `no_bound` param; diff reviewed)
**Log:** `mech_chain/link3_run.log` (40 C-branch .npz outputs preserved)

**Design.** Branch C, 40 seeds (100–139): identical to intact branch A until
fork t0=11.0, then the anti-windup bound forced to 1 (throttle off) for t>t0.
λ=0.5 kept; coupling, damping, EOMs otherwise unchanged.

## Findings

The bound is not a quantitative modulator. It is the only thing preventing
**finite-time runaway**:

- **35/40 seeds:** psi goes NaN between t=49 and t=67 (max|chi| ~ 1e6 before
  blowup).
- **5/40 seeds:** survive to t=70 but are mid-runaway (e.g. seed 107:
  ⟨|chi|⟩ 4.8e-3 at t=50 → 35.2 at t=70).
- The preregistered amplitude comparison is moot — there is no stable C
  branch to compare. The D_sign output of the analysis script is
  NaN-contaminated and discarded.

**Blowup mechanism (analytical, checked against the data).** Linearizing
psi's EOM at the well bottom psi0=±0.316: effective curvature is
m2 − 6D·psi0² + C·chi = −0.08 + chi (C=1). The well bottom destabilizes when
chi ≳ 0.08. Without the throttle, chi drifts toward its linear equilibrium
~(C/2)⟨psi²⟩/F ≈ 0.1 — above threshold — the well ejects psi, psi² drives chi
harder, super-exponential runaway. The bound caps chi below the
destabilization threshold. This is genuine ODE-level positive feedback, not a
dt artifact (a smaller dt would resolve the explosion more accurately, not
prevent it).

## Verdict (preregistered rule fired)

**Mean |C−A| > 0.02 → the bound is load-bearing → mechanism survives as
structurally distinct in this toy.** A conventional linear internal variable
in this coupling blows up; chi is not one. Chain ends (one run, as
authorized). Survival is not validation.

## Owned error

The preregistration stated "unconditionally stable; no blowup expected." That
was wrong: I analyzed chi's EOM in isolation (a damped linear oscillator —
stable) and missed the feedback loop through psi's EOM (+C·chi·psi
destabilizes the well). The adversarial process caught what the analysis
missed. The error is recorded, not edited out.

## Skeptical caveat (limits)

The bound is load-bearing *within the +C·chi·psi architecture* — but that
architecture is the theory's own design choice. The coupling creates the
positive-feedback instability; the bound repairs it. This confirms the
stability postulate is not decorative (its first direct ablation test), but
it does not show that no ordinary architecture captures the same phenomena —
an ordinary modeler would choose a non-amplifying coupling and need no
bespoke throttle.

## Chain verdict (all three links)

- **Outcome selection: BROKEN** (Link 2: ablating all of M leaves the final
  domain pattern unchanged in 39/40 seeds).
- **Mnemonic content (psi_prime, tau, λ): INERT** everywhere tested
  (λ-pair null + Link 2).
- **Amplitude modulation: REAL** (Link 2: chi deepens wells by +0.051 mean
  via the psi²→chi integrator).
- **Anti-windup bound: LOAD-BEARING** (Link 3: prevents finite-time runaway;
  first direct test of the stability postulate — it holds).

Net: the mechanism as posed — retained history guiding/selecting structure —
breaks. What survives is narrower: a stabilized amplitude-modulation channel
whose specifically mnemonic structure does no detectable work.
