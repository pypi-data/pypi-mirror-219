'''Print messages on screen and ask for user input.'''

import sys as _sys

from .text_color import TextFormat
from .text_color import print_colored_text as _print_colored_text
from .text_color import input_colored as _input_colored
from .text_color import clear_line as _clear_line


def message(*text: str | object,
            text_min_len: list[int] = [], default_text_options: list = [], additional_text_options: list[list] = [[]],
            icon: str = None, icon_options: list = [], blink: bool = False,
            end: str = '\n', file = _sys.stderr):
    '''
    Generic and customizable message.

    :param text: The message(s) to print.
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param default_text_options: Styling options applied to all messages.
    :param additional_text_options: Styling options applied to single messages.
    :param icon: Character to use as icon, between ``[ ]``.
    :param icon_options: Styling options applied to the icon.
    :param blink: If True, the icon blinks.
    :param end: Character to output at the end of the message.
    :param file: Where to write the message.
    '''

    _clear_line()

    # icon
    if icon is not None:
        _print_colored_text('[', *icon_options, TextFormat.Style.BOLD, end='', file=file)
        
        if blink:
            _print_colored_text(icon, *icon_options, TextFormat.Style.BOLD, TextFormat.Style.BLINK, end='', file=file)
        else:
            _print_colored_text(icon, *icon_options, TextFormat.Style.BOLD, end='', file=file)
        
        _print_colored_text(']', *icon_options, TextFormat.Style.BOLD, end='', file=file)
        _print_colored_text(' ', end='', file=file)
    
    # text
    for i in range(len(text)):
        line_text = str(text[i])
        line_options = default_text_options + additional_text_options[i] if i < len(additional_text_options) else default_text_options
        line_end = ' ' if i < len(text) - 1 else ''

        _print_colored_text(line_text, *line_options, end=line_end, file=file)

        # padding
        if i < len(text_min_len):
            line_padding = text_min_len[i] - len(line_text)
            if line_padding > 0:
               _print_colored_text(' ' * line_padding, end='', file=file)
        

    # line end and flushing
    _print_colored_text(end=end, file=file, flush=True)
    

def info(*text: str | object, text_min_len: list[int] = [], text_options: list[list] = [[]], blink: bool = False):
    '''
    Message indicating an information.
    
    :param text: The message(s) to print.
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param text_options: Styling options applied to single messages.
    :param blink: If True, the icon blinks.
    '''

    message(*text,
            icon='*',
            icon_options=[
                TextFormat.Color.BLUE
            ],
            text_min_len=text_min_len,
            additional_text_options=text_options,
            blink=blink)


def progress(*text: str | object, text_min_len: list[int] = [], text_options: list[list] = [[]]):
    '''
    Message indicating an action which is still happening.
    
    :param text: The message(s) to print.
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param text_options: Styling options applied to single messages.
    '''

    message(*text,
            icon=' ',
            end='\r',
            text_min_len=text_min_len,
            default_text_options=[
                TextFormat.Color.DARKGRAY,
                TextFormat.Style.ITALIC
            ],
            additional_text_options=text_options
    )


def error(*text: str | object, text_min_len: list[int] = [], text_options: list[list] = [[]], blink: bool = False):
    '''
    Message indicating an error.
    
    :param text: The message(s) to print.
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param text_options: Styling options applied to single messages.
    :param blink: If True, the icon blinks.
    '''
    
    message(*text, 
            icon='-', 
            blink=blink,
            icon_options=[
                TextFormat.Color.RED
            ],
            text_min_len=text_min_len,
            default_text_options=[
                TextFormat.Color.RED
            ],
            additional_text_options=text_options
    )


def critical_error(*text: str | object, text_min_len: list[int] = [], blink: bool = False, exit_code: int = 1):
    '''
    Message indicating a critical error. The program terminates after showing this message.
    
    :param text: The message(s) to print.
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param blink: If True, the icon blinks.
    :param exit_code: The exit code of the program.
    '''
    
    message(*text, 
            icon='x', 
            blink=blink,
            icon_options=[
                TextFormat.Color.RED
            ],
            text_min_len=text_min_len,
            default_text_options=[
                TextFormat.Color.RED
            ]
    )

    _sys.exit(exit_code)


def warning(*text: str | object, text_min_len: list[int] = [], text_options: list[list] = [[]], blink: bool = False):
    '''
    Message indicating a warning.
    
    :param text: The message(s) to print.
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param text_options: Styling options applied to single messages.
    :param blink: If True, the icon blinks.
    '''

    message(*text, 
            icon='!', 
            blink=blink,
            icon_options=[
                TextFormat.Color.YELLOW
            ],
            text_min_len=text_min_len,
            default_text_options=[
                TextFormat.Color.YELLOW
            ]
    )


def success(*text: str | object, text_min_len: list[int] = [], text_options: list[list] = [[]], blink: bool = False):
    '''
    Message indicating a successfully completed action.
    
    :param text: The message(s) to print.
    :param text_min_len: Minimum length for each message. Fill the remaining characters with spaces.
    :param text_options: Styling options applied to single messages.
    :param blink: If True, the icon blinks.
    '''

    message(*text, 
            icon='+', 
            blink=blink,
            icon_options=[
                TextFormat.Color.GREEN
            ],
            text_min_len=text_min_len,
            default_text_options=[TextFormat.Color.GREEN],
            additional_text_options=text_options
    )


def ask(question: str, end=': ') -> str:
    '''
    Prints a question to screen and returns the answer.
    
    :param question: The question to print.
    :param end: Characters to be printed at the end of the question.
    
    :returns: The user's answer.
    '''

    message(f'{question}{end}',
            icon='?',
            icon_options=[
                TextFormat.Color.PURPLE
            ],
            end='')
    
    return _input_colored(
        TextFormat.Style.ITALIC,
    )

def ask_continue(text: str=None):
    '''
    Prints a question asking the user if they want to continue executing the program:
    a positive answer makes the program continues its normal execution;
    a negative answer terminates the program.
    Optionally supports a custom message.
    
    :param text: The message to print.
    '''
    if text is not None:
        message = f'{text}. Continue? (y/N)'
    else:
        message = 'Continue? (y/N)'

    while True:
        ans = ask(message, end=' ')

        if ans.lower() == 'y':
            break
        if ans.lower() == 'n' or len(ans) == 0:
            _sys.exit()