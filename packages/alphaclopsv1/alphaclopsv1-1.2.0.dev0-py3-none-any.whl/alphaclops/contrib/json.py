# pylint: disable=wrong-or-nonexistent-copyright-notice
"""Functions for JSON serialization and de-serialization for classes in Contrib.
"""

from alphaclops.protocols.json_serialization import DEFAULT_RESOLVERS


def contrib_class_resolver(alphaclops_type: str):
    """Extend alphaclops's JSON API with resolvers for alphaclops contrib classes."""
    from alphaclops.contrib.acquaintance import SwapPermutationGate
    from alphaclops.contrib.bayesian_network import BayesianNetworkGate
    from alphaclops.contrib.quantum_volume import QuantumVolumeResult

    classes = [BayesianNetworkGate, QuantumVolumeResult, SwapPermutationGate]
    d = {cls.__name__: cls for cls in classes}
    return d.get(alphaclops_type, None)


DEFAULT_CONTRIB_RESOLVERS = [contrib_class_resolver] + DEFAULT_RESOLVERS
