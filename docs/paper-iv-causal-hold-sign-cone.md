# A causal hold protocol and complete-history sign cones for the clamped FHN decision

Status: **proved for an ideal finite-time state-overwrite protocol on the
fixed rank-one two-module \(D=3,E=2\) network.** Holding every voltage and
recovery state at \((r,0)\) for one maximum-delay window produces the constant
complete history \(\Phi_r\) exactly, after which the voltage is released while
the collective recovery clamp remains active. The protocol is causal and
finite in time, but its hold is an ideal state constraint. It is not a
bounded additive actuator or a hardware realization.

The main dynamical conclusion is stronger than the constant-reset result in
[the clamped-separator theorem](paper-iv-same-model-clamped-separator.md).
Every synchronous complete history of one voltage sign, with nonzero current
value and zero recovery history, reaches the corresponding voltage face in
finite time. The proof uses the global strict monotonicity of the delayed
actuator field and does not require the delayed values to be ordered relative
to the current value.

The directed constants used below come from
[fhn_same_model_separator.json](../experiments/results/fhn_same_model_separator.json),
whose SHA-256 digest is

~~~text
9e859f31c177638a70b3ca451fe743227308343792d77eeca286fca26afc8a86
~~~

The causal hold and sign-cone extension are analytic consequences of the
declared hybrid protocol and the same certified gain box; they are not
silently attributed to a new flag in that artifact.

## 1. The fixed controlled network

Let \(C_1,C_2\) be nonempty modules of arbitrary finite sizes \(n_1,n_2\).
Write

\[
 \pi_i=\frac{1}{2n_a}\quad (i\in C_a),
 \qquad P=\mathbf 1\pi^T,
 \qquad \pi^T\mathbf 1=1.
\tag{1.1}
\]

The two delay layers \(B_0,B_1\) assign mass \(1/2\), respectively, to the
same source module and the other source module. Thus

\[
 B_0+B_1=P,
 \qquad B_0\mathbf 1=B_1\mathbf 1=\frac12\mathbf 1.
\tag{1.2}
\]

We retain the dual-scaffold FHN voltage equation

\[
\begin{aligned}
 \dot v={}&v-\frac{v^{\circ3}}3-w+D(P-I)v\\
 &+\varepsilon\kappa _1
   \{B_0v(t-\tau _0)+B_1v(t-\tau _1)-v\}\\
 &+\varepsilon\kappa _3
   \{B_0h(v(t-\tau _0))+B_1h(v(t-\tau _1))-h(v)\},
\end{aligned}
\tag{1.3}
\]

where powers are componentwise and \(h(s)=(s-1)^3\). During the released
decision stage the recovery equation is

\[
 \dot w=\varepsilon(v-a\mathbf 1)+E(P-I)w+u^w,
 \qquad
 u^w=-\varepsilon(\pi^Tv-a)\mathbf 1.
\tag{1.4}
\]

The fixed parameters and physical delays are

\[
 \varepsilon=\frac15,
 \quad a=\frac35,
 \quad D=3,
 \quad E=2,
 \quad \tau_0=4\sqrt5,
 \quad \tau_1=5\sqrt5,
 \quad \tau_*=5\sqrt5.
\tag{1.5}
\]

The gains range over the certified box

\[
 U=\left\{(\kappa _1,\kappa _3):
 \left|\kappa _1-\frac15\right|\le10^{-12},
 \quad
 \left|\kappa _3-\frac14\right|\le10^{-12}
 \right\}.
\tag{1.6}
\]

Multiplying (1.4) by \(\pi^T\) gives

\[
 \frac{d}{dt}\pi^Tw=0.
\tag{1.7}
\]

Moreover, the completely synchronous leaf is invariant. If its recovery
history is zero, then \(w(t)=0\) throughout the released decision stage.
Writing \(v=x\mathbf1\), equation (1.3) reduces exactly to

\[
 \dot x(t)=x(t)-\frac{x(t)^3}{3}
 +\varepsilon\left[
 \frac{g_b(x(t-\tau_0))+g_b(x(t-\tau_1))}{2}-g_b(x(t))
 \right],
\tag{1.8}
\]

where \(b=(\kappa_1,\kappa_3)\) and

\[
 g_b(s)=\kappa_1s+\kappa_3(s-1)^3.
\tag{1.9}
\]

The hold protocol below concerns this same plant, but temporarily replaces
its state equations by prescribed state constraints. It is therefore a
hybrid preparation stage, not an additional term hidden in (1.3).

## 2. A causal maximum-delay hold

Fix \(r\in[-1,1]\), a hold-start time \(t_h\), and the release time

\[
 t_r=t_h+\tau_*.
\tag{2.1}
\]

At \(t=t_h\), overwrite the node states and, for the entire closed hold
interval, impose the ideal constraints

\[
 v_i(t)=r,
 \qquad w_i(t)=0,
 \qquad i=1,\ldots,n_1+n_2,
 \qquad t_h\le t\le t_r.
\tag{2.2}
\]

At \(t_r\), release the voltage constraint, retain the collective recovery
input (1.4), and evolve (1.3)--(1.4). Denote a released history by

\[
 (v_{t_r},w_{t_r})(\theta)
   =(v(t_r+\theta),w(t_r+\theta)),
 \qquad -\tau_*\le\theta\le0.
\tag{2.3}
\]

> **Theorem 2.1 (causal complete-history overwrite).** For every pre-hold
> history, every \(r\in[-1,1]\), and every pair of positive module sizes, the
> protocol (2.1)--(2.2) produces at release the exact complete history
>
> \[
>  (v_{t_r},w_{t_r})=\Phi_r,
>  \qquad
>  \Phi_r(\theta)=(r\mathbf1,0),
>  \qquad -\tau_*\le\theta\le0.
> \tag{2.4}
> \]
>
> The preparation time is exactly one maximum-delay window, \(5\sqrt5\).

**Proof.** If \(-\tau_*\le\theta\le0\), then
\(t_h\le t_r+\theta\le t_r\). Equation (2.2) therefore gives

\[
 v(t_r+\theta)=r\mathbf1,
 \qquad w(t_r+\theta)=0.
\]

This is (2.4), independently of every state value before \(t_h\).
\(\square\)

The construction is causal in the ordinary control sense: at each time in
the hold interval it enforces a command already issued at \(t_h\); it does
not prescribe a future history at \(t_r\). Its exactness nevertheless comes
from the ideal overwrite in (2.2). In particular, delayed values inherited
from the pre-hold history may exert arbitrarily large forces during the early
part of the hold, and the constraint is postulated to cancel them exactly.
Nothing here bounds the required reaction force, impulse at \(t_h\), energy,
bandwidth, slew rate, or state-estimation error. Thus Theorem 2.1 must not be
restated as controllability from arbitrary histories by a bounded additive
voltage or recovery input.

## 3. Monotonicity and the two complete-history cones

The gain signs in (1.6) give the global identity

\[
 g_b'(s)=\kappa_1+3\kappa_3(s-1)^2
 \ge \inf_U\kappa_1>0,
 \qquad s\in\mathbb R.
\tag{3.1}
\]

Hence \(g_b\) is strictly increasing on the whole real line, uniformly in
\(b\in U\). On the synchronous zero-recovery history space define

\[
\begin{aligned}
 \mathcal C_+
 &=\{(\varphi\mathbf1,0):
       \varphi(\theta)\ge0\text{ for all }\theta,
       \ 0<\varphi(0)<1\},\\
 \mathcal C_-
 &=\{(\varphi\mathbf1,0):
       \varphi(\theta)\le0\text{ for all }\theta,
       \ -1<\varphi(0)<0\}.
\end{aligned}
\tag{3.2}
\]

Set

\[
 c_+(b)=\frac23-\varepsilon(\kappa_1+3\kappa_3),
 \qquad
 c_-(b)=\frac23-\varepsilon(\kappa_1+7\kappa_3).
\tag{3.3}
\]

Directed evaluation on \(U\) supplies the uniform lower bounds

\[
 \underline c_+
 =0.4766666666658666666666666666666666666666666666649547831,
\tag{3.4}
\]

and

\[
 \underline c_-
 =0.2766666666650666666666666666666666666666666666645611784.
\tag{3.5}
\]

> **Theorem 3.1 (complete-history sign-cone first hits).** Fix \(b\in U\)
> and retain the collective recovery clamp. If the released history belongs
> to \(\mathcal C_+\), then the solution of (1.8) remains positive until it
> reaches \(x=1\), and its first-hit time satisfies
>
> \[
>  0<T_+(\varphi)
>  \le \frac1{c_+(b)}\log\frac1{\varphi(0)}
>  \le \frac1{\underline c_+}\log\frac1{\varphi(0)}.
> \tag{3.6}
> \]
>
> Before the hit,
>
> \[
>  \dot x(t)\ge c_+(b)x(t)>0.
> \tag{3.7}
> \]
>
> If the released history belongs to \(\mathcal C_-\), then the solution
> remains negative until it reaches \(x=-1\), and
>
> \[
>  0<T_-(\varphi)
>  \le \frac1{c_-(b)}\log\frac1{|\varphi(0)|}
>  \le \frac1{\underline c_-}\log\frac1{|\varphi(0)|}.
> \tag{3.8}
> \]
>
> Before this hit,
>
> \[
>  \dot x(t)\le c_-(b)x(t)<0.
> \tag{3.9}
> \]

**Proof.** Consider first a solution while \(0<x(t)\le1\). As long as
the solution has remained positive, both delayed values are nonnegative:
they lie either in the prescribed history or on the already constructed
positive trajectory. By (3.1),

\[
 \frac{g_b(x(t-\tau_0))+g_b(x(t-\tau_1))}{2}
 \ge g_b(0).
\tag{3.10}
\]

For \(0<x\le1\), direct factorization gives

\[
 g_b(x)-g_b(0)
 =x\{\kappa_1+\kappa_3(x^2-3x+3)\},
 \qquad x^2-3x+3\le3,
\tag{3.11}
\]

whereas

\[
 x-\frac{x^3}{3}\ge\frac23x.
\tag{3.12}
\]

Substitution in (1.8) proves (3.7). A first exit from \((0,1)\) cannot
therefore occur through zero. Moreover,
\(x(t)\ge\varphi(0)e^{c_+(b)t}\) until the first hit. If \(x=1\) had not
been reached by the first time on the right side of (3.6), this lower bound
would already equal one, a contradiction. This proves the positive claim.

For the negative cone, while \(-1\le x(t)<0\), every delayed value is
nonpositive. Strict monotonicity now yields

\[
 \frac{g_b(x(t-\tau_0))+g_b(x(t-\tau_1))}{2}
 \le g_b(0).
\tag{3.13}
\]

For \(-1\le x<0\),

\[
 g_b(0)-g_b(x)
 =-x\{\kappa_1+\kappa_3(x^2-3x+3)\},
 \qquad x^2-3x+3\le7.
\tag{3.14}
\]

Consequently

\[
\begin{aligned}
 \dot x
 &\le x\left[
  1-\frac{x^2}{3}
  -\varepsilon\{\kappa_1+\kappa_3(x^2-3x+3)\}
 \right]\\
 &\le c_-(b)x<0.
\end{aligned}
\tag{3.15}
\]

The last inequality reverses in the coefficient because \(x<0\): the
bracket in (3.15) is at least \(c_-(b)\). Thus a first exit from
\((-1,0)\) cannot occur through zero. With \(u=-x\), inequality (3.9)
becomes \(\dot u\ge c_-(b)u\), which proves (3.8). \(\square\)

No step of this proof assumes
\(x(t-\tau_j)\le x(t)\) in the positive channel or the reverse ordering in
the negative channel. The delayed histories may have arbitrary continuous
shapes and arbitrary magnitudes of the appropriate sign. Only their sign,
the sign of the present value, and the exact condition \(w=0\) are used.

For the exact hold history (2.4), Theorem 3.1 recovers

\[
 T_+(\Phi_r)\le\underline c_+^{-1}\log(1/r)
 \quad(0<r<1),
\tag{3.16}
\]

and

\[
 T_-(\Phi_r)\le\underline c_-^{-1}\log(1/|r|)
 \quad(-1<r<0).
\tag{3.17}
\]

Measured from the start of the hold rather than from voltage release, the
corresponding protocol deadlines are obtained by adding \(5\sqrt5\).

## 4. Explicit synchronous history robustness

The cones in (3.2) contain genuine sup-norm neighborhoods of every nonzero
constant history that stays away from the detector faces. This gives a
quantitative robustness statement within the synchronous zero-recovery
history space, even though no nonsynchronous or recovery-error tube is
claimed.

For \(0<|r|<1\), define

\[
 \rho_{\rm syn}(r)
 =\frac12\min\{|r|,1-|r|\}.
\tag{4.1}
\]

In particular,

\[
 0<\rho_{\rm syn}(r)<|r|.
\tag{4.2}
\]

Use the synchronous voltage-history norm

\[
 \|\varphi-r\|_\infty
 =\max_{-\tau_*\le\theta\le0}|\varphi(\theta)-r|.
\tag{4.3}
\]

> **Corollary 4.1 (explicit sign-robust history balls).** Let
> \(0<|r|<1\) and suppose
>
> \[
>  \|\varphi-r\|_\infty\le\rho_{\rm syn}(r),
>  \qquad
>  \phi(\theta)=(\varphi(\theta)\mathbf1,0).
> \tag{4.4}
> \]
>
> If \(r>0\), then \(\phi\in\mathcal C_+\) and
>
> \[
>  T_+(\phi)
>  \le\frac1{\underline c_+}
>       \log\frac1{r-\rho_{\rm syn}(r)}.
> \tag{4.5}
> \]
>
> If \(r<0\), then \(\phi\in\mathcal C_-\) and
>
> \[
>  T_-(\phi)
>  \le\frac1{\underline c_-}
>       \log\frac1{|r|-\rho_{\rm syn}(r)}.
> \tag{4.6}
> \]
>
> The total time from the start of the ideal hold is bounded by
> \(5\sqrt5\) plus the appropriate right side of (4.5) or (4.6).

**Proof.** If \(r>0\), (4.1)--(4.4) give

\[
 0<r-\rho_{\rm syn}(r)
 \le\varphi(\theta)
 \le r+\rho_{\rm syn}(r)<1.
\]

Thus the history lies in \(\mathcal C_+\), and
\(\varphi(0)\ge r-\rho_{\rm syn}(r)\). Equation (4.5) follows from
(3.6). For \(r<0\), the same estimates applied to absolute values put the
history in \(\mathcal C_-\) and give
\(|\varphi(0)|\ge|r|-\rho_{\rm syn}(r)\). Equation (3.8) proves (4.6).
\(\square\)

More generally, any radius

\[
 0<\rho<\min\{|r|,1-|r|\}
\tag{4.7}
\]

is admissible, with \(\rho\) replacing \(\rho_{\rm syn}(r)\) in the
deadline. This is robustness to the *shape of a synchronous voltage
history*. It does not allow nonzero recovery histories, module mismatch,
nodewise noise, clamp error, or uncertainty in the full-network state.

## 5. The declared detector and its stopping boundary

For this decision protocol we declare

\[
 \mathcal D_+=\{x=1\}
\tag{5.1}
\]

to be the physical voltage-threshold onset detector. Theorem 3.1 proves
that every history in \(\mathcal C_+\) reaches this detector, with the stated
deadline, and that the crossing is outward because
\(\dot x\ge c_+(b)>0\) at the first hit. This is a rigorous event statement
about the measured voltage coordinate.

The word *onset* is part of the declared operational interpretation of
\(\mathcal D_+\). The theorem stops when \(x=1\) is first reached. It does
not prove that the released trajectory then lies in a biological spiking
basin, completes an action potential, follows a relaxation excursion, or
cannot return across the face. Those conclusions require a beyond-face
invariant-region, basin, or no-return theorem that is not supplied here.

Similarly,

\[
 \mathcal D_-=\{x=-1\}
\tag{5.2}
\]

is the declared negative decision face. Reaching it is not a proof of
capture by a biological quiet basin. Neither detector is identified here
with an unforced maximal-canard threshold.

The sign-cone theorem is synchronous. The previously proved transverse
Halanay estimate is a linear variational statement and does not promote
Corollary 4.1 to nonlinear capture of noisy nonsynchronous histories.

## 6. Deadband versus the three-output safety margin

The staged three-output response uses

\[
 \mathcal Q_{\rm op}(b,r)
 =\bigl(F(b),R_h(b),S_{\rm op}\bigr),
 \qquad S_{\rm op}=-r.
\tag{6.1}
\]

The tracked block-diagonal inverse theorem gives a target-ball radius

\[
 \rho_3\ge
 1.62187273782174089504757331762715967009378618047942197
 \times10^{-14}
\tag{6.2}
\]

about \(S_{\rm op}=0\). Its tracked artifact is
[fhn_same_model_three_output.json](../experiments/results/fhn_same_model_three_output.json),
with SHA-256 digest

~~~text
afc03431d61d86c6bda8b56a73bdeea76b357e9a31a4a843d9f55cebbf666532
~~~

Exact sign classification holds for every \(r\ne0\), but its robustness
radius tends to zero and its deadline tends to infinity as \(r\to0\). A
uniform operational specification should therefore impose a separator
deadband

\[
 |r|=|S_{\rm op}|\ge\delta>0.
\tag{6.3}
\]

Suppose more generally that commands satisfy

\[
 \delta\le|r|\le1-\gamma,
 \qquad
 0\le\eta<\min\{\delta,\gamma\},
\tag{6.4}
\]

and that the synchronous voltage preparation error is at most \(\eta\) in
the norm (4.3). Then its sign is unchanged, its current magnitude is at
least \(\delta-\eta\), and the release-to-hit deadlines are uniformly bounded
by

\[
 T_+\le\underline c_+^{-1}\log\frac1{\delta-\eta},
 \qquad
 T_-\le\underline c_-^{-1}\log\frac1{\delta-\eta}.
\tag{6.5}
\]

Thus increasing \(\delta\) enlarges the admissible sign-error budget and
shortens the worst-case decision time. The cost is geometric: no ball of
positive radius centered at \(S_{\rm op}=0\) lies wholly in the two-sided
deadband set \(\{|S_{\rm op}|\ge\delta\}\). Consequently the centered target
ball (6.2) is a reachability result for the signed operational coordinate,
not a uniform deadband-robust onset ball.

Because the reset column in (6.1) is exactly \(-1\), the same
block-diagonal inverse argument can be recentered at \(r_0\), without changing
its derivative constants, whenever the radius-\(10^{-12}\) input ball remains
in the reset interval; it is enough that
\(|r_0|+10^{-12}<1\). This recentering is an analytic consequence of the
proved block structure, not a separate flag in the tracked artifact.

For a nonzero safety center \(S_0=-r_0\), an output ball of radius \(\rho\)
remains on one declared channel, outside the deadband, and before the
detector face only if

\[
 \rho<\min\{|S_0|-\delta,\ 1-|S_0|\}.
\tag{6.6}
\]

After also imposing the inverse-theorem radius, the usable robust target
radius can be no larger than

\[
 \rho_{\rm robust}
 \le\min\{\rho_3,\ |S_0|-\delta,\ 1-|S_0|\}.
\tag{6.7}
\]

Equations (6.5)--(6.7) display the tradeoff without hiding it in a rescaling
of the safety output: a larger deadband improves history-sign tolerance and
deadline, while reducing the connected target neighborhood available around
a chosen safety operating point. They do not include hardware command
error or nonsynchronous state noise.

## 7. Claim ledger

| Statement | Status |
|---|---|
| One-max-delay ideal hold maps every pre-hold history to \(\Phi_r\) | **Proved by Theorem 2.1** |
| Hold is causal and has duration \(5\sqrt5\) | **Proved for the hybrid state-overwrite definition** |
| Hold is realizable by a bounded additive actuator from arbitrary histories | **Not proved; the ideal overwrite may require unbounded reaction force or an impulse** |
| Exact collective recovery clamp and synchronous \(w=0\) decision leaf | **Inherited from the same-model clamped network and (1.7)** |
| \(g_b\) is globally strictly increasing on the gain box | **Proved by (3.1)** |
| Positive and negative complete-history sign cones | **Proved by Theorem 3.1 without delayed-value ordering** |
| Uniform first-hit deadlines | **Proved by (3.6), (3.8), and (6.5)** |
| Explicit sup-norm balls around every nonzero \(\Phi_r\), \(0<|r|<1\) | **Proved within the synchronous zero-recovery history space** |
| \(x=+1\) is the declared voltage-threshold onset detector | **Defined operationally; its finite outward first hit is proved** |
| Biological pulse basin or no-return after \(x=+1\) | **Not proved** |
| Biological quiet basin after \(x=-1\) | **Not proved** |
| Nonlinear transverse or noisy-history capture | **Not proved** |
| Hardware amplitude, energy, bandwidth, slew-rate, and clamp-error containment | **Not proved** |
| Equality with an unforced or maximal-canard threshold | **Not proved** |
| Three-output centered target ball | **Proved by the tracked block-diagonal inverse artifact** |
| Deadband-robust three-output ball centered at zero | **Impossible for every positive deadband; a nonzero safety center must satisfy (6.6)** |
| General network topology | **Not proved; the network remains the fixed rank-one two-module family** |

The new bridge is therefore precise but limited: it replaces a noncausal
prescription of a complete history by a causal ideal hold and enlarges the
constant-reset first-hit result to infinite-dimensional synchronous sign
cones. The remaining physical step is to replace the ideal overwrite by an
implementable actuator with quantified preparation error. The remaining
biological step is a beyond-detector basin or no-return theorem.
