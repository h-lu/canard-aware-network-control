# A directed fourth-order parameter model for the physical pulse

Status: **proved fixed-time wide-parameter Taylor model through
\(24\sqrt5\); no Route-C event, stable-sheet, onset, or routing theorem.**

Let

\[
 J_0=\frac{2409}{8000},\qquad
 h=\frac{3}{40000},\qquad
 \xi=\frac{J-J_0}{h}\in[-1,1].
\]

For the exact quiet initial history, write

\[
 z(t,J_0+h\xi)=B(t,\xi)+R_5(t,\xi),
 \qquad
 B(t,\xi)=\sum_{k=0}^{4}b_k(t)\xi^k,
\]

where

\[
 b_k(t)=\frac{h^k}{k!}\partial_J^k z(t,J_0).
\]

The scaling is part of the proof, not a display convention.  It retains the
descending hierarchy observed in Stage 5A and prevents the raw fourth
derivative, of size about \(10^{10}\), from destroying the interval
calculation.

## The joint coefficient enclosure

The ten coefficient components are propagated together on the exact
two-origin grid

\[
 \{n\sqrt5/24\}\cup\{1+n\sqrt5/24\},
\]

through \(24\sqrt5\).  Hence the pulse release at one and both delay
translations remain exact cell boundaries.  Each of the 1152 cells carries
a degree-16 time-Taylor guide.  Bernstein ranges give continuous-time
coefficient boxes.

The error norm is

\[
 \max_{0\le k\le4}\|\delta b_k\|_P.
\]

The diagonal block uses the same \(P\)-logarithmic norm as the physical
two-dimensional state.  The lower-triangular Bell couplings are bounded as
off-diagonal block operators, with both delayed Toeplitz families treated
separately.  This is a joint correlated coefficient enclosure, not five
independent zero-centered variation majorants.

All 1152 coefficient cells close.  The maximum joint \(P\)-error radius is
less than

\[
 8.58\times10^{-19},
\]

the largest time-guide residual is less than \(2.39\times10^{-24}\), and
the minimum directed cell-closure gap is positive.  Dividing the scaled
coefficient errors by \(h^k\) and multiplying by \(k!\) yields continuous
directed envelopes for the actual derivatives
\(z_k=\partial_J^kz(t,J_0)\); these values are stored order by order in the
artifact.

## The degree-five remainder

Because the RFDE vector field is cubic in the current and delayed voltages,
substituting \(B(t,\xi)\) produces parameter degrees only up to twelve.  The
coefficient equations cancel degrees zero through four exactly.  The
remaining forcing is therefore the explicit directed sum of degrees
\(5,\ldots,12\) in

\[
 -\frac13V^3+arepsilon\kappa_3
 \left(\frac{(D_4-1)^3+(D_5-1)^3}{2}-(V-1)^3\right).
\]

The linear, recovery, and affine pulse terms have no parameter tail of
degree at least five.  Interval convolution of the validated coefficient
boxes gives a maximum tail forcing below

\[
 2.06\times10^{-9}
\]

in the \(P\)-norm.

For every \(\xi\in[-1,1]\), the remainder then satisfies a cellwise delayed
inequality of the form

\[
 D^+\|R_5\|_P
 \le \mu_P(T)\|R_5(t)\|_P
 +\beta_4(T)\|R_5(t-4\sqrt5)\|_P
 +\beta_5(T)\|R_5(t-5\sqrt5)\|_P+\rho_{\ge5}.
\]

Every one of the 1152 remainder cells closes.  Uniformly for the entire
wide pulse interval and all \(0\le t\le24\sqrt5\),

\[
 \|R_5(t,\xi)\|_P<1.73\times10^{-8}.
\]

Thus Stage 5B proves a genuine wide-parameter fourth-order flow model.  The
earlier 30,000-state-shard estimate is no longer the relevant route for this
fixed-time family.

## Exact scope

The theorem is at common physical times.  A Route-C section evaluates each
parameter at its own event time \(T(J)\).  The present result does not yet
prove that event exists uniquely, does not divide by an event-speed lower
bound, and does not pull the delayed history to the common event graph.
Accordingly the event bracket, speed, event-time jet, event-aligned complete
history, Riesz stable coordinate, endpoint stable signs, interval-Newton
root, onset threshold, and two-sided basin routing remain `null` or `false`.

Generate the artifact with

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
PYTHONPATH=.venv/lib/python3.14/site-packages:src /usr/bin/python3 \
  experiments/leaky_pulse_parameter_jet_directed_enclosure.py
```

`--check` audits the registered hashes and claim ledger without replay;
`--check --recompute` repeats the complete directed calculation.
