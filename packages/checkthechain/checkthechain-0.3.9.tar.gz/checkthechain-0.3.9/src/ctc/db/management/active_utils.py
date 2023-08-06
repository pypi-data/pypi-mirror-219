from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from .. import schema_utils

from ctc import spec


def get_active_schemas() -> typing.Mapping[spec.SchemaName, bool]:
    """return specification of which subset of incoming data to store in db"""
    return {
        # 'block_gas_stats': False,
        'block_timestamps': True,
        'block_gas': True,
        'blocks': True,
        'contract_abis': True,
        'contract_creation_blocks': True,
        'dex_pools': True,
        'erc20_metadata': True,
        'events': True,
        'transactions': True,
        # 'erc20_state': False,
        '4byte': True,
        'chainlink': True,
        'schema_versions': True,
    }


def get_active_timestamp_schema() -> spec.NetworkSchemaName | None:
    active_schemas = get_active_schemas()
    if active_schemas['block_timestamps']:
        return 'block_timestamps'
    elif active_schemas['blocks']:
        return 'blocks'
    else:
        return None
