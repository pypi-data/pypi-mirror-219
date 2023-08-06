from __future__ import annotations

import typing

from ctc import spec


@typing.overload
async def async_get_eth_balance(
    address: spec.Address,
    *,
    normalize: typing.Literal[False],
    context: spec.Context = None,
    block: typing.Optional[spec.BlockNumberReference] = None,
) -> int:
    ...


@typing.overload
async def async_get_eth_balance(
    address: spec.Address,
    *,
    normalize: typing.Literal[True] = True,
    context: spec.Context = None,
    block: typing.Optional[spec.BlockNumberReference] = None,
) -> float:
    ...


@typing.overload
async def async_get_eth_balance(
    address: spec.Address,
    *,
    normalize: bool,
    context: spec.Context = None,
    block: typing.Optional[spec.BlockNumberReference] = None,
) -> int | float:
    ...


async def async_get_eth_balance(
    address: spec.Address,
    *,
    normalize: bool = True,
    context: spec.Context = None,
    block: typing.Optional[spec.BlockNumberReference] = None,
) -> typing.Union[int, float]:
    """get ETH balance"""

    from ctc import rpc

    result = await rpc.async_eth_get_balance(
        address=address,
        block_number=block,
        context=context,
    )
    if not isinstance(result, int):
        raise Exception('invalid rpc result')
    balance: int | float = result

    if normalize:
        balance /= 1e18

    return balance


@typing.overload
async def async_get_eth_balance_by_block(
    address: spec.Address,
    *,
    blocks: typing.Sequence[spec.BlockNumberReference],
    normalize: typing.Literal[False],
    context: spec.Context = None,
) -> list[int]:
    ...


@typing.overload
async def async_get_eth_balance_by_block(
    address: spec.Address,
    *,
    blocks: typing.Sequence[spec.BlockNumberReference],
    normalize: typing.Literal[True] = True,
    context: spec.Context = None,
) -> list[float]:
    ...


@typing.overload
async def async_get_eth_balance_by_block(
    address: spec.Address,
    *,
    normalize: bool = True,
    blocks: typing.Sequence[spec.BlockNumberReference],
    context: spec.Context = None,
) -> typing.Union[list[int], list[float]]:
    ...


async def async_get_eth_balance_by_block(
    address: spec.Address,
    *,
    blocks: typing.Sequence[spec.BlockNumberReference],
    normalize: bool = True,
    context: spec.Context = None,
) -> typing.Union[list[int], list[float]]:
    """get historical ETH balance over multiple blocks"""

    coroutines = []
    for block in blocks:
        coroutine = async_get_eth_balance(
            address=address, context=context, block=block, normalize=normalize
        )
        coroutines.append(coroutine)

    import asyncio

    return await asyncio.gather(*coroutines)


@typing.overload
async def async_get_eth_balance_of_addresses(
    addresses: typing.Sequence[spec.Address],
    *,
    normalize: typing.Literal[False],
    block: typing.Optional[spec.BlockNumberReference] = None,
    context: spec.Context = None,
) -> list[int]:
    ...


@typing.overload
async def async_get_eth_balance_of_addresses(
    addresses: typing.Sequence[spec.Address],
    *,
    block: typing.Optional[spec.BlockNumberReference] = None,
    normalize: typing.Literal[True] = True,
    context: spec.Context = None,
) -> list[float]:
    ...


@typing.overload
async def async_get_eth_balance_of_addresses(
    addresses: typing.Sequence[spec.Address],
    *,
    normalize: bool = True,
    block: typing.Optional[spec.BlockNumberReference] = None,
    context: spec.Context = None,
) -> typing.Union[list[int], list[float]]:
    ...


async def async_get_eth_balance_of_addresses(
    addresses: typing.Sequence[spec.Address],
    *,
    normalize: bool = True,
    block: typing.Optional[spec.BlockNumberReference] = None,
    context: spec.Context = None,
) -> typing.Union[list[int], list[float]]:
    """get ETH balance of multiple addresses"""

    from ctc import rpc

    balances = await rpc.async_batch_eth_get_balance(
        addresses=addresses,
        context=context,
        block_number=block,
    )

    if normalize:
        balances = [balance / 1e18 for balance in balances]

    return balances
