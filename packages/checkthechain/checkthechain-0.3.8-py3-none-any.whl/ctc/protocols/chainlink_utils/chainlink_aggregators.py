from __future__ import annotations

import asyncio
import functools
import typing

from ctc import evm
from ctc import rpc
from ctc import spec

from . import chainlink_db
from . import chainlink_feed_metadata


async def async_get_aggregator_description(
    aggregator: spec.Address,
    *,
    context: spec.Context = None,
) -> str:

    function_abi: spec.FunctionABI = {
        'inputs': [],
        'name': 'description',
        'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}],
        'stateMutability': 'view',
        'type': 'function',
    }

    result = await rpc.async_eth_call(
        to_address=aggregator,
        function_abi=function_abi,
        context=context,
    )
    if not isinstance(result, str):
        raise Exception('invalid rpc result')
    return result


async def async_get_aggregator_base_quote(
    aggregator: spec.Address,
    *,
    context: spec.Context = None,
) -> dict[str, str]:
    description = await async_get_aggregator_description(
        aggregator=aggregator,
        context=context,
    )
    try:
        base, quote = description.split(' / ')
        return {'base': base, 'quote': quote}
    except Exception:
        raise Exception(
            'could not determine base or quote from description: '
            + str(description)
        )


async def async_get_feed_aggregator_history(
    feed: spec.Address,
    *,
    context: spec.Context = None,
) -> typing.Mapping[spec.Address, int]:
    # TODO: can make it go 2x as fast by searching at start and end concurrently
    # TODO: be able to give block range to search within

    feed = await chainlink_feed_metadata.async_resolve_feed_address(
        feed,
        context=context,
    )

    # query current feed aggregator
    aggregator_coroutine = chainlink_feed_metadata.async_get_feed_aggregator(
        feed=feed,
        block='latest',
        context=context,
    )

    # get known updates
    db_results = await chainlink_db.async_query_aggregator_updates(
        feed=feed,
        context=context,
    )
    if db_results is not None:
        db_results = sorted(
            db_results, key=lambda result: result['block_number']
        )
        feed_aggregator_updates = {
            update['aggregator']: update['block_number']
            for update in db_results
        }
    else:
        feed_aggregator_updates = {}

    # await current aggregator
    aggregator = await aggregator_coroutine

    # if current aggregator is in database, then data are up to date
    if aggregator in feed_aggregator_updates:
        return feed_aggregator_updates

    # otherwise, need to update data
    else:

        # collect new update data
        previous_aggregators = await async_get_feed_previous_aggregators(
            feed=feed,
            context=context,
        )
        previous_aggregators = [
            aggregator
            for aggregator in previous_aggregators
            if aggregator not in feed_aggregator_updates
        ]
        aggregator_start_blocks = await _async_get_aggregator_start_blocks(
            previous_aggregators=previous_aggregators,
            feed=feed,
            context=context,
        )

        # intake new data to database
        updates: typing.Sequence[
            chainlink_db.chainlink_schema_defs._FeedAggregatorUpdate
        ] = [
            {
                'feed': feed,
                'aggregator': aggregator,
                'block_number': block_number,
            }
            for aggregator, block_number in aggregator_start_blocks.items()
        ]
        await chainlink_db.async_intake_aggregator_updates(
            updates=updates,
            context=context,
        )

        return dict(feed_aggregator_updates, **aggregator_start_blocks)


async def _async_get_aggregator_start_blocks(
    previous_aggregators: typing.Sequence[spec.Address],
    feed: spec.Address,
    *,
    context: spec.Context = None,
) -> typing.Mapping[spec.Address, int]:

    print('locating Chainlink aggregator update blocks...')

    from ctc.toolbox import search_utils

    latest = await evm.async_get_latest_block_number(context=context)

    # TODO: use chainlink feed registry for this
    feed_creation_block = await evm.async_get_contract_creation_block(
        contract_address=feed,
        context=context,
    )

    aggregator_start_blocks = {}
    aggregator_start_blocks[previous_aggregators[0]] = feed_creation_block

    last_known_block = latest
    for next_aggregator in reversed(previous_aggregators[1:]):

        async_is_match = functools.partial(
            _async_aggregator_transition,
            feed=feed,
            next_aggregator=next_aggregator,
            context=context,
        )

        block = await search_utils.async_binary_search(
            async_is_match=async_is_match,
            start_index=feed_creation_block,
            end_index=last_known_block,
        )

        if block is None:
            raise Exception('could not determine start block of aggregator')

        aggregator_start_blocks[next_aggregator] = block
        last_known_block = block - 1

    return dict(
        sorted(aggregator_start_blocks.items(), key=lambda item: item[1])  # type: ignore
    )


async def _async_aggregator_transition(
    block: int,
    next_aggregator: spec.Address,
    *,
    feed: spec.Address,
    context: spec.Context = None,
) -> bool:

    aggregator = await chainlink_feed_metadata.async_get_feed_aggregator(
        feed,
        block=block,
        context=context,
    )
    return next_aggregator == aggregator


async def async_get_feed_previous_aggregators(
    feed: str,
    *,
    context: spec.Context = None,
) -> list[spec.Address]:

    feed = await chainlink_feed_metadata.async_resolve_feed_address(
        feed, context=context
    )

    phase_id_abi: spec.FunctionABI = {
        'inputs': [],
        'name': 'phaseId',
        'outputs': [{'internalType': 'uint16', 'name': '', 'type': 'uint16'}],
        'stateMutability': 'view',
        'type': 'function',
    }

    current_phase = await rpc.async_eth_call(
        to_address=feed,
        function_abi=phase_id_abi,
        context=context,
    )

    phase_aggregators_abi: spec.FunctionABI = {
        'inputs': [{'internalType': 'uint16', 'name': '', 'type': 'uint16'}],
        'name': 'phaseAggregators',
        'outputs': [
            {
                'internalType': 'contract AggregatorV2V3Interface',
                'name': '',
                'type': 'address',
            }
        ],
        'stateMutability': 'view',
        'type': 'function',
    }

    coroutines = [
        rpc.async_eth_call(
            to_address=feed,
            function_abi=phase_aggregators_abi,
            function_parameters=[i],
            context=context,
        )
        for i in range(1, current_phase + 1)
    ]
    aggregators = await asyncio.gather(*coroutines)

    return aggregators

