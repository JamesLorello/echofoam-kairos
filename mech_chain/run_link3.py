#!/usr/bin/env python
"""Link-3 driver: branch C = intact until t0=11, then anti-windup bound off.

40 seeds (100-139). Compares against Link-2 branch A outputs (already on disk).
"""
import hashlib
import time

import vcf1_1_fork as m


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


if __name__ == "__main__":
    print("model sha256:", sha("vcf1_1_fork.py"), flush=True)
    t0 = time.time()
    for seed in range(100, 140):
        print(f"===== C seed={seed} (bound off at t0=11) =====", flush=True)
        p = m.Params()
        p.seed = seed
        p.fork_t0 = 11.0
        p.fork_ablate = False
        p.no_bound = True
        m.run(p)
    print(f"LINK3 DONE in {time.time() - t0:.0f}s", flush=True)
