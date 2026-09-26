#!/usr/bin/env python
"""Link-3 analysis (preregistered in link3_prereg.md).

Primary: per-seed late-window |<|psi|>_C - <|psi|>_A|, mean over seeds.
Margin 0.02. Verdict: mean <= 0.02 -> bound inert -> DISTINCTNESS BREAK.
Descriptive: D_sign(C vs A).
"""
import os

import numpy as np

D = os.path.dirname(os.path.abspath(__file__))
SEEDS = list(range(100, 140))
N_BOOT = 10_000
BOOT_SEED = 20260926


def load(seed, tag):
    fn = (f"echofoam_quench_d0_Dt0_gphi0_lam0.5_fork{tag}_seed{seed}_output.npz")
    return np.load(os.path.join(D, fn))


def main():
    d_amp, d_sign = [], []
    for s in SEEDS:
        # A files were written before the nobound tag existed (nobound=0);
        # C files carry fork11_ablate0_nobound1.
        a = np.load(os.path.join(
            D, f"echofoam_quench_d0_Dt0_gphi0_lam0.5_fork0_ablate0_seed{s}_output.npz"))
        c = load(s, "11_ablate0_nobound1")
        assert np.array_equal(a["t"], c["t"]), f"t grid mismatch seed {s}"
        assert c["no_bound"] == True, f"no_bound flag missing seed {s}"
        late = a["t"] >= 60.0
        d_amp.append(abs(np.mean(np.abs(c["psi"][late]))
                         - np.mean(np.abs(a["psi"][late]))))
        d_sign.append(np.mean(np.sign(c["psi"][-1]) != np.sign(a["psi"][-1])))

    d_amp = np.array(d_amp)
    d_sign = np.array(d_sign)

    # NaN check FIRST: a non-finite trajectory is a stability failure, not data.
    # The preregistered amplitude comparison is undefined on NaN runs, and
    # NaN <= 0.02 evaluates False -- it must never silently select a verdict.
    n_nan = int(np.isnan(d_amp).sum())
    if n_nan > 0:
        print(f"n seeds: {len(SEEDS)}")
        print(f"STABILITY FAILURE: {n_nan}/{len(SEEDS)} C-branch runs went "
              f"non-finite (NaN).")
        print("The preregistered amplitude comparison is UNDEFINED on these "
              "runs; no threshold rule fires.")
        print("Post-hoc observation only: removing the anti-windup bound "
              "produces finite-time runaway under this feedback coupling, so "
              "the bound is load-bearing for stability within this "
              "architecture. The distinctness question (can a stabilized "
              "ordinary IV reproduce the amplitude effect?) is NOT answered "
              "by this link.")
        return

    rng = np.random.default_rng(BOOT_SEED)
    boots = np.array([rng.choice(d_amp, size=len(d_amp), replace=True).mean()
                      for _ in range(N_BOOT)])
    lo, hi = np.percentile(boots, [2.5, 97.5])

    print(f"n seeds: {len(SEEDS)}")
    print(f"|C-A| late amplitude: mean={d_amp.mean():.4f} sd={d_amp.std(ddof=1):.4f} "
          f"95% CI=[{lo:.4f},{hi:.4f}]")
    print(f"per-seed: min={d_amp.min():.4f} max={d_amp.max():.4f}")
    print(f"D_sign(C vs A): mean={d_sign.mean():.4f} max={d_sign.max():.3f}")
    if d_amp.mean() <= 0.02:
        print("VERDICT: bound inert -> DISTINCTNESS BREAK. "
              "chi == conventional linear internal variable.")
    else:
        print("VERDICT: bound is load-bearing -> mechanism survives as "
              "structurally distinct in this toy.")


if __name__ == "__main__":
    main()
