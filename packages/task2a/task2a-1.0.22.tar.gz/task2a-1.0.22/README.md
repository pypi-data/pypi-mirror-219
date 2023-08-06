<p align="center">
  <a href="https://gitlab.com/Bill-EPAM-DevOpsInt2023/devops-7-avramenko-bill">
    <img src="https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/ecd2eb07b44c03c4bcdf5493b45fe46238a12e14/shared/images/title-logo-origin.svg" alt="EPAM DevOps-7 Internal Lab title logo" width="100%" height="300px">
  </a>
</p>

<h1 align="center">
  <div align="center" aria-colspan="0">Password generator.</div>
  <div align="center" aria-colspan="0">Module 2: Python. Task 2A.</div>
</h1>

<p align="center">
  <div align="center">
    <a href="https://pypi.org/project/task2a/">
      <img src="https://img.shields.io/pypi/v/task2a.svg?style=for-the-badge&label=task 2a" alt="PYPI v." />
    </a>&nbsp;
    <a href="https://gitlab.com/Bill-EPAM-DevOpsInt2023/python/task2a/-/blob/783fe98d0c073fb7de18c872eb6b2d9dfbe81dbc/LICENSE">
      <img src="https://img.shields.io/pypi/l/task2a.svg?style=for-the-badge" alt="License" />
    </a>&nbsp;
    <a href="https://python-poetry.org/">
      <img src="https://img.shields.io/pypi/v/poetry.svg?style=for-the-badge&label=poetry&color=green" alt="License" />
    </a>&nbsp;
    <a href="https://www.python.org/downloads/">
      <img src="https://img.shields.io/pypi/pyversions/task2a?style=for-the-badge" alt="Python v." />
    </a>&nbsp;
  </div>
</p>


## Preface

This project contains a solution to one of the tasks of the EPAM DevOps Initial Internal Training Course #7 in 2023.
Detailed information about the course, as well as reports on each of the completed tasks (including this one) can be found [here](https://gitlab.com/Bill-EPAM-DevOpsInt2023/devops-7-avramenko-bill) [![/^](https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/45ed5458fe7cf837b62a423fcdff6a52b8db3cdb/shared/images/external-link-blue-12.png)](https://gitlab.com/Bill-EPAM-DevOpsInt2023/devops-7-avramenko-bill).
<br>
As mentioned above, the project contains a solution to task #2A as part of module #2 of learning the Python programming language.
Below you will find a detailed description of the task, as well as a brief description of the implementation.

## Table of Contents

- [Task description](#task-description)
- [Detailed conditions](#detailed-conditions)
    - [Generation Based on Character Sets](#generation-based-on-character-sets)
    - [Generation Based on Patterns](#generation-based-on-patterns)
    - [CLI interface arguments](#cli-interface-can-support-next-commands)
- [Code description](#code-description)
- [Implementation](#implementation)
    - [Structure](#structure)
- [Installation](#installation)
- [Usage](#usage)
    - [Library](#library)
    - [CLI](#cli)
    - [Pipes and files](#pipes-and-files)
    - [Showcase](#showcase)
- [General Provisions](#general-provisions)

## Task description

The main goal is to implement a password generator that returns whether a randomly generated password or password generated based on the passed template.

## Detailed conditions

Write a utility for generating passwords according to a given template that supports the CLI interface,
be able to work in PIPE and logging (-vvv – show detailed information during processing).

This password generation app should be implements two ways to generate random passwords:
- the random method (a password of a given length is randomly generated from a set of
  characters);
- the pattern-based generation method is used if passwords follow special rules or fulfill certain
  conditions.

#### Generation Based on Character Sets

Generation based on a character set is very simple. You simply let Password Gen know which characters
can be used (e.g. upper-case letters, digits, ...) and Password Gen will randomly pick characters out of the
set.

###### Defining a character set:

The character set can be defined directly in the argument line. For convenience, PasswordGen offers to add
commonly used ranges of characters to the set. This is done by chouse the appropriate optional in the
argument line. Additionally, to these predefined character ranges, you can specify characters manually: all
characters that you enter in the value of the -S option will be directly added to the character set.

###### Character sets are sets:

In mathematical terms, character sets are sets, not vectors. This means that characters cannot be added
twice to the set. Either a character is in the set or it is not.   
For example, if you enter 'AAAAB' into the value of -S option argument line, this is exactly the same set as
'AB'. 'A' will not be 4 times as likely as 'B'! If you need to follow rules like 'character A is more likely than B',
you must use pattern-based generation + permuting password characters.  
Password Gen will 'optimize' your character set by removing all duplicate characters. If you'd enter the
character set 'AAAAB' into the value of -S optional argument line, the password generator, should be
optimized to the shorter character set 'AB'. Similarly, if you set the '\d' optional check box and enter '3' into
the value of the '-S' option, '3' will be ignored because it is already included in the 'Digits' character range.

###### Supported characters:

All Unicode characters in the ranges [U+0001, U+D7FF] and [U+E000, U+FFFF] except { U+0009 / '\t', U+000A
/ '\n', U+000D / '\r' } are supported. Characters in the range [U+010000, U+10FFFF] (which need to be
encoded in UTF-16 using surrogate pairs from [0xD800, 0xDFFF]) are not supported. Subsequent processing
of passwords may have further limitations (for example, the character U+FFFF is forbidden in XML files and
will be replaced or removed).

#### Generation Based on Patterns

The password generator can create passwords using patterns. A pattern is a string defining the layout of
the new password. The following placeholders are supported:

<span id="placeholders"/>

| Placeholder | Type                | Character Set                                         |
|-------------|---------------------|-------------------------------------------------------|
| d           | Digit               | 0123456789                                            |
| l           | Lower-Case Letter   | abcdefghijklmnopqrstuvwxyz                            |
| L           | Mixed-Case Letter   | ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz |
| u           | Upper-Case Letter   | ABCDEFGHIJKLMNOPQRSTUVWXYZ                            |
| p           | Punctuation         | ,.;:u                                                 |
| \           | Escape (Fixed Char) | Use following character as is.                        |                                   |
| {n}         | Escape (Repeat)     | Repeat the previous placeholder n times.              |
| [...]       | Custom Char Set     | Define a custom character set.                        |

The \ placeholder is special: it's an escape character. The next character that follows the \ is written directly
into the generated password. If you want a \ in your password at a specific place, you must write \\.

Using the {n} code you can define how many times the previous placeholder should occur. The { } operator duplicates
placeholders, not generated characters. Examples:
- d{4} is equivalent to dddd,
- dL{4}a is equivalent to dLLLLa and
- udl{1}du is equivalent to udldu.

The [...] notation can be used to define a custom character set, from which the password generator will pick one
character randomly. All characters between the '[' and ']' brackets follow the same rules as the placeholders above.
The '^' character removes the next placeholders from the character set. Examples:
- [dp] generates exactly 1 random character out of the set digits + punctuation,
- [d\m\\@^\3]{5} generates 5 characters out of the set "012456789m@",
- [u\\_][u\\_] generates 2 characters out of the set upper-case + '_'.

###### More examples:

ddddd => generates for example: 41922, 12733, 43960, 07660, 12390, 74680, ...  
u{4}d{3}\-l{2} => DHRF345-st  
u{4}[dl]{3}\-l{2} => DHRF3s4-st | FHGFds4-vt | DERS774-sd

###### Generating Passwords that Follow Rules

Below are some examples of how the pattern generator can be used to generate passwords that follow certain rules.
Important! For all the following examples you must enable the 'Randomly permute characters of password' option (-p)!

| Rule                                                                                                | Pattern   |
|-----------------------------------------------------------------------------------------------------|-----------|
| Must consist of 2 upper-case letters, 2 lower-case letters and 2 digits.                            | uullddd   |
| Must consist of 9 digits and 1 letter.                                                              | d{9}L     |
| Must consist of 10 alphanumeric characters, where at least 1 is a letter and at least 1 is a digit. | ld[Ld]{8} |

#### CLI interface can support next commands:

- n: Set length of password and generate random password from set {small lateral ASCII, big lateral ASCII,
  digit}
- t: Set template for generate passwords
- f: Getting list of patterns from file and generate for each random password
- c: number of passwords
- vvv: Verbose mode (-v |-vv |-vvv )
- h: help
- S: character set
- p: Randomly permute characters of password

**Output:** Can be support pipe redirect (output must view by formatted column or table).

## Code description
<small>* To better understand the gist, some segments of the actual code may be excluded or simplified in the following snippets.</small>

To describe the solution of the task in general terms, the following sequence of actions happens:
- transform the template into a set of placeholders
- transform the set of placeholders into a set of characters
- select a random character from the list of characters repeatedly until the password reaches the desired length
- if necessary permute the characters in the password, then randomly select symbols to shuffle them

```python 
def generate_passwords(length: int = 8, count: int = 1, template: Optional[str] = None,
                       placeholders_set: Optional[str] = None, permute: Optional[bool] = False) -> List[str]:
    # Library entry point 

def generate_password_from_pattern(pattern: str) -> str:
    # Transform pattern to the list placeholders set

def generate_character_set(placeholders: str) -> Optional[str]:
    # Transform placeholders set to character set

def generate_password_from_character_set(character_set: str, length: int = 1) -> str:
    # Randomly choose as mach symbols as it needs bases on a password length  
```

The process of transformation, whether a template or placeholder-based generation follows some simple steps.
- split template or placeholder-based string to a list of single placeholder elements
- multiply on n the previous element if a special placeholder like [{n}](#placeholders) is present
- convert placeholder set to a character set, using for this set type to avoid duplication of characters
- exclude some character sets or a particular character from the character set

```python 
pat_ls = split_pattern(n_pattern)

while any([el for el in pat_ls if <...list contains {n} placeholder ...>]):  # Multiply previous element while tuples present in the list
  pat_ls = [dup for i, el in enumerate(pat_ls)
            for dup in ([pat_ls[i - 1]] * el[0] if type(el) is tuple and type(pat_ls[i - 1]) is str else [el])]

pat_ls = [generate_character_set(el) for el in pat_ls]  # Replace placeholders to character sets
```

If there is a need to create a password using the designated placeholders, we execute our algorithm at a lower level.
Ultimately, the process comes down to randomly selecting characters from a list and repeating it until the desired password length is achieved.

```python 
def generate_password_from_character_set(length: int, character_set: str) -> str:
    password = ''.join(random.choice(character_set) for _ in range(length))
    return password 
```

The character set can be formed both on the basis of `CHARACTER_SETS` dictionary (by default, all placeholders from this dictionary are used),
and on the basis of explicitly specified characters by using a special symbol in front of them [\\](#placeholders).

```python 
CHARACTER_SETS = {
  'd': string.digits,  # Digits
  'l': string.ascii_lowercase,  # Small lateral ASCII
  'L': string.ascii_letters,  # Mixed-case lateral ASCII
  'u': string.ascii_uppercase,  # Big lateral ASCII
  'p': ',.;:',
}
```

When considering the implementation required to fulfill the conditions for the application to operate as a [CLI](#cli-interface-can-support-next-commands)
with a list of incoming arguments also, it can be seen that the task algorithm is wrapped by a wrapper.

```python 
def main():
  parser = argparse.ArgumentParser(description='Password Generator')
  [parser.add_argument('-' + key, **ARGUMENTS[key].to_argparse()) for key, val in ARGUMENTS.items()]
  args = parser.parse_args()

  if args.t:
    generate_passwords(length=args.n, count=args.c, template=args.t, permute=args.p)
  elif args.f:
    for i, pattern in enumerate(patterns):
      generate_passwords(length=args.n, count=args.c, template=pattern, permute=args.p)
  elif args.S:
    generate_passwords(length=args.n, count=args.c, placeholders_set=args.S, permute=args.p)
  else:
    generate_passwords(length=args.n, count=args.c, permute=args.p)
```

###### Examining the template transformation algorithm through an example

Let's examine the template transformation behavior with the following example `u{2}p{5}l{2}d{2}L\-[Ld^l^\4^\5^\6^\7^\8\@\$\%\&\#\*\!]{3}`.

**Step #1:** Separate the template into individual placeholders, while keeping elements like {n}, \<some character>, or [...] intact for the future list.
The result will be a list of `['u', '{2}', 'p', '{5}', 'd', '{2}', 'L', '\-', '[Ld^l^\4^\5^\6^\7^\8\@\$\%\&\#\*\!]', '{3}']`.

```python
t = ''
for el in list(pattern):
    if el in '[{\\' and not t:
        t = el
    elif el in '}]' or t == '\\':
        t += el
        split_list.append(t)
        t = ''
    elif t:
        t += el
    else:
        split_list.append(el)
```

**Step #2:** Multiply previous elements when {n} element occurs by n. The result will be a list of `['u', 'u', 'p', 'p', 'p', 'p', 'p', 'd', 'd', 'L', '\-', '[Ld^l^\4^\5^\6^\7^\8\@\$\%\&\#\*\!]', '[Ld^l^\4^\5^\6^\7^\8\@\$\%\&\#\*\!]', '[Ld^l^\4^\5^\6^\7^\8\@\$\%\&\#\*\!]']`  
<br>**Step #3:** Replace all the elements with a character set using [the placeholder set transformation algorithm](#examining-the-placeholder-set-transformation-algorithm-through-an-example).
For \<some character> elements just omit the \ symbol and leave <some character>. The result will be a list of

```python
[
  'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
  'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
  ',.;:',
  ',.;:',
  ',.;:',
  ',.;:',
  ',.;:',
  '0123456789',
  '0123456789',
  'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
  '-',
  'ABCDEFGHIJKLMNOPQRSTUVWXYZ01239@$%&#*!',
  'ABCDEFGHIJKLMNOPQRSTUVWXYZ01239@$%&#*!',
  'ABCDEFGHIJKLMNOPQRSTUVWXYZ01239@$%&#*!'
]`
````
<br>**Step #4:** Randomly choose one character from a character set for each element of the list and join the list. The final result will be a string like `'BA,.,:.43g-F$W'`.

###### Examining the placeholder set transformation algorithm through an example

Let's examine the placeholder set transformation behavior with the following example `Ld^l^\4^\5^\6^\7^\8\@\$\%\&\#\*\!d`.

**Step #1:** Separate the placeholders string into individual placeholders, while keeping elements like \<some character>, ^<some placeholder> or ^\<some character> intact for the future list.
The result will be a list of `['L', 'd', '^l', '^\4', '^\5', '^\6', '^\7', '^\8', '\@', '\$', '\%', '\&', '\#', '\*', '\!', 'd']`.

```python
t = ''
for el in list(placeholders):
    if el in '^\\' and not t:
        t = el
    elif t == '^' and el == '\\':
        t += el
    elif t == '^' or t == '\\' or t == '^\\':
        t += el
        split_list.append(t)
        t = ''
    else:
        split_list.append(el)
```

**Step #2:** Replace placeholders with character sets and decouple list to two lists - the first one for included characters and the second one for excluded characters.
Included character list
```python
[
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
    '0123456789',
    '@',
    '$',
    '%',
    '&',
    '#',
    '*',
    '!',
    '0123456789',
]
```
Excluded character list will be
```python
[
    'abcdefghijklmnopqrstuvwxyz',
    '4',
    '5',
    '6',
    '7',
    '8',
]
```

**Step #3:** Convert lists to sets of characters to eliminate the repetitions.
Included character set will be
```python
{
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
    'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '@', '$',
    '%', '&', '#', '*', '!',  
}
```
Excluded character set will be
```python
{
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '4', '5', '6', '7', '8',
}
```

**Step #4:** Subtract the excluded character set from the included character set to leave the differences of them and join it to the string.
```python
character_set -= excluded_character_set

return ''.join(str(c) for c in character_set)
```
The differences and the final string will be
```python
{
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '9',
    '@', '$', '%', '&', '#', '*', '!',
}

''.join(str(c) for c in character_set)  # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ012349@$%&#*!'
```

## Implementation

[Pwgen](https://pypi.org/project/task2a/)[![/^](https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/45ed5458fe7cf837b62a423fcdff6a52b8db3cdb/shared/images/external-link-blue-12.png)](https://pypi.org/project/task2a/)
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
task_2a/
├── README.md (You are here now)
├── task_2a.toml # Poetry package management file
└── pwgen/ (Module 1. Git)
    ├── __init__.py # library entry point
    ├── __main__.py # CLI entry point
    ├── __version__.py 
    ├── pwgen.py # library implementation
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

Use your preferred installation method via different package installation managers to install Pwgen.

###### Pip

To install Pwgen packet to your environment using pip manager invoke `pip install task2a`.

```bash
$ pip install task2a
Collecting task2a
  Using cached task2a-0.1.N-py3-none-any.whl (10 kB)
Collecting questionary<2.0.0,>=1.10.0 (from task2a)
  Downloading questionary-1.10.0-py3-none-any.whl (31 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 31.1/31.1 kB N.N MB/s eta 0:00:00
Collecting prompt_toolkit<4.0,>=2.0 (from questionary<2.0.0,>=1.10.0->task2a)
  Downloading prompt_toolkit-3.0.39-py3-none-any.whl (385 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 385.2/385.2 kB N.N MB/s eta 0:00:00
Requirement already satisfied: wcwidth in <your environment folder>\.venv\lib\site-packages (from prompt_toolkit<4.0,>=2.0->questionary<2.0.0,>=1.10.0->task2a) (0.2.6)
Installing collected packages: prompt_toolkit, questionary, task2a
Successfully installed prompt_toolkit-3.0.39 questionary-1.10.0 task2a-0.1.N
```

To uninstall Pwgen from your environment invoke `pip uninstall task2a`.

```bash
$ pip uninstall task2a
Found existing installation: task2a 0.1.N
Uninstalling task2a-0.1.N:
  Would remove:
    <your environment folder>\.venv\lib\site-packages\task2a-0.1.N.dist-info\*
    <your environment folder>\.venv\lib\site-packages\task2a\*
    <your environment folder>\.venv\scripts\pwgen.exe
    <your environment folder>\.venv\scripts\pwgen_showcase.exe
Proceed (Y/n)? y
  Successfully uninstalled task2a-0.1.N
```

It's important to note that the pip manager does not uninstall dependent packages. Therefore, if you wish to remove them, you'll need to take
the initiative and perform the task yourself. You can do this by using the commands `pip uninstall questionary` and `pip uninstall prompt-toolkit`.

```bash
$ pip uninstall questionary
Found existing installation: questionary 1.10.0
Uninstalling questionary-1.10.0:
  Would remove:
    <your environment folder>\.venv\lib\site-packages\questionary-1.10.0.dist-info\*
    <your environment folder>\.venv\lib\site-packages\questionary\*
Proceed (Y/n)? y
  Successfully uninstalled questionary-1.10.0
```

```bash
$ pip uninstall prompt-toolkit
Found existing installation: prompt-toolkit 3.0.39
Uninstalling prompt-toolkit-3.0.39:
  Would remove:
    <your environment folder>\.venv\lib\site-packages\prompt_toolkit-3.0.39.dist-info\*
    <your environment folder>\.venv\lib\site-packages\prompt_toolkit\*
Proceed (Y/n)? y
  Successfully uninstalled prompt-toolkit-3.0.39
```

###### Poetry

To install Pwgen packet to your environment using poetry manager invoke `poetry add task2a`.

```bash
$ poetry add task2a
Using version ^0.1.N for task2a

Updating dependencies
Resolving dependencies...

Package operations: 4 installs, 0 updates, 0 removals

  • Installing wcwidth (0.2.6)
  • Installing prompt-toolkit (3.0.39)
  • Installing questionary (1.10.0)
  • Installing task2a (0.1.N)

Writing lock file
```

By taking this action, a new dependency line will be added to your <project name>.toml file.

```toml
[tool.poetry.dependencies]
task2a = "^0.1.N"
```

To uninstall Pwgen from your environment invoke `poetry remove task2a`.
One of the benefits of utilizing Poetry is that it allows for the removal of all dependent packages with a single command.

```bash
$ poetry remove task2a
Updating dependencies
Resolving dependencies...

Package operations: 0 installs, 0 updates, 4 removals

  • Removing prompt-toolkit (3.0.39)
  • Removing questionary (1.10.0)
  • Removing task2a (0.1.N)
  • Removing wcwidth (0.2.6)

Writing lock file
```

## Usage

There are various ways to use this library, as mentioned earlier.
- Utilize it like a library you can just import it into your .py file and use generate password methods within your code.
- Utilize CLI via the command shell, either as a Python module or as a standalone command.
- Utilize CLI command in a pipe by passing stdout of other commands to the stdin of the pwgen command, writing stdout and stderr to files, or passing them to following commands.
- The library contains rich showcase command that allows you to test all the use cases and even perform them in batches.


#### Library

Below is a code snippet that demonstrates how to be able to use the pwgen library in your code.

```python
import logging
from task2a.pwgen import generate_passwords

class User:
    def __init__(self, login: str, name: str, surname:str, department:Optional[str] = None, phone:Optional[str] = None,
                 one_time_pwd: bool = False, pw_charset:Optional[str] = None, pw_template:Optional[str] = None):
        self.login = login
        self.name = name
        self.surname = surname
        self.department = department
        self.phone = phone
        if one_time_pwd:
            if  pw_charset:
                self.password = generate_passwords(placeholders_set=pw_charset)
            elif pw_pattern:
                self.password = generate_passwords(template=pw_template)
            else:
                self.password = generate_passwords()
        
# Interactively gather user information
login = input("Enter login: ")
name = input("Enter name: ")
surname = input("Enter surname: ")
department = input("Enter department: ")
phone = input("Enter phone: ")

# Create an instance of the User class
user = User(login, name, surname, department, phone)
```
#### CLI

The CLI interface has a single command called "pwgen." It can be invoked using two methods: `python -m pwgen` or simply `pwgen`.
Pwgen accepts various arguments, which are described in the "ARGUMENT" dictionary.

```python
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
```

There are some rules for argument handling:
- if you pass argument -f, the -t and -S arguments will be ignored
- if you pass argument -t, the -S arguments will be ignored
- if no -f, -t, -S arguments are passed, passwords are generated based on the default character set

When using input files or stdin via the pipe, it's important to pass patterns or lists of patterns only (avoid character sets and other variations).
Each line in the file will be treated as one pattern.

To handle the arguments, the [argparse](https://docs.python.org/3/library/argparse.html)[![/^](https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/45ed5458fe7cf837b62a423fcdff6a52b8db3cdb/shared/images/external-link-blue-12.png)](https://docs.python.org/3/library/argparse.html)
module is used. If you are already acquainted with it, you will have no difficulty in passing the arguments along with their values and comprehending their behavior.

Here is an example list of CLI using, more examples in a more convenient form you could find in the [showcase](#showcase):

| Call example                                                             | Outcome explanation                                                                                                                                                                             |
|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `pwgen` or `python -m pwgen`                                             | One eight-character (default value) password will be generated based on the default character set.                                                                                              |
| `pwgen -n5` or `pwgen -n 5`                                              | One five-character password will be generated based on the default character set.                                                                                                               |
| `pwgen -c3`                                                              | Three eight-character passwords will be generated based on the default character set.                                                                                                           |
| `pwgen -n5 -c3 -p`                                                       | Three five-character passwords will be generated based on the default character set and permutate.                                                                                              |
| `pwgen -n5 -c3 -v`                                                       | Three five-character passwords will be generated based on the default character set. Warning messages will also be displayed during the generation.                                             |
| `pwgen -n5 -c3 -vv`                                                      | Three five-character passwords will be generated based on the default character set. Warning and info messages will also be displayed during the generation.                                    |
| `pwgen -n5 -c3 -vvv`                                                     | Three five-character passwords will be generated based on the default character set. All types of messages will be displayed during the generation.                                             |
| `pwgen -f .venv/Lib/site-packages/pwgen/test/pattern-list.txt`           | N passwords (based on text lines in the file) will be generated based on each line given template. Pattern length sets the password length.                                                     |
| `pwgen -f .venv/Lib/site-packages/pwgen/test/pattern-list.txt -n5 -c3`   | N * 3 passwords will be generated based on each line given template. The -n flag will be ignored.                                                                                               |
| `pwgen -t u{2}p{5}l{2}d{2}L -n5 -c3 -p`                                  | Three passwords will be generated based on a given template and will be permutate after the generation. The -n flag will be ignored.                                                            |
| `pwgen -S Ld^l^\\4^\\5^\\6^\\7^\\8 -n5 -c3`                              | Three five-character passwords will be generated based on the given character set. (Please note that in certain cases, you may need to double the \ symbol to prevent any errors in execution). |
| `pwgen -t u{2}p{5}l{2}d{2}L -S Ld^l^\\4^\\5^\\6^\\7^\\8 -n5 -c3`         | N * 3 passwords will be generated based on each line given template. The -n and -s flags will be ignored.                                                                                       |


#### Pipes and files

The pwgen command could be used inside the pipe of the BASH commands. It can be used in various ways within a pipeline:
- receiving input
- direct output to a file
- direct logging also to a file
- direct output to the next command in the pipeline

Here is an example list of pipeline using, more examples in a more convenient form you could find in the [showcase](#showcase):

| Call example                                                                                                                                                       | Outcome explanation                                                                                                                                                                                                                                                                                      |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `cat .venv/Lib/site-packages/pwgen/test/pattern-list.txt \| pwgen -n5 -c3` or `cat .venv/Lib/site-packages/pwgen/test/pattern-list.txt \| python -m pwgen -n5 -c3` | A template list is taken from a file and passed as input to pwgen.  Three passwords on each template will be generated. The -n flag will be ignored.                                                                                                                                                     |
| `pwgen -S "Ld^l^\\4^\\5^\\6^\\7^\\8" -n5 -c3 -vv > ./pwd-lst.txt`                                                                                                  | Three five-character passwords will be generated based on the given character set. The generated passwords will not be displayed on the screen and will be saved to a file. Warning and info messages will also be displayed during the generation.                                                      |
| `pwgen -S "Ld^l^\\4^\\5^\\6^\\7^\\8" -n5 -c3 -vvv 2> ./pwgen.log`                                                                                                  | Three five-character passwords will be generated based on the given character set. The generated passwords will be displayed. All types of messages will not be displayed during the generation and will be saved to a file.                                                                             |
| `echo u{4}[Ld^l^\\4^\\5^\\6^\\7^\\8]{3}l{2} \| pwgen -c6 -n5 \| sort -r`                                                                                           | The echo message will not be displayed and passed as input to pwgen. Six passwords will be generated based on the echo template, will not be displayed, and passed as input to the sort command. The sort command will sort passwords in reverse order and print them out. The -n flag will be ignored.  |


#### Showcase

To showcase the behavior of the pwgen library, an interactive command called "pwgen_showcase" has been created.
This command utilizes both the pwgen CLI and the pwgen library. It's an interactive command you can invoke via `pwgen_showcase` or `python -m pwgen.showcase`.
It has an optional flag that allows you to view all use cases at once without any interaction.
You can use the command `pwgen_showcase --all` to activate this feature.

![showcase_demo.gif](https://gitlab.com/EPAM-DevOpsInt2023/devops-7-assets/-/raw/45ed5458fe7cf837b62a423fcdff6a52b8db3cdb/m2-python/task-2a/images/showcase_demo.gif)

## General provisions

All materials provided and/or made available contain EPAM’s proprietary and confidential information and must not to be copied,
reproduced or disclosed to any third party or to any other person, other than those persons who have a bona fide need to review it
for the purpose of participation in the online courses being provided by EPAM.
The intellectual property rights in all materials (including any trademarks) are owned by EPAM Systems Inc or its associated companies,
and a limited license, terminable at the discretion of EPAM without notice, is hereby granted to you solely for the purpose of participating
in the online courses being provided by EPAM. Neither you nor any other party shall acquire any intellectual property rights of any kind
in such materials.


