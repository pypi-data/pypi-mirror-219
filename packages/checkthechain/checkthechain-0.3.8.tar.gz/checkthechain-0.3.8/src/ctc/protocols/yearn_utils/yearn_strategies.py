from __future__ import annotations

import asyncio
import typing

from ctc import evm
from ctc import rpc
from ctc import spec

import numpy as np


# async def async_get_vault_strategies(
#     vault: spec.Address,
# ) -> typing.Sequence[spec.Address]:
#     pass


async def async_get_harvests(
    strategy: spec.Address,
    *,
    include_aprs: bool = True,
    context: spec.Context = None,
) -> spec.DataFrame:
    import polars as pl

    harvests = await evm.async_get_events(
        contract_address=strategy,
        event_name='Harvested',
        include_timestamps=True,
        verbose=False,
        context=context,
    )
    harvests.with_columns(pl.col('arg__profit').apply(int))

    if include_aprs:
        aprs = await async_get_harvest_aprs(
            strategy=strategy, harvests=harvests, context=context
        )
        harvests = harvests.with_columns(pl.Series('apr', aprs))

    return harvests


async def async_get_harvest_aprs(
    strategy: spec.Address,
    *,
    harvests: spec.DataFrame | None = None,
    context: spec.Context = None,
) -> spec.NumpyArray:

    if harvests is None:
        harvests = await async_get_harvests(strategy, context=context)

    durations_task = asyncio.create_task(
        async_get_harvest_durations(harvests, context=context)
    )
    total_debts = await async_get_harvest_total_debts(
        strategy, harvests, context=context
    )
    total_debts = [debt if debt != 0 else float('-inf') for debt in total_debts]
    durations = await durations_task

    aprs = (
        harvests['arg__profit']
        / np.array(total_debts)
        / np.array(durations)
        * 86400
        * 365
    )
    return aprs.to_numpy()


async def async_get_harvest_durations(
    harvests: spec.DataFrame,
    *,
    context: spec.Context = None,
) -> typing.Sequence[int | float]:
    blocks = harvests['block_number'].to_list()
    timestamps = await evm.async_get_block_timestamps(blocks, context=context)
    durations = [float('inf')] + [
        after - before for after, before in zip(timestamps[1:], timestamps[:-1])
    ]
    return durations


async def async_get_harvest_total_debts(
    strategy: spec.Address,
    harvests: spec.DataFrame,
    *,
    context: spec.Context = None,
) -> typing.Sequence[int | float]:

    function_abi: spec.FunctionABI = {
        'inputs': [],
        'name': 'estimatedTotalAssets',
        'outputs': [
            {
                'internalType': 'uint256',
                'name': '',
                'type': 'uint256',
            },
        ],
        'stateMutability': 'view',
        'type': 'function',
    }

    total_debts = await rpc.async_batch_eth_call(
        to_address=strategy,
        function_abi=function_abi,
        block_numbers=harvests['block_number'].to_list(),
        context=context,
    )
    return [float('inf')] + total_debts[:-1]

