"""Handlers for post-processing options."""
import os
import json
from jsonschema import validate

from .helper import get_tempfile


def grid_metrics(gm_obj):
    """Validate the file for custom grid metrics.

        Args:
            gm_obj: An object with custom grid metrics. This can be either a
                JSON file, a string, or a list of grid metrics.

        Returns:
            str -- Path to a the custom grid metrics file.
    """
    _of_schema = {
        'type': 'array',
        'items': {
            'properties': {
                'minimum': {'type': 'number'},
                'maximum': {'type': 'number'},
                'exclusiveMinimum': {'type': 'number'},
                'exclusiveMaximum': {'type': 'number'}
            },
            'additionalProperties': False
        }
    }
    schema = {
        'type': 'array',
        'items': {
            'type': 'object',
            'properties': {
                'minimum': {'type': 'number'},
                'maximum': {'type': 'number'},
                'exclusiveMinimum': {'type': 'number'},
                'exclusiveMaximum': {'type': 'number'},
                'allOf': _of_schema,
                'anyOf': _of_schema
            },
            'additionalProperties': False
        }
    }

    if isinstance(gm_obj, str):
        if os.path.isfile(gm_obj):
            with open(gm_obj) as file:
                grid_metrics = json.load(file)
        else:
            grid_metrics = json.loads(gm_obj)
    elif isinstance(gm_obj, list):
        grid_metrics = gm_obj
    else:
        raise TypeError(
            'Unexpected type of input gm_obj. Valid types are str and list. '
            'Type of input is: %s.' % type(gm_obj)
            )

    validate(grid_metrics, schema)

    file_path = get_tempfile('json', 'grid_metrics')
    with open(file_path, 'w') as f:
        json.dump(grid_metrics, f)

    return file_path
