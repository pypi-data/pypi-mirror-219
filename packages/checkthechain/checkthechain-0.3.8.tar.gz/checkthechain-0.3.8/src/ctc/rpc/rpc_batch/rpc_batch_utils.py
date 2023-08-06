"""
digestors are simpler than constructors and so they do not have batch versions
"""

from __future__ import annotations

import typing

from ctc import spec
from .. import rpc_registry
from .. import rpc_request
from .. import rpc_spec


#
# # batch construction
#


def batch_construct(
    method: str, **constructor_kwargs: typing.Any
) -> spec.RpcPluralRequest:
    """construct a batch of rpc calls"""
    batch_inputs = _get_batch_constructor_inputs(method=method)
    if len(batch_inputs) == 0:
        raise Exception('no batch inputs available for method: ' + str(method))
    singular_constructor = rpc_registry.get_constructor(method=method)
    parameter, values, other_constructor_kwargs = _get_batch_parameter(
        constructor_kwargs,
        batch_inputs,
    )
    return [
        singular_constructor(**{parameter: value}, **other_constructor_kwargs)
        for value in values
    ]


def _get_batch_parameter(
    kwargs: typing.Mapping[str, typing.Any],
    batch_inputs: typing.Mapping[str, str],
) -> typing.Tuple[str, typing.Any, typing.Mapping[str, typing.Any]]:
    """identify the batch parameter given in kwargs

    return (singular_parameter, parameter_value, other_kwargs)
    """

    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    # find suitable candidates
    candidates = []
    for plural_name, singular_name in batch_inputs.items():
        if plural_name in kwargs:
            candidates.append(plural_name)

    # select candidate
    if len(candidates) == 0:
        raise Exception('no batch parameter specified')
    elif len(candidates) > 1:
        raise Exception('too many batch parameters specified')
    else:
        parameter = candidates[0]
        return (
            batch_inputs[parameter],
            kwargs[parameter],
            {k: v for k, v in kwargs.items() if k not in batch_inputs},
        )


def _get_batch_constructor_inputs(method: str) -> typing.Mapping[str, str]:
    return rpc_spec.rpc_constructor_batch_inputs.get(method, {})


#
# # batch execution
#


async def async_batch_execute(
    method: str,
    *,
    context: spec.Context = None,
    convert_reverts_to: typing.Any = None,
    convert_reverts_to_none: bool = False,
    **kwargs: typing.Any,
) -> spec.RpcPluralResponse:
    """execute batch rpc call asynchronously"""

    constructor_kwargs, digestor_kwargs = _separate_execution_kwargs(
        method=method,
        kwargs=kwargs,
    )
    request = batch_construct(method=method, **constructor_kwargs)
    response = await rpc_request.async_send(
        request=request,
        context=context,
        convert_reverts_to_none=convert_reverts_to_none,
        convert_reverts_to=convert_reverts_to,
    )
    return batch_digest(response=response, method=method, **digestor_kwargs)


def _separate_execution_kwargs(
    method: str,
    kwargs: typing.Mapping[str, typing.Any],
) -> tuple[typing.Mapping[str, typing.Any], typing.Mapping[str, typing.Any]]:
    """separate constructor kwargs from digestor kwargs"""

    import inspect

    # compile digestor kwargs
    digestor = rpc_registry.get_digestor(method)
    signature = inspect.getfullargspec(digestor)
    digestor_args = signature.args + signature.kwonlyargs

    # separate kwargs into constructor and digestor kwargs
    constructor_kwargs = {}
    digestor_kwargs = {}
    for key, value in kwargs.items():
        if key in digestor_args:
            digestor_kwargs[key] = value
        else:
            constructor_kwargs[key] = value

    # add args that are passed to both constructors and digestors
    if method == 'eth_call':
        if kwargs.get('function_abi') is not None:
            constructor_kwargs['function_abi'] = kwargs['function_abi']

    return constructor_kwargs, digestor_kwargs


#
# # batch digestion
#


def batch_digest(
    response: spec.RpcPluralResponse,
    method: str,
    **digestor_kwargs: typing.Any,
) -> spec.RpcPluralResponse:
    digestor = rpc_registry.get_digestor(method)
    results = []
    for s, subresponse in enumerate(response):
        result = digestor(subresponse, **digestor_kwargs)
        results.append(result)
    return results

