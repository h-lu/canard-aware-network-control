# Choosing the physical-pulse separator bracket

Status: **source-bound binary64 feasibility diagnostic plus a conditional
selection rule, not a separator theorem.**

The previously selected interval

\[
 [0.30113,0.30114]
\]

keeps the third-return histories within about \(1.05\times10^{-4}\) of the
finite-section reference, but its smaller endpoint coordinate is only about
\(6.50\times10^{-5}\).  It was chosen before a quantitative stable-graph
radius was available.  There is therefore no mathematical reason to make
this narrow interval part of the final theorem.

On the same 180-step finite section, the wider interval

\[
 [0.30105,0.30120]
\]

has the following binary64 endpoint data:

\[
\begin{array}{c|c|c|c}
J&\widehat g_3(J)&\widehat g_3'(J)&
 \|\widehat B_3(J)-\widehat\gamma_i\|_{\infty,\mathrm{mesh}}\\ \hline
0.30105& 1.1780217\times10^{-3}&-13.6698&1.6584050\times10^{-3}\\
0.30120&-9.0825944\times10^{-4}&-14.1526&1.2770923\times10^{-3}
\end{array}
\]

Thus the smaller observed endpoint margin is more than thirteen times the
narrow-bracket margin, while the larger endpoint mesh distance remains
below \(1.7\times10^{-3}\).  These values are not interval enclosures: the
finite left vector is not the RFDE Riesz covector, the mesh norm is not the
continuous history norm, and sampled derivatives do not prove monotonicity.

The rigorous selection rule is independent of this diagnostic.  A bracket
may be used only after directed estimates prove all three facts:

1. its entire return-history tube lies inside the validated stable-graph
   ball;
2. the exact stable-manifold gap has opposite strict signs at the two
   endpoints;
3. the exact gap derivative has one strict sign throughout the interval.

Consequently the quantitative stable-graph calculation should expose its
actual radius before the pulse bracket is frozen.  If that radius contains
the wider endpoint tubes, the proof can use an endpoint-error allowance on
the order of \(8\times10^{-4}\), instead of the earlier
\(3\times10^{-5}\) target.  If it does not, the narrow bracket remains
available.  Neither alternative is promoted by this diagnostic.

Reproduce with

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
PYTHONPATH=src:.venv/lib/python3.14/site-packages /usr/bin/python3 \
  experiments/leaky_pulse_separator_bracket_tradeoff.py
```

The continuous-history tube, directed endpoint signs, uniform derivative,
RFDE covector, stable graph, pulse separator, onset threshold, and two-sided
routing all remain open.
