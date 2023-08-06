from ..conftest import linux_run_only

import pathlib
import os

import pytest
from pytest_lazyfixture import lazy_fixture
import chimerapy.engine as cpe

cpe.debug()

# Constant
TEST_DIR = pathlib.Path(os.path.abspath(__file__)).parent.parent
TEST_PACKAGE_DIR = TEST_DIR / "mock"


@pytest.fixture
def local_node_graph(gen_node):
    graph = cpe.Graph()
    graph.add_node(gen_node)
    return graph


@pytest.fixture
def packaged_node_graph():
    # Installing test package (in case this test package hasn't been done before)
    # Reference: https://stackoverflow.com/a/55188705/13231446
    try:
        import test_package as tp
    except ImportError:
        import pip._internal as pip

        pip.main(["install", str(TEST_PACKAGE_DIR)])
    finally:
        import test_package as tp

    node = tp.TestNode(name="test")
    graph = cpe.Graph()
    graph.add_node(node)
    return graph


@linux_run_only
@pytest.mark.parametrize(
    "_worker, config_graph",
    [
        (lazy_fixture("worker"), lazy_fixture("local_node_graph")),
        (lazy_fixture("worker"), lazy_fixture("packaged_node_graph")),
        pytest.param(
            lazy_fixture("dockered_worker"),
            lazy_fixture("local_node_graph"),
            marks=pytest.mark.skip,
        ),
        pytest.param(
            lazy_fixture("dockered_worker"),
            lazy_fixture("packaged_node_graph"),
            marks=pytest.mark.skip,
        ),
    ],
)
def test_sending_package(manager, _worker, config_graph):
    _worker.connect(host=manager.host, port=manager.port)

    assert manager.commit_graph(
        graph=config_graph,
        mapping={_worker.id: list(config_graph.G.nodes())},
        send_packages=[
            {"name": "test_package", "path": TEST_PACKAGE_DIR / "test_package"}
        ],
    ).result(timeout=30)

    for node_id in config_graph.G.nodes():
        assert manager.workers[_worker.id].nodes[node_id].fsm != "NULL"
