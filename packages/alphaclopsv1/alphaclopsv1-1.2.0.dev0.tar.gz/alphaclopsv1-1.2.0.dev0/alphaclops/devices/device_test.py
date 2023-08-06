# pylint: disable=wrong-or-nonexistent-copyright-notice
import networkx as nx
import alphaclops


def test_device_metadata():
    class RawDevice(alphaclops.Device):
        pass

    assert RawDevice().metadata is None


def test_metadata():
    qubits = alphaclops.LineQubit.range(4)
    graph = nx.star_graph(3)
    metadata = alphaclops.DeviceMetadata(qubits, graph)
    assert metadata.qubit_set == frozenset(qubits)
    assert metadata.nx_graph == graph


def test_metadata_json_load_logic():
    qubits = alphaclops.LineQubit.range(4)
    graph = nx.star_graph(3)
    metadata = alphaclops.DeviceMetadata(qubits, graph)
    str_rep = alphaclops.to_json(metadata)
    assert metadata == alphaclops.read_json(json_text=str_rep)


def test_metadata_equality():
    qubits = alphaclops.LineQubit.range(4)
    graph = nx.star_graph(3)
    graph2 = nx.star_graph(3)
    graph.add_edge(1, 2, directed=False)
    graph2.add_edge(1, 2, directed=True)

    eq = alphaclops.testing.EqualsTester()
    eq.add_equality_group(alphaclops.DeviceMetadata(qubits, graph))
    eq.add_equality_group(alphaclops.DeviceMetadata(qubits, graph2))
    eq.add_equality_group(alphaclops.DeviceMetadata(qubits[1:], graph))
