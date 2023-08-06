from . import commands
from . import query_language
from . import utils


def run_pipeline(pipeline):
    functions = []
    for command_def in pipeline:
        CommandCls = commands.COMMANDS.get(command_def['function'])
        if CommandCls is None:
            raise ValueError('Invalid function "{}"'.format(command_def['function']))
        if getattr(CommandCls, 'preparsed_arguments'):
            allow_kwargs = getattr(CommandCls, 'accepts_kwargs', True)
            allow_sub = getattr(CommandCls, 'accepts_sub_commands', False)
            args, kwargs = query_language.parse_arguments(command_def['args'], allow_kwargs=allow_kwargs)
            if allow_sub:
                kwargs['sub_commands'] = command_def['sub']
            configured_command = CommandCls(*args, **kwargs)
        else:
            configured_command = CommandCls(command_def.get('args', None))
        functions.append(configured_command)

    generator = functions[0]
    processors = functions[1:]

    previous_iterator = generator.generate()
    for function in processors:
        previous_iterator = function.stream(previous_iterator)

    for item in previous_iterator:
        yield item
