from __future__ import annotations

import typing

from ctc import spec

from . import chainlink_data


async def async_get_eth_price(
    block: spec.BlockNumberReference = 'latest',
    *,
    normalize: bool = True,
    context: spec.Context = None,
) -> typing.Union[int, float]:
    return await chainlink_data.async_get_feed_datum(
        feed='ETH_USD',
        normalize=normalize,
        block=block,
        context=context,
    )


async def async_get_eth_price_by_block(
    blocks: typing.Sequence[spec.BlockNumberReference],
    *,
    normalize: bool = True,
    context: spec.Context = None,
) -> typing.Union[spec.DataFrame, spec.Series]:
    return await chainlink_data.async_get_feed_data(
        feed='ETH_USD',
        normalize=normalize,
        blocks=blocks,
        context=context,
    )
