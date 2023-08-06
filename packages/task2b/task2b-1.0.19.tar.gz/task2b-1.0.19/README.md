<p align="center">
  <a href="https://gitlab.com/Bill-EPAM-DevOpsInt2023/devops-7-avramenko-bill">
    <img src="https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/ecd2eb07b44c03c4bcdf5493b45fe46238a12e14/shared/images/title-logo-origin.svg" alt="EPAM DevOps-7 Internal Lab title logo" width="100%" height="300px">
  </a>
</p>

<h1 align="center">
  <div align="center" aria-colspan="0">Password generator v2.</div>
  <div align="center" aria-colspan="0">Module 2: Python. Task 2B.</div>
</h1>

<p align="center">
  <div align="center">
    <a href="https://pypi.org/project/task2b/">
      <img src="https://img.shields.io/pypi/v/task2b.svg?style=for-the-badge&label=task 2b" alt="PYPI v." />
    </a>&nbsp;
    <a href="https://gitlab.com/Bill-EPAM-DevOpsInt2023/python/task2b/-/blob/783fe98d0c073fb7de18c872eb6b2d9dfbe81dbc/LICENSE">
      <img src="https://img.shields.io/pypi/l/task2b.svg?style=for-the-badge" alt="License" />
    </a>&nbsp;
    <a href="https://python-poetry.org/">
      <img src="https://img.shields.io/pypi/v/poetry.svg?style=for-the-badge&label=poetry&color=green" alt="License" />
    </a>&nbsp;
    <a href="https://www.python.org/downloads/">
      <img src="https://img.shields.io/pypi/pyversions/task2b?style=for-the-badge" alt="Python v." />
    </a>&nbsp;
  </div>
</p>


## Preface

This project contains a solution to one of the tasks of the EPAM DevOps Initial Internal Training Course #7 in 2023.
Detailed information about the course, as well as reports on each of the completed tasks (including this one) can be found [here](https://gitlab.com/Bill-EPAM-DevOpsInt2023/devops-7-avramenko-bill) [![/^](https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/45ed5458fe7cf837b62a423fcdff6a52b8db3cdb/shared/images/external-link-blue-12.png)](https://gitlab.com/Bill-EPAM-DevOpsInt2023/devops-7-avramenko-bill).
<br>
This project builds upon [task #2A](https://gitlab.com/Bill-EPAM-DevOpsInt2023/python/task2a)[![/^](https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/45ed5458fe7cf837b62a423fcdff6a52b8db3cdb/shared/images/external-link-blue-12.png)](https://gitlab.com/Bill-EPAM-DevOpsInt2023/python/task2a)
with some modifications specific to this task condition. Please review the [documentation](https://gitlab.com/Bill-EPAM-DevOpsInt2023/python/task2a/-/blob/b6da352d87b8c68783dd3dfa7d6f72538c24daaa/README.md)[![/^](https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/45ed5458fe7cf837b62a423fcdff6a52b8db3cdb/shared/images/external-link-blue-12.png)](https://gitlab.com/Bill-EPAM-DevOpsInt2023/python/task2a/-/blob/b6da352d87b8c68783dd3dfa7d6f72538c24daaa/README.md)
to familiarize yourself with these changes. Below you will find additional information on the new features in task #2B.

## Table of Contents

- [Task description](#task-description)
- [Detailed conditions](#detailed-conditions)
    - [Password generation additional function](#password-generation-additional-function)
- [Code description](#code-description)
- [Implementation](#implementation)
    - [Structure](#structure)
- [Installation](#installation)
- [Showcase](#showcase)
- [General Provisions](#general-provisions)

## Task description

The objective is to implement a password generator that returns whether a randomly generated password or password generated based on the passed template.
As part of this task, several features were added to a password generator that enables users to:
* use a space character as one of the symbols in a password
* use new placeholder '|' to randomly choose between two other placeholders
* utilize new character set placeholders

## Detailed conditions

Please review [main conditions](https://gitlab.com/Bill-EPAM-DevOpsInt2023/python/task2a#detailed-conditions)[![/^](https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/45ed5458fe7cf837b62a423fcdff6a52b8db3cdb/shared/images/external-link-blue-12.png)](https://gitlab.com/Bill-EPAM-DevOpsInt2023/python/task2a#detailed-conditions) from the task #2A.

#### Password generation additional function

Expand the placeholders set.

| Placeholder | Type                              | Character Set                                                                                                                          |
|-------------|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| a           | Lower-Case Alphanumeric           | abcdefghijklmnopqrstuvwxyz0123456789                                                                                                   |
| A           | Mixed-Case Alphanumeric           | ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789                                                                         |
| U           | Upper-Case Alphanumeric           | ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789                                                                                                   |
| h           | Lower-Case Hex Character          | 0123456789abcdef                                                                                                                       |
| H           | Upper-Case Hex Character          | 0123456789ABCDEF                                                                                                                       |
| v           | Lower-Case Vowel                  | aeiou                                                                                                                                  |
| V           | Mixed-Case Vowel                  | AEIOUaeiou                                                                                                                             |
| Z           | Upper-Case Vowel                  | AEIOU                                                                                                                                  |
| c           | Lower-Case Consonant              | bcdfghjklmnpqrstvwxyz                                                                                                                  |
| C           | Mixed-Case Consonant              | BCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz                                                                                             |
| z           | Upper-Case Consonant              | BCDFGHJKLMNPQRSTVWXYZ                                                                                                                  |
| b           | Bracket                           | ()[]{}<>                                                                                                                               |
| s           | Printable 7-Bit Special Character | !"#$%&\'()*+,-./:;<=>?@\[\\\]^_`{\|}~                                                                                                  |                                                               |
| S           | Printable 7-Bit ASCII             | A-Z, a-z, 0-9, !"#$%&'()*+,-./:;<=>?@\[\\\]^_`{\|}~                                                                                    |
| x           | Latin-1 Supplement                | Range \[U+00A1, U+00FF\] except U+00AD: ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ |
| \|          | Char Set or Char Set              | Allows you to randomly select one of two sets of characters to generate                                                                |


More examples:
<br>ddddd
<br>Generates for example: 41922, 12733, 43960, 07660, 12390, 74680, ...
<br>\H\e\x\:\ HHHHHH
<br>Generates for example: 'Hex: 13567A', 'Hex: A6B99D', 'Hex: 02243C', ...

###### Common password patterns:

| Name              | Pattern                  |
|-------------------|--------------------------|
| Hex Key - 40-Bit  | H{10}                    |
| Hex Key - 128-Bit | H{32}                    |
| Hex Key - 256-Bit | H{64}                    |
| MAC Address       | HH\-HH\-HH\-HH\-HH\-HH   |

Important! For all the following examples, you must enable the 'Randomly permute characters of password' option!

| Rule                                                                                                                        | Pattern                      |
|-----------------------------------------------------------------------------------------------------------------------------|------------------------------|
| Must consist of 10 alphanumeric characters, where at least 2 are upper-case  letters and at least 2 are lower-case letters. | uullA{6}                     |
| Must consist of 9 characters of the set "ABCDEF" and an '@' symbol.                                                         | \\@\[\\A\\B\\C\\D\\E\\F\]{9} |

## Code description
<small>* To better understand the gist, some segments of the actual code may be excluded or simplified in the following snippets.</small>

To meet the task conditions minor changes were made in the task #2A code. 
* Utilization new character set placeholders

```python 
CHARACTER_SETS = {
  'd': string.digits,  # Digits
  'l': string.ascii_lowercase,  # Small lateral ASCII
  'L': string.ascii_letters,  # Mixed-case lateral ASCII
  'u': string.ascii_uppercase,  # Big lateral ASCII
  'p': ',.;:',
}

EXTENDED_CHARACTER_SETS = {
  'a': string.ascii_lowercase + string.digits,
  'A': string.ascii_letters + string.digits,
  'U': string.ascii_uppercase + string.digits,
  'h': string.digits + 'abcdef',
  'H': string.digits + 'ABCDEF',
  'v': 'aeiou',
  'V': 'AEIOUaeiou',
  'Z': 'AEIOU',
  'c': 'bcdfghjklmnpqrstvwxyz',
  'C': 'BCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz',
  'z': 'BCDFGHJKLMNPQRSTVWXYZ',
  'b': '()[]{}<>',
  's': '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~',
  'S': string.ascii_lowercase + string.ascii_uppercase + string.digits + '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~',
  'x': '¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ',
}

CHARACTER_SETS |= EXTENDED_CHARACTER_SETS 
```
* Utilization a space character as one of the symbols in a password
Just one check condition was commented.

```python 
def generate_password_from_pattern(pattern: str) -> str:
  if type(pattern) is not str:  # Initial checks
    logger.error(f'Incorrect pattern {pattern}. String expected.')
    return ''
  elif not pattern:
    logger.error(f'Pattern cannot be empty')
    return ''
  # elif pattern.find(' ') != -1:
  #     logger.error(f'You cannot use space symbol in pattern ({pattern})')
```
* New code snippet was added to handle the placeholder '|' (to randomly choose between two other placeholders).

```python 
# Multiply previous element while tuples present in the list

if any(pat_ls) and (pat_ls[:1] == '|' or pat_ls[-1] == '|'):
  logger.error(f'The "|" placeholder is not allowed at the beginning or end of the pattern ({pattern}).')
  return ''

if any([val for ind, val in enumerate(pat_ls)
        if val == '|' and ind + 1 < len(pat_ls) and pat_ls[ind + 1] == '|']):
  logger.error(f'The pattern ({pattern}) has an error as the "|" placeholder cannot go in a row.')
  return ''

# Let's proceed random selection between two placeholders via | (for instance, l|H or l|[daA])
pat_ls = [random.choice([val, pat_ls[ind + 2]]) if ind + 2 < len(pat_ls) and pat_ls[ind + 1] == '|' else val
          for ind, val in enumerate(pat_ls) if not(val == '|' or pat_ls[ind - 1] == '|')]

# Replace placeholders to character sets
```

First of all, additional checks were added. The | placeholder is not allowed to be placed at the start or end of the pattern,
because it must be situated between two placeholders to ensure random selection. Additionally, placing consecutive | placeholders is prohibited.
Following preliminary checks, three-placeholder sequences such as l|H or l|\[daA\] are proceeds in a pattern.
A single placeholder is selected randomly and replaces the three originally present.

## Implementation

[Pwgen](https://pypi.org/project/task2b/)[![/^](https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/45ed5458fe7cf837b62a423fcdff6a52b8db3cdb/shared/images/external-link-blue-12.png)](https://pypi.org/project/task2b/)
is a Python package that could be added to your global or virtual environment by preferable package manager pip, pipenv, poetry, etc.
The project itself was managed and built using the [Poetry library](https://python-poetry.org/)[![/^](https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/45ed5458fe7cf837b62a423fcdff6a52b8db3cdb/shared/images/external-link-blue-12.png)](https://python-poetry.org/),
so if you intend to clone this repo and make some changes for your own purposes, please install [Poetry](https://python-poetry.org/docs/#installation)[![/^](https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/45ed5458fe7cf837b62a423fcdff6a52b8db3cdb/shared/images/external-link-blue-12.png)](https://python-poetry.org/docs/#installation)
or migrate to your preferred package management library.

Based on the need to build and the possibility of using both the library and the CLI, the code was split into a library for importing and a script for execution
via the command line. Additionally, the package contains a showcase that demonstrates all use cases when run through the command line.

To enhance the command line's functionality and expand showcase capabilities, the [Questionary](https://questionary.readthedocs.io/en/stable/)[![/^](https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/45ed5458fe7cf837b62a423fcdff6a52b8db3cdb/shared/images/external-link-blue-12.png)](https://questionary.readthedocs.io/en/stable/)
library is used and will be installed through a dependency link upon package installation.

### Structure

```markdown
task_2b/
├── README.md (You are here now)
├── task_2b.toml # Poetry package management file
└── pwgen2/ (Module 1. Git)
    ├── __init__.py # library entry point
    ├── __main__.py # CLI entry point
    ├── __version__.py 
    ├── pwgen2.py # library implementation
    ├── cli/
    │   ├── __init__.py
    │   ├── __main__.py
    │   └── cli.py # CLI code implementation
    │
    └── showcase/
        ├── __init__.py 
        ├── __main__.py # showcase entry point when using python -m showcase
        ├── pattern-list.txt # input pattern examples file 
        ├── pattern-list-error.txt # input pattern examples file with intentional errors
        └── showcase.py # showcase implementation
```

## Installation

To install pwgen2 packet please follow the [instruction](https://gitlab.com/Bill-EPAM-DevOpsInt2023/python/task2a#installation)[![/^](https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/45ed5458fe7cf837b62a423fcdff6a52b8db3cdb/shared/images/external-link-blue-12.png)](https://gitlab.com/Bill-EPAM-DevOpsInt2023/python/task2a#installation)
from the previous task #2A. You should only change name of the packet from `task2a` to `task2b`.
Also, you should call now `pwgen2` instead of pwgen and `pwgen2_showcase` instead of pwgen_showcase. Or if you need to invoke CLI or showcase from the module, invoke them
like `python -m pwgen2` or `python3 -m pwgen2` and `python -m pwgen2.showcase` or `python3 -m pwgen2.showcase`.
 
## Showcase

To showcase the behavior of the pwgen library, an interactive command called "pwgen_showcase" has been created.
This command utilizes both the pwgen CLI and the pwgen library. It's an interactive command you can invoke via `pwgen2_showcase` or `python -m pwgen2.showcase` or `python3 -m pwgen2.showcase`.
It has an optional flag that allows you to view all use cases at once without any interaction.
You can use the command `pwgen2_showcase --all` to activate this feature.

A new part (special features pwgen ver.2), which includes additional use case examples, was added.
Additionally, the "pattern-list.txt" file was updated with new patterns.

![showcase_demo.gif](https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/20f3d559b93c5ff9a7e8ca7780e6f4b23dfc8f85/m2-python/task-2b/images/showcase_demo_task2b.gif)

## General provisions

All materials provided and/or made available contain EPAM’s proprietary and confidential information and must not to be copied,
reproduced or disclosed to any third party or to any other person, other than those persons who have a bona fide need to review it
for the purpose of participation in the online courses being provided by EPAM.
The intellectual property rights in all materials (including any trademarks) are owned by EPAM Systems Inc or its associated companies,
and a limited license, terminable at the discretion of EPAM without notice, is hereby granted to you solely for the purpose of participating
in the online courses being provided by EPAM. Neither you nor any other party shall acquire any intellectual property rights of any kind
in such materials.


