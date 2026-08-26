# Stage 4T: direct two-period derivative bridge

## Status

**Proved and frozen.** The certificate byte-binds the repaired Stage-4S-A
direct event tube and the Stage-4S-C, Stage-4L, and Stage-4R analytic parents.

The central conclusion is independent of a nonlinear one-period return:

\[
 \boxed{D Q_Y(Y_*)=A^2.}
\]

Here \(Q_Y\) is the direct near-\(2P\) selected map on the physical
phase-zero section of the reduced history space \(Y\), while \(A\) is the
Stage-4L one-period phase-fixed derivative on that same space. This is a
derivative identity, not a nonlinear identity \(Q=P^2\).

The repaired Stage-4S-A certificate distinguishes the full RFDE phase space
\(X\) from \(Y\). They must not be identified: on compatible lifted
histories the full derivative is intertwined with \(A^2\), not literally
equal to it.

## 1. The two maps and their types

Stage 4S-A has an exact projection/lift pair

\[
 \pi:X\to Y,\qquad \mathcal I:Y\to X,\qquad
 \pi\mathcal I=I_Y,
\]

and reduced/full semiflows satisfying

\[
 \Psi_t=\pi\Phi_t\mathcal I.
\]

It parameterizes the reduced affine section by

\[
 j(z)=Y_*+Jz,
 \qquad
 J(x_s,x_u)=x_s+\widehat q x_u,
\]

and constructs the reduced hit

\[
 R_Y(y)=\Psi_{T(y)}(y).
\]

The reduced physical, compatible full, and coordinate returns are different
typed objects:

\[
 Q_Y=R_Y|_{j(D)},
 \qquad
 Q_X(\mathcal I(y))=\mathcal I(Q_Y(y)),
 \qquad
 Q_{\rm coord}=\chi\circ R_Y\circ j.
\]

The terminal chart satisfies

\[
 D\chi(Y_*)=J^{-1}.
\]

Consequently the correctly typed fixed-point statements are

\[
 Q_Y(Y_*)=Y_*,
 \qquad
 Q_X(\mathcal I(Y_*))=\mathcal I(Y_*),
 \qquad
 Q_{\rm coord}(0)=0.
\]

Writing \(DQ_X=A^2\) is ill typed because \(DQ_X\) acts on full two-component
histories whereas \(A^2\) acts on reduced histories. Likewise, the coordinate
derivative is conjugate to \(A^2\); it is not literally the same operator
until the coordinate space is identified with the reduced physical tangent
section through \(J\).

## 2. Exact center event

Stage 4S-A proves at the exact phase-zero reduced periodic history that

\[
 T(Y_*)=2P,
 \qquad
 \Psi_{2P}(Y_*)=Y_*,
 \qquad
 \Phi_{2P}(\mathcal I(Y_*))=\mathcal I(Y_*).
\]

The selected zero is unique in the fixed near-\(2P\) window. No statement
about the first positive return, the second positive-oriented hit, or any
other event ordinal is used here.

It follows immediately that

\[
 Q_Y(Y_*)=Y_*,
 \qquad
 Q_X(\mathcal I(Y_*))=\mathcal I(Y_*),
 \qquad
 Q_{\rm coord}(0)=0.
\]

## 3. Direct selected-event derivative

Let

\[
 \ell=Dg=\ell_0,
 \qquad
 v=\dot Y_*(0),
 \qquad
 a=\ell(v)\ne0,
\]

and let

\[
 U_Y(t,s)=D_y\Psi_{t-s}(Y_*(s))
\]

be the reduced variational evolution along the exact periodic orbit. Define
the event projection

\[
 \Pi=I-v\frac{\ell}{a}.
\]

The implicit event equation

\[
 g_Y(\Psi_{T(y)}(y))=0
\]

gives at \(y=Y_*\)

\[
 DT(Y_*)h
 =-\frac{\ell(U_Y(2P,0)h)}{a}.
\]

Substitution in the complete-history hit derivative yields

\[
 DQ_Y(Y_*)
 =\Pi U_Y(2P,0)|_{\Sigma_0},
 \qquad
 \Sigma_0=\ker\ell.
\tag{3.1}
\]

This calculation depends only on the direct event branch through \(2P\).
It neither constructs nor invokes a nonlinear one-period map.

## 4. Periodic cocycle and the missing middle projection

Put

\[
 M=U_Y(P,0).
\]

Autonomy, periodicity, and the forward variational cocycle give

\[
 U_Y(2P,P)=U_Y(P,0)=M,
 \qquad
 U_Y(2P,0)=M^2.
\tag{4.1}
\]

Differentiating the time-shifted periodic orbit gives the phase-tangent
identity

\[
 Mv=v.
\tag{4.2}
\]

The orbit point, tangent, affine event differential, and event speed repeat
after every period, so

\[
 \Pi_P=\Pi_{2P}=\Pi.
\tag{4.3}
\]

Stage 4L defines

\[
 A=\Pi M|_{\Sigma_0}.
\]

For \(h\in\Sigma_0\),

\[
\begin{aligned}
 A^2h
 &=\Pi M\Pi Mh\\
 &=\Pi M^2h-\Pi M(I-\Pi)Mh.
\end{aligned}
\]

But

\[
 (I-\Pi)y=v\frac{\ell(y)}a,
 \qquad
 \Pi Mv=\Pi v=0.
\]

Hence the last term vanishes exactly and

\[
 A^2h=\Pi M^2h.
\tag{4.4}
\]

Combining (3.1), (4.1), and (4.4) proves

\[
 \boxed{DQ_Y(Y_*)=A^2.}
\tag{4.5}
\]

Only forward RFDE cocycle identities are used; invertibility of the semiflow
is not assumed.

The exact lift/projection factorization further gives the correctly typed
full-space relation

\[
 DQ_X(\mathcal I(Y_*))\,D\mathcal I(Y_*)
 =
 D\mathcal I(Y_*)\,A^2.
\tag{4.6}
\]

Equation (4.6), not \(DQ_X=A^2\), is the full-\(X\) statement.

## 5. Coordinate conjugacy

The chain rule through the initial and terminal section charts gives

\[
 \boxed{
 DQ_{\rm coord}(0)=J^{-1}A^2J.
 }
\tag{5.1}
\]

Thus \(A^2\) and the coordinate derivative are similar and have the same
hyperbolic splitting and spectrum. Stage-4S-C's numerical power rates are
stated in the inherited physical \(Y\)-norm. They transfer unchanged to
coordinates in the pullback norm

\[
 \|z\|_J:=\|Jz\|_Y.
\]

They are not automatically unchanged in an arbitrary product norm on
\(E_s\times\mathbb R\).

## 6. Imported fixed splitting and rates

Stage 4S-C proves for \(B=A^2\) the fixed splitting

\[
 \Sigma_0=E_s\oplus E_u
\]

and the power estimates

\[
 \|(B|_{E_s})^n\|_Y\le0.01^n,
 \qquad K_s=1,
\]

and

\[
 \|((B|_{E_u})^{-1})^n\|_Y
 \le \rho_{u,2}^n,
 \qquad K_u=1,
\]

where

\[
 \rho_{u,2}\le
 0.302183501335053468766049321268313699617093109911449469063818668425607982682870864983343314167041012216402531488839876224555070910009877958313689944253533344086871769103550439695624961741628356.
\]

Equation (4.5) transfers these statements to the derivative of the direct
reduced physical selected map at \(Y_*\). Equation (5.1) transfers the
splitting to \(J^{-1}E_s\oplus J^{-1}E_u\) in coordinates, while (4.6)
records the compatible full-history intertwining.

## 7. Required semantic bindings

The executable certificate must bind all of the following, rather than rely
only on a shared branch label:

1. Stage-4S-A's \(Y_*=\pi(X_*^X)\) and Stage-4L's phase-zero center are the
   same exact reduced RFDE periodic orbit.
2. Stage-4L's \(T\) is the same exact period \(P\) used by the direct center
   event.
3. Stage-4L's \(U\) is \(U_Y=D_y\Psi\) along that orbit in the same reduced
   history space \(Y\); the full \(\Phi\) is connected only through the
   explicit \(\pi,\mathcal I\) factorization.
4. Stage-4S-A has \(Dg=\ell_0\) and
   \(\Sigma_0=\ker\ell_0\), identical to the Stage-4L event projection.
5. The periodic identities (4.1)--(4.3) and the phase identity (4.2) are
   registered explicitly.
6. The reduced physical, compatible full, and coordinate maps are separated,
   with (4.6) and (5.1) as their exact typed relations.

The final repaired Stage-4S-A result is byte-bound before any of these
semantics are consumed.

## 8. Claim boundary

### Proved

- \(T(Y_*)=2P\), \(Q_Y(Y_*)=Y_*\),
  \(Q_X(\mathcal I(Y_*))=\mathcal I(Y_*)\), and \(Q_{\rm coord}(0)=0\).
- \(DQ_Y(Y_*)=A^2\) without constructing a nonlinear one-period return.
- The full-history derivative intertwining (4.6).
- \(DQ_{\rm coord}(0)=J^{-1}A^2J\).
- Transfer of the fixed splitting and Stage-4S-C rates at the center in the
  physical or pullback norm.

### Still false or open

- \(Q=P^2\) as a nonlinear map identity.
- A nonlinear one-period selected map.
- A self-map of the same scaled anisotropic ball, \(\lambda_*=1\), or a
  numerical lower bound for \(\lambda_*\).
- First-return/no-earlier-hit/ordinal semantics.
- Uniform Hessian blocks, a quantitative stable graph, or the Stage-4R
  periodic-orbit stable-set-germ hypotheses.
- Pulse crossing, onset, biological control, routing, capture, or safety.
