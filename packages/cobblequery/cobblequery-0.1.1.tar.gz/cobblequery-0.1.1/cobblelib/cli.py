from . import query_language as QL
from .core import run_pipeline
from . import commands

import sys
import json

DEFAULT_GENERATOR = {
    'function': 'from',
    'args': '-',
}

def parse_query(query_text):
    try:
        query = QL.parse_pipeline(query_text)
    except ValueError as e:
        error = str(e)
        print('Error parsing query: {}'.format(error))
        print('Given query:\n{}'.format(query_text))
        return False
    print('Given query:\n{}'.format(json.dumps(query, indent=4)))
    return True


def execute(query_text):
    try:
        query = QL.parse_pipeline(query_text)
    except ValueError as e:
        error = str(e)
        print('Error parsing query: {}'.format(error))
        print('Given query:\n{}'.format(query_text))
        return False

    if not query:
        query.insert(0, DEFAULT_GENERATOR)

    first_command = commands.COMMANDS.get(query[0]['function'], None)
    if not first_command or not getattr(first_command, 'is_generator', False):
        query.insert(0, DEFAULT_GENERATOR)

    for entry in run_pipeline(query):
        print(json.dumps(entry))
