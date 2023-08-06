from googlesearch import search
from argparse import ArgumentParser

ARGS = (
    ('query', {
        'type': str,
        'help': 'Google Search query'
    }),
    ('--tld', {
        'type': str,
        'help': 'Top level domain',
        'default': 'com'
    }),
    ('--lang', {
        'type': str,
        'help': 'Results language'
    }),
    ('--tbs', {
        'type': str,
        'help': 'Time limits ("qdr:(h/d/m)")'
    }),
    ('--safe', {
        'type': str,
        'help': 'Safe search (on/off)',
        'choices': ('on', 'off'),
        'default': 'off'
    }),
    ('--num', {
        'type': int,
        'help': 'Result count',
        'default': 10
    })
)

def parseArguments(*args: tuple[str, dict]):
    argument_parser = ArgumentParser()

    for arg in args:
        argument_parser.add_argument(arg[0], **arg[1])

    input_args = argument_parser.parse_args().__dict__
    return input_args

def main():
    args = parseArguments(*ARGS)

    results = search(**args)

    for index in range(args['num']):
        try:print(f'{index+1}. {next(results)}')
        except: break