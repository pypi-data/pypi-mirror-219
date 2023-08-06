import logging
import random
import string
from typing import Optional, List

from pwgen import __version__

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.ERROR)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


CHARACTER_SETS = {
    'd': string.digits,  # Digits
    'l': string.ascii_lowercase,  # Small lateral ASCII
    'L': string.ascii_letters,  # Mixed-case lateral ASCII
    'u': string.ascii_uppercase,  # Big lateral ASCII
    'p': ',.;:',
}


def set_log_level(level: int) -> None:
    # match level:
    #     case 1:
    #         console_handler.setLevel(logging.WARNING)
    #         logger.setLevel(logging.WARNING)
    #     case 2:
    #         console_handler.setLevel(logging.INFO)
    #         logger.setLevel(logging.INFO)
    #     case v if v >= 3:
    #         console_handler.setLevel(logging.DEBUG)
    #         logger.setLevel(logging.DEBUG)
    if level == 1:
        console_handler.setLevel(logging.WARNING)
        logger.setLevel(logging.WARNING)
    elif level == 2:
        console_handler.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
    elif level >= 3:
        console_handler.setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)


def packet_version() -> str:
    return __version__


def split_placeholders(placeholders: str) -> List[str]:
    """
    Split pattern to a char list and join ^, \\<char> and ^\\<char> into one element
    :param placeholders: placeholder charset string, for instance, Ld^l^\\4^\\5^\\6^\\7^\\8
    :return: list with a single placeholder
    """
    ret = []
    t = ''
    for el in list(placeholders):
        if el in '^\\' and not t:
            t = el
        elif t == '^' and el == '\\':
            t += el
        elif t == '^' or t == '\\' or t == '^\\':
            t += el
            ret.append(t)
            t = ''
        else:
            ret.append(el)

    return ret


def split_pattern(pattern: str) -> List[str]:
    """
    Split pattern to a char list and join {..}, [..] and \\<char> into one element
    :param pattern: for instance, ud{5}{4}du[d\\m\\@^\\3]
    :return: list with a single placeholder
    """
    ret = []
    t = ''
    for el in list(pattern):
        if el in '[{\\' and not t:
            t = el
        elif el in '}]' or t == '\\':
            t += el
            ret.append(t)
            t = ''
        elif t:
            t += el
        else:
            ret.append(el)

    return ret


def generate_character_set(placeholders: str) -> Optional[str]:
    pat_ls = split_placeholders(placeholders)

    if any(el_ls := [el for el in pat_ls if el and el[0] not in '^\\' and not CHARACTER_SETS.get(el, None)]):
        logger.error(f'Wrong symbols {el_ls} inside the custom char set ({placeholders})')
        return None

    pat_ls = [CHARACTER_SETS.get(el, None)  # Change placeholders (except ^, ^\) to char set
              if el and el[0] not in '^\\'
              else el.replace('\\', '') if el and el[0] == '\\' else el for el in pat_ls]

    ch_set = {spl for el in pat_ls if el and el[0] not in '^\\'   # Make set of chars (allows remove duplicates)
              for spl in list(el)}
    excl_ch_set = {spl for el in pat_ls if el and el[0:2] == '^\\'
                   for spl in list(el.replace('^\\', ''))}   # Make set of excluded simple symbols

    if any(el_ls := [el for el in pat_ls
                     if el and el[0] == '^' and el[0:2] != '^\\'
                        and not CHARACTER_SETS.get(el.replace('^', ''), None)]):
        logger.error(f'Wrong symbols {el_ls} inside the custom char set ({placeholders})')
        return None

    excl_ch_set |= {symbol for el in pat_ls if el and el[0] == '^' and el[0:2] != '^\\'
                    for spl in list(el.replace('^', ''))
                    for symbol in CHARACTER_SETS.get(spl, '')}  # Add to the excluded symbols set excluded char sets

    ch_set -= excl_ch_set

    return ''.join(str(c) for c in ch_set)


def generate_password_from_pattern(pattern: str) -> str:
    if type(pattern) is not str:  # Initial checks
        logger.error(f'Incorrect pattern {pattern}. String expected.')
        return ''
    elif not pattern:
        logger.error(f'Pattern cannot be empty')
        return ''
    # elif pattern.find(' ') != -1:
    #     logger.error(f'You cannot use space symbol in pattern ({pattern})')

    # Convert \{ \} \[ \] to the { } [ ]. It could be an error, but it's a minor error. Just sanitize string.
    n_pattern = pattern.replace('\\{', '{').replace('\\}', '}').replace('\\[', '[').replace('\\]', ']')

    # Remove double quotes at the start and at the end of the pattern.
    if len(n_pattern) > 1 and n_pattern[:1] == '"' and n_pattern[-1] == '"':
        n_pattern = (n_pattern[1:])[:-1]

    if n_pattern[0] == '{':
        logger.error(f'Incorrect utilization of braces in the pattern ({pattern}) due to braces cannot come first')
        return ''

    pat_ls = split_pattern(n_pattern)

    pat_ls = [(el.replace('{', '').replace('}', ''), ) if el.find('{') != -1 else el
              for el in pat_ls]  # Replace '{..}' with a tuple ('..') without braces

    if any([el for el in pat_ls if type(el) is tuple and not el[0].isdigit()]):
        logger.error(f'The pattern ({pattern}) has an error as an incorrect number was passed into the braces.')
        return ''

    pat_ls = [(int(el[0]) - 1, ) if type(el) is tuple else el
              for el in pat_ls]  # Convert string in the tuple to number

    while any([el for el in pat_ls if type(el) is tuple]):  # Multiply previous element while tuples present in the list
        pat_ls = [dup for i, el in enumerate(pat_ls)
                  for dup in ([pat_ls[i - 1]] * el[0] if type(el) is tuple and type(pat_ls[i - 1]) is str else [el])]

    if any(er := [el for el in pat_ls
                  if el and el[0] != '\\' and not generate_character_set(el.replace('[', '').replace(']', ''))]):
        logger.error(f'The pattern ({pattern}) has an error charsets {er}')
        return ''

    pat_ls = [el.replace('\\', '') if el and el[0] == '\\'
              else generate_character_set(el.replace('[', '').replace(']', ''))
              for el in pat_ls]  # Replace placeholders to character sets

    return ''.join(generate_password_from_character_set(el) for el in pat_ls)


def generate_password_from_character_set(character_set: str, length: int = 1) -> str:
    password = ''.join(random.choice(character_set) for _ in range(length))
    return password


def generate_passwords_to_file(file: str, length: int, count: int, template: Optional[str] = None,
                               character_set: Optional[str] = None, permute: Optional[bool] = False) -> bool:

    passwords = generate_passwords(length=length, count=count, template=template,
                                   placeholders_set=character_set, permute=permute)

    try:
        logger.debug(f'Start writing generated passwords to the {file} file.')

        with open(file, 'w') as f:
            f.writelines(password + '\n' for password in passwords)

        logger.info(f'The generated passwords was written to the {file} file.')
        return True
    except Exception as e:
        logger.error(f'An error occurred while writing generated passwords to the file: {e}')
        return False


def generate_passwords(length: int = 8, count: int = 1, template: Optional[str] = None,
                       placeholders_set: Optional[str] = None, permute: Optional[bool] = False) -> List[str]:

    if template:
        logger.info(f'Let\'s generate {count} passwords based on template {template}')

        passwords = [generate_password_from_pattern(template) for _ in range(count)]
    else:
        if not placeholders_set:  # If no character_set passed take default character set
            placeholders_set = ''.join(key for key in CHARACTER_SETS.keys())

        logger.info(f'Let\'s generate {count} passwords based on a charset {"".join(sorted(placeholders_set))}')

        if not (character_set := generate_character_set(placeholders_set)):
            logger.error(f'Wrong custom character set {placeholders_set}')
            return []

        passwords = [generate_password_from_character_set(character_set, length=length) for _ in range(count)]

    if permute:
        logger.debug(f'List of the generated passwords before permutation: {passwords}')

        passwords = [''.join(random.sample(password, len(password))) for password in passwords]

    logger.debug(f'Final list of the generated passwords: {passwords}')

    return passwords
