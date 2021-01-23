import re
import os
import sys
import time

KEYS = 'asdfjklgh'
NUM_FILES = len(KEYS)

def human_time_delta(s):
    """
    Three-character-wide human-readable approximate time delta of s seconds.
    """
    seconds = int(s)
    if seconds < 60:
        return f'{seconds}s'

    minutes = seconds // 60
    if minutes < 60:
        return f'{minutes}m'

    hours = minutes // 60
    if hours < 24:
        return f'{hours}h'

    days = hours // 24
    if days <= 14:
        return f'{days}d'

    weeks = days // 7
    if weeks <= 6:
        return f'{weeks}w'

    months = days // 30
    if months <= 18:
        return f'{months}M'

    years = days // 365
    if years < 10:
        return f'{years}y'

    return '9+y'


def render_preview(data, space_left):
    d = re.sub('[\x00-\x1f\x80-\x9f]', '.', data.replace('\n', '⏎  '))

    if len(d) > space_left:
        return d[:space_left - 1] + '…'

    return d


def read_content(name, max_chars):
    try:
        return open(name, encoding='utf8').read(max_chars)
    except UnicodeDecodeError:
        return open(name, encoding='latin1').read(max_chars)


def load_default_directory():
    try:
        default = open(os.path.join(
            os.getenv('HOME'), '.config', 'redit', 'default-location')
        ).read().strip()

        return os.path.expanduser(default)
    except FileNotFoundError:
        return None


def list_files():
    files = (
        (dir_entry.stat().st_mtime, dir_entry.name)
        for dir_entry in os.scandir()
        if dir_entry.is_file()
    )

    return sorted(files, reverse=True)[:NUM_FILES]


def get_terminal_width():
    try:
        columns, _ = os.get_terminal_size()
        return columns
    except OSError:
        return 80


def run():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    directory = arg or load_default_directory() or '.'
    os.chdir(directory)
    recent_files = list_files()
    now = time.time()
    columns = get_terminal_width()

    for key, (timestamp, name) in zip(KEYS, recent_files):
        age = human_time_delta(now - timestamp)
        space_left = columns - 11 - len(name)
        preview = render_preview(read_content(name, space_left + 1), space_left)
        print(f' \033[34;1m{key}\033[0m \033[33;1m{age:>3}\033[0m \033[37m{name}\033[0m  {preview}')


    while True:
        try:
            key = input('?> ')
            if not key or key not in KEYS:
                print(f'bad input, try one of {{{",".join(KEYS)}}}, ^D or ^C to quit')
                continue
            name = recent_files[KEYS.find(key)][1]
            editor = os.getenv('EDITOR')
            os.execlp(editor, editor, name)
        except (EOFError, KeyboardInterrupt):
            print()
            break
