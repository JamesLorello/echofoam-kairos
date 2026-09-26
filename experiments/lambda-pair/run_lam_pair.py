#!/usr/bin/env python
"""run_lam_pair.py -- execute the preregistered lambda=0 vs 0.5 quench pair.

Preregistration: ../lam_pair_prereg.md
Seeds [7,8,9,10,11] x lam {0.0, 0.5}; all other Params at defaults.
Outputs: echofoam_quench_d0_Dt0_gphi0_lam{LAM}_seed{SEED}_output.npz (10 files).
"""
import numpy as np
import vcf1_1_quench as q

SEEDS = [7, 8, 9, 10, 11]
for seed in SEEDS:
    for lam in [0.0, 0.5]:
        p = q.Params()
        p.seed = seed
        p.lam = lam
        print(f"===== PAIR seed={seed} lam={lam} =====", flush=True)
        q.run(p)
print("LAM_PAIR_DONE")
