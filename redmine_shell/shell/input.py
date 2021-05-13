""" Input for Redmine shell. """


import sys
import os
import termios
import contextlib
from enum import Enum
from .command import Command
from redmine_shell.command.system.commands import History, HistoryMove


class State(Enum):
    ''' Character Key Event State. '''
    CONTINUE = -1
    BREAK = -2


@contextlib.contextmanager
def _raw_mode(file):
    """ Make terminal raw mode for getting an event pressing a key. """
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)


def redmine_input(prompt='', complete_command=None, history=False):
    """ Customized input function for redmine shell. """
    if complete_command is None:
        complete_command = []

    # TODO: inline
    sys.stdout.write(prompt)
    sys.stdout.flush()

    with _raw_mode(sys.stdin):
        def rewrite(new, old):
            origin_len = len(old)
            sys.stdout.write('\r{}\r'.format(' ' * (origin_len + len(prompt))))
            sys.stdout.write(prompt + ''.join(new))
            sys.stdout.flush()

        def complete(buf):
            target = ''.join(buf).strip()
            if not target:
                sys.stdout.write('\r{}\r'.format(' ' * (len(buf) + len(prompt))))
                for command in complete_command:
                    print(command)
                sys.stdout.write(prompt)
                sys.stdout.flush()
                return []

            str_len = len(target)
            filtered = [x for x in complete_command if len(x) >= str_len]
            filtered = [x for x in filtered if x.startswith(target) is True]
            if filtered:
                min_cmd = sorted(filtered)[0]
                if min_cmd == target:
                    return list(target)

                i = start = len(target)
                until = len(min_cmd)
                while start <= i < until:
                    compare = filtered[0][i]
                    is_diff = False
                    for cmd in filtered:
                        if compare != cmd[i]:
                            is_diff = True
                            break

                    if is_diff is True:
                        break
                    i += 1
                return list(min_cmd[:i])
            else:
                return buf

        def finder(buf):
            target = ''.join(buf)
            lookup = []
            for cmd in complete_command:
                if cmd.startswith(target) is True:
                    lookup.append(cmd)

            if lookup:
                sys.stdout.write('\r{}\r'.format(' ' * (len(buf) + len(prompt))))
                print("---------- CMDS ---------")
                for cmd in lookup:
                    print(cmd)
                sys.stdout.write(prompt + ''.join(target))
                sys.stdout.flush()

        def ctrl_d(keyword):
            raise EOFError

        def ctrl_p(keyword):
            # chr(16)
            # history up
            if keyword['history'] is True:
                old = keyword['type_buf']
                cmd = keyword['history_move'].move_up()
                if cmd is None:
                    pass
                else:
                    new = list(cmd)
                    rewrite(new, old)
                    keyword['type_buf'] = new
            return State.CONTINUE

        def ctrl_j(keyword):
            # char(14)
            # Ctrl + j
            # history down
            if keyword['history'] is True:
                old = keyword['type_buf']
                cmd = keyword['history_move'].move_down()
                if cmd is None:
                    new = ['']
                else:
                    new = list(cmd)
                rewrite(new, old)
                keyword['type_buf'] = new
            return State.CONTINUE

        def ctrl_l(keyword):
            # chr(12)
            # Ctrl + l
            return State.CONTINUE

        def ctrl_h(keyword):
            # chr(8)
            # Ctrl + h
            old = keyword['type_buf']
            new = keyword['type_buf'][:-1]
            rewrite(new, old)
            keyword['type_buf'] = new
            return State.CONTINUE

        def tab(keyword):
            # chr(9)
            # Tab
            old = keyword['type_buf']
            new = complete(old)
            if new:
                if ''.join(new) == ''.join(old):
                    finder(new)
                else:
                    rewrite(new, old)
                    keyword['type_buf'] = new
            return State.CONTINUE

        def newline(keyword):
            # chr(10)
            # Newline
            print("")
            return ''.join(keyword['type_buf'])

        def backspace(keyword):
            # chr(127)
            # Backspace
            old = keyword['type_buf']
            new = keyword['type_buf'][:-1]
            rewrite(new, old)
            keyword['type_buf'] = new
            return State.CONTINUE

        def normal(keyword):
            keyword['type_buf'].append(keyword['char'])
            rewrite(keyword['type_buf'], keyword['type_buf'])
            return State.CONTINUE

        def other(keyword):
            return State.CONTINUE

        keyword = {'prompt': prompt, 'complete_command': complete_command,
                   'history': history,}
        keyword['type_buf'] = []
        keyword['history_move'] = HistoryMove(
            History.instance().load())

        special_key_handlers = {chr(4): ctrl_d,
                                chr(16): ctrl_p,
                                chr(14): ctrl_j,
                                # MacOS uses 13 as ctrl-j
                                chr(13): ctrl_j,
                                chr(12): ctrl_l,
                                chr(8): ctrl_h,
                                chr(9): tab,
                                chr(10): newline,
                                chr(127): backspace, }

        while True:
            char = sys.stdin.read(1)

            if not char:
                break

            if char in special_key_handlers:
                handler = special_key_handlers[char]
            elif 41 <= ord(char) <= 176 or ord(char) == 32:
                handler = normal
            else:
                handler = other

            keyword['char'] = char
            ret = handler(keyword)
            if ret == State.CONTINUE:
                continue
            elif ret == State.BREAK:
                break
            else:
                return ret
