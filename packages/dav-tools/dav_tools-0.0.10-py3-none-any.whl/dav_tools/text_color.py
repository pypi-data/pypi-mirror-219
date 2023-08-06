'''Utilities for handling text formatting.'''

import sys as _sys
import os as _os
from ._text_format import TextFormat


def get_format(*options) -> str:
    '''
    Get the format string generated from the arguments.
    Needed for manually setting text style. Otherwise use ``set_format()``.

    :param option: Text styling options.

    :returns: The format string corresponding to the options.
    '''

    result = ''

    for option in options:
        result += option.decode()

    return result

def set_format(*options, file = _sys.stdout):
    '''
    Set text styling.

    :param option: Text styling options.
    :param file: Where to set text styling.
    '''

    for option in options:
        print(option.decode(), end='', file=file)

def get_colored_text(text: str, *format_options) -> str:
    '''
    Return a styled text.

    :param text: Text to print.
    :param format_options: Text styling options.

    :returns: The text properly styled.
    '''
    
    result = ''
    result += get_format(*format_options)
    result += text
    result += get_format(TextFormat.RESET)

    return result

def print_colored_text(text: str = '', *format_options, end: str='\n', file=_sys.stdout, flush=False):
    '''
    Print a styled text.

    :param text: Text to print.
    :param format_options: Text styling options.
    :param end: Character to be printed after the text.
    :param file: Where to print the text.
    :param flush: Whether to flush the stream after printing.
    '''

    text = get_colored_text(text, *format_options)
    print(text, end=end, file=file, flush=flush)

def input_colored(*format_options) -> str:
    '''
    Ask input from a user using specified styling options.

    :param format_options: Text styling options.

    :returns: User input.
    '''
    set_format(*format_options, file=_sys.stderr)
    result = input()
    set_format(TextFormat.RESET)

    return result

def clear_line(file=_sys.stdout, flush=False):
    '''
    Clears the current line from any text of formatting.
    Not really suitable for files.

    :param file: Stream to clear.
    :param flush: Whether to flush the stream after printing.
    '''
    print('\r', ' ' * _os.get_terminal_size().columns, '\r',
          sep='', end='', file=file, flush=flush)
