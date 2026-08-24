# A directed finite-window longitudinal-jet gap seed

## Status and claim boundary

This note proves and certifies the finite-window Green row for one explicit
**longitudinal first-order forcing datum**.  It provides a reproducible
precursor to the first numerical subproblem isolated in the
[fixed-epsilon sliding-window bridge](fixed-epsilon-sliding-window-w1p-bridge.md):
the Gaussian moment is now a genuinely finite-window quantity, rather than
an imported whole-line asymptotic.

The datum below is **not** the complete admissible preparation

\[
 \mathcal P=(p,B,\chi_{\rm graph},\chi_{\rm plan},
             \mathcal E_\perp,\{\mathscr H=0\})
\]

of the nonlinear RFDE graph theorem.  In particular, it does not construct
the frozen graph family, enclose its deformed positive-amplitude tubular
depth-two flow hull, or solve the positive-amplitude prepared trace problem.
Consequently the
unique zero of the affine seed row is denoted \(\nu_{0,\chi}\), not
\(\nu_{0,S,\mathcal P}\).  The exact promotion condition is stated in
Section 5.

## 1. The frozen linear trace datum

Let

\[
 q_0(X,Y)=(Y-X^2,-X),\qquad
 \gamma _0(s)=\left(-\frac{s}{2},\frac{s^2-2}{4}\right).
\]

For the reproducible reference calculation, freeze

\[
 S=4,\qquad B=18,\qquad R=S+B=22.
\tag{1}
\]

The value \(S=4\) is a finite reference section.  It is not asserted to
equal the logarithmic moving radius \(S_{\delta_*}\), nor is it asserted to
exceed the non-explicit \(S_0\) in the growing-tube theorem.

Define the even cutoff

\[
 \chi(s)=
 \begin{cases}
  1,& |s|\le 20,\\[2mm]
  1-h(|s|-20),&20<|s|<21,\\[2mm]
  0,&|s|\ge21,
 \end{cases}
\tag{2}
\]

where

\[
 h(r)=35r^4-84r^5+70r^6-20r^7,
 \qquad h'(r)=140r^3(1-r)^3.
\tag{3}
\]

Thus \(0\le\chi\le1\), \(\chi\) is nonincreasing for positive \(s\),
and its value and first three derivatives join the constant pieces.  It is
globally \(C^3\), but not \(C^4\):

\[
 (h,h',h'',h''',h'''')(0)=(0,0,0,0,840),
\]

\[
 (h,h',h'',h''',h'''')(1)=(1,0,0,0,-840).
\]

This makes (4) a \(C^3\) curve datum along \(\gamma_0\).  It
must not be reused as the higher-regularity anisotropic graph cutoff.  The
larger plateau is deliberate: Section 4 proves that it contains the retained
singular segment and every continuous depth-two delayed backtrack for the
pinned horizon.

Freeze the forcing along \(\gamma _0\) as

\[
 f_\chi(s;\nu)
 =\chi(s)
 \begin{pmatrix}s^3/24+9/20\\ \nu\end{pmatrix}.
\tag{4}
\]

The uncut expression in (4) is the exact first \(\varrho\)-jet of the
quadratic period-lock carrier on the singular orbit.  Equation (4) declares
how that jet is joined to zero near the artificial tails; it does not claim
that an already validated nonlinear graph preparation produces this join.

## 2. Finite-window Green-row theorem

Write \(\xi=(U,V)\) and

\[
 L_0(U,V)=\binom{U'-sU-V}{V'+U}.
\]

On the attracting and repelling half intervals solve

\[
 L_0\xi^a=f_\chi\quad(-R\le s\le0),
 \qquad
 L_0\xi^r=f_\chi\quad(0\le s\le R),
\tag{5}
\]

with phase and linearized tail conditions

\[
 U^a(0)=U^r(0)=0,
\tag{6}
\]

\[
 -R U^a(-R)+V^a(-R)=0,
 \qquad
 R U^r(R)+V^r(R)=0.
\tag{7}
\]

These are the fixed-phase and \(\mathscr H=0\) conditions from the
[one-sided Green theorem](green-phase-selected-traces.md).  Its normal
coefficient satisfies

\[
 b'(s)=e^{-s^2/2}\{s f_1(s)+f_2(s)\}.
\tag{8}
\]

The endpoint conditions set the incoming normal coefficients to zero, and
the phase removes the remaining tangent homogeneous solution.  Hence (5)--(7)
have unique one-sided solutions.  For the section gap

\[
 M_\chi(\nu)=V^a(0)-V^r(0)
\]

equation (8) gives the exact identity

\[
 \boxed{
 M_\chi(\nu)=
 \int_{-R}^{R}e^{-s^2/2}
 \{s f_{\chi,1}(s;\nu)+f_{\chi,2}(s;\nu)\}\,ds
 =A_\chi\nu+B_\chi .}
\tag{9}
\]

Because \(\chi\) is even, the \(9s/20\) contribution is odd and cancels.
Therefore

\[
 A_\chi=\int_{-R}^{R}e^{-s^2/2}\chi(s)\,ds>0,
\tag{10}
\]

\[
 B_\chi=\frac1{24}\int_{-R}^{R}
 s^4e^{-s^2/2}\chi(s)\,ds>0.
\tag{11}
\]

The strict inequalities are analytic: the integrands are nonnegative and
strictly positive on an interval of positive length.  The same argument
applies to every nonzero, nonnegative even cutoff.  Thus the affine row has
the unique negative root

\[
 \boxed{\nu_{0,\chi}=-B_\chi/A_\chi<0.}
\tag{12}
\]

This nondegeneracy does not rely on numerical quadrature.  Because
\(\chi=0\) on the full endpoint neighborhoods
\([-22,-21]\cup[21,22]\), the forcing is zero there and the fixed
\(\mathscr H=0\) conditions are exactly \(b_a(-22)=b_r(22)=0\); there is no
hidden parameter derivative of a moving tail anchor.

## 3. Directed evaluation

On the positive transition interval, (2) has the exact polynomial

\[
\begin{aligned}
 \chi(s)={}&20s^7-2870s^6+176484s^5-6028435s^4\\
 &+123538800s^3-1518804000s^2\\
 &+10372320000s-30354399999.
\end{aligned}
\tag{13}
\]

For

\[
 J_n(a,b)=\int_a^b s^n e^{-s^2/2}\,ds,
\]

the generator evaluates

\[
 J_0=\sqrt{\frac\pi2}
 \left[\operatorname{erfc}\!\left(\frac a{\sqrt2}\right)
      -\operatorname{erfc}\!\left(\frac b{\sqrt2}\right)\right],
\tag{14}
\]

\[
 J_1=e^{-a^2/2}-e^{-b^2/2},
\]

\[
 J_n=a^{n-1}e^{-a^2/2}-b^{n-1}e^{-b^2/2}
       +(n-1)J_{n-2}.
\tag{15}
\]

Equations (13)--(15) reduce (10)--(11) to a finite combination of moments
through \(J_{11}\).  Every rational operation and every MPFR evaluation of
\(\pi,\sqrt{\cdot},\exp\), and \(\operatorname{erfc}\) is rounded outward at
512 bits.  The resulting enclosures are

\[
 2.5066282746310005024157652848110452530069867406099
 <A_\chi
 <2.5066282746310005024157652848110452530069867406100,
\tag{16}
\]

\[
 0.3133285343288750628019706606013806566258733425762
 <B_\chi
 <0.3133285343288750628019706606013806566258733425763,
\tag{17}
\]

\[
 \nu_{0,\chi}=-\frac18+\Delta_\chi,
 \qquad
 1.04939743217124\times10^{-87}
 <\Delta_\chi
 <1.04939743217125\times10^{-87}.
\tag{18}
\]

The exact outward decimal endpoints and widths are stored in
[`fixed_window_prepared_gap_seed.json`](../experiments/results/fixed_window_prepared_gap_seed.json).
The serialized directed widths are below \(2.1\times10^{-153}\),
\(3.4\times10^{-154}\), and \(2.2\times10^{-154}\), respectively.

For comparison, the whole-line values are

\[
 A_\infty=\sqrt{2\pi},\qquad B_\infty=\frac{\sqrt{2\pi}}8,
 \qquad \nu_{0,\infty}=-\frac18.
\]

The certificate proves both finite-window defects positive.  Numerically,

\[
 A_\infty-A_\chi\approx3.7797261\times10^{-91},
 \qquad
 B_\infty-B_\chi\approx2.6304965\times10^{-87}.
\]

For this explicit cutoff, this directly proves that the frozen-window root
is not exactly \(-1/8\).  The parent theorem identifies \(-1/8\) only as a
moving-window limit; this calculation does not assert that every possible
finite preparation has a different root.  The certificate also encloses
\(\nu_{0,\chi}+1/8>0\), whose midpoint is approximately
\(1.0493974322\times10^{-87}\).  The result JSON stores every directed core
moment through \(J_4\) and every transition moment through \(J_{11}\), so
the displayed coefficients can be independently reassembled from the
certificate.

## 4. Horizon and buffer audit

The pinned periodic-orbit validation gives

\[
16.5403877931809337427<T_*<16.5403878031809337428.
\]

At \(\delta_*=1/\sqrt5\), directed multiplication gives

\[
 7.39708629595206<\Theta_*=\delta_*T_*<7.39708630042420.
\tag{19}
\]

The lower endpoint in (19) exceeds both plant fold delays \(4\) and \(5\),
so the complete declared fold-time horizon is
\(\Theta_{\max}=\max\{4,5,\Theta_*\}=\Theta_*\).  Consequently the numerical
buffer choice satisfies

\[
 B-(2\Theta_*+2)>1.20582739915160>0.
\tag{20}
\]

Along \(\gamma_0\), the parameter \(s\) is exactly the \(q_0\)-flow time.
Starting from the retained singular segment \([-5,5]\), every continuous
depth-two backward delay chain therefore lies in the interval whose radius is
\(5+2\Theta_*\).  Directed arithmetic gives

\[
 19.79417259190412<5+2\Theta_*<19.79417260084840<20.
\]

Thus the plateau \(|s|\le20\) covers the complete pinned **singular**
depth-two hull with margin greater than \(0.20582739915160\).  Equation (20)
also leaves the declared unit-width joining interval and unit-width zero-tail
interval before \(R=22\).  These statements do not validate the deformed
positive-\(\varrho\) flow hull; that enclosure remains part of the nonlinear
graph/preparation gate.

## 5. Exact promotion condition

Suppose a later construction provides a single jointly \(C^1\) frozen
family \(Q^{\rm pr}_{\varrho,S,\mathcal P}\), constructs the corresponding
one-sided traces as a jointly \(C^1\) family in \((\varrho,\nu)\), and
proves that their derivative is the unique solution of (5)--(7).  Assume
also that

\[
 Q^{\rm pr}_{0,S,\mathcal P}=q_0,
 \qquad
 \left.\partial_\varrho
 Q^{\rm pr}_{\varrho,S,\mathcal P}(\gamma_0(s);\nu,0)
 \right|_{\varrho=0}=f_\chi(s;\nu),
\tag{21}
\]

and the two tail levels and phase are fixed as in (6)--(7).  Then the
one-sided Green theorem promotes (9) to

\[
 \partial_\varrho D_{S,\mathcal P}(0,\nu,0)
 =A_\chi\nu+B_\chi,
\tag{22}
\]

Equation (16) then supplies the scalar parameter-transversality ingredient
for an implicit-function continuation.  It does not supply the nonlinear
trace-BVP inverse, joint regularity, or a positive-\(\varrho\) remainder
bound; those hypotheses must be proved independently.  Equation (21) has
not yet been proved for the same RFDE graph preparation.

The current claim ledger is therefore:

| Statement | Status |
|---|---|
| One-sided linear BVP, \(M_\chi\) Green row, and affine zero | proved |
| Exact cutoff algebra, positivity, and directed \(A_\chi,B_\chi,\nu_{0,\chi}\) | proved |
| Period-horizon interval and scalar buffer inequality | proved |
| Plateau coverage of the complete singular depth-two hull | proved |
| Identification \(M_\chi=\partial_\varrho D_{S,\mathcal P}(0,\cdot,0)\) | conditional on (21) and the trace family |
| Complete \(\chi_{\rm graph}\), positive-amplitude flow-hull enclosure, and normal extension | open |
| Realisation (21) by one frozen RFDE graph preparation | open |
| Nonlinear prepared traces and positive-\(\varrho\) root continuation | open |
| Fixed-\(\varepsilon\) complete-history canard root | open |
| General-network Fredholm lift | open |
| Biological pulse onset-to-output control chain | open |

## 6. Reproduction

From the repository root run

```sh
PYTHONPATH=src /usr/bin/python3 experiments/fixed_window_prepared_gap_seed.py
PYTHONPATH=build/testdeps:src /usr/bin/python3 -m pytest -q \
  tests/test_fixed_window_prepared_gap_seed.py
```

The generator pins the Green/phase theorem, the periodic horizon result, and
the sliding-window bridge.  It also checks that the parent bridge still marks
the complete graph preparation and actual fixed-window row as open.  Thus the
new first-jet certificate cannot silently promote itself into a nonlinear
fixed-epsilon canard theorem.
