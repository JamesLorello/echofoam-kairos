#!/usr/bin/env python
"""vcf1_1_quench.py -- the molecule breaks and re-forms.

Kibble-Zurek-style quench protocol:
  Phase 1 (t < t_quench): single well (m2 < 0). The field relaxes to Psi~0.
      This is the stable molecule.
  Quench (t = t_quench): the potential flips to a double well (m2 > 0) AND
      the field gets a random kick. The kick is the energy input that breaks
      the old configuration -- bond-breaking is never free.
  Phase 2 (t > t_quench): different regions fall into different wells ->
      phase-locked domains separated by walls. Walls coarsen (tension at
      walls = mismatch between neighbors' choices), chi accumulates at the
      walls (memory of the breaking), and the system settles into fewer,
      larger domains: a new, more stable base.

Chi keeps the validated anti-windup bound; Psi keeps its damping (the cost
of correction). Tension mode: linear (validated combo).
"""

import numpy as np
from scipy.ndimage import gaussian_filter1d

class Params:
    N = 256
    L = 10.0
    dt = 1e-3
    t_quench = 10.0
    t_end = 70.0
    output_every = 1000
    A = 1.0; B = 1.0; C = 1.0; D = 0.2; E = 1.0; F = 0.5
    gamma_chi = 0.1
    gamma_psi_settle = 0.3   # phase 1: relax fast
    gamma_psi = 0.1          # phase 2: cost of correction
    lam = 0.5; tau_m = 0.5
    m2_single = -0.09        # phase 1: single well at 0
    m2_double = 0.04         # phase 2: wells at +-sqrt(m2/2D) = +-0.316
    overcorrect_delta = 0.0  # repair aims past the wound: |chi| <= (1+delta)|tau|
    D_tau = 0.0              # tension conduction: mismatch diffuses, D_tau*laplacian(tau)
    chi_source = "psi2"      # "psi2": amplitude-driven (C/2)Psi^2; "tau2": tension-driven K_tau*tau^2
    K_tau = 2.0              # strength of tension-driven chi sourcing
    T_noise = 0.0            # Langevin bath temperature: feeder-history fluctuations.
                             # 0 = deterministic (baseline). Noise ~ sqrt(2*gamma*T*dt).
    G_eff = 1.0              # gravity: Nabla^2 phi = 4 pi G_eff (chi - <chi>)
    g_phi = 0.0              # gravity back-reaction: Psi EOM += -g_phi * phi * Psi
                             # phi<0 near surviving history -> amplifies Psi there
    psi_noise_0 = 0.05
    kick_amp = 0.25          # the breaking: energy input at quench
    chi_noise = 0.001
    seed = 7
    fork_t0 = 0.0        # M-ablation fork time; 0 = disabled (intact run)
    fork_ablate = False  # at fork_t0: zero chi/chi_dot and skip chi updates
    no_bound = False     # Link 3: force anti-windup bound to 1 (throttle off)


def laplacian(f, dx):
    return (np.roll(f, 1) - 2 * f + np.roll(f, -1)) / dx**2


def poisson_phi(chi, dx, G_eff):
    """Solve Nabla^2 phi = 4 pi G_eff (chi - <chi>) on a periodic grid via FFT.
    The k=0 mode is set to 0: uniform surviving history does not gravitate --
    only inhomogeneities do (the background goes into the scale factor)."""
    k = 2 * np.pi * np.fft.fftfreq(len(chi), dx)
    chi_hat = np.fft.fft(chi - chi.mean())
    k2 = np.where(k == 0, 1.0, k**2)
    phi_hat = -4 * np.pi * G_eff * chi_hat / k2
    phi_hat[k == 0] = 0.0
    return np.real(np.fft.ifft(phi_hat))


def run(p: Params):
    rng = np.random.default_rng(p.seed)
    dx = p.L / p.N
    psi = p.psi_noise_0 * rng.standard_normal(p.N)
    psi_dot = np.zeros(p.N)
    chi = p.chi_noise * rng.standard_normal(p.N)
    chi_dot = np.zeros(p.N)
    psi_prime = psi.copy()

    n_steps = int(p.t_end / p.dt)
    t_hist, psi_hist, chi_hist, walls_hist, e_hist, tau_hist, phi_hist = [], [], [], [], [], [], []
    quenched = False
    forked = False
    for step in range(1, n_steps + 1):
        t = step * p.dt
        if p.fork_t0 > 0 and t >= p.fork_t0 and not forked:
            forked = True
            if p.fork_ablate:
                chi[:] = 0.0; chi_dot[:] = 0.0
                print(f"--- FORK at t={t:.1f}: chi channel ablated ---", flush=True)
            else:
                print(f"--- FORK at t={t:.1f}: sham fork (intact) ---", flush=True)
        if t >= p.t_quench and not quenched:
            quenched = True
            psi = psi + p.kick_amp * rng.standard_normal(p.N)  # the breaking
            print(f"--- QUENCH at t={t:.1f}: double well + kick ---", flush=True)
        m2 = p.m2_double if quenched else p.m2_single
        gpsi = p.gamma_psi if quenched else p.gamma_psi_settle

        # Gravity: chi -> phi via Poisson (instantaneous Newtonian handoff),
        # then phi guides Psi: where surviving history is dense (phi<0),
        # the wells deepen -- mass-like structure from persistent history.
        phi = poisson_phi(chi, dx, p.G_eff) if p.g_phi > 0 else 0.0
        a_cons = (p.B * laplacian(psi, dx) + m2 * psi
                  - 2 * p.D * psi**3 + p.C * chi * psi
                  - p.g_phi * phi * psi) / p.A
        # Langevin bath: the feeder histories never shut up. Fluctuation-
        # dissipation pairs the noise with the damping: sqrt(2*gamma*T*dt).
        noise = (np.sqrt(2 * gpsi * p.T_noise * p.dt) * rng.standard_normal(p.N)
                 if p.T_noise > 0 else 0.0)
        psi_dot = (psi_dot + p.dt * a_cons + noise) / (1 + p.dt * gpsi)
        psi = psi + p.dt * psi_dot

        tau = psi - psi_prime
        # Overcorrection: the engine applies (1+delta) times the correction
        # and tolerates (1+delta) times the wound. delta=0 recovers the
        # validated anti-windup baseline.
        gain = 1.0 + p.overcorrect_delta
        cap = gain * np.abs(tau) + 1e-12
        bound = 1.0 if p.no_bound else np.maximum(0.0, 1.0 - np.abs(chi) / cap)
        # Tension conduction: mismatch spreads to neighbors, so the source
        # feels tau curvature. tau is smoothed first: the Laplacian of raw
        # grid-scale spikes would amplify noise (1/dx^2), not conduct wounds.
        # Corrections propagate instead of staying local.
        tau_s = gaussian_filter1d(tau, sigma=2.0, mode='wrap')
        if p.chi_source == "tau2":
            base = p.K_tau * tau**2
        else:
            base = 0.5 * p.C * psi**2
        source = gain * (base + 0.5 * p.lam * tau / p.tau_m
                         + p.D_tau * laplacian(tau_s, dx)) * bound
        chi_ddot = (-p.F * chi + source - p.gamma_chi * chi_dot) / p.E
        if not (forked and p.fork_ablate):
            chi_dot = chi_dot + p.dt * chi_ddot
            chi = chi + p.dt * chi_dot

        psi_prime = psi_prime + (p.dt / p.tau_m) * (psi - psi_prime)

        if step % p.output_every == 0:
            t_hist.append(t); psi_hist.append(psi.copy()); chi_hist.append(chi.copy())
            tau_hist.append((psi - psi_prime).copy())
            phi_hist.append(poisson_phi(chi, dx, p.G_eff))
            walls_hist.append(np.sum(np.sign(psi[:-1]) != np.sign(psi[1:])))
            g = (np.roll(psi, -1) - psi) / dx
            e_hist.append(np.mean(
                0.5 * psi_dot**2 + 0.5 * p.B * g**2 - 0.5 * m2 * psi**2
                + 0.5 * p.D * psi**4 - 0.5 * p.C * chi * psi**2
                + 0.5 * chi_dot**2 + 0.5 * p.F * chi**2))
            if step % 10000 == 0:
                print(f"step {step:6d} t={t:5.1f} <|Psi|>={np.mean(np.abs(psi)):.4f} "
                      f"walls={walls_hist[-1]:.0f} E={e_hist[-1]:.4f} "
                      f"<|chi|>={np.mean(np.abs(chi)):.2e}", flush=True)

    fn = (f"echofoam_quench_d{p.overcorrect_delta:g}_Dt{p.D_tau:g}_gphi{p.g_phi:g}_lam{p.lam:g}"
          f"_fork{p.fork_t0:g}_ablate{int(p.fork_ablate)}_nobound{int(p.no_bound)}"
          f"_seed{p.seed}_output.npz")
    np.savez(fn, t=np.array(t_hist),
             psi=np.array(psi_hist), chi=np.array(chi_hist),
             tau=np.array(tau_hist), phi=np.array(phi_hist),
             walls=np.array(walls_hist), energy=np.array(e_hist),
             t_quench=p.t_quench, m2_double=p.m2_double, D=p.D,
             delta=p.overcorrect_delta, D_tau=p.D_tau, g_phi=p.g_phi,
             lam=p.lam, fork_t0=p.fork_t0, fork_ablate=p.fork_ablate,
             no_bound=p.no_bound)
    print(f"Saved {fn}")


if __name__ == "__main__":
    run(Params())
