import dataclasses
from typing import _GenericAlias

import dict_tools
from dict_tools.typing import is_computed


def get_defaults_if_dataclass(hub, param) -> dict:
    # Return dictionary with the default values for a dataclass argument
    # Otherwise an empty dictionary
    param_structure_with_defaults = {}
    if dataclasses.is_dataclass(param.annotation):
        _annotation_recursive(param_structure_with_defaults, param.annotation)
    elif (
        isinstance(param.annotation, _GenericAlias)
        and isinstance(param.annotation.__args__, tuple)
        and dataclasses.is_dataclass(param.annotation.__args__[0])
    ):
        _annotation_recursive(
            param_structure_with_defaults, param.annotation.__args__[0]
        )

    return param_structure_with_defaults


def calculate_changes(hub, old_state, new_state, params, func_ref) -> dict:
    # Calculate resource changes skipping values of Computed parameters

    computed_params = {}

    # Step 1: Get function parameters that are marked Computed, including nested parameters
    for name, param in params.items():
        if is_computed(param.annotation):
            computed_params[name] = None
        elif dataclasses.is_dataclass(param.annotation):
            computed_param_nested = _get_computed_params_nested_dataclass(
                param.annotation
            )
            if computed_param_nested:
                computed_params[param.name] = computed_param_nested
        elif (
            isinstance(param.annotation, _GenericAlias)
            and isinstance(param.annotation.__args__, tuple)
            and dataclasses.is_dataclass(param.annotation.__args__[0])
        ):
            computed_param_nested = _get_computed_params_nested_dataclass(
                param.annotation.__args__[0]
            )
            if computed_param_nested:
                computed_params[param.name] = computed_param_nested

    # Step 2: Calculate recursive diff of old_state and new_state ignoring changes in Computed values
    if computed_params:
        hub.log.info(
            f"Calculating changes for resource function '{func_ref}', ignoring Computed parameters [{computed_params}]."
        )
    changes = dict_tools.data.recursive_diff(
        old_state if old_state else dict(),
        new_state if new_state else dict(),
        ignore_keys_dict=computed_params,
        ignore_order=True,
    )

    return changes


def populate_default_values(hub, default_vals: dict, value):
    # Recursive method to set default values in an argument
    # of type dataclass
    if default_vals is None:
        return

    if isinstance(value, list):
        for elem in value:
            for arg_name, arg_value in default_vals.items():
                if arg_value is None:
                    continue
                if not elem.get(arg_name) and not isinstance(arg_value, dict):
                    elem[arg_name] = arg_value
                elif isinstance(arg_value, dict):
                    populate_default_values(hub, arg_value, elem[arg_name])
    else:
        for arg_name, arg_value in default_vals.items():
            if arg_value is None:
                continue
            if not value.get(arg_name) and not isinstance(arg_value, dict):
                value.update({arg_name: arg_value})
            elif isinstance(arg_value, dict):
                populate_default_values(hub, arg_value, value[arg_name])


def _annotation_recursive(defaults, param_annotation):
    # Populate the default values of an argument of type dataclass
    # from the parameter annotation
    for field in dataclasses.fields(param_annotation):
        if dataclasses.is_dataclass(field.type):
            defaults[field.name] = {}
            _annotation_recursive(defaults[field.name], field.type)
        else:
            defaults[field.name] = field.default


def _get_computed_params_nested_dataclass(param_annotation):
    computed_params = {}

    for field in dataclasses.fields(param_annotation):
        if is_computed(field.type):
            computed_params[field.name] = None
        elif dataclasses.is_dataclass(field.type):
            computed_param_nested = _get_computed_params_nested_dataclass(field.type)
            if computed_param_nested:
                computed_params[field.name] = computed_param_nested

    return computed_params if len(computed_params) > 0 else None
