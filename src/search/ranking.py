"""Compatibility re-export shim for the live ranking module.

The real implementation lives in :mod:`services.search.ranking`, which is what
the search runtime (services/search/core.py) imports. This module used to hold a
parallel copy; it now re-exports so the two cannot drift out of sync again.
"""

from services.search.ranking import (  # noqa: F401
    _AGE_FORMATS,
<<<<<<< HEAD
=======
    _SPORTS_HINT_RE,
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483
    _utcnow_naive,
    rank_search_results,
    recency_score,
)
