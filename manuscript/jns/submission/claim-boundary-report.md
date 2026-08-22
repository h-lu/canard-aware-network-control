# Claim-boundary report

This report records the scope used for the JNS submission and is not part of
the manuscript.

## Proved in the manuscript

- Exact algebra and anisotropic fold scaling for the stated two-module,
  two-delay FitzHugh--Nagumo RFDE.
- Exact invariance of the total delayed gain and of the complete delay
  measure projected onto the critical fold mode along the parameter
  \(\eta\)-family.
- A preparation-indexed logarithmic special-flow graph with an injective
  complete-history embedding and the rectangular regularity needed by the
  root calculation.
- Canonical one-sided trace existence, uniqueness, moving transition hits,
  and exact lifting of the retained pieces to the original RFDE history
  space.
- A unique local canonical connection root and the uniform displacement law

  \[
  \mu_{c,\mathcal P}(\delta,\eta)-\mu_{c,\mathcal P}(\delta,0)
  =\frac{K(\theta_0-\theta_1)}{4\alpha}\delta^3\eta
   +O(\delta^4|\eta|+\delta^3\eta^2),
  \qquad \alpha=\frac{\sqrt6}{4}.
  \]

The exact finite-\(\delta\) root depends on the frozen admissible
preparation \(\mathcal P\). Uniformity over a class requires a common fixed
logarithmic exponent and common finite preparation bounds.

## Conditional only

Transfer of the canonical coefficient to a separately prescribed physical
outer attracting/repelling selection is conditional on a
parameter-coherent complete-history boundary-jet estimate. The manuscript
states the required estimate and the resulting root-error propagation, but
does not assert that every physical outer Fenichel family satisfies it.

## Not claimed

- A global maximal-canard or spike-onset threshold for arbitrary physical
  outer selections.
- A theorem for general finite networks, arbitrary heterogeneity, moving
  delay support, distributed delays, or graph limits.
- Independent control of frequency, amplitude, and a canard safety
  coordinate.
- A numerical proof or a validated enclosure of the canonical root.
- Novelty of the scalar single-delay van der Pol coefficient already covered
  by Zhang et al. (SIADS, 2026).

## Computational role

Symbolic tests verify exact identities and coefficients used in the proof.
The method-of-steps experiment checks the sign and scale of the predicted
coefficient for a finite-section diagnostic. It is explicitly not used to
identify that diagnostic root with the canonical history root or with a
physical outer maximal canard.
