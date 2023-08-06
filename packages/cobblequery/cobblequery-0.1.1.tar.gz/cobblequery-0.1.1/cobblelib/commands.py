from . import parsers
from . import utils
from . import query_language
from . import aggregators
from .extractor import Extractor

from contextlib import contextmanager
import os
import sys
import json

class SkipError(ValueError):
    pass

class GenerateSeries():
    is_generator = True
    preparsed_arguments = True
    
    def __init__(self, end=20, start=0):
        self.start = int(start)
        self.end = int(end)

    def generate(self):
        for i in range(self.start, self.end):
            yield {'i': i}

class FileLoader():
    is_generator = True
    preparsed_arguments = True
    PARSERS = {
        None: parsers.parse_text,
        'csv': parsers.parse_csv,
        'json_rows': parsers.json_rows,
    }
    
    def __init__(self, path, loader=None, parser=None):
        self.path = path
        self.loader = loader
        self.parser_name = parser

    @contextmanager
    def load(self, *args, **kwargs):
        if self.path == '-':
            f = sys.stdin
            should_close = False
        else:
            f = open(self.path, 'r')
            should_close = True
        try:
            yield f
        finally:
            if should_close:
                f.close()

    def sniff(self, text):
        if text.startswith('{'):
            try:
                loaded = json.loads(text)
                return 'json_rows'
            except Exception as e:
                pass
        if ',' in text:
            return 'csv'
        return None


    def generate(self):
        with self.load() as source:
            if self.parser_name is None:
                source = utils.StreamPeek(source)
                self.parser_name = self.sniff(source.peek(lines=1))
            self.parser = self.PARSERS.get(self.parser_name)

            for entry in self.parser(source):
                yield entry

class PyExecFilter():
    preparsed_arguments = True
    accepts_kwargs = False

    def __init__(self, *args):
        self.executors = []
        for filter_clause in args:
            self.executors.append(utils.py_executor(filter_clause))

    def stream(self, source):
        for entry in source:
            context = {'value': utils.DotWrapper(entry)}
            expression_results = []
            for e in self.executors:
                expression_results.append(e(context)[1])
            if all(expression_results):
                yield entry

class SliceFilter():
    preparsed_arguments = True
    accepts_kwargs = False

    def __init__(self, *args):
        if len(args) == 1:
            start = 0
            end = int(args[0])
        elif len(args) > 1:
            start = int(args[0])
            end = int(args[1])
        if end < 1:
            end = None
        if start < 0:
            start = 0
        self.end = end
        self.start = start

    def stream(self, source):
        for i, entry in enumerate(source):
            if self.start is not None and i < self.start:
                continue
            if self.end is not None and i >= self.end:
                continue
            yield entry

class PyExecSet():
    preparsed_arguments = True

    def __init__(self, **kwargs):
        self.executors = {}
        for target, expression in kwargs.items():
            self.executors[target] = utils.py_executor(expression)

    def stream(self, source):
        for entry in source:
            context = {'value': utils.DotWrapper(entry)}
            for target, executor in self.executors.items():
                result = executor(context)[1]
                entry[target] = result
            yield entry

class Aggregate():
    preparsed_arguments = True

    def __init__(self, *args, **kwargs):
        if 'by' in kwargs:
            self.by_fields = kwargs.pop('by').split(',')
        elif args:
            args.remove('by')
            self.by_fields = args
        else:
            self.by_fields = None

        self.by_extractors = None
        if self.by_fields:
            self.by_extractors = [Extractor(f) for f in self.by_fields]
        self.aggregation_funcs = self.parse_aggregations(kwargs)

    def parse_aggregations(self, specs):
        aggregations = {}
        for target, operation in specs.items():
            agg_name, source = query_language.parse_function_syntax(operation)
            agg_func = aggregators.AGG_FUNCTIONS.get(agg_name, None)
            if agg_func is  None:
                raise ValueError('Aggregation function "{}" does not exist'.format(agg_name))
            aggregations[target] = {
                'extractor': Extractor(source).extract,
                'source': source,
                'func': agg_func,
            }
        return aggregations
        
    def get_by_value(self, entry):
        if self.by_fields is None:
            return None
        if len(self.by_fields) == 1:
            return self.by_extractors[0](entry)
        return tuple(extractor(entry) in self.by_extractors)

    def get_key_pairs(self, key_values):
        if self.by_fields is None:
            return {}
        if len(self.by_fields) == 1:
            return {self.by_fields[0]: key_values}
        else:
            return dict(zip(self.by_fields, key_values))

    def create_aggregations(self):
        aggs_for_key = []
        for target, agg in self.aggregation_funcs.items():
            aggs_for_key.append({
                'extractor': agg['extractor'],
                'aggregator': agg['func'](),
                'target': target,
            })
        return aggs_for_key

    def stream(self, source):
        aggs_by_key = {}
        for entry in source:
            key = self.get_by_value(entry)
            aggs_for_key = aggs_by_key.get(key)
            if key not in aggs_by_key:
                aggs_for_key = self.create_aggregations()
                aggs_by_key[key] = aggs_for_key

            for agg in aggs_for_key:
                source_value = agg['extractor'](entry)
                agg['aggregator'].handle(source_value)

        for key_value, aggs in aggs_by_key.items():
            key_pairs = self.get_key_pairs(key_value)
            agg_results = {agg['target']: agg['aggregator'].result() for agg in aggs}

            record = {}
            record.update(key_pairs)
            record.update(agg_results)
            yield record

class JoinPipeline():
    preparsed_arguments = True
    accepts_sub_commands = True

    def __init__(self, *keys, type='left', first=False, output=None, sub_commands=None):
        self.sub_pipeline = query_language.parse_pipeline(sub_commands)
        if not keys:
            raise ValueError('Join must have at least one condition')
        self.join_keys = keys
        self.join_extractors = [Extractor(f) for f in self.join_keys]
        self.join_type = type


    def get_join_key(self, entry):
        if self.join_keys is None:
            return None
        if len(self.join_keys) == 1:
            return self.join_extractors[0](entry)
        return tuple(extractor(entry) in self.by_extractors)

    def stream(self, source):
        from .core import run_pipeline
        index = {} # whoa, this is going to get big fast
        used = set()
        for entry in run_pipeline(self.sub_pipeline):
            index[self.get_join_key(entry)] = entry

        for entry in source:
            join_key = self.get_join_key(entry)
            match = index.get(join_key, None)
            if match:
                entry.update(match)
                if self.join_type == 'outer':
                    used.add(join_key)
            if self.join_type == 'inner' and not match:
                continue
            yield entry

        if self.join_type == 'outer':
            for key, entry in index.items():
                if key not in used:
                    yield entry

class AppendPipeline():
    preparsed_arguments = True
    accepts_sub_commands = True

    def __init__(self, sub_commands=None):
        self.sub_pipeline = query_language.parse_pipeline(sub_commands)

    def stream(self, source):
        from .core import run_pipeline

        for entry in source:
            yield entry

        for entry in run_pipeline(self.sub_pipeline):
            yield entry


COMMANDS = {
    'from': FileLoader,
    'range': GenerateSeries,
    'append': AppendPipeline,
    'where': PyExecFilter,
    'slice': SliceFilter,
    'set': PyExecSet,
    'eval': PyExecSet,          # Alias
    'aggregate': Aggregate,
    'stats': Aggregate,         # Alias
    'agg': Aggregate,         # Alias
    'join': JoinPipeline,
}
