#!/usr/bin/env python
"""Link-2 driver (mech-chain-2026-09-26): intact (A) vs M-ablated (B) forks.

Per seed: branch A = full dynamics; branch B = identical until t0=11.0,
then the chi channel is removed (chi zeroed, chi updates skipped).
Controls: sham forks (machinery armed, no ablation) must match A
bit-identically; one repeated A-run checks rng discipline.
"""
import hashlib
import time

import vcf1_1_fork as m


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run_branch(seed, fork_t0, ablate):
    p = m.Params()
    p.seed = seed
    p.fork_t0 = fork_t0
    p.fork_ablate = ablate
    m.run(p)


if __name__ == "__main__":
    print("model sha256:", sha("vcf1_1_fork.py"), flush=True)
    print("driver sha256:", sha("run_mechanism_chain.py"), flush=True)
    t0 = time.time()
    seeds = list(range(100, 140))
    for seed in seeds:
        print(f"===== A seed={seed} =====", flush=True)
        run_branch(seed, 0.0, False)
        print(f"===== B seed={seed} (ablate at t0=11) =====", flush=True)
        run_branch(seed, 11.0, True)
    for seed in (100, 101, 102):
        print(f"===== SHAM seed={seed} =====", flush=True)
        run_branch(seed, 11.0, False)
    h_before = sha("echofoam_quench_d0_Dt0_gphi0_lam0.5_fork0_ablate0_seed100_output.npz")
    print("===== REPEAT A seed=100 =====", flush=True)
    run_branch(100, 0.0, False)
    h_after = sha("echofoam_quench_d0_Dt0_gphi0_lam0.5_fork0_ablate0_seed100_output.npz")
    print("determinism check (hash equal):", h_before == h_after, flush=True)
    print(f"LINK2 DONE in {time.time() - t0:.0f}s", flush=True)
