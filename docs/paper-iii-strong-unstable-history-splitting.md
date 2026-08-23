# Paper III: a delay-length-uniform relative strong-unstable history graph

Status: **the direct forward Lyapunov--Perron graph theorem below is
proved. It constructs a codimension-one invariant graph of complete initial
histories and a scalar defining covector, with constants independent of the
history length. It does not infer a phase-space exponential dichotomy or
invariant projectors from current-state admissibility. For the physical
two-module RFDE, the model-fitting implication remains conditional on the
strengthened outer-tracker jet contract U-OUT\({}^+\) defined in Section 5.
No uniform stable spectral gap, stable foliation, physical outer tracker,
fold-event map, or pulse/quiet capture theorem is asserted.**

The former Gate U-TR asked for more than the geometric reset argument uses.
A codimension-one separator needs the graph of histories whose forward
growth excludes one strong unstable current direction. It does not need a
uniformly stable complement, and it does not need a full
\(E^u\oplus E^c\oplus E^s\) trichotomy. The latter stable-gap statement is
false in the present long-delay scaling.

The scalar bounds are executable in
[strong_unstable_history.py](../src/canard_control/strong_unstable_history.py),
with regressions in
[test_strong_unstable_history.py](../tests/test_strong_unstable_history.py).
They audit hypotheses and constants; the proof is the forward fixed-point
argument given here.

## 1. Abstract graph theorem

Let

\[
 X_\tau=C([ -\tau,0],\mathbb R^m),
 \qquad
 \|\phi\|_\tau=\sup_{-\tau\leq\vartheta\leq0}|\phi(\vartheta)|,
\tag{1.1}
\]

where \(\tau\) may be arbitrarily large. Parameters \(p\) range in a fixed
compact set. The delay atoms are fixed while \(p\) varies. In the physical
application, \(p\) may contain \(\nu,\eta\), and gain or coefficient controls
that do not move the atoms, but it does not contain \(\delta\), \(\tau\), or
moving atom locations. No derivative with respect to \(\tau\) or \(\delta\)
is used.

Consider the nonautonomous ODE

\[
 \dot x=A_0(t,p)x
\tag{1.2}
\]

with evolution \(\Phi_0(t,s;p)\). Assume that it has continuous invariant
current-state projectors

\[
 \pi^u(t,p)+\pi^{cs}(t,p)=I,
 \qquad \operatorname{rank}\pi^u=1,
\tag{1.3}
\]

and constants \(M_0\geq1\), \(0\leq\alpha_0<\beta_0\), such that

\[
 \begin{aligned}
 \|\Phi_0(t,s)\pi^{cs}(s)\|
   &\leq M_0e^{\alpha_0(t-s)}, &&t\geq s,\\
 \|\Phi_0(s,t)\pi^u(t)\|
   &\leq M_0e^{-\beta_0(t-s)}, &&t\geq s.
 \end{aligned}
\tag{1.4}
\]

The second line uses the inverse only on the one-dimensional unstable
range. Assume the coefficients, projectors, normalized unstable frame, and
restricted evolutions are jointly \(C^1\) in \(p\), with uniform
differentiated bounds.

Perturb (1.2) by

\[
 \dot x(t)=A_0(t,p)x(t)+\mathcal B_{\delta,p}(t)x_t
              +\mathcal N_{\delta,p}(t,x_t),
 \qquad x_t(\vartheta)=x(t+\vartheta),
\tag{1.5}
\]

where

\[
 \sup_{t,p}\|\mathcal B_{\delta,p}(t)\|_{X_\tau\to\mathbb R^m}
 \leq b_\delta,
 \qquad b_\delta\longrightarrow0.
\tag{1.6}
\]

The maps \(\mathcal B\) and \(\mathcal N\) are jointly \(C^1\) in \(p\),
including the mixed history--parameter derivatives used below, and
\(\mathcal N(t,0)=D_\phi\mathcal N(t,0)=0\). After a fixed cutoff, assume a
common \(C^2_\phi C^1_p\) bound. This smooth globally Lipschitz
modification is a hypothesis in the abstract theorem; it is not obtained
from a radial bump on an arbitrary \(C\)-history space. In the physical
finite-evaluation polynomial model, it is constructed by cutting off the
finitely many evaluation coordinates. Put

\[
 \kappa_\sigma
 =M b_\delta\left\{
   \frac1{\sigma-\alpha_0}
   +\frac1{\beta_0-\sigma}
 \right\},
 \qquad \alpha_0<\sigma<\beta_0,
\tag{1.7}
\]

where \(M\) depends only on the current evolution, the current projectors,
and the normalized unstable history introduced below.

Choose a normalized unstable current vector \(e^u(t)\) and covector
\(\ell^u(t)\), so that

\[
 \pi^u(t)=e^u(t)\ell^u(t),
 \qquad \ell^u(t)e^u(t)=1.
\tag{1.8}
\]

Its complete backward history is

\[
 h_t^u(\vartheta)=\Phi_0(t+\vartheta,t)e^u(t),
 \qquad -\tau\leq\vartheta\leq0.
\tag{1.9}
\]

Define

\[
 \Lambda_{0,t}\phi=\ell^u(t)\phi(0),
 \qquad K_t=\ker\Lambda_{0,t}.
\tag{1.10}
\]

Every \(\phi\in X_\tau\) has the unique base decomposition
\(\phi=\psi+a h_t^u\), with \(\psi\in K_t\).

> **Theorem 1.1 (delay-length-uniform relative strong-unstable
> graph).** Suppose \(\kappa_\sigma<1\). There is a radius \(r>0\), chosen so
> that the cutoff nonlinear Lipschitz contribution preserves this strict
> inequality, and maps
>
> \[
>  g_{\delta,p,t}:K_t\cap B_r\longrightarrow\mathbb R
> \tag{1.11}
> \]
>
> such that
>
> \[
>  W^{<\sigma}_{\delta,p}(t)
>  =\{\psi+g_{\delta,p,t}(\psi)h_t^u:
>       \psi\in K_t\cap B_r\}
> \tag{1.12}
> \]
>
> is exactly the local set of initial histories whose cutoff forward
> solution satisfies
>
> \[
>  \sup_{s\geq t}e^{-\sigma(s-t)}\|x_s\|_\tau<\infty.
> \tag{1.13}
> \]
>
> The graph is forward invariant while the orbit remains in the uncut
> neighborhood. It is \(C^1\) in history and \(C^1\) in \(p\), in local
> bundle charts for the varying spaces \(K_t(p)\). Its scalar defining
> function
>
> \[
>  G_{\delta,p,t}(\psi+a h_t^u)
>  =a-g_{\delta,p,t}(\psi)
> \tag{1.14}
> \]
>
> satisfies \(D_\phi G_{\delta,p,t}(0)h_t^u=1\). At the reference
> history,
>
> \[
>  \|D_\phi G_{\delta,p,t}(0)-\Lambda_{0,t}\|
>  \leq \frac{C_{\rm LP}b_\delta}{1-\kappa_\sigma},
> \tag{1.15}
> \]
>
> where \(C_{\rm LP}\) is independent of \(\tau\). More precisely, on the
> complete coordinate cylinder
>
> \[
>  \mathcal C_{r,r_a}(t)
>  =\{\psi+a h_t^u:\ \psi\in K_t,\ \|\psi\|_\tau\le r,
>                       \ |a|\le r_a\},
> \tag{1.16}
> \]
>
> formula (1.14) defines the same scalar off the graph and
>
> \[
>  D_\phi G_{\delta,p,t}(\psi+a h_t^u)
>  =\Lambda_{0,t}-Dg_{\delta,p,t}(\psi)\Pi^K_{0,t},
>  \qquad
>  \|D_\phi G_{\delta,p,t}-\Lambda_{0,t}\|
>  \le C(b_\delta+r).
> \tag{1.17}
> \]
>
> The estimate is independent of \(a\); it follows from the differentiated
> graph contraction and the common \(C^2_\phi\) bound. If the
> differentiated perturbation is also \(O(b_\delta)\), the declared
> parameter derivatives of (1.15) obey the same order. The theorem does
> not assert a complementary invariant projector or a full phase-space
> exponential dichotomy.

## 2. Uniform base-history coordinates

Treat (1.2) as an RFDE with no delayed term. Its phase evolution is explicit:
for \(-\tau\leq\vartheta\leq0\),

\[
 [\mathcal T_{0,\tau}(t,s)\phi](\vartheta)
 =\begin{cases}
   \phi(t+\vartheta-s),&t+\vartheta\leq s,\\
   \Phi_0(t+\vartheta,s)\phi(0),&t+\vartheta>s.
  \end{cases}
\tag{2.1}
\]

Old history is translated with norm one. The backward estimate in (1.4)
gives

\[
 C_h:=\sup_t\|h_t^u\|_\tau\leq C_0
\tag{2.2}
\]

with no \(\tau\)-factor. The base coefficient and complementary history
maps

\[
 \Lambda_{0,t}\phi=\ell^u(t)\phi(0),
 \qquad
 \Pi^K_{0,t}\phi=\phi-h_t^u\Lambda_{0,t}\phi
\tag{2.3}
\]

are therefore bounded independently of \(\tau\). This is a Banach-space
coordinate decomposition, not a claimed perturbed invariant splitting.
Differentiating (1.9) with respect to \(p\) introduces integrals bounded by
\(\sup_{q\geq0}q e^{-\beta_0q}\), independently of \(\tau\). Thus
\(h_t^u,\Lambda_{0,t}\), and \(\Pi^K_{0,t}\) have uniform \(C^1_p\) bounds.

## 3. Direct forward Lyapunov--Perron proof

Fix a base time \(t_0\), \(\psi\in K_{t_0}\), and
\(\alpha_0<\sigma<\beta_0\). A candidate history and future current path are
encoded by a pair \((a,y)\):

\[
 x_{t_0}=\psi+a h_{t_0}^u,
 \qquad x(r)=y(r),\quad r\geq t_0.
\tag{3.1}
\]

The fixed-point space is the closed affine subspace on which
\(y(t_0)=\psi(0)+a e^u(t_0)\), so the two pieces agree at the common
endpoint.

Let \(\mathscr H_{t_0}(\psi,a,y)_s\in X_\tau\) denote the assembled
history at \(s\geq t_0\): before \(t_0\) it uses the first expression in
(3.1), and afterwards it uses \(y\). On pairs use

\[
 \|(a,y)\|_{\sigma,t_0}
 =\max\left\{C_h|a|,
   \sup_{r\geq t_0}e^{-\sigma(r-t_0)}|y(r)|\right\}.
\tag{3.2}
\]

Translation of the prescribed old history gives

\[
 \sup_{s\geq t_0}e^{-\sigma(s-t_0)}
 \|\mathscr H_{t_0}(0,a_1-a_2,y_1-y_2)_s\|_\tau
 \leq \|(a_1-a_2,y_1-y_2)\|_{\sigma,t_0}.
\tag{3.3}
\]

Indeed, if \(s+\vartheta<t_0\), the difference is
\((a_1-a_2)h^u_{t_0}(s+\vartheta-t_0)\); if
\(s+\vartheta\geq t_0\), then
\(e^{-\sigma(s-t_0)}e^{\sigma(s+\vartheta-t_0)}\leq1\). There is no
\(e^{\sigma\tau}\) loss.

Put

\[
 F(s,\phi)=\mathcal B_{\delta,p}(s)\phi
             +\mathcal N_{\delta,p}(s,\phi).
\tag{3.4}
\]

The Lyapunov--Perron map sends \((a,y)\) to
\((\widetilde a,\widetilde y)\), where

\[
 \begin{aligned}
 \widetilde a\,e^u(t_0)
  ={}&-\int_{t_0}^{\infty}
     \Phi_0(t_0,s)\pi^u(s)
     F\bigl(s,\mathscr H_{t_0}(\psi,a,y)_s\bigr)\,ds,\\
 \widetilde y(r)
  ={}&\Phi_0(r,t_0)\pi^{cs}(t_0)\psi(0)\\
  &+\int_{t_0}^{r}\Phi_0(r,s)\pi^{cs}(s)
     F\bigl(s,\mathscr H_{t_0}(\psi,a,y)_s\bigr)\,ds\\
  &-\int_r^{\infty}\Phi_0(r,s)\pi^u(s)
     F\bigl(s,\mathscr H_{t_0}(\psi,a,y)_s\bigr)\,ds.
 \end{aligned}
\tag{3.5}
\]

At \(r=t_0\), the two equations in (3.5) give
\(\widetilde y(t_0)=\psi(0)+\widetilde a e^u(t_0)\), so the history and
future pieces match. Equations (1.4), (3.3), and (3.5) imply

\[
 \|\mathscr T_\psi(a_1,y_1)-\mathscr T_\psi(a_2,y_2)\|_{\sigma,t_0}
 \leq M L_F
 \left\{\frac1{\sigma-\alpha_0}
          +\frac1{\beta_0-\sigma}\right\}
 \|(a_1-a_2,y_1-y_2)\|_{\sigma,t_0},
\tag{3.6}
\]

where \(L_F\leq b_\delta+L_{\mathcal N}(r)\) and
\(L_{\mathcal N}(r)\to0\) as \(r\to0\). Thus (1.7) and a smaller cutoff
radius make (3.5) a contraction on a ball with radius proportional to
\(\|\psi\|_\tau\). This proves existence and uniqueness of
\((a(\psi),y(\psi))\), and defines \(g_{\delta,p,t_0}(\psi)=a(\psi)\).

Conversely, variation of constants for a forward solution satisfying
(1.13), followed by projection onto \(\pi^u\) and passage of the terminal
time to infinity, gives the first equation in (3.5); the
\(\pi^{cs}\) projection gives the second. Hence the graph characterizes
exactly the stated growth class. Repeating this characterization at a later
base time and using fixed-point uniqueness proves forward invariance. The
argument uses the RFDE only through its current-state
variation-of-constants formula and the explicit history assembly
\(\mathscr H\); it does not introduce an unbounded boundary insertion on
\(X_\tau\).

Uniform contraction with jointly \(C^2_\phi C^1_p\) data gives
\(C^1_{\psi,p}\) dependence by differentiating the fixed-point equation.
At \(\psi=0\), \(D_\phi\mathcal N=0\), so the unstable integral and the
resolvent bound give

\[
 \|D_\psi g_{\delta,p,t_0}(0)\|
 \leq \frac{C_{\rm LP}b_\delta}{1-\kappa_\sigma}.
\tag{3.7}
\]

Formula (1.14) and the decomposition (2.3) then prove (1.15). This
completes the proof of Theorem 1.1. Fixed delay atoms are essential for the
stated \(C^1_p\) conclusion: moving atoms are not \(C^1\) in the ordinary
sup-history operator norm.

## 4. Scope of the graph

Let the exact reference history curve be defined on a slightly extended
outer interval, with its whole-line cutoff or terminal normalization fixed
as part of the selected data. Theorem 1.1 gives a local codimension-one
history graph along that extended curve. On the retained uncut interval,
its histories and forward orbits solve the physical RFDE exactly.

The graph may contain weak pseudo-continuous modes whose forward growth is
below \(\sigma\). It is therefore a **relative strong-unstable history
graph**, not a stable foliation or a basin boundary. It nevertheless has
the only structure used by the geometric reset argument: a codimension-one
scalar equation, a nonzero normal derivative, and the covector convergence
estimate (1.15). Any claim about stable fibers, pulse/quiet outcomes, or no
return requires a separate theorem.

The future integral in (3.5) requires coefficients beyond the retained
physical tracker. The following selected extension keeps that auxiliary
choice separate from the physical outer-matching problem.

> **Lemma 4.1 (selected future extension).** Suppose a finite physical
> tracker segment, written in a smooth current Riesz frame, satisfies the
> finite-segment versions of (1.3)--(1.6) and the \(C^1_p\) bounds in
> (5.1). Suppose also that the terminal current splitting remains in a
> compact one-strong-unstable gap and that its time derivative is
> \(O_{C^1_p}(\delta^2)\). Fix a smooth longitudinal extension profile and
> finite-evaluation cutoff profiles. Assume on the common finite coordinate
> neighborhood a uniform \(C^2_\phi C^1_p\) bound for every current and
> delayed-evaluation remainder to which those profiles are applied. Then the
> moving-coordinate equation
> has a \(C^2_\phi C^1_p\) extension to the future half-line which:
>
> 1. agrees exactly with the physical equation on the retained segment;
> 2. freezes the slow base and current block after one fixed collar;
> 3. preserves the rates in (1.4), after an arbitrarily small fixed inward
>    change of \(\alpha_0,\beta_0\); and
> 4. preserves the \(O_{C^1_p}(\delta)\) perturbation bound and fixed-atom
>    property.
>
> The exact graph depends on this declared extension profile.

**Proof.** Fix once and for all a bounded linear Hermite extension operator
\(\mathcal E\) acting on the joint coefficient maps \(c(t,p)\), with kernels
and longitudinal profiles independent of \(p\). Extend the scalar slow base
through the collar using its terminal value and derivative and then freeze
it. Because the same operator acts on the joint map, rather than separately
on a coefficient and on a declared jet,
\(D_p(\mathcal Ec)=\mathcal E(D_pc)\). Thus the extension is genuinely
\(C^1_p\) and retains the stated differentiated bounds.

In the moving Riesz coordinates the extended base block is the direct sum
of the scalar unstable equation and the tangent--stable block. The unstable
restricted evolution is bounded by direct integration of its scalar
coefficient. On the tangent--stable block use the uniformly equivalent
Lyapunov norms of the compact frozen family; the frame derivative and collar
coupling are \(O_{C^1_p}(\delta^2)\), so the corresponding energy inequality
changes the exponent by \(O(\delta^2)\). Composition across the fixed collar
changes only the common prefactor. After the collar the blocks are frozen.
Consequently the two estimates in (1.4) hold with uniform \(M_0\) after the
declared fixed inward change of \(\alpha_0,\beta_0\); this is an evolution
estimate, not an inference from pointwise eigenvalues.

Multiply the delayed layer coefficient maps by the same parameter-independent
longitudinal profile without moving their atoms. Apply finite-coordinate
cutoffs to the jointly extended polynomial remainders, with profiles equal
to one on the retained segment and chosen so that
\(\mathcal N(t,0)=D_\phi\mathcal N(t,0)=0\) remains exact. Boundedness of
\(\mathcal E\), the common finite-evaluation bounds, and the fixed profiles
preserve the \(O_{C^1_p}(\delta)\) estimates. The extension is identical to
the physical equation before the collar, while after the collar all
coefficients are frozen or cut off. \(\square\)

This lemma is an auxiliary selection device, not a physical continuation
theorem. It removes the whole-half-line interface once the finite tracker
jets have been established, but it does not prove those jets or the
action-supercritical U-OUT matching.

## 5. Model fit for the physical two-module RFDE

Fix a compact middle-branch recovery interval
\(J_R\Subset(\rho_-,0)\), separated from both folds and containing
\(\rho_R=-1/2\). Define **Gate U-OUT\({}^+\)** to be the existing terminal-
matching Gate U-OUT together with an exact selected finite tracker on a
slightly larger interval and the uniform jet bounds, for
\(p=(\nu,\eta,\ldots)\),

\[
 \|z^m_{\delta,p}-z^m_{0,p}\|_{C^1_pC^0_t}
 \leq C_{\rm tr}\delta,
 \qquad
 \|\dot\rho\|_{C^1_pC^0_t}\leq C_\rho\delta^2.
\tag{5.1}
\]

on that finite segment. The current U-OUT terminal-matching contract does
not yet prove (5.1), so U-OUT\({}^+\) remains open. Lemma 4.1 turns these
finite bounds into the selected whole-future extension used in (3.5).
Equation (5.1), rather than backward completeness alone, is the model
input.

At \(\delta=0\), the current-state Jacobian along the singular middle branch
is block triangular. Its spectrum consists of one simple positive fast
eigenvalue, one simple zero tangent eigenvalue, one negative fast
eigenvalue, and the transverse recovery eigenvalue \(-D_w\). Compactness of
\(J_R\) gives a positive unstable floor \(\lambda_*\), stable Riesz frames,
and uniformly conditioned current coordinates.

In those smooth Riesz coordinates, define \(A_0\) to be the frozen block-
diagonal unstable--tangent--stable generator. The frame derivative, every
off-diagonal term created by the actual tracker, and the difference between
the physical current Jacobian and this frozen generator are placed in
\(\mathcal B_{\delta,p}\); their combined contribution is included in
\(C_{\rm tr}\delta+C_{\rm mv}\delta^2\) below.

The stable-block estimate is not inferred from pointwise Hurwitz matrices.
On the compact frozen stable bundle, solve

\[
 A_s(\rho)^TH(\rho)+H(\rho)A_s(\rho)=-I.
\tag{5.2}
\]

The positive matrices \(H,H^{-1},H'\) are uniformly bounded. Since
\(\dot\rho=O(\delta^2)\), the additional energy term
\(\dot\rho H'(\rho)\) is small. Thus the current base has
\(\alpha_0=0\) and \(\beta_0\geq\lambda_*>0\) after reducing \(\delta_0\).

The exact delayed voltage functional is

\[
 \delta^2K\{B\phi(0)-C_0^\eta\phi(-\theta_0/\delta)
                      -C_1^\eta\phi(-\theta_1/\delta)\}.
\tag{5.3}
\]

On \(|\eta|\leq1/20\), its exact vector-maximum operator norm before the
factor \(\delta^2|K|\) is

\[
 \|[B,-C_0^\eta,-C_1^\eta]\|_\infty
 =\frac83.
\tag{5.4}
\]

The second output row realizes the maximum. The \(\eta\)-dependence in the
two delayed row sums cancels; maximizing the two layer norms at different
values of \(\eta\) would give the valid but non-sharp bound \(43/15\).

The tracker/current-Jacobian error in (5.1) is \(O(\delta)\). After the
fixed current coordinate change, all perturbations satisfy

\[
 b_\delta
 \leq C_*\left\{
 C_{\rm tr}\delta+\frac83|K|\delta^2+C_{\rm mv}\delta^2
 \right\}\longrightarrow0,
\tag{5.5}
\]

with the same order for the declared \(p\)-derivatives. The history
constant in Sections 2--3 is independent of
\(\tau_* =\theta_*/\delta\). The rescaling

\[
 C([ -\tau_*,0],\mathbb R^4)\longrightarrow
 C([ -\theta_*,0],\mathbb R^4),
 \qquad
 \phi\longmapsto[\vartheta\mapsto\phi(\vartheta/\delta)]
\tag{5.6}
\]

is an isometry in the sup norm. Fixed atoms give the required \(C^1_p\)
operator bounds on the scaled-history space.

> **Theorem 5.1 (selected relative-history-graph implication in the physical
> history space).** If Gate
> U-OUT\({}^+\) supplies the exact finite tracker and bounds (5.1), and the
> selected future extension is fixed by Lemma 4.1, then for all sufficiently
> small \(\delta>0\) the declared selected extension has the
> parameter-\(C^1\) codimension-one history graph (1.12) in the physical
> history space, with constants independent of the physical delay length.
> It is an exact graph for the physical RFDE only while the extension agrees
> with that RFDE on the retained interval. At the tracker,
>
> \[
>  D_\phi G_{\delta,p,t}(0)
>  =\Lambda_{0,t}+O_{C^1_p}(\delta).
> \tag{5.7}
> \]
>
> In particular, at \(\rho_R\) its action on a constant voltage-reset
> tangent converges to the corresponding singular left unstable covector.

The last assertion follows from (1.15), (5.5), and smooth convergence of
the current Riesz frame. It supplies the covector estimate used in the
reset implicit-function theorem. It does not supply stable fibers inside
the graph.

## 6. Exact, conditional, and open statements

| Statement | Status |
|---|---|
| Base history decomposition and constants independent of \(\tau\) | Proved, Section 2 |
| Forward relative-growth history graph | Proved under (1.3)--(1.7), Theorem 1.1 |
| Parameter-\(C^1\) graph for fixed atoms | Proved under the displayed mixed derivative bounds |
| Defining covector and \(O(b_\delta)\) base-point closeness | Proved, (1.14)--(1.15) |
| Exact layer norm \(8/3\) | Proved algebraically and tested |
| Singular middle current index: one unstable, one center, two stable | Proved by exact block structure; numerically audited at \(\rho=-1/2\) |
| Selected future extension from finite tracker jets | Proved construction, Lemma 4.1 |
| Physical graph and reset covector from U-OUT\({}^+\) | Proved implication, Theorem 5.1 |
| U-OUT terminal BVP, exact common leaf, and action-supercritical residual | Open |
| U-OUT\({}^+\) finite-segment uniform \(C^1_p\) jets | Open |
| Full perturbed phase-space dichotomy/projectors | Not asserted |
| Uniform stable spectral gap as \(\delta\to0\) | False in general and not needed |
| Stable foliation or basin separation inside the graph | Not asserted |
| Lower-fold event and biological pulse/quiet capture | Open repaired U-EX/U-CAP gates |

The proof boundary is now precise. The long delay does not obstruct the
direct codimension-one relative-growth graph because old history is carried
once, isometrically, in (3.3). The remaining physical obstruction is
selecting and tracking the correct repelling outer history with
exponentially sufficient accuracy. A full RFDE dichotomy may still be of
independent interest, but it is not used to define the geometric reset
root.
