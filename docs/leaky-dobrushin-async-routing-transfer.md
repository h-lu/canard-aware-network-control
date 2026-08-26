# Conditional asynchronous routing and threshold transfer

Status: **the composition implication and all radius/shift formulas below are
proved.  No scalar forced-routing tube, target-lift margin, concrete
asynchronous radius, perturbed pulse threshold, or two-sided network basin
routing has been validated.**

This result closes a logical gap, not the biological theorem.  Exponential
decay of node diameter does not alone keep the collective state in the
voltage strip or put the full network in a target basin.  The theorem states
the exact additional scalar and product-basin constants that make that
promotion valid.

## 1. Proved network input

For every admitted finite balanced Dobrushin network, while all retained node
voltages remain in the declared strip, the parent certificates give

\[
 M(t)\le M_0e^{-(t-t_0)/10},
 \qquad
 \|R_{\rm coll}\|_{L^1(t_0,\infty)}
 \le C_RM_0^2,
 \qquad C_R=\frac{703}{40}+\frac{27\sqrt5}{800}
 <\frac{56483}{3200}.                            \tag{1.1}
\]

The second term in \(C_R\) is the exact residence correction for the two
delayed initial-history pieces.  The executable inequalities below use the
strict rational upper \(56483/3200\).

The \(\pi\)-mean solves the scalar leaky RFDE with the single additive
voltage forcing \(R_{\rm coll}\).  Moreover,

\[
 |v_i-\bar v|\le\operatorname{osc}v\le M(t).     \tag{1.2}
\]

Neither (1.1) nor (1.2) assumes a Euclidean norm equivalence or introduces a
factor involving \(N\) or \(\pi_{\min}^{-1}\).

## 2. Scalar robust-route and product-lift hypotheses

The still-missing scalar theorem must provide positive constants
\(\eta_{\rm route}\), \(d_{\rm strip}\), and \(L_0\) with the following
meaning.  For every admitted scalar entrance history at distance
\(\delta_{\rm mean}\) from the physical pulse entrance and every additive
voltage forcing \(e\),

\[
 L_0\delta_{\rm mean}+\|e\|_{L^1}<\eta_{\rm route}       \tag{2.1}
\]

must imply the declared signed scalar route, while the scalar voltage stays
at least \(d_{\rm strip}\) inside the network voltage strip.

A full-network basin statement needs one more theorem, represented by a
positive product-lift margin \(d_{\rm lift}\): a routed scalar target history
with transverse diameter below \(d_{\rm lift}\) must belong to the
corresponding full-network target basin.  A scalar basin alone does not prove
this implication.

Put

\[
 M_0=\sup_{t_0-r\le s\le t_0}M(s),
 \qquad
 R_0=\max\{\delta_{\rm mean},M_0\}.                      \tag{2.2}
\]

Then the exact sufficient budget is

\[
 R_0<\min\{d_{\rm strip},d_{\rm lift}\},
 \qquad
 L_0R_0+\frac{56483}{3200}R_0^2<\eta_{\rm route}.        \tag{2.3}
\]

When the initial mean is exactly the scalar pulse entrance, the simpler
strict squared-radius formula is

\[
 M_0^2<
 \min\left\{
 d_{\rm strip}^2,
 d_{\rm lift}^2,
 \frac{3200}{56483}\eta_{\rm route}
 \right\}.                                               \tag{2.4}
\]

### Proof of the strip bootstrap

Suppose a first nodewise strip exit exists.  Up to that time, the parent
theorems apply.  Extend the resulting \(R_{\rm coll}\) by zero after the
hypothetical exit; its full \(L^1\) norm still satisfies (1.1), so it is an
accepted forcing in (2.1).  The scalar
robust-route hypothesis keeps the mean at least \(d_{\rm strip}\) inside the
strip.  Equations (1.2) and (2.3) keep every node strictly closer than that
margin to the mean, contradicting first exit.  Hence the strip hypothesis
bootstraps through the routed interval.  The same decay estimate keeps the
entire retained transverse history diameter at most \(M_0\).  At target
entry, (2.3) and the separate product-lift theorem therefore give the
full-network basin conclusion.

This is why every inequality is strict.  It is also why
\(d_{\rm lift}\) cannot be omitted when the conclusion concerns the full
network rather than only its mean.

## 3. Perturbed threshold lemma

Assume the scalar signed gap \(H\) and the network-perturbed gap
\(\widetilde H\) are \(C^1\), and

\[
 H(J_c)=0,
 \qquad
 H'(J)\ge m_J>0
 \quad\hbox{on }[J_c-r_J,J_c+r_J].                      \tag{3.1}
\]

For a fixed admitted network perturbation, write its corresponding gap as
\(\widetilde H\).  A future scalar response certificate must supply
nonnegative constants \(L_{H0},L_{H1},L_{HJ0},L_{HJ1}\) such that

\[
 \begin{aligned}
 \|\widetilde H-H\|_\infty
 &\le \epsilon_H(R_0)
 =L_{H0}R_0+L_{H1}\frac{56483}{3200}R_0^2,\\
 \|\widetilde H'-H'\|_\infty
 &\le \delta_{HJ}(R_0)
 =L_{HJ0}R_0+L_{HJ1}\frac{56483}{3200}R_0^2.
 \end{aligned}                                          \tag{3.2}
\]

If

\[
 \epsilon_H(R_0)<m_Jr_J,
 \qquad
 \delta_{HJ}(R_0)<m_J,                                  \tag{3.3}
\]

then \(\widetilde H\) has opposite signs at the two endpoints and has
strictly positive derivative throughout the interval.  It therefore has
exactly one root \(J_{c,N}\) in this interval, and the mean-value theorem gives

\[
 |J_{c,N}-J_c|
 \le\frac{\epsilon_H(R_0)}{m_J}.                         \tag{3.4}
\]

Consequently, for \(J\in[J_c-r_J,J_c+r_J]\), the scalar signed side is robust
whenever

\[
 |J-J_c|>\frac{\epsilon_H(R_0)}{m_J}.                    \tag{3.5}
\]

Equations (3.1)--(3.5) are an elementary but exact monotone-root
perturbation theorem on the displayed local interval.  They assert neither
the absence of roots outside that interval nor global threshold uniqueness.
Calling \(J_{c,N}\) a *biological onset* additionally
requires the two-sided routing and product-basin hypotheses of Section 2.

## 4. Exact boundary of the result

The formulas become dimension- and topology-uniform once the scalar route,
gap-response, and product-lift constants are common.  At present none of the
following numerical fields exists:

- \(\eta_{\rm route}\), \(d_{\rm strip}\), or \(d_{\rm lift}\);
- \(m_J\) or the four gap-response constants in (3.2);
- a positive value of (2.3) or (2.4);
- a threshold displacement bound in (3.4).

Therefore this artifact does **not** prove strip invariance for the current
model, an asynchronous basin, an asynchronous \(J_c\), or a biological
safety margin.  It supplies the exact acceptance interface that the scalar
routing and stable-manifold validations must fill.

The source-bound result is generated by
`experiments/leaky_dobrushin_async_routing_transfer.py` and binds the proved
quadratic collective-defect parent by hash.
