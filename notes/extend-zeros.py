#!/usr/bin/env python3
"""extend-zeros.py — recompute the Gram crystal to 800 intervals.

Extends /tmp/zero-data.json (400 gaps) to 800 gaps, matching lou's "thirty
slips in eight hundred gaps" so the collective's counts can be cross-checked
against the actual critical line.

Output: /tmp/zero-data-800.json
  grams[801]  — Gram points g_0..g_800 (theta(t) = n*pi)
  zeros[]     — all zeta zeros with Im(z) < g_800
  counts[800] — zeros per interval (g_n, g_{n+1}]
  diff[801]   — N(g_n) - (n+1): the count difference, the never-moving count
  events[]    — runs where diff != 0: each run is one Frenkel slip (a vacancy
                with its doubling)
  near[]      — for every Gram point: [g_n, nearest_zero, |nearest-g_n|/gap]
"""

import json
import numpy as np
from mpmath import zetazero, grampoint, mp

mp.dps = 20

NGAP = 800

# --- Gram points ----------------------------------------------------------
print("computing Gram points...")
grams = [float(grampoint(k)) for k in range(NGAP + 1)]
gmax = grams[-1]
print(f"  g_800 = {gmax:.2f}")

# --- zeros up to gmax ------------------------------------------------------
print("computing zeros...")
zeros = []
k = 1
# zetazero(1) is the first non-trivial zero
while True:
    z = float(zetazero(k).imag)
    if z > gmax:
        break
    zeros.append(z)
    if k % 200 == 0:
        print(f"  {k} zeros, last {z:.2f}")
    k += 1
    if k > 3000:   # safety: should never hit
        break
zeros = np.array(zeros)
print(f"  {len(zeros)} zeros below g_800 = {gmax:.2f}")

# --- per-interval counts ----------------------------------------------------
def N_at(t):
    """N(t) = number of zeros with 0 < Im < t (zeros list is sorted)."""
    return int(np.searchsorted(zeros, t, side="right"))

counts = []
for n in range(NGAP):
    lo, hi = grams[n], grams[n + 1]
    c = N_at(hi) - N_at(lo)
    counts.append(c)
counts = np.array(counts)

diff = []
for n in range(NGAP + 1):
    diff.append(N_at(grams[n]) - (n + 1))
diff = np.array(diff)

# --- slip events: consecutive runs of diff != 0 -----------------------------
events = []          # each: (start_gap_idx, end_gap_idx) of a diff!=0 run
in_run = False
for n in range(NGAP + 1):
    if diff[n] != 0 and not in_run:
        start = n
        in_run = True
    elif diff[n] == 0 and in_run:
        events.append((start, n - 1))
        in_run = False
if in_run:
    events.append((start, NGAP - 1))

# anomalous intervals (c != 1) count
n_anom = int((counts != 1).sum())
n_vac = int((counts == 0).sum())
n_dbl = int((counts == 2).sum())

# --- near-misses: nearest zero to each Gram point, in fractions of a gap ----
near = []
for n in range(NGAP):
    t = grams[n]
    # local gap spacing, symmetric
    lo_gap = grams[n + 1] - grams[n]
    hi_gap = grams[n] - grams[n - 1] if n > 0 else lo_gap
    gap = (lo_gap + hi_gap) / 2.0
    # nearest zero to t: index of the first zero >= t, and its predecessor
    i = int(np.searchsorted(zeros, t))
    cands = []
    if i < len(zeros):
        cands.append(zeros[i])
    if i > 0:
        cands.append(zeros[i - 1])
    zc = min(cands, key=lambda z: abs(z - t))
    near.append([float(t), float(zc), float(abs(zc - t) / gap)])

# records: near-misses that lower the running minimum
records = []         # (gram_index, miss_fraction) for each record-setting event
best = 1e9
for n, (_, _, f) in enumerate(near):
    if f < best:
        best = f
        records.append([n, float(f)])

out = {
    "grams": grams,
    "zeros": zeros.tolist(),
    "counts": counts.tolist(),
    "diff": diff.tolist(),
    "near": near,
    "records": records,
    "events": events,
    "meta": {
        "ngap": NGAP,
        "n_anom": n_anom,
        "n_vac": n_vac,
        "n_dbl": n_dbl,
        "n_events": len(events),
        "gmax": gmax,
        "first_event": events[0] if events else None,
    },
}
json.dump(out, open("/tmp/zero-data-800.json", "w"))
print("meta:", json.dumps(out["meta"], indent=1))
print(f"records ({len(records)}): first 8 = {records[:8]}")
print("wrote /tmp/zero-data-800.json")
