# Stage 4S: exact Route-C event-speed radius adapter

## Result

This certificate removes the Route-C event-speed estimate as an independent
numerical unknown, but it does **not** promote the open Stage-4N return-tube
contract.

Stage 2 proves, in the complete-history norm

\[
 \|(\phi,w)\|_Y=\max\{\|\phi\|_\infty,|w|\},
\]

that the exact phase-zero voltage event row has physical speed at least

\[
 a_{\rm orb}^-=0.246926966042201268440571312807745\ldots
\]

at the orbit and that the RFDE vector field has Lipschitz upper bound

\[
 L_F^+=4.017305229418049955399147224363310\ldots
\]

on its directed radius-

\[
 R_0^-=0.0099999999999999999999999999999999999\ldots
\]

ball about the exact phase-zero Route-C history.

Stage 4N declares the preferred-B coordinates

\[
 x-X_*=x_s+\widehat q x_u,
 \qquad \|\widehat q\|_Y=1,
\]

with

\[
 \|x_s\|_Y\le0.0097,
 \qquad |x_u|\le0.00025.
\]

The exact triangle inequality therefore gives

\[
 \|x-X_*\|_Y\le0.0097+0.00025=0.00995<R_0^-.
\]

The directed inclusion slack is

\[
 R_0^- - 0.00995
 =0.00004999999999999999999999999999999999999999999998246666.
\]

Restricting the Stage-2 speed calculation to the smaller ball yields

\[
 \begin{aligned}
 a_* &\ge a_{\rm orb}^- - L_F^+(0.00995)\\
 &=0.2069547790094916713843497979253308516874029625928539498445\\
 &>0.
 \end{aligned}
\]

This is slightly sharper than the inherited radius-
\(R_0^-\) lower bound
\(0.206753913748020768886579840564112686\ldots\).

## Exact conditional theorem

Let \(\mathcal B\) be the full preferred-B anisotropic initial-history ball
declared by Stage 4N. Suppose a source-bound nonlinear flow enclosure proves

\[
 \|X_t(x)-X_*\|_Y\le0.00995
 \quad
 \text{for every }x\in\mathcal B,
 \quad t\in[T_-,T_+].
\]

Then, on that same common window,

\[
 \inf_{x\in\mathcal B,\ t\in[T_-,T_+]}
 Dg[F(X_t(x))]
 \ge0.2069547790094916713843497979253308516874029625928539498445>0.
\]

Thus the Stage-4N uniform-speed slot can be filled automatically once the
complete-history containment premise is proved. Likewise, if every returned
history satisfies \(\|R(x)-X_*\|_Y\le0.00995\), its endpoint event speed has
the same lower bound.

## Boundary of the result

The containment hypotheses above remain false in the claim ledger. In
particular, this certificate proves neither the existence of one common event
window nor that histories evolved from the initial ball stay near \(X_*\).
Initial-ball inclusion is not flow-tube invariance.

It also does not establish endpoint signs, a selected or first return, a
\(C^2\) return map, six continuous-history Hessian blocks, a stable graph, a
pulse crossing, physical onset, two-sided routing, outer/quiet capture, or a
frequency--amplitude safety radius. Finite samples or finitely many history
nodes cannot replace the quantified complete-history containment premise.

The mathematical gain is a strict dependency reduction: the next shared
object is one nonlinear complete-history tube. A separate event-speed
computation is no longer needed if that tube enters the certified ball.

## Reproduction

```bash
PYTHONPATH=src /usr/bin/python3 \
  experiments/leaky_inner_event_speed_adapter_stage4s.py
```

The generator validates both parent artifacts, performs directed decimal
arithmetic, binds all sources and parents by SHA-256, and installs the result
atomically.
