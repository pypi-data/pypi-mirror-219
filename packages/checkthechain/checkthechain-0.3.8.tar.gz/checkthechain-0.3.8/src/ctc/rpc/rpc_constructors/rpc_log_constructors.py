from __future__ import annotations

import typing

from ctc import evm
from ctc import spec
from .. import rpc_request


def construct_eth_new_filter(
    address: spec.BinaryData | None = None,
    topics: typing.Sequence[spec.BinaryData | None] | None = None,
    *,
    start_block: spec.BlockNumberReference | None = None,
    end_block: spec.BlockNumberReference | None = None,
) -> spec.RpcSingularRequest:

    if start_block is not None:
        start_block = evm.encode_block_number(start_block)
    if end_block is not None:
        end_block = evm.encode_block_number(end_block)

    parameters = {
        'address': address,
        'topics': topics,
        'fromBlock': start_block,
        'toBlock': end_block,
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}

    return rpc_request.create('eth_newFilter', [parameters])


def construct_eth_new_block_filter() -> spec.RpcSingularRequest:
    return rpc_request.create('eth_newBlockFilter', [])


def construct_eth_new_pending_transaction_filter() -> spec.RpcSingularRequest:
    return rpc_request.create('eth_newPendingTransactionFilter', [])


def construct_eth_uninstall_filter(
    filter_id: spec.GenericBinaryData,
) -> spec.RpcSingularRequest:
    return rpc_request.create('eth_uninstallFilter', [filter_id])


def construct_eth_get_filter_changes(
    filter_id: spec.GenericBinaryData,
) -> spec.RpcSingularRequest:
    return rpc_request.create('eth_getFilterChanges', [filter_id])


def construct_eth_get_filter_logs(
    filter_id: spec.GenericBinaryData,
) -> spec.RpcSingularRequest:
    return rpc_request.create('eth_getFilterLogs', [filter_id])


def construct_eth_get_logs(
    address: spec.BinaryData | None = None,
    topics: typing.Sequence[spec.BinaryData | None] | None = None,
    *,
    start_block: spec.BlockNumberReference | None = None,
    end_block: spec.BlockNumberReference | None = None,
    block_hash: spec.BinaryData | None = None,
) -> spec.RpcSingularRequest:

    if start_block is not None:
        start_block = evm.encode_block_number(start_block)
    if end_block is not None:
        end_block = evm.encode_block_number(end_block)

    parameters = {
        'address': address,
        'topics': topics,
        'fromBlock': start_block,
        'toBlock': end_block,
        'blockHash': block_hash,
    }
    parameters = {k: v for k, v in parameters.items() if v is not None}

    return rpc_request.create('eth_getLogs', [parameters])

