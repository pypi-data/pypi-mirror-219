# This file is a copy of classiq/interface/generator/validations/flow_graph.py
# It will be removed when we remove wiring from the UserModel in favor of Port Handles
# as described in this epic: https://classiq.atlassian.net/browse/CAD-5142

from collections import defaultdict
from itertools import chain
from typing import Collection, Mapping

import networkx as nx

from classiq.interface.generator.quantum_function_call import WireName
from classiq.interface.generator.validations.flow_graph import (
    CYCLE_ERROR_MSG,
    IO_MULTI_USE_ERROR_MSG,
    RECURRING_NAMES_ERROR_MSG,
    UNCONNECTED_FLOW_IO_ERROR_MSG,
    UNCONNECTED_WIRES_ERROR_MSG,
    Wire,
    _join_errors,
    _recurring_names,
    _wire_name_and_unique_slice_names,
    get_wire_name,
)
from classiq.interface.generator.wiring.sliced_wire import PortBinding
from classiq.interface.model.quantum_function_call import QuantumFunctionCall


def validate_legal_wiring(
    body: Collection[QuantumFunctionCall],
    *,
    flow_input_names: Collection[str],
    flow_output_names: Collection[str],
) -> None:
    call_input_names = _wire_name_and_unique_slice_names(
        list(chain(*(function_call.non_zero_input_wires for function_call in body)))
    )
    call_output_names = _wire_name_and_unique_slice_names(
        list(chain(*(function_call.non_zero_output_wires for function_call in body)))
    )

    if (
        len(set(call_input_names)) == len(call_input_names)
        and len(set(call_output_names)) == len(call_output_names)
        and sorted([*call_input_names, *flow_output_names])
        == sorted([*call_output_names, *flow_input_names])
    ):
        return

    error_messages = list()

    recurring_names: Collection[str] = {
        *_recurring_names([*call_input_names, *flow_output_names]),
        *_recurring_names([*call_output_names, *flow_input_names]),
    }

    if recurring_names:
        error_messages.append(f"{RECURRING_NAMES_ERROR_MSG}: {recurring_names}")

    unconnected_flow_ios = [
        name for name in flow_input_names if name not in call_input_names
    ] + [name for name in flow_output_names if name not in call_output_names]
    if unconnected_flow_ios:
        error_messages.append(
            f"{UNCONNECTED_FLOW_IO_ERROR_MSG}: {unconnected_flow_ios}"
        )

    unconnected_wires = [
        name
        for name in call_input_names
        if name not in call_output_names and name not in flow_input_names
    ] + [
        name
        for name in call_output_names
        if name not in call_input_names and name not in flow_output_names
    ]
    if unconnected_wires:
        error_messages.append(f"{UNCONNECTED_WIRES_ERROR_MSG}: {unconnected_wires}")

    raise ValueError(_join_errors(error_messages))


def _parse_call_inputs(
    function_call: QuantumFunctionCall,
    wires: Mapping[WireName, Wire],
    flow_input_names: Collection[str],
) -> None:
    if not function_call.non_zero_input_wires:
        return

    for wire_name_or_slice in function_call.non_zero_input_wires:
        wire_name = get_wire_name(wire_name_or_slice)
        if wire_name in flow_input_names:
            continue

        wire = wires[wire_name]

        if wire.end and not isinstance(wire_name_or_slice, PortBinding):
            raise ValueError(
                IO_MULTI_USE_ERROR_MSG
                + f". The name {wire_name} is used multiple times."
            )
        wire.end = function_call.name


def _parse_call_outputs(
    function_call: QuantumFunctionCall,
    wires: Mapping[WireName, Wire],
    flow_output_names: Collection[str],
) -> None:
    if not function_call.non_zero_output_wires:
        return

    for wire_name_or_slice in function_call.non_zero_output_wires:
        wire_name = get_wire_name(wire_name_or_slice)
        if wire_name in flow_output_names:
            continue

        wire = wires[wire_name]

        if wire.start and not isinstance(wire_name_or_slice, PortBinding):
            raise ValueError(
                IO_MULTI_USE_ERROR_MSG
                + f". The name {wire_name} is used multiple times."
            )
        wire.start = function_call.name


def _create_flow_graph(
    body: Collection[QuantumFunctionCall],
    flow_input_names: Collection[str],
    flow_output_names: Collection[str],
) -> nx.DiGraph:
    wires: Mapping[str, Wire] = defaultdict(Wire)

    for function_call in body:
        _parse_call_inputs(
            function_call=function_call, wires=wires, flow_input_names=flow_input_names
        )
        _parse_call_outputs(
            function_call=function_call,
            wires=wires,
            flow_output_names=flow_output_names,
        )

    edges = [(wire.start, wire.end) for wire in wires.values()]

    graph = nx.DiGraph()
    graph.add_nodes_from(
        (function_call.name, {"function_call": function_call}) for function_call in body
    )
    graph.add_edges_from(edges)
    return graph


def validate_acyclic_logic_flow(
    body: Collection[QuantumFunctionCall],
    *,
    flow_input_names: Collection[str],
    flow_output_names: Collection[str],
) -> nx.DiGraph:
    graph = _create_flow_graph(
        body=body,
        flow_input_names=flow_input_names,
        flow_output_names=flow_output_names,
    )

    if not nx.algorithms.is_directed_acyclic_graph(graph):
        cycles = list(nx.algorithms.simple_cycles(graph))
        raise ValueError(CYCLE_ERROR_MSG + ". Cycles are: " + str(cycles))

    return graph
