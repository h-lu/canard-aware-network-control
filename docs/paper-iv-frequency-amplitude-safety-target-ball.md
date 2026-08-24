# A same-model frequency--amplitude--operational-safety target ball

Status: **proved for the fixed staged FHN protocol and the fixed rank-one
two-module \(D=3,E=2\) instance.** Two closed three-dimensional Euclidean
input balls, centered at reset values \(r_0=\pm\frac12\), cover nonzero
closed Euclidean output balls for frequency, unsquared voltage amplitude,
and the exact controlled operational margin \(S_{\rm op}=-r\). The result
does not prove finite-time preparation, a biological basin statement,
periodic attraction, an unforced or maximal-canard onset, or a general
network-topology theorem.

The proof implementation is
[fhn_same_model_amplitude_safety.py](../src/canard_control/fhn_same_model_amplitude_safety.py),
the driver is
[fhn_same_model_amplitude_safety.py](../experiments/fhn_same_model_amplitude_safety.py),
the source-bound result is
[fhn_same_model_amplitude_safety.json](../experiments/results/fhn_same_model_amplitude_safety.json),
and the refusal tests are
[test_fhn_same_model_amplitude_safety.py](../tests/test_fhn_same_model_amplitude_safety.py).

## 1. The four parent results

Write \(b=(\kappa_1,\kappa_3)\), \(b_c=(0.2,0.25)\), and let

\[
 A(b)=\max_\theta V_b(\theta)-\min_\theta V_b(\theta).
\tag{1.1}
\]

The amplitude certificate proves

\[
\begin{aligned}
 A_-={}&
 2.94737622302543311589267704607213287465934506175704116,\\
 A_+={}&
 2.94737869577245638555737941249143755810909328788192661
\end{aligned}
\tag{1.2}
\]

with

\[
 0<A_-\le A(b)\le A_+
\tag{1.3}
\]

throughout the microscopic gain box.

The same-model squared-range certificate concerns the staged map

\[
 Q_R(b,r)=\bigl(F(b),A(b)^2,-r\bigr).
\tag{1.4}
\]

It proves that the closed Euclidean input ball

\[
 \overline B_R((b_c,0))\subset\mathbb R^3,
 \qquad R=10^{-12},
\tag{1.5}
\]

covers the closed Euclidean output ball about
\(Q_R(b_c,0)\) of radius

\[
 \rho_R=
 1.62187273782174089504757331762715967009378618047942197
 \times10^{-14}.
\tag{1.6}
\]

Every target in that output ball has a unique preimage in (1.5). This is a
genuinely three-dimensional Euclidean theorem; no product-domain
replacement is made below.

The separator certificate supplies two further exact facts for the same
plant, gain box, and reset family:

1. \(r\in(-1,1)\) is the declared constant-history reset coordinate and
   the controlled operational threshold is \(r_c=0\);
2. \(0<r<1\) reaches the \(+1\) detector face, while
   \(-1<r<0\) reaches the \(-1\) detector face.

We call these the pulse-side and quiet-side **operational** channels,
respectively. These labels refer only to the declared first-hit detector.
They do not identify the two faces with biological pulse and quiet basins.

All four ingredients are tied to the same parameter-box result. The new
driver pins and checks the hashes of

- the uniform amplitude result;
- the same-model three-output squared-range result;
- the same-model separator result; and
- the periodic parameter-box result.

It also verifies every available parent generator and proof-source manifest.

## 2. Three-dimensional inverse-coordinate transfer

Define the desired map

\[
 Q_A(b,r)=\bigl(F(b),A(b),-r\bigr).
\tag{2.1}
\]

Let

\[
 Q_A(b_c,r_0)=(F_c,A_c,-r_0).
\tag{2.2}
\]

A desired output displacement in the \((F,A,S_{\rm op})\) coordinates is
written

\[
 z=(d_F,d_A,d_S).
\tag{2.3}
\]

The corresponding squared-range displacement is exactly

\[
 \Psi(z)=
 \bigl(d_F,\,2A_c d_A+d_A^2,\,d_S\bigr).
\tag{2.4}
\]

The third component is retained in (2.4); this is the point at which a
two-dimensional argument would be insufficient.

> **Lemma 2.1 (three-dimensional square-to-amplitude inner ball).**
> Suppose \(0<A_-\le A_c\le A_+\), and suppose the image of a
> three-dimensional input domain under \(Q_R\) contains
> \(\overline B_{\rho_R}(Q_R(b_c,r_0))\), with a unique preimage for every
> target. If \(\rho_A>0\) satisfies
> \[
> \rho_A\le\rho_R,\qquad
> \rho_A\le A_-/2,\qquad
> (2A_++\rho_A)\rho_A\le\rho_R,
> \tag{2.5}
> \]
> then the same input domain under \(Q_A\) contains
> \[
> \overline B_{\rho_A}(Q_A(b_c,r_0)),
> \tag{2.6}
> \]
> and every target in (2.6) has a unique preimage.

**Proof.** Let \(\|z\|_2\le\rho_A\), and put

\[
 L=2A_++\rho_A.
\tag{2.7}
\]

Since \(|d_A|\le\rho_A\),

\[
 |2A_c d_A+d_A^2|\le L|d_A|.
\tag{2.8}
\]

Consequently

\[
\begin{aligned}
 \|\Psi(z)\|_2^2
 &=
 d_F^2+(2A_c d_A+d_A^2)^2+d_S^2\\
 &\le d_F^2+L^2d_A^2+d_S^2\\
 &\le \max\{1,L^2\}\|z\|_2^2.
\end{aligned}
\tag{2.9}
\]

The first and third inequalities in (2.5) give

\[
 \|\Psi(z)\|_2
 \le\max\{\rho_A,L\rho_A\}\le\rho_R.
\tag{2.10}
\]

The squared-range theorem therefore supplies a unique input whose squared
amplitude equals \((A_c+d_A)^2\). The second inequality in (2.5) gives

\[
 A_c+d_A\ge A_--\rho_A\ge A_-/2>0.
\tag{2.11}
\]

Exact voltage amplitude is nonnegative, so equality of the squares implies
that its amplitude is exactly \(A_c+d_A\). The safety component is unchanged
by \(\Psi\). Hence this input realizes the original target \(z\), and
uniqueness is inherited from the squared-range theorem. \(\square\)

For the public radius

\[
 \boxed{
 \rho_A=
 2.75138166016477172021072951467987182906462947064987861
 \times10^{-15},}
\tag{2.12}
\]

the directed three-dimensional composition gives

\[
\begin{aligned}
 (2A_++\rho_A)\rho_A
 \le{}&
 1.62187273782174089504757331762588023809767484060466179538\\
 &{}\times10^{-14}
 <\rho_R.
\end{aligned}
\tag{2.13}
\]

The strict directed slack in (2.13) is at least

\[
 1.27943199611133987476017461990222313665\times10^{-44}.
\tag{2.14}
\]

The unchanged frequency and safety components also satisfy
\(\rho_A<\rho_R\), while

\[
 A_--\rho_A>
 2.9473762230254303645.
\tag{2.15}
\]

Thus the positive square-root branch is separated from zero by a very large
margin relative to the target radius.

## 3. Exact recentering in the reset coordinate

The baseline periodic response depends only on \(b\); the reset \(r\) is
used in the later controlled decision stage. Hence, for every fixed
\(r_0\) and every displacement \(u\),

\[
 Q_R(b,r_0+u)-Q_R(b_c,r_0)
 =
 \bigl(P(b)-P(b_c),-u\bigr).
\tag{3.1}
\]

The right side is exactly the displacement used by the parent theorem at
\(r_0=0\).

> **Lemma 3.1 (translation of the three-dimensional input ball).**
> Suppose
> \[
> [r_0-R,r_0+R]\subset(-1,1).
> \tag{3.2}
> \]
> Then the parent squared-range theorem translates without loss from the
> input ball \(\overline B_R((b_c,0))\) to
> \[
> \overline B_R((b_c,r_0)).
> \tag{3.3}
> \]
> The translated image contains the closed squared-range output ball of
> radius \(\rho_R\) about \(Q_R(b_c,r_0)\), and every target has a unique
> preimage in (3.3).

**Proof.** A point \((b,r_0+u)\) belongs to (3.3) exactly when
\((b,u)\) belongs to the original input ball. Identity (3.1) identifies
their relative outputs. Existence and uniqueness therefore transfer
bijectively. Condition (3.2) keeps every translated reset inside the
declared separator family. \(\square\)

This is an exact translation of a Euclidean ball. It is not an argument on
\(B_R(b_c)\times(-R,R)\).

## 4. Two operational deadband charts

For \(r_0=+\frac12\), the reset projection of the entire closed input ball
is

\[
 [0.499999999999,\,0.500000000001]\subset(0,1).
\tag{4.1}
\]

It neither crosses the operational threshold \(r=0\) nor the \(+1\)
detector face. Its distance from each is at least

\[
 0.499999999999.
\tag{4.2}
\]

The output center is

\[
 Q_A(b_c,\tfrac12)=(F_c,A_c,-\tfrac12).
\tag{4.3}
\]

This is the pulse-side positive-face operational chart.

For \(r_0=-\frac12\), the reset projection is

\[
 [-0.500000000001,\,-0.499999999999]\subset(-1,0).
\tag{4.4}
\]

It neither crosses \(r=0\) nor the \(-1\) detector face, again with
deadband at least \(0.499999999999\). Its output center is

\[
 Q_A(b_c,-\tfrac12)=(F_c,A_c,\tfrac12).
\tag{4.5}
\]

This is the quiet-side negative-face operational chart.

The containment in \((-1,1)\) also shows that neither input ball can cross
the opposite detector face.

## 5. Same-model three-output theorem

Lemmas 2.1 and 3.1 give the main result.

> **Theorem 5.1 (frequency--amplitude--operational-safety balls).**
> For each
> \[
> r_0\in\left\{\frac12,-\frac12\right\},
> \tag{5.1}
> \]
> the staged map
> \[
> Q_A(b,r)=\bigl(F(b),A(b),-r\bigr)
> \tag{5.2}
> \]
> maps the closed three-dimensional Euclidean input ball
> \[
> \overline B_{10^{-12}}((b_c,r_0))
> \tag{5.3}
> \]
> onto a set containing the closed three-dimensional Euclidean output ball
> \[
> \overline B_{\rho_A}(Q_A(b_c,r_0)),
> \tag{5.4}
> \]
> where \(\rho_A\) is the positive number in (2.12). Every target in
> (5.4) has a unique preimage in (5.3).
>
> The \(r_0=+\frac12\) input ball lies wholly in the positive-face
> operational channel, and the \(r_0=-\frac12\) input ball lies wholly in
> the negative-face operational channel.

The output center uses the exact periodic-orbit amplitude \(A_c\), not the
binary64 candidate amplitude. The theorem combines the validated staged
periodic branch with controlled operational first-hit safety. It does not
assert that a bounded additive actuator prepares the constant history in
finite time.

## 6. Proof dependencies and source binding

\[
\begin{array}{c}
 \text{parameter-box periodic branch}\\
 \downarrow\\
 \text{uniform positive exact-orbit amplitude enclosure}\\
 \downarrow\\
 \text{source-bound }(F,A)\text{ inverse-coordinate radius}\\
 \text{same-model separator}
 \longrightarrow
 \text{exact }S_{\rm op}=-r\text{ and }(-1,1)\text{ reset family}\\
 \downarrow\hspace{25mm}\downarrow\\
 \text{same-model }(F,R_h,S_{\rm op})\text{ Euclidean target ball}\\
 \downarrow\\
 \text{three-dimensional inverse-coordinate estimate (2.9)}\\
 \downarrow\\
 \text{exact reset translations at }r_0=\pm\tfrac12\\
 \downarrow\\
 \text{Theorem 5.1}.
\end{array}
\tag{6.1}
\]

The generated result records the exact hashes

\[
\begin{array}{ll}
 \text{amplitude result:}&
 28e74d2316f7e9324f03874c3294d27d83708c9dbb3f4eefaf04925f55bbba60,\\
 \text{three-output result:}&
 afc03431d61d86c6bda8b56a73bdeea76b357e9a31a4a843d9f55cebbf666532,\\
 \text{separator result:}&
 9e859f31c177638a70b3ca451fe743227308343792d77eeca286fca26afc8a86,\\
 \text{parameter-box result:}&
 ff13b5352c2b4e9898a4044be63fd490a3e7bb4217445a6a062188c2457c22a0.
\end{array}
\tag{6.2}
\]

The amplitude parent itself pins the squared target-ball result, while the
same-model three-output parent pins that same target ball and the separator.
The new semantic validator refuses any mismatch of these links.

## 7. Claim ledger

| Statement | Status |
|---|---|
| Uniform positive unsquared amplitude on the gain box | **Proved by the amplitude parent** |
| Three-dimensional Euclidean \((F,R_h,-r)\) target ball | **Proved by the same-model parent** |
| Three-dimensional inverse-coordinate norm estimate (2.9) | **Proved with directed public decimals** |
| Closed \((F,A,-r)\) output ball of radius (2.12) | **Proved** |
| Unique preimage in each translated Euclidean input ball | **Proved by exact reset translation and parent uniqueness** |
| Pulse-side chart stays in \(0<r<1\) | **Proved operationally** |
| Quiet-side chart stays in \(-1<r<0\) | **Proved operationally** |
| The operational faces are biological pulse and quiet basins | **Not asserted** |
| Bounded-additive finite-time preparation of the reset history | **Open and delegated to a separate theorem** |
| Finite physical pulse, hardware/noise robustness, or basin capture | **Not proved** |
| Periodic attraction | **Not proved** |
| Unforced onset or maximal-canard onset | **Not asserted** |
| General network topology | **Not proved; the fixed rank-one two-module instance is used** |
| Closure of issue 15 | **No** |

The advance is a same-model three-output theorem with the physically
interpretable unsquared voltage excursion and two detector-safe operational
charts. Its scope remains staged and local: preparation, attraction,
biological basin capture, and general topology are separate problems.
