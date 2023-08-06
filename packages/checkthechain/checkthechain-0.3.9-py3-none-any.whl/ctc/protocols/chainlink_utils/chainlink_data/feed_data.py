from __future__ import annotations

import typing

from ctc import evm
from ctc import spec

from .. import chainlink_feed_metadata
from .. import chainlink_spec
from . import feed_datum_by_block
from . import feed_events


if typing.TYPE_CHECKING:
    import tooltime


async def async_get_feed_data(
    feed: chainlink_spec._FeedReference,
    *,
    fields: typing.Literal['answer', 'full'] = 'answer',
    blocks: typing.Sequence[spec.BlockNumberReference] | None = None,
    start_block: spec.BlockNumberReference | None = None,
    end_block: spec.BlockNumberReference | None = None,
    start_time: tooltime.Timestamp | None = None,
    end_time: tooltime.Timestamp | None = None,
    invert: bool = False,
    normalize: bool = True,
    interpolate: bool = False,
    context: spec.Context = None,
) -> spec.DataFrame:

    start_block, end_block = await evm.async_resolve_block_range(
        start_block=start_block,
        end_block=end_block,
        start_time=start_time,
        end_time=end_time,
        allow_none=True,
        context=context,
    )

    # determine blocks
    if (blocks is not None) and [start_block, end_block].count(None) < 2:
        raise Exception('should only provide one block specification')
    if blocks is None:
        if start_block is None:
            start_block = (
                await chainlink_feed_metadata.async_get_feed_first_block(
                    feed=feed,
                    context=context,
                )
            )
        if end_block is None:
            end_block = 'latest'

    # perform query
    if fields == 'answer':

        if blocks is not None:
            return (
                await feed_datum_by_block.async_get_feed_answer_datum_by_block(
                    feed,
                    blocks=blocks,
                    normalize=normalize,
                    interpolate=interpolate,
                    invert=invert,
                    context=context,
                )
            )

        else:
            return await feed_events.async_get_answer_feed_event_data(
                feed,
                normalize=normalize,
                start_block=start_block,
                end_block=end_block,
                interpolate=interpolate,
                invert=invert,
                context=context,
            )

    elif fields == 'full':

        if blocks is not None:
            return await feed_datum_by_block.async_get_feed_full_datum_by_block(
                feed,
                blocks=blocks,
                normalize=normalize,
                interpolate=interpolate,
                invert=invert,
                context=context,
            )

        else:
            return await feed_events.async_get_full_feed_event_data(
                feed,
                normalize=normalize,
                start_block=start_block,
                end_block=end_block,
                interpolate=interpolate,
                invert=invert,
                context=context,
            )

    else:
        raise Exception('unknown fields format: ' + str(fields))
