#  Copyright (c) 2022 zfit

from ._loss.binnedloss import (
    ExtendedBinnedNLL,
    BinnedNLL,
    ExtendedBinnedChi2,
    BinnedChi2,
)
from .core.loss import BaseLoss, ExtendedUnbinnedNLL, SimpleLoss, UnbinnedNLL

__all__ = [
    "ExtendedUnbinnedNLL",
    "UnbinnedNLL",
    "BinnedNLL",
    "ExtendedBinnedNLL",
    "BaseLoss",
    "SimpleLoss",
    "ExtendedBinnedNLL",
    "BinnedChi2",
    "ExtendedBinnedChi2",
]

from .util.warnings import warn_experimental_feature


@warn_experimental_feature
def experimental_enable_loss_penalty(enable=True):
    """EXPERIMENTAL! Enable a loss penalty if the loss is NaN, which can push back the minimizer.

    Won't work with every minimizer

    Args:
        enable: If True, enable this feature.
    """
    from .util.exception import BreakingAPIChangeError

    raise BreakingAPIChangeError(
        "This has been removed and is now activated by default."
        " Remove this function call."
        "Many thanks for the feedbacks received."
    )
