#!/usr/bin/env python
"""Link-2 analysis (preregistered in mechanism_chain_prereg.md).

Primary: D_sign = mean over seeds of fraction of grid points with
sign(psi) disagreement at t_end between intact (A) and M-ablated (B).
H0: mean D_sign <= 0.05.
Secondaries: DeltaD late-window amplitude (margin 0.02); walls (descriptive).
Controls: sham forks bit-identical to A.
"""
import glob
import os

import numpy as np

D = os.path.dirname(os.path.abspath(__file__))
SEEDS = list(range(100, 140))
N_BOOT = 10_000
BOOT_SEED = 20260926


def load(seed, fork, ablate):
    fn = (f"echofoam_quench_d0_Dt0_gphi0_lam0.5_fork{fork:g}_ablate{int(ablate)}"
          f"_seed{seed}_output.npz")
    z = np.load(os.path.join(D, fn))
    assert int(z["fork_ablate"]) == int(ablate) and z["fork_t0"] == fork, fn
    return z


def main():
    d_sign, d_amp, walls_a, walls_b = [], [], [], []
    for s in SEEDS:
        a = load(s, 0.0, False)
        b = load(s, 11.0, True)
        assert np.array_equal(a["t"], b["t"]), f"t grid mismatch seed {s}"
        pa, pb = a["psi"][-1], b["psi"][-1]
        d_sign.append(np.mean(np.sign(pa) != np.sign(pb)))
        late = a["t"] >= 60.0
        da = np.mean(np.abs(a["psi"][late]))
        db = np.mean(np.abs(b["psi"][late]))
        d_amp.append(abs(da - db))
        walls_a.append(a["walls"][-1])
        walls_b.append(b["walls"][-1])

    d_sign = np.array(d_sign)
    d_amp = np.array(d_amp)
    rng = np.random.default_rng(BOOT_SEED)
    boots = np.array([rng.choice(d_sign, size=len(d_sign), replace=True).mean()
                      for _ in range(N_BOOT)])
    lo, hi = np.percentile(boots, [2.5, 97.5])

    print(f"n seeds: {len(SEEDS)}")
    print(f"D_sign mean={d_sign.mean():.4f} sd={d_sign.std(ddof=1):.4f} "
          f"95% CI=[{lo:.4f},{hi:.4f}]")
    print(f"D_sign per-seed: min={d_sign.min():.3f} max={d_sign.max():.3f} "
          f"n_zero={(d_sign == 0).sum()}")
    print(f"H0 (mean D_sign <= 0.05): {'HOLDS' if hi <= 0.05 else 'REJECTED'}")
    print(f"DeltaD late-window: mean={d_amp.mean():.4f} max={d_amp.max():.4f} "
          f"(margin 0.02: {'within' if d_amp.mean() <= 0.02 else 'EXCEEDED'})")
    print(f"walls at t_end: A={np.array(walls_a, dtype=int)} "
          f"B={np.array(walls_b, dtype=int)}")

    # Sham-fork control: bit-identical to A.
    for s in (100, 101, 102):
        a = load(s, 0.0, False)
        sh = load(s, 11.0, False)
        diff = np.max(np.abs(sh["psi"] - a["psi"]))
        print(f"sham seed {s}: max|psi_sham - psi_A| = {diff:.3e} "
              f"({'OK' if diff == 0 else 'MISMATCH'})")

    n_files = len(glob.glob(os.path.join(D, "echofoam_quench_*_output.npz")))
    print(f"npz files present: {n_files}")


if __name__ == "__main__":
    main()
