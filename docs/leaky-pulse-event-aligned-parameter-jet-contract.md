# Stage 5: event-aligned parameter jets for the physical pulse

Status: **source-bound proof architecture only.  No numerical jet tube,
event, complete-history family, stable-sheet intersection, onset, or routing
claim is validated here.**

The wide-family pilot shows that independent state shards can be made small,
but its zero-centered first and second variation majorants stay enormous even
at zero shard width.  Stage 5 therefore preserves parameter correlation
directly.

## 1. Factorial parameter jets

On a shard write \(J=J_0+\delta\), \(|\delta|\le h\), and

\[
 z(t,J_0+\delta)=
 \sum_{k=0}^{4}\frac{\delta^k}{k!}z_k(t)+R_5(t,\delta),
 \qquad z_k=\partial_J^kz(t,J_0).
\]

Let \(L_t\) be the full RFDE linearization along \(z_0\), retaining the
current, \(4\sqrt5\)-delayed, and \(5\sqrt5\)-delayed slots separately.  Let
\(B_m=D^mF(z_0)\).  The vector field is cubic in those slots, so
\(B_m=0\) for \(m\ge4\).  The coefficient equations are

\[
\begin{aligned}
 \dot z_0&=F(z_0)+J_0\chi_{[0,1)}e_v,\\
 \dot z_1&=L_tz_1+\chi_{[0,1)}e_v,\\
 \dot z_2&=L_tz_2+B_2[z_1,z_1],\\
 \dot z_3&=L_tz_3+3B_2[z_1,z_2]+B_3[z_1,z_1,z_1],\\
 \dot z_4&=L_tz_4+4B_2[z_1,z_3]+3B_2[z_2,z_2]
              +6B_3[z_1,z_1,z_2].
\end{aligned}
\]

The initial quiet history is independent of \(J\), so \(z_k=0\) initially
for \(k\ge1\).  Release at \(t=1\) and both delay-translation families must
remain exact cell boundaries for every coefficient.

After substituting the degree-four polynomial into the cubic RFDE, all
parameter coefficients of degree at least five and all time-Taylor residuals
form \(\rho_5\).  A directed cellwise radius must close an inequality of the
form

\[
 D^+\|R_5\|_P\le
 \mu_P\|R_5(t)\|_P+b_4\|R_5(t-4\sqrt5)\|_P
 +b_5\|R_5(t-5\sqrt5)\|_P+\rho_5+N_2(r).
\]

This is the highest-order remainder tube; the lower jets are not replaced by
independent symmetric norm balls.

## 2. The implicit Route-C event jet

Set

\[
 g(t,J)=h_C(z_t(J))=v(t,J)-V_{\rm true}(0).
\]

For a center crossing \(g(t_0,J_0)=0\), write

\[
 T(\delta)=t_0+\sum_{k=1}^{4}\frac{\tau_k}{k!}\delta^k
             +R_{\tau,5}(\delta).
\]

The first two coefficients are

\[
 \tau_1=-\frac{g_J}{g_t},\qquad
 \tau_2=-\frac{g_{JJ}+2g_{tJ}\tau_1+g_{tt}\tau_1^2}{g_t}.
\]

At every order \(k=3,4\), factorial series composition of
\(g(T(\delta),J_0+\delta)\) produces one linear term \(g_t\tau_k\); moving
all other order-\(k\) terms to the other side defines \(\tau_k\).  This
recurrence is less error-prone than hand-expanding the fourth derivative and
is directly executable with truncated power-series arithmetic.

The event proof additionally needs directed endpoint signs, a uniform
interval for \(g_t\) excluding zero, and an interval-Newton-in-time enclosure
of \(R_{\tau,5}\).  Orbit speed alone cannot fill any of these pulse-family
fields.

## 3. Pulling the complete history to one event graph

The correct section object is

\[
 \mathcal Y(\delta)=
 \left(\theta\mapsto v(T(\delta)+\theta,J_0+\delta),
       w(T(\delta),J_0+\delta)\right),
 \quad \theta\in[-5\sqrt5,0].
\]

For the voltage-history component,

\[
 \mathcal Y_1=z_1+\tau_1\dot z_0,
\]

and

\[
 \mathcal Y_2=z_2+2\tau_1\dot z_1+\tau_1^2\ddot z_0+\tau_2\dot z_0,
\]

evaluated at \(t_0+\theta\); the current recovery component uses the same
composition at \(\theta=0\).  Orders three and four follow from the same
factorial Faà-di-Bruno composition.  Every \(\theta\)-cell must be bounded
continuously by Bernstein arithmetic.  A sampled history mesh is not a
substitute.

## 4. Stable gap and interval Newton

After a validated RFDE Riesz splitting and stable graph are available, write
the common-event history as \(y=(y_s,y_u)\) and define

\[
 H(J)=f_u y_u(J)-h_s(y_s(J)).
\]

Its derivative includes the event-time terms already incorporated in
\(\mathcal Y_1\):

\[
 H'(J)=f_uD_Jy_u-Dh_s(y_s)D_Jy_s.
\]

For \(I=[0.30105,0.30120]\) and \(m=\operatorname{mid}I\), the final local
root gate is

\[
 N(I)=m-\frac{H(m)}{H'(I)}\subset\operatorname{int}I,
 \qquad 0\notin H'(I).
\]

All event histories must first lie in the validated stable-graph chart, and
the endpoint \(H\)-intervals must have the declared opposite signs.  If
these directed gates close, they prove one local stable-sheet intersection.
They still do not identify the basins on its two sides.

## 5. Current ledger

Every strict numerical field is `null`: shard choice, coefficient errors,
order-five radius, event bracket and speed, \(\tau_1,\ldots,\tau_4\), event
remainder, complete-history radius, Riesz covector and projection, stable
graph bounds, endpoint stable gaps, derivative interval, and Newton image.
Every corresponding validation flag is `false`.

In particular, the binary64 finite-section endpoint signs remain forbidden
as proof inputs.  The contract records equations and gates, not their
premises.

Generate or audit with

```bash
PYTHONPATH=src /usr/bin/python3 \
  experiments/leaky_pulse_event_aligned_parameter_jet_contract.py
PYTHONPATH=src /usr/bin/python3 \
  experiments/leaky_pulse_event_aligned_parameter_jet_contract.py --check
```
