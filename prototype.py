import os
import time

def human_time_delta(s):
    """Three-character-wide human-readable approximate time delta of s."""
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
    return f'{years}y'


def render_preview(data, space_left):
    d = data.replace('\n', '⏎  ')

    if len(d) > space_left:
        return d[:space_left - 1] + '…'

    return d



KEYS = 'asdfjklgh'
NUM_FILES = len(KEYS)


os.chdir(os.path.join(os.getenv('HOME'), 'n'))
dir_entries = os.scandir('.')
files = (
    (dir_entry.stat().st_mtime, dir_entry.name)
    for dir_entry in dir_entries
    if dir_entry.is_file()
)
recent_files = sorted(files, reverse=True)[:NUM_FILES]
now = time.time()
columns, _ = os.get_terminal_size()

for key, (timestamp, name) in zip(KEYS, recent_files):
    age = human_time_delta(now - timestamp)
    space_left = columns - 11 - len(name)
    preview = render_preview(open(name).read(space_left + 1), space_left)
    print(f' \033[34;1m{key}\033[0m \033[33;1m{age:>3}\033[0m \033[37m{name}\033[0m  {preview}')


while True:
    try:
        key = input('?> ')
        if not key or key not in KEYS:
            print(f'bad input, try one of {{{",".join(KEYS)}}}')
            continue
        name = recent_files[KEYS.find(key)][1]
        editor = os.getenv('EDITOR')
        os.execlp(editor, editor, name)
    except (EOFError, KeyboardInterrupt):
        print()
        break
