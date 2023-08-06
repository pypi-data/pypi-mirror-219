from __future__ import annotations

import typing

from ctc import spec
from . import rpc_batch_utils


def batch_construct_eth_accounts(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_accounts', **constructor_kwargs
    )


def batch_construct_eth_block_number(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_block_number', **constructor_kwargs
    )


def batch_construct_eth_call(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_call', **constructor_kwargs
    )


def batch_construct_eth_coinbase(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_coinbase', **constructor_kwargs
    )


def batch_construct_eth_compile_lll(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_compile_lll', **constructor_kwargs
    )


def batch_construct_eth_compile_serpent(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_compile_serpent', **constructor_kwargs
    )


def batch_construct_eth_compile_solidity(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_compile_solidity', **constructor_kwargs
    )


def batch_construct_eth_estimate_gas(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_estimate_gas', **constructor_kwargs
    )


def batch_construct_eth_gas_price(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_gas_price', **constructor_kwargs
    )


def batch_construct_eth_get_balance(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_balance', **constructor_kwargs
    )


def batch_construct_eth_get_block_by_hash(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_block_by_hash', **constructor_kwargs
    )


def batch_construct_eth_get_block_by_number(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_block_by_number', **constructor_kwargs
    )


def batch_construct_eth_get_block_transaction_count_by_hash(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_block_transaction_count_by_hash', **constructor_kwargs
    )


def batch_construct_eth_get_block_transaction_count_by_number(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_block_transaction_count_by_number', **constructor_kwargs
    )


def batch_construct_eth_get_code(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_code', **constructor_kwargs
    )


def batch_construct_eth_get_compilers(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_compilers', **constructor_kwargs
    )


def batch_construct_eth_get_filter_changes(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_filter_changes', **constructor_kwargs
    )


def batch_construct_eth_get_filter_logs(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_filter_logs', **constructor_kwargs
    )


def batch_construct_eth_get_logs(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_logs', **constructor_kwargs
    )


def batch_construct_eth_get_storage_at(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_storage_at', **constructor_kwargs
    )


def batch_construct_eth_get_transaction_by_block_hash_and_index(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_transaction_by_block_hash_and_index',
        **constructor_kwargs,
    )


def batch_construct_eth_get_transaction_by_block_number_and_index(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_transaction_by_block_number_and_index',
        **constructor_kwargs,
    )


def batch_construct_eth_get_transaction_by_hash(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_transaction_by_hash', **constructor_kwargs
    )


def batch_construct_eth_get_transaction_count(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_transaction_count', **constructor_kwargs
    )


def batch_construct_eth_get_transaction_receipt(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_transaction_receipt', **constructor_kwargs
    )


def batch_construct_eth_get_uncle_by_block_hash_and_index(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_uncle_by_block_hash_and_index', **constructor_kwargs
    )


def batch_construct_eth_get_uncle_by_block_number_and_index(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_uncle_by_block_number_and_index', **constructor_kwargs
    )


def batch_construct_eth_fee_history(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_fee_history', **constructor_kwargs
    )


def batch_construct_eth_get_uncle_count_by_block_hash(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_uncle_count_by_block_hash', **constructor_kwargs
    )


def batch_construct_eth_get_uncle_count_by_block_number(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_uncle_count_by_block_number', **constructor_kwargs
    )


def batch_construct_eth_get_work(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_get_work', **constructor_kwargs
    )


def batch_construct_eth_hashrate(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_hashrate', **constructor_kwargs
    )


def batch_construct_eth_mining(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_mining', **constructor_kwargs
    )


def batch_construct_eth_new_block_filter(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_new_block_filter', **constructor_kwargs
    )


def batch_construct_eth_new_filter(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_new_filter', **constructor_kwargs
    )


def batch_construct_eth_new_pending_transaction_filter(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_new_pending_transaction_filter', **constructor_kwargs
    )


def batch_construct_eth_protocol_version(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_protocol_version', **constructor_kwargs
    )


def batch_construct_eth_send_raw_transaction(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_send_raw_transaction', **constructor_kwargs
    )


def batch_construct_eth_send_transaction(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_send_transaction', **constructor_kwargs
    )


def batch_construct_eth_sign(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_sign', **constructor_kwargs
    )


def batch_construct_eth_sign_transaction(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_sign_transaction', **constructor_kwargs
    )


def batch_construct_eth_submit_hashrate(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_submit_hashrate', **constructor_kwargs
    )


def batch_construct_eth_submit_work(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_submit_work', **constructor_kwargs
    )


def batch_construct_eth_syncing(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_syncing', **constructor_kwargs
    )


def batch_construct_eth_chain_id(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_chain_id', **constructor_kwargs
    )


def batch_construct_eth_uninstall_filter(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='eth_uninstall_filter', **constructor_kwargs
    )


def batch_construct_net_listening(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='net_listening', **constructor_kwargs
    )


def batch_construct_net_peer_count(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='net_peer_count', **constructor_kwargs
    )


def batch_construct_net_version(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='net_version', **constructor_kwargs
    )


def batch_construct_shh_add_to_group(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='shh_add_to_group', **constructor_kwargs
    )


def batch_construct_shh_get_filter_changes(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='shh_get_filter_changes', **constructor_kwargs
    )


def batch_construct_shh_get_messages(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='shh_get_messages', **constructor_kwargs
    )


def batch_construct_shh_has_identity(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='shh_has_identity', **constructor_kwargs
    )


def batch_construct_shh_new_filter(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='shh_new_filter', **constructor_kwargs
    )


def batch_construct_shh_new_group(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='shh_new_group', **constructor_kwargs
    )


def batch_construct_shh_new_identity(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='shh_new_identity', **constructor_kwargs
    )


def batch_construct_shh_post(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='shh_post', **constructor_kwargs
    )


def batch_construct_shh_uninstall_filter(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='shh_uninstall_filter', **constructor_kwargs
    )


def batch_construct_shh_version(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='shh_version', **constructor_kwargs
    )


def batch_construct_web3_client_version(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='web3_client_version', **constructor_kwargs
    )


def batch_construct_web3_sha3(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='web3_sha3', **constructor_kwargs
    )


def batch_construct_trace_transaction(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='trace_transaction', **constructor_kwargs
    )


def batch_construct_trace_replay_transaction(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='trace_replay_transaction', **constructor_kwargs
    )


def batch_construct_trace_raw_transaction(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='trace_raw_transaction', **constructor_kwargs
    )


def batch_construct_trace_call(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='trace_call', **constructor_kwargs
    )


def batch_construct_trace_call_many(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='trace_call_many', **constructor_kwargs
    )


def batch_construct_trace_get(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='trace_get', **constructor_kwargs
    )


def batch_construct_trace_filter(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='trace_filter', **constructor_kwargs
    )


def batch_construct_trace_block(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='trace_block', **constructor_kwargs
    )


def batch_construct_trace_replay_block_transactions(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='trace_replay_block_transactions', **constructor_kwargs
    )


def batch_construct_debug_trace_call(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='trace_call', **constructor_kwargs
    )


def batch_construct_debug_trace_call_many(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='trace_call_many', **constructor_kwargs
    )


def batch_construct_debug_trace_transaction(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='trace_transaction', **constructor_kwargs
    )


def batch_construct_debug_trace_block_by_number(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='trace_block_by_number', **constructor_kwargs
    )


def batch_construct_debug_trace_block_by_hash(
    **constructor_kwargs: typing.Any,
) -> spec.RpcPluralRequest:
    return rpc_batch_utils.batch_construct(
        method='trace_block_by_hash', **constructor_kwargs
    )

