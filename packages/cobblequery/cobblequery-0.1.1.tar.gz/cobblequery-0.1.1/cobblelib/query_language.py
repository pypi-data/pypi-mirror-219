import re

QUOTE_CHAR = '"'
QUOTE_SPLIT = '(?<!\\\\)(")'
def token_split(text):
    if text is None:
        return
    tokens = re.split(QUOTE_SPLIT, text)
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == QUOTE_CHAR:
            yield QUOTE_CHAR + tokens[i+1] + QUOTE_CHAR, True
            i += 3
            continue
        yield token, False
        i += 1

def unquote_token(token, strip_whitespace=True):
    if not token:
        return token
    quoted = token[0] == QUOTE_CHAR and token[-1] == QUOTE_CHAR
    if quoted:
        token = token[1:-1]
        token = token.replace(r'\"', '"')
    else:
        if strip_whitespace:
            token, _ = re.subn('\\s+', '', token)
    return token


def find_all(text, substr):
    indexes = []
    i = 0
    while True:
        matching_index = text.find(substr, i)
        if matching_index == -1:
            break
        else:
            indexes.append(matching_index)
            i = matching_index + 1
    return indexes


class Lexer():
    counter = 0

    def __init__(self, text):
        Lexer.counter += 1
        self.id = Lexer.counter
        self.text = text
        self.tokens = list(token_split(text))
        self.tokens.reverse()

    def consume_whitespace(self):
        while self.tokens:
            token, is_quoted = self.tokens.pop()
            if is_quoted:
                self.tokens.append((token, True))
                break

            remaining = token.lstrip()
            if remaining:
                self.tokens.append((remaining, False))
                break

    def seek_till(self, *targets, consume=True, keep_quotes=True):
        captured_tokens = []
        target_index = None
        target_found = None

        while self.tokens:
            token, is_quoted = self.tokens.pop()
            # We ignore all tokens found in quoted strings
            if is_quoted:
                if not keep_quotes:
                    token = token[1:-1]
                captured_tokens.append(token)
                continue
                
            # Find the closest one of our "stop targets" in token
            for target in targets:
                if isinstance(target, re.Pattern):
                    match_obj = target.search(token)
                    if match_obj is not None:
                        index = match_obj.start()
                        match = match_obj.group()
                    else:
                        index = -1
                        match = None
                else:
                    index = token.find(target)
                    match = target

                if index >= 0:
                    if target_index is None:
                        target_index = index
                        target_found = match
                    elif index < target_index:
                        target_index = index
                        target_found = match

            if target_found is not None:
                captured = token[:target_index]
                remaining_index = target_index
                if consume:
                    remaining_index += len(target_found)
                remaining = token[remaining_index:]
                if remaining:
                    self.tokens.append((remaining, False))
                if captured:
                    captured_tokens.append(captured)
                break

            # If this token didn't contain any of our "stop targets" keep going
            captured_tokens.append(token)
            continue
                
        return ''.join(captured_tokens), target_found

    def seek_closing_pair(self, open_char, close_char, keep_quotes=True):
        captured_tokens = []
        layers = 0
        final_index = None

        while self.tokens:
            token, is_quoted = self.tokens.pop()
            # We ignore all tokens found in quoted strings
            if is_quoted:
                if not keep_quotes:
                    token = token[1:-1]
                captured_tokens.append(token)
                continue
                
            # Find the closest one of our "stop targets" in token
            open_indexes = [('open', m) for m in find_all(token, open_char)]
            close_indexes = [('close', m) for m in find_all(token, close_char)]
            indexes = [*open_indexes, *close_indexes]
            indexes.sort(key=lambda x: x[1])
            if not indexes:
                captured_tokens.append(token)
                continue

            for state, index in indexes:
                if state == 'open':
                    layers += 1
                elif layers > 0:
                    layers -= 1
                else:
                    # We finally closed it
                    final_index = index
                    captured = token[:final_index]
                    remaining_index = final_index + 1
                    remaining = token[remaining_index:]
                    if remaining:
                        self.tokens.append((remaining, False))
                    if captured:
                        captured_tokens.append(captured)
                    break

            if final_index is not None:
                break
            else:
                captured_tokens.append(token)


        if final_index is None:
            raise ValueError('Unable to find closing pair!')

        return ''.join(captured_tokens)


SUB_PIPELINE_PAIRS = {
    '{': '}',
    '[': ']',
}
TOKEN_FUNCTION_SEP = '|'
def parse_pipeline(text):
    pipeline = []
    lexer = Lexer(text)

    garbage, pipe = lexer.seek_till('|')
    if pipe is None or garbage.strip():
        raise ValueError('Yo, your query should start with a pipe:' + garbage)

    while True:
        sub = None
        lexer.consume_whitespace()
        function_name, closing_token = lexer.seek_till(re.compile(r'\s+'), '(')
        if closing_token is None:
            if function_name:
                pipeline.append({'function': function_name, 'args': '', 'sub': sub})
            break
        elif closing_token == '|':
            continue

        parens = closing_token == '('
        if parens:
            arguments = lexer.seek_closing_pair('(', ')', keep_quotes=True)
            garbage, closing_token = lexer.seek_till('|', re.compile(r'\{|\['))
        else:
            arguments, closing_token = lexer.seek_till('|', re.compile(r'\{|\['))

        if closing_token in ('[', '{'):
            sub = lexer.seek_closing_pair(closing_token, SUB_PIPELINE_PAIRS[closing_token], keep_quotes=True).strip()
            garbage, closing_token = lexer.seek_till('|')
        elif closing_token == ')':
            garbage, closing_token = lexer.seek_till('|')

        pipeline.append({'function': function_name, 'args': arguments.strip(), 'sub': sub})
        if closing_token is None:
            break

    return pipeline

def parse_arguments(text, allow_kwargs=True):
    lexer = Lexer(text)
    args, kwargs = [], {}
    parameter_seek_till = [',']
    if allow_kwargs:
        parameter_seek_till.append('=')

    key = None
    while True:
        parameter, closing_token = lexer.seek_till(*parameter_seek_till)
        parameter = unquote_token(parameter)
        if closing_token == '=':
            key = parameter
            continue

        parameter = parameter.strip()
        if parameter:
            if key:
                kwargs[key] = parameter
                key = None
            else:
                args.append(parameter)
        if closing_token is None:
            break
    return args, kwargs

def parse_function_syntax(text):
    text = text.strip()
    match = re.match(r'(?P<func>[\w_]+)\s*\((?P<args>.*)\)', text)
    if not match:
        raise ValueError('Invalid function syntax: ' + text)

    result = match.groupdict()
    args = result['args']
    if args and args[0] == '"' and args[-1] == '"' and len(args) > 1:
        args = args[1:-1]
    return result['func'], args
