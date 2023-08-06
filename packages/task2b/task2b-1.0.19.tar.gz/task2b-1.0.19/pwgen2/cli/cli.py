import argparse
import sys
from typing import List

from pwgen2.pwgen2 import set_log_level, logger, generate_passwords


class Argument:
    def __init__(self, name, descr, metavar=None, type=None, default=None, action=None):
        self.name = name
        self.descr = descr
        self.metavar = metavar
        self.type = type
        self.default = default
        self.action = action
        self.help = f'{self.descr}{f" (default: {self.default})" if self.default else ""}'

    def to_argparse(self):
        return {key: val for key, val in vars(self).items() if key not in ('self', 'name', 'descr') and val is not None}


ARGUMENTS = {
    'n': Argument('Password length', 'Set length of password and generate random password from character sets',
                  metavar='', type=int, default=8),
    't': Argument('Password pattern', 'Set template for generating passwords', metavar='', type=str),
    'f': Argument('File with list of patterns', 'Get list of patterns from file and generate passwords for each pattern',
                  metavar='', type=str),
    'c': Argument('Number of passwords', 'Number of passwords to generate', metavar='', type=int, default=1),
    'S': Argument('Custom character set', 'Define custom character set', metavar='', type=str),
    'p': Argument('Permutation', 'Randomly permute characters of password', action='store_true'),
    'v': Argument('Verbosity level', 'Increase verbosity level', action='count', default=0),
}


def read_patterns_file(name: str) -> List[str]:
    try:
        logger.debug(f'Start reading a password pattern list from the {name} file.')

        with open(name, 'r') as f:
            patterns = f.read().splitlines()

        logger.info(f'{len(patterns)} patterns was read from the {name} file.')
    except Exception as e:
        logger.error(f'An error occurred while reading pattern list from the file: {e}')
        return []

    return patterns


def proceed_stdin() -> List[str]:
    if sys.stdin.isatty():
        return []

    return sys.stdin.read().strip().splitlines()


def pwgen_cli():
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description='Password Generator v.2')
    [parser.add_argument('-' + key, **ARGUMENTS[key].to_argparse()) for key, val in ARGUMENTS.items()]
    args = parser.parse_args()

    set_log_level(args.v)

    logger.info(f'Password generator has started as a standalone application.')
    [logger.debug(f'{ARGUMENTS[key].name}: {val}') for key, val in vars(args).items() if
     ARGUMENTS.get(key, None) is not None]

    stdin_patterns = proceed_stdin()
    args.t = ''.join(stdin_patterns[:1]) if len(stdin_patterns) == 1 else args.t

    if args.t:
        logger.debug(f'Let\'s generate passwords based on a given template with the following parameters:')
        [logger.debug(f'{ARGUMENTS[key].name}: {val}') for key, val in
         {'c': args.c, 't': args.t, 'p': args.p}.items() if ARGUMENTS.get(key, None) is not None]

        print('\n'.join(generate_passwords(length=args.n, count=args.c, template=args.t, permute=args.p)))
    elif args.f or len(stdin_patterns) > 1:
        patterns = stdin_patterns if len(stdin_patterns) > 1 else read_patterns_file(args.f)

        logger.debug(f'Let\'s generate passwords based on a list of patterns {patterns} from the file:')
        [logger.debug(f'{ARGUMENTS[key].name}: {val}')
         for key, val in {'c': args.c, 'n': args.n, 'p': args.p}.items()
         if ARGUMENTS.get(key, None) is not None]

        for i, pattern in enumerate(patterns):
            logger.debug(f'Pattern {i + 1}: {pattern}')

            print('\n'.join(generate_passwords(length=args.n, count=args.c, template=pattern, permute=args.p)))
    elif args.S:
        logger.debug(f'Let\'s generate passwords based on a custom character set:')
        [logger.debug(f'{ARGUMENTS[key].name}: {val}')
         for key, val in {'c': args.c, 'n': args.n, 'S': args.S, 'p': args.p}.items()
         if ARGUMENTS.get(key, None) is not None]

        print('\n'.join(generate_passwords(length=args.n, count=args.c, placeholders_set=args.S, permute=args.p)))
    else:
        logger.debug(f'Let\'s generate passwords based on a default character set:')
        [logger.debug(f'{ARGUMENTS[key].name}: {val}')
         for key, val in {'c': args.c, 'n': args.n, 'p': args.p}.items()
         if ARGUMENTS.get(key, None) is not None]

        print('\n'.join(generate_passwords(length=args.n, count=args.c, permute=args.p)))


if __name__ == '__main__':
    pwgen_cli()
