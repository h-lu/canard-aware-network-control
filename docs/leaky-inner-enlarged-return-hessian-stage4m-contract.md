# Stage 4M: enlarged-ball projected return-Hessian contract

Status: **NONCLOSING CONTRACT — exact cap feasibility is proved; no RFDE
Hessian block is certified.**

Stage 4M fixes the theorem interface for all six projected Hessian blocks of
the selected near-period return on the Stage-4K preferred-B box.  It also
freezes the first missing parent.  At present there is no source-bound
nonlinear selected-return tube/event graph on the full anisotropic
complete-history ball.  Consequently (D^2P(x)) has no validated common
domain on which a uniform operator supremum can be taken.

The executable source is
[leaky_inner_enlarged_return_hessian_stage4m_contract.py](../src/canard_control/leaky_inner_enlarged_return_hessian_stage4m_contract.py),
the atomic generator is
[leaky_inner_enlarged_return_hessian_stage4m_contract.py](../experiments/leaky_inner_enlarged_return_hessian_stage4m_contract.py),
and the source-bound result is
[leaky_inner_enlarged_return_hessian_stage4m_contract.json](../experiments/results/leaky_inner_enlarged_return_hessian_stage4m_contract.json).

Stage 4M binds and normally validates Stage 4K.  It does not bind an
unpublished Stage-4L result.  A terminal linear stable-row estimate cannot
replace the nonlinear flow/event family required to define the Hessian
suprema below.

## 1. Fixed coordinates and enlarged box

Let

\[
 Y=C([-\tau_{\max},0],\mathbb R)_v\times\mathbb R_w,
 \qquad \Sigma_0=\{h\in Y:h_v(0)=0\},
\]

with the inherited max norm.  Starting from the fixed physical pair
(f(q)=1), Stage 4M registers the unit-(Y) splitting

\[
 \widehat q=\frac{q}{\|q\|_Y},\qquad
 \widehat f=\|q\|_Y f,qquad
 P_s=I-widehat q\widehat f=I-qf,qquad
 E_s=\ker\widehat f.
\]

This pair is fixed while the base point varies.  A moving eigensplitting is
not admissible.  The proposed return domain is

\[
 \mathcal B=
 \left\{X_*+x_s+widehat q x_u:
   x_s\in E_s, \|x_s\|_Y\le0.0097, |x_u|\le0.00025\right\}.
\]

Thus the split-radius sum is exactly (0.00995).  This is a design domain,
not a validated return ball.

## 2. One common six-cap row

Stage 4K source-binds the Stage-4A refinement envelope but correctly labels
it a finite-section heuristic.  Stage 4M uses those six decimal values only
to define proof-design caps.  Exact rational multiplication by the lower
closing probe (13.2353) gives

| block | strict Stage-4M cap |
|---|---:|
| (C_s^{ss}) | (0.29737958147168548073886622) |
| (C_s^{su}) | (1.17481996400215002469463264) |
| (C_s^{uu}) | (105.178488996792070958566234) |
| (C_u^{ss}) | (3.9299772663315943951298061) |
| (C_u^{su}) | (3.7468621607891535185969481) |
| (C_u^{uu}) | (346.72372256934974231438886) |

A future Stage-4M theorem certificate must obtain all six bounds from one
nonlinear return tube and prove each inequality strictly.  It may not choose
individually favorable caps from different majorant rows.

Inserting the entire cap vector simultaneously into the exact Stage-4
majorant, with the preferred-B *design hypotheses*

\[
 r=0.0094,quad R_s=0.0097,quad \widehat R_u=0.00025,quad
 \beta=0.9999,quad K_s=1,quad \rho_s=0.1,
\]

reproduces the Stage-4K lower probe.  The exact directed outputs include

\[
 \rho(M)<0.162716,qquad
 s_s>2.77635\times10^{-4},qquad
 s_u>1.70143\times10^{-9}.
\]

The (13.2354) probe fails the unstable self-map condition.  Hence 13.2353
is a useful common ceiling, not a reason to insist on a factor-two estimate.
This calculation proves only conditional design feasibility: the stable rate,
(K_s), return ball, and six RFDE block bounds are not supplied by Stage 4M.

## 3. The six operator bounds

For every (x\in\mathcal B), let (P(x)) denote the selected near-period
return, once that map has been constructed on a common event window.  The
required uniform bounds are

\[
\begin{array}{lll}
 C_s^{ss}\ge
 \displaystyle\sup_{x,h_s,k_s}
 \|P_sD^2P(x)[h_s,k_s]\|_Y,
&
 C_s^{su}\ge
 \displaystyle\sup_{x,h_s}
 \|P_sD^2P(x)[h_s,\widehat q]\|_Y,
&
 C_s^{uu}\ge
 \displaystyle\sup_x
 \|P_sD^2P(x)[\widehat q,\widehat q]\|_Y,\\[2mm]
 C_u^{ss}\ge
 \displaystyle\sup_{x,h_s,k_s}
 |\widehat f(D^2P(x)[h_s,k_s])|,
&
 C_u^{su}\ge
 \displaystyle\sup_{x,h_s}
 |\widehat f(D^2P(x)[h_s,\widehat q])|,
&
 C_u^{uu}\ge
 \displaystyle\sup_x
 |\widehat f(D^2P(x)[\widehat q,\widehat q])|,
\end{array}
\]

where (|h_s|_Y,|k_s|_Y\le1).  Symmetry identifies the two mixed input
orders but does not remove either output family.  A four-block shortcut is
therefore invalid.

## 4. Complete moving-event Hessian

For (x\in\mathcal B), the physical flow and its variations satisfy

\[
 \dot X=F(X_t),qquad
 \dot U_h=DF(X_t)U_{h,t},qquad
 \dot V_{hk}=DF(X_t)V_{hk,t}
      +D^2F(X_t)[U_{h,t},U_{k,t}].
\]

Let (T=T(x)) be the selected event time in a common near-period window,
(ell_0(y)=y_v(0)), and

\[
 a(x)=\ell_0(\dot X(T;x))>0,qquad
 T_h=-\frac{\ell_0(U_h(T;x))}{a(x)}.
\]

For every returned-history coordinate
(-\tau_{\max}\le\theta\le0), form

\[
\begin{aligned}
 W_{hk}(\theta)={}&V_{hk}(T+\theta)
  +\dot U_h(T+\theta)T_k
  +\dot U_k(T+\theta)T_h\\
 &+\ddot X(T+\theta)T_hT_k,\\
 T_{hk}={}&-\frac{\ell_0(W_{hk}(0))}{a(x)},\\
 D^2P(x)[h,k](\theta)={}&
 W_{hk}(\theta)+\dot X(T+\theta)T_{hk}.
\end{aligned}
\]

The recovery component is evaluated at the returned current time.  Every
translation term must be retained over the complete history; an endpoint-only
event correction is insufficient.

For the leaky two-delay field, the nonzero fast-row second derivatives are

\[
 -2v(t)-6\varepsilon\kappa_3(v(t)-1),qquad
 3\varepsilon\kappa_3(v(t-\tau_j)-1),\quad j=0,1,
\]

and the corresponding third derivatives are
(-2-6\varepsilon\kappa_3) and
(3\varepsilon\kappa_3).  These third derivatives are needed for uniformity
over (mathcal B), not merely for a base-orbit calculation.

## 5. Correlated output order

The stable and unstable outputs must be formed before norms:

\[
 G_s=D^2P-\widehat q\,\widehat f(D^2P),qquad
 G_u=\widehat f(D^2P).
\]

The event terms, current atom, continuous delayed-history density, Fourier
tail, physical column, and normalization uncertainty must first be combined
in these common rows.  Bounding the raw return, rank-one correction, and event
correction separately and then adding their norms destroys the cancellation
that the fixed splitting is intended to preserve.

## 6. First missing parent

The first missing theorem input is a source-bound nonlinear selected-return
tube on all of (mathcal B).  Its currently null fields are:

- a complete-history nonlinear flow-family remainder;
- one common selected-event window;
- a uniform positive event-speed lower bound;
- a returned-history tube through every (	heta\in[-\tau_{\max},0]);
- a positive separation from every earlier section hit.

Without this parent there is no validated base domain for (U,V,T_h,T_{hk})
and hence no legitimate uniform (D^2P(x)) supremum.  Stage 4M freezes these
fields as null rather than importing Stage-4A samples or prospective Stage-4L
numbers.

After that parent exists, a closing Hessian evaluator must additionally cover
arbitrary stable input histories, the unit unstable column, all three second-
variation sectors, delay-activation and cell seams, continuous output phase,
the fixed ((\widehat q,\widehat f)) normalization, and both correlated output
rows.  Only then may the six directed upper bounds be compared strictly with
the caps and inserted together into the majorant.

## 7. Claim boundary

Stage 4M proves the exact cap arithmetic and records the correct proof
interface.  It proves none of the following:

- a nonlinear selected or first return on the enlarged ball;
- any one of the six projected return-Hessian bounds;
- the preferred-B stable rate, (K_s=1), or return ball;
- a quantitative stable graph;
- a pulse/stable-sheet crossing, biological onset, routing, capture, or
  network safety statement.

The generator validates the parent and the complete claim ledger before an
fsynced atomic replacement.  Hostile tests reject filled Hessian fields,
Stage-4L substitution, omitted moving-event terms, separately normed
projection pieces, and every downstream theorem promotion.
