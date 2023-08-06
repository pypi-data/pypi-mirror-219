import itertools
from copy import deepcopy
from rich.console import Console

c = Console()

def generate_param_grid(param_grid):
    if not isinstance(param_grid, dict):
        return param_grid

    keys = list(param_grid.keys())
    values = [generate_param_grid(param_grid[k]) for k in keys]
    param_combinations = itertools.product(*values)
    param_grid_list = []
    for combination in param_combinations:
        param_grid_dict = {}
        for i, key in enumerate(keys):
            param_grid_dict[key] = combination[i]
        param_grid_list.append(param_grid_dict)
    return param_grid_list

def update_nested_dict(nested_dict, update_dict):
    for key, value in update_dict.items():
        if isinstance(value, dict) and key in nested_dict and isinstance(nested_dict[key], dict):
            update_nested_dict(nested_dict[key], value)
        else:
            nested_dict[key] = value
    return deepcopy(nested_dict)

def get_parameters_list(parameters, grids):
    parameters_list = []
    for set_ in generate_param_grid(grids):
        parameters_list.append(update_nested_dict(parameters, set_))
    return parameters_list


def flatten_dict(dictionary, parent_key='', separator='_'):
    items = []
    for key, value in dictionary.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key, separator).items())
        else:
            items.append((new_key, value))
    return dict(items)