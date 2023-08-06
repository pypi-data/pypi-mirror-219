"""
sets up sparse integration over a Gaussian
"""
from pathlib import Path

import numpy as np

from bs_python_utils.bsnputils import TwoArrays
from bs_python_utils.bsutils import bs_error_abort


def setup_sparse_gaussian(
    ndims: int, iprec: int, GHsparsedir: str | None = None
) -> TwoArrays:
    """
    get nodes and weights for sparse integration Ef(X) with X = N(0,1) in `ndims` dimensions

    usage: nodes, weights = setup_sparse_gaussian(mdims, iprec); intf = f(nodes) @ weights

    Args:
        ndims: number of dimensions (1 to 5)
        iprec: precision (must be 9, 13, or 17)

    Returns:
        a pair of  arrays `nodes` and `weights`;
        `nodes` has `ndims`-1 columns and `weights` is a vector
    """
    GHdir = (
        Path.home() / "Dropbox" / "GHsparseGrids"
        if GHsparsedir is None
        else Path(GHsparsedir)
    )
    if iprec not in [9, 13, 17]:
        bs_error_abort(
            f"We only do sparse integration with precision 9, 13, or 17, not {iprec}"
        )

    if ndims in [1, 2, 3, 4, 5]:
        grid = np.loadtxt(GHdir / f"GHsparseGrid{ndims}prec{iprec}.txt")
        weights = grid[:, 0]
        nodes = grid[:, 1:]
        return nodes, weights
    else:
        bs_error_abort(
            f"We only do sparse integration in one to five dimensions, not {ndims}"
        )
        return np.zeros(1), np.zeros(1)  # for mypy
