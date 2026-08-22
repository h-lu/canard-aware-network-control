# JNS manuscript

The target venue is the *Journal of Nonlinear Science*.  The paper proves a
preparation-indexed canonical local complete-history connection theorem for
the frozen two-module FitzHugh--Nagumo RFDE.  General finite-network transfer,
three-coordinate control, and an unconditional physical outer maximal-canard
claim are outside the manuscript.

Build from this directory with

```sh
make paper
```

The default command expects `tectonic` and `python3` on `PATH`; either may be
overridden, for example `make TECTONIC=/path/to/tectonic paper`.  Install the
paper dependencies from the repository root with
`python3 -m pip install -e '.[paper]'`.  The computed figure is regenerated from
`../../experiments/results/exact_chart_threshold_convergence.json`.
