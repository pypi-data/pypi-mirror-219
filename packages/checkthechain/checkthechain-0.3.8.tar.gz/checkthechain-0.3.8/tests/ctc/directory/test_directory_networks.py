
import pytest

from ctc import evm
from ctc.spec.typedefs import network_types
from ctc.config import config_defaults


@pytest.mark.parametrize(
    'test',
    [
        [1, 'ethereum'],
        ['ethereum', 'ethereum'],
        [3, 'ropsten'],
    ],
)
def test_get_network_name(test):
    network_reference, network_name = test

    actual_network_name = evm.get_network_name(network=network_reference)
    assert actual_network_name == network_name


@pytest.mark.parametrize(
    'test',
    [
        [1, 1],
        ['ethereum', 1],
        ['ropsten', 3],
    ],
)
def test_get_chain_id(test):
    network_reference, network_chain_id = test

    actual_network_chain_id = evm.get_network_chain_id(
        network=network_reference
    )
    assert actual_network_chain_id == network_chain_id


def test_get_network_metadata():
    metadata = evm.get_network_metadata(network=1)
    assert metadata['name'] == 'ethereum'
    assert metadata['chain_id'] == 1
    assert metadata['block_explorer'] == 'etherscan.io'


def test_get_networks():
    config_defaults.get_default_networks_metadata()

