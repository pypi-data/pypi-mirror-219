import argparse
import os
import platform
import subprocess
import sys
import time
from typing import Dict, List, Union

import questionary
import select
from questionary import prompt, Choice

if sys.platform.startswith('win32'):
    import msvcrt


intro = '''
███    ███  ██████  ██████  ██    ██ ██      ███████     ██████     
████  ████ ██    ██ ██   ██ ██    ██ ██      ██               ██    
██ ████ ██ ██    ██ ██   ██ ██    ██ ██      █████        █████     
██  ██  ██ ██    ██ ██   ██ ██    ██ ██      ██          ██         
██      ██  ██████  ██████   ██████  ███████ ███████     ███████ 
                                                                    
    ██████  ██    ██ ████████ ██   ██  ██████  ███    ██            
    ██   ██  ██  ██     ██    ██   ██ ██    ██ ████   ██            
    ██████    ████      ██    ███████ ██    ██ ██ ██  ██            
    ██         ██       ██    ██   ██ ██    ██ ██  ██ ██            
    ██         ██       ██    ██   ██  ██████  ██   ████         
                                                                    
    ████████  █████  ███████ ██   ██     ██████  ██████              
       ██    ██   ██ ██      ██  ██           ██ ██   ██            
       ██    ███████ ███████ █████        █████  ███████            
       ██    ██   ██      ██ ██  ██      ██      ██   ██            
       ██    ██   ██ ███████ ██   ██     ███████ ██████ 
'''

# Determine the platform
current_platform = platform.system()

# Set the Python command based on the platform
if current_platform == 'Windows':
    python_command = 'python -m'
    bash_symbol = '$'
else:
    python_command = 'python3 -m'
    bash_symbol = '\$'

select_style = questionary.Style([
    #     ('default', "bg:#ffffff fg:#000000"),
    # ('selected', 'bg:#336699 fg:#ffffff'),
    ('highlighted', '#008888'),
    ('pointer', '#008888'),
    # ('question', 'fg:#009b06'),
    ('qmark', 'fg:#009b06'),
    ('instruction', "#008888"),
    ('answer', "#009b06"),
])

OPTIONS_ARGUMENTS = {
    'n': {
        'descr': 'n',
        'type': 'text',
        'message': 'What password length would you like to set?',
        'default': '8',
        'validation': lambda val: True if val.isdigit() else 'Please, provide a number',
    },
    'f': {
        'descr': 'f',
        'type': 'path',
        'message': 'Which file would you like to use?',
        'validation': lambda val: True if val else 'Please, provide a path to the file',
        'default': f'{os.path.dirname(os.path.abspath(__file__))}/pattern-list.txt',
        'filter': lambda val: f'"{val}"' if val else val,
    },
    'f_out': {
        'descr': 'f',
        'type': 'path',
        'message': 'In which file would you like to write generated passwords (it may be new)?',
        'validation': lambda val: True if val else 'Please specify the path to the file',
        'default': './pwd-lst.txt',
        'filter': lambda val: f'"{val}"' if val else val,
    },
    'f_log': {
        'descr': 'f',
        'type': 'path',
        'message': 'In which file would you like to write log messages (it may be new)?',
        'validation': lambda val: True if val else 'Please specify the path to the file',
        'default': './pwgen.log',
        'filter': lambda val: f'"{val}"' if val else val,
    },
    'f_err': {
        'descr': 'f',
        'type': 'path',
        'message': 'Which file would you like to use?',
        'validation': lambda val: True if val else 'Please, provide a path to the file',
        'default': f'{os.path.dirname(os.path.abspath(__file__))}/pattern-list-error.txt',
        'filter': lambda val: f'"{val}"' if val else val,
    },
    'c': {
        'descr': 'c',
        'type': 'text',
        'message': 'What amount of passwords would you like to get?',
        'default': '1',
        'validation': lambda val: True if val.isdigit() else 'Please, provide a number',
    },
    'p': {
        'descr': 'p',
        'type': 'confirm',
        'message': 'Would you like to permute passwords?',
        'default': False,
        'filter': lambda val: '-p' if val else '',
    },
    'v': {
        'descr': 'v',
        'type': 'text',
        'message': 'What logging level would you like to set?',
        'default': '0',
        'validation': lambda val: True if val.isdigit() else 'Please, provide a number',
        'filter': lambda val: f'{"-" if int(val) > 0 else ""}{"v" * (int(val) if int(val) <= 3 else 3)}',
    },
}

# OPTIONS: Dict[str, Dict[str, str | List[Dict] | Dict[str, Dict[str, str | List[Dict]]]]] = {
OPTIONS: Dict[str, Dict[str, Union[str, List[Dict], Dict[str, Dict[str, Union[str, List[Dict]]]]]]] = {
    'charset': {
        'descr': 'character sets',
        'options': {
            'charset_default': {
                'descr': 'default charset',
                'command': 'pwgen2 -n{} -c{} {}',
                'module_command': f'{python_command} pwgen2 -n{{}} -c{{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['n'], OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['v'], ],
            },
            'charset_custom': {
                'descr': 'custom charset based on default',
                'command': 'pwgen2 -S dp -n{} -c{} {}',
                'module_command': f'{python_command} pwgen2 -S dp -n{{}} -c{{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['n'], OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['v'], ],
            },
            'charset_additional': {
                'descr': 'custom charset with additional symbols',
                'command': f'pwgen2 -S "u\\@\\{bash_symbol}\\%\\&\\#\\*\\!" -n{{}} -c{{}} {{}}',
                'module_command': f'{python_command} pwgen2 -S "u\\@\\{bash_symbol}\\%\\&\\#\\*\\!" -n{{}} -c{{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['n'], OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['v'], ],
            },
            'charset_exclusions': {
                'descr': 'custom charset with exclusions',
                'command': 'pwgen2 -S "Ld^l^\\4^\\5^\\6^\\7^\\8" -n{} -c{} {}',
                'module_command': f'{python_command} pwgen2 -S "Ld^l^\\4^\\5^\\6^\\7^\\8" -n{{}} -c{{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['n'], OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['v'], ],
            },
        },
    },
    'pattern': {
        'descr': 'pattern-based approach',
        'options': {
            'pattern_default': {
                'descr': 'pattern based on a default charset',
                'command': 'pwgen2 -t uupllddL -c{} {} {}',
                'module_command': f'{python_command} pwgen2 -t uupllddL -c{{}} {{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['p'], OPTIONS_ARGUMENTS['v'], ],
            },
            'pattern_multiply': {
                'descr': 'pattern with placeholder multiplication',
                'command': 'pwgen2 -t u{{2}}p{{5}}l{{2}}d{{2}}L -c{} {} {}',
                'module_command': f'{python_command} pwgen2 -t u{{{{2}}}}p{{{{5}}}}l{{{{2}}}}d{{{{2}}}}L -c{{}} {{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['p'], OPTIONS_ARGUMENTS['v'], ],
            },
            'pattern_specific': {
                'descr': 'pattern with a specific symbol placeholder',
                'command': 'pwgen2 -t "u{{4}}d{{3}}\\-l{{2}}" -c{} {} {}',
                'module_command': f'{python_command} pwgen2 -t "u{{{{4}}}}d{{{{3}}}}\\-l{{{{2}}}}" -c{{}} {{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['p'], OPTIONS_ARGUMENTS['v'], ],
            },
            'pattern_custom_charset': {
                'descr': 'pattern with a custom charset placeholder',
                'command': 'pwgen2 -t u{{4}}[pd]{{3}}l{{2}} -c{} {} {}',
                'module_command': f'{python_command} pwgen2 -t u{{{{4}}}}[pd]{{{{3}}}}l{{{{2}}}} -c{{}} {{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['p'], OPTIONS_ARGUMENTS['v'], ],
            },
            'pattern_custom_charset_specific': {
                'descr': 'pattern with a custom charset with a specific symbol placeholder',
                'command': f'pwgen2 -t "u{{{{4}}}}[pd\\@\\{bash_symbol}\\%\\&\\#\\*\\!]{{{{3}}}}l{{{{2}}}}" -c{{}} {{}} {{}}',
                'module_command': f'{python_command} pwgen2 -t "u{{{{4}}}}[pd\\@\\{bash_symbol}\\%\\&\\#\\*\\!]{{{{3}}}}l{{{{2}}}}" -c{{}} {{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['p'], OPTIONS_ARGUMENTS['v'], ],
            },
            'pattern_custom_charset_exclusions': {
                'descr': 'pattern with a custom charset placeholder with exclusions',
                'command': 'pwgen2 -t "u{{4}}[Ld^l^\\4^\\5^\\6^\\7^\\8]{{3}}l{{2}}" -c{} {} {}',
                'module_command': f'{python_command} pwgen2 -t "u{{{{4}}}}[Ld^l^\\4^\\5^\\6^\\7^\\8]{{{{3}}}}l{{{{2}}}}" -c{{}} {{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['p'], OPTIONS_ARGUMENTS['v'], ],
            },
            'pattern_complex': {
                'descr': 'complex pattern',
                'command':
                    f'pwgen2 -t "u{{{{4}}}}\\-[Ld^l^\\4^\\5^\\6^\\7^\\8\\@\\{bash_symbol}\\%\\&\\#\\*\\!]{{{{3}}}}l{{{{2}}}}" -c{{}} {{}} {{}}',
                'module_command':
                    f'{python_command} pwgen2 -t "u{{{{4}}}}\\-[Ld^l^\\4^\\5^\\6^\\7^\\8\\@\\{bash_symbol}\\%\\&\\#\\*\\!]{{{{3}}}}l{{{{2}}}}" -c{{}} {{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['p'], OPTIONS_ARGUMENTS['v'], ],
            },
        },
    },
    'file': {
        'descr': 'pattern from a file',
        'command': 'pwgen2 -f {} -c{} {} {}',
        'module_command': f'{python_command} pwgen2 -f {{}} -c{{}} {{}} {{}}',
        'arguments': [OPTIONS_ARGUMENTS['f'], OPTIONS_ARGUMENTS['c'],
                      OPTIONS_ARGUMENTS['p'], OPTIONS_ARGUMENTS['v'], ],
    },
    'pipe': {
        'descr': 'pipes with the pwgen command',
        'options': {
            'pipe_stdin': {
                'descr': 'pipe stdin from a file',
                'command': 'cat {} | pwgen2 -c{} {} {}',
                'module_command': f'cat {{}} | {python_command} pwgen2 -c{{}} {{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['f'], OPTIONS_ARGUMENTS['c'],
                              OPTIONS_ARGUMENTS['p'], OPTIONS_ARGUMENTS['v'], ],
            },
            'pipe_stdout': {
                'descr': 'pipe stdout to a file',
                'command': 'pwgen2 -S "Ld^l^\\4^\\5^\\6^\\7^\\8" -n{} -c{} {} > {}',
                'module_command': f'{python_command} pwgen2 -S "Ld^l^\\4^\\5^\\6^\\7^\\8" -n{{}} -c{{}} {{}} > {{}}',
                'arguments': [OPTIONS_ARGUMENTS['n'], OPTIONS_ARGUMENTS['c'],
                              OPTIONS_ARGUMENTS['v'], OPTIONS_ARGUMENTS['f_out'], ],
            },
            'pipe_stderr': {
                'descr': 'pipe stderr to a file',
                'command': 'pwgen2 -S "Ld^l^\\4^\\5^\\6^\\7^\\8" {} 2> {}',
                'module_command': f'{python_command} pwgen2 -S "Ld^l^\\4^\\5^\\6^\\7^\\8" {{}} 2> {{}}',
                'arguments': [OPTIONS_ARGUMENTS['v'], OPTIONS_ARGUMENTS['f_log'], ],
            },
            'pipe_complex': {
                'descr': 'complex pipe with a sort command',
                'command': 'echo "u{{4}}d{{3}}\\-l{{2}}" | pwgen2 -c6 {} | sort -r',
                'module_command': f'echo "u{{{{4}}}}d{{{{3}}}}\\-l{{{{2}}}}" | {python_command} pwgen2 -c6 {{}} | sort -r',
                'arguments': [OPTIONS_ARGUMENTS['v'], ],
            },
        }
    },
    'with_errors': {
        'descr': 'patterns and character sets with errors',
        'options': {
            'charset_error': {
                'descr': 'custom charset with an error',
                'command': 'pwgen2 -S "Ld^lwkr^\\4^\\5^\\6^\\7^\\8" {}',
                'module_command': f'{python_command} pwgen2 -S "Ld^lwkr^\\4^\\5^\\6^\\7^\\8" {{}}',
                'arguments': [OPTIONS_ARGUMENTS['v'], ],
            },
            'pattern_error': {
                'descr': 'pattern with an error placeholder',
                'command': 'pwgen2 -t "{{5}}Ld^l^\\4^\\5^\\6^\\7^\\8" {}',
                'module_command': f'{python_command} pwgen2 -t "{{{{5}}}}Ld^l^\\4^\\5^\\6^\\7^\\8" {{}}',
                'arguments': [OPTIONS_ARGUMENTS['v'], ],
            },
            'file_error': {
                'descr': 'pattern with errors from a file',
                'command': 'pwgen2 -f {} {}',
                'module_command': f'{python_command} pwgen2 -f {{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['f_err'], OPTIONS_ARGUMENTS['v'], ],
            },
        }
    },
    'task2b': {
        'descr': 'special features pwgen ver.2',
        'options': {
            'new_default_charset': {
                'descr': 'extended default charset',
                'command': 'pwgen2 -n{} -c{} {}',
                'module_command': f'{python_command} pwgen2 -n{{}} -c{{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['n'], OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['v'], ],
            },
            'new_placeholders': {
                'descr': 'pattern with extended placeholders',
                'command': 'pwgen2 -t "\\H\\e\\x\\:\\ HHHHHH" -c{} {} {}',
                'module_command': f'{python_command} pwgen2 -t "\\H\\e\\x\\:\\ HHHHHH" -c{{}} {{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['p'], OPTIONS_ARGUMENTS['v'], ],
            },
            'mac_address': {
                'descr': 'pattern generates MAC addresses',
                'command': 'pwgen2 -t "HH\\-HH\\-HH\\-HH\\-HH\\-HH" -c{} {} {}',
                'module_command': f'{python_command} pwgen2 -t "HH\\-HH\\-HH\\-HH\\-HH\\-HH" -c{{}} {{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['p'], OPTIONS_ARGUMENTS['v'], ],
            },
            'choose_one': {
                'descr': 'pattern with a placeholder to choose from two',
                'command': f'pwgen2 -t "u{{{{4}}}}|[pd\\@\\{bash_symbol}\\%\\&\\#\\*\\!]{{{{3}}}}l{{{{2}}}}" -c{{}} {{}} {{}}',
                'module_command': f'{python_command} pwgen2 -t "u{{{{4}}}}|[pd\\@\\{bash_symbol}\\%\\&\\#\\*\\!]{{{{3}}}}l{{{{2}}}}" -c{{}} {{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['p'], OPTIONS_ARGUMENTS['v'], ],
            },
            'symbol_space': {
                'descr': 'pattern with a space character \\ ',
                'command': f'pwgen2 -t "u{{{{4}}}}[pd\\@\\{bash_symbol}\\%\\&\\ \\#\\*\\!]{{{{3}}}}\\ l{{{{2}}}}" -c{{}} {{}} {{}}',
                'module_command': f'{python_command} pwgen2 -t "u{{{{4}}}}[pd\\@\\{bash_symbol}\\%\\&\\ \\#\\*\\!]{{{{3}}}}\\ l{{{{2}}}}" -c{{}} {{}} {{}}',
                'arguments': [OPTIONS_ARGUMENTS['c'], OPTIONS_ARGUMENTS['p'], OPTIONS_ARGUMENTS['v'], ],
            },
        }
    },
}

questions = [
    {
        'type': 'select',
        'name': 'category',
        'message': 'Which password generation category would you like to choose?',
        'choices': [Choice(title=val['descr'], value=key) for key, val in OPTIONS.items()],
        'instruction': '(Use arrow keys to navigate through the menu)',
        'pointer': '>',
        'use_shortcuts': True,
        'style': select_style,
    },
    *[
        {
            'type': 'select',
            'name': key,
            'message': 'Which password generation approach would you like to choose?',
            'choices': [Choice(title=o_val['descr'], value=o_key) for o_key, o_val in val['options'].items()],
            'when': lambda x, key=key: x['category'] == key,
            'instruction': '(Use arrow keys to navigate through the menu)',
            'pointer': '>',
            'use_shortcuts': True,
            'style': select_style,
        } for key, val in OPTIONS.items() if 'options' in val
    ],
    *[
        {
            'type': a_val.get('type', 'text'),
            'name': f'{key}_{a_val.get("descr", "")}',
            'message': a_val.get('message', ''),
            'when': lambda x, key=key: x['category'] == key,
            'style': select_style,
            **({'filter': a_val['filter']} if 'filter' in a_val else {}),
            **({'validate': a_val['validation']} if 'validation' in a_val else {}),
            **({'default': a_val['default']} if 'default' in a_val else {}),
        }
        for key, val in OPTIONS.items() if 'options' not in val and 'arguments' in val
        for a_val in val['arguments']
    ],
    *[
        {
            'type': a_val.get('type', 'text'),
            'name': f'{o_key}_{a_val.get("descr", "")}',
            'message': a_val.get('message', ''),
            'when': lambda x, key=key, o_key=o_key: x.get(key, None) == o_key,
            'style': select_style,
            **({'filter': a_val['filter']} if 'filter' in a_val else {}),
            **({'validate': a_val['validation']} if 'validation' in a_val else {}),
            **({'default': a_val['default']} if 'default' in a_val else {}),
        }
        for key, val in OPTIONS.items() if 'options' in val
        for o_key, o_val in val['options'].items() if 'arguments' in o_val
        for a_val in o_val['arguments']
    ],
]


def wait_for_input(timeout):
    start_time = time.time()
    input_str = ""

    try:
        if sys.platform.startswith('win'):
            while True:
                if msvcrt.kbhit():
                    char = msvcrt.getwch()
                    if char == '\r':  # Check for Enter key
                        input_str += 'Enter'
                    else:
                        input_str += char
                    break
                elif time.time() - start_time >= timeout:
                    break
                time.sleep(0.1)  # Adjust the sleep duration as needed

        else:  # Unix-based systems (Linux, macOS)
            while True:
                # Check if there is input available to read
                if sys.stdin in select.select([sys.stdin], [], [], timeout)[0]:
                    char = sys.stdin.read(1)
                    if char == '\n':  # Check for Enter key
                        input_str += 'Enter'
                    else:
                        input_str += char
                    break
                elif time.time() - start_time >= timeout:
                    break
                time.sleep(0.1)  # Adjust the sleep duration as needed
    except KeyboardInterrupt:
        exit()

    return input_str.strip()


def print_output(command: str, main_message='According to your choice, the command to be invoked will be:') -> None:
    if not command:
        return

    print(f'\n{main_message}')
    questionary.print(f'{command}', style='#009b06')

    result = subprocess.run(command, capture_output=True, text=True, shell=True)

    if result.stdout and result.stdout.strip():
        print('\nThe output is:')
        questionary.print(f'{result.stdout.strip()}', style='#009b06')

    if result.stderr:
        print('\nThe log messages are:')
        questionary.print(f'{result.stderr}', style='#009b06')


def packet_output(command_key_name: str = 'command') -> None:
    command_packet = [
        *[
            (val.get('descr', ''),
             val.get(command_key_name, '').format(
                *[
                    arg.get('default', '') if 'filter' not in arg
                    else arg.get('filter', lambda x: '')(arg.get('default', ''))
                    for arg in val['arguments']
                ]),
            )
            if 'arguments' in val else val.get(command_key_name, '')
            for key, val in OPTIONS.items() if val.get(command_key_name, None)
        ],
        *[
            (o_val.get('descr', ''),
             o_val.get(command_key_name, '').format(
                *[
                    arg.get('default', '') if 'filter' not in arg
                    else arg.get('filter', lambda x: '')(arg.get('default', ''))
                    for arg in o_val['arguments']
                ]),
             )
            if 'arguments' in o_val else o_val.get(command_key_name, '')
            for key, val in OPTIONS.items() if 'options' in val
            for o_key, o_val in val['options'].items() if o_val.get(command_key_name, None)
        ]
    ]

    [print_output(el[1], el[0]) for el in command_packet]


def pwgen_showcase():
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description='Password Generator showcase')
    parser.add_argument('--all', action='store_true', help='Show all use cases at once without any interaction')
    parser.add_argument('-m', action='store_true', help='Invoke pwgen2 using python -m approach')
    args = parser.parse_args()

    command_key_name = 'module_command' if args.m else 'command'

    if args.all:
        packet_output(command_key_name)
        return

    delay = 0.3
    for line in intro.splitlines():
        print(line)

        if delay and wait_for_input(delay):
            delay = 0

    time.sleep(3.3 * delay)

    answers = prompt(questions)
    command = ''.join(
        [
            *[
                o_val.get(command_key_name, '').format(*[a_val for _, a_val in list(answers.items())[2:]])
                for key, val in OPTIONS.items() if key == answers.get('category', None) and 'options' in val
                for o_key, o_val in val['options'].items() if o_key == answers.get(key, None)
            ],
            *[
                val.get(command_key_name, '').format(*[a_val for _, a_val in list(answers.items())[1:]])
                for key, val in OPTIONS.items()
                if key == answers.get('category', None) and 'arguments' in val and command_key_name in val
            ],
        ]
    )

    print_output(command)


if __name__ == '__main__':
    pwgen_showcase()
