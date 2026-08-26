# Outer continuous kernel: Stage-3D primitive reduction

Status: **the 21 delay-word integrals have been collapsed exactly to
one-dimensional primitives, and the continuous linear phase-projection error
is now proved; the exact-orbit signed density errors \(E_v,E_w\) and the
\(C^0\) return contraction remain open.**

The executable source is
[the Stage-3D module](../src/canard_control/leaky_outer_delay_word_stage3d_primitives.py),
the generator is
[the experiment](../experiments/leaky_outer_delay_word_stage3d_primitives.py),
and the tracked output is
[the result](../experiments/results/leaky_outer_delay_word_stage3d_primitives.json).

## 1. Duffy integrals become one-dimensional primitives

Let \(F'=AF\), \(F(0)=I\), and \(G=F^{-1}\). Define

\[
 C_j(r)=G(r)B_j(r)F(r-\tau_j),
 \qquad H_j'(r)=C_j(r),
\]

with \(H_j=0\) before \(r=\tau_j\). For the two-letter words define

\[
 L_{jk}'(r)=C_j(r)H_k(r-\tau_j),
\]

with \(L_{jk}=0\) before \(r=\tau_j+\tau_k\). Then

\[
 R_j(t,s)=F(t)\{H_j(t)-H_j(s+\tau_j)\}G(s),
\tag{1.1}
\]

and, writing \(a=s+\tau_j+\tau_k\),

\[
 R_{jk}(t,s)=F(t)\{L_{jk}(t)-L_{jk}(a)
 -[H_j(t)-H_j(a)]H_k(s+\tau_k)\}G(s).
\tag{1.2}
\]

Equation (1.2) is the exact antiderivative of the ordered Duffy
two-simplex. Because Stage-3C proved that every longer word vanishes, the
whole resolvent now requires only
\(F,G,H_0,H_1,L_{00},L_{01},L_{10},L_{11}\).
There is no remaining multidimensional path quadrature.

The implementation sums all seven resolvent words and both history-injection
branches, performs the phase subtraction, and only then applies absolute
quadrature. Thus the decisive Stage-2 cancellation is retained.

## 2. Continuous center-kernel pilot

Two independent DOP853 ladders rebuild the primitive functions and evaluate
the actual continuous history density. The initial history is never sampled
or interpolated: the quadrature is over the density in the Riesz
representation. The fine guide returns a maximum voltage row near the
Stage-2 value \(0.127\) and a recovery row near \(0.00277\). Its \(FG-I\)
consistency defect is also recorded.

These are source-bound binary64 diagnostics. Step refinement and history
quadrature agreement do not bound the exact RFDE kernel and are not used as
\(E_v\) or \(E_w\).

## 3. A proved continuous phase-projection bound

The phase projection itself does not require the resolvent kernel. On

\[
 Y=C([-\tau_1,0],\mathbb R)\times\mathbb R,
\]

its linear norm satisfies

\[
 \|I-q\otimes\ell\|
 \le 1+\frac{\max\{\|q_v\|_\infty,\|q_w\|_\infty\}}{q_v(0)},
 \qquad \ell(h)=\frac{h_v(0)}{q_v(0)}.
\tag{3.1}
\]

For the exact orbit, \(q=f(X)\). The source compares this vector field with
the stored Fourier derivative using the validated periodic residual, the
\(10^{-8}\) Wiener orbit ball, and a mean-value bound for the RFDE field.
This proves a positive exact event speed, a continuous projection norm below
the ambient-entry ceiling, and an explicit \(E_{\rm phase}\). The resulting
linear projection of the already validated pulse history lies strictly
inside the \(10^{-4}\) section radius.

This is a linear tangent projection result. It does not prove a nonlinear
phase chart on the ambient tube and is not promoted to exact nonlinear pulse
capture.

## 4. Directed frontier and remaining obstruction

A 512-cell directed coefficient cover recomputes the absolute
logarithmic-norm wrapper. Its full-period growth is enormous because it takes
absolute values before the word and phase cancellation. The certificate
marks this bound unusable and never inserts it as a transfer error.

The next directed calculation is sharply delimited:

1. represent \(F,G,H,L\) on 256, 512 and 1024 phase cells by degree
   \(12,16,20,24\) Taylor/Chebyshev polynomials;
2. use a relative residual for \(F\), so the large condition number is not
   paid as an absolute Gronwall factor;
3. retain
   \(F(t)\{\sum_\omega I_\omega(t,s)\}G(s)\), the two injections and the
   phase term as one tensor polynomial;
4. convert the signed polynomial to Bernstein form before integrating its
   absolute value.

At present that relative-residual polynomial enclosure is the first missing
object. Therefore

\[
 E_v=E_w=\varnothing,
\]

the linear return gate is not evaluated, and arbitrary-\(C^0\) contraction,
nonlinear outer attraction, capture and physical onset all remain false.
