from sys import stdout
from time import time

from config import SCREEN_WIDTH, DISABLE_UNICODE


def write(text: str):
    """Writes text to standard output"""
    stdout.write(text)


def flush():
    """Flushes standard output"""
    stdout.flush()


class Cursor:
    """Class with functions relating to the terminal cursor"""
    def up(n: int = 1):
        write(f'\x1b[{n}A')
    def down(n: int = 1):
        write(f'\x1b[{n}B')
    def right(n: int = 1):
        write(f'\x1b[{n}C')
    def left(n: int = 1):
        write(f'\x1b[{n}D')
    def hide():
        write('\x1b[?25l')
    def show():
        write('\x1b[?25h')


def getFormatedTime(seconds: float) -> str:
    """Formats a float representing seconds into a readable format and returns it as a string"""
    if seconds < 0:
        return 'N/A'
    minutes = int(seconds//60)
    seconds %= 60
    hours = minutes//60
    minutes %= 60
    return f'{str(hours) + "h " if hours else ""}{str(minutes) + "m " if minutes else ""}{seconds:.2f}s'


def getPaddedText(text: str, width: int, left: bool = False) -> str:
    """Adds spaces to the start or end of a string to match a particular length and return it"""
    pad = ' '*(width - len(text))
    if left:
        return pad + text
    return text + pad


def getExpandedLine(width: int = SCREEN_WIDTH, left: str = '', right: str = '') -> str:
    """Spaces two strings as far apart as possible."""
    return getPaddedText(left, width - len(right)) + right


def displaySeparator(width: int = SCREEN_WIDTH, char: str = '-' if DISABLE_UNICODE else '─'):
    """Displays a horizontal line"""
    write(f'{char*width}\n')
    flush()


def displayTitle(title: str, width: int = SCREEN_WIDTH, char: str = '=' if DISABLE_UNICODE else '━'):
    """Displays a thick horizontal line with centered text"""
    spaceLeft = width - len(title) - 2
    line = char*(spaceLeft//2)
    write(f'{line} {title} {line}')
    if spaceLeft % 2:
        write(char)
    write('\n\n')
    flush()


def displaySubtitle(subtitle: str, width: int = SCREEN_WIDTH):
    """Displays a horizontal line with centered text"""
    displayTitle(subtitle, width, '-' if DISABLE_UNICODE else '─')


class Progress:
    """Class to display a progress bar"""
    def __init__(self, total: int, prog: int = 0, width: int = SCREEN_WIDTH):
        self.total = total
        self.prog = prog
        self.width = width
        self.start = time()
        self.last_update = None
        self.time_taken = None
        self.info = Info()
        self.status = ''
        write('\n')
        self.display()

    def set_prog(self, prog: int):
        self.prog = prog
        self.last_update = time()
        if prog == self.total:
            self.time_taken = self.estim_total()
        else:
            self.time_taken = None
        self.display()

    def set_status(self, status: str):
        self.status = status
        self.display()

    def estim_total(self) -> float:
        if not self.prog:
            return -1
        return (self.last_update - self.start)*self.total/self.prog

    def display(self, chars: str = '[#]' if DISABLE_UNICODE else '⦗╍⦘'):
        msg = f'[{self.prog}/{self.total}]'
        width = self.width - len(msg) - 2
        if self.prog == self.total:
            write(f'{msg}{chars[0]}{chars[1]*width}{chars[2]}')
        else:
            barLen = int((self.width - len(msg) - 2)*self.prog/self.total)
            write(f'{msg}{chars[0]}{chars[1]*barLen}{" "*(width - barLen)}{chars[2]}')
        Cursor.left(self.width)
        if self.time_taken:
            progMsg = f'Time taken: {getFormatedTime(self.estim_total())}'
        else:
            progMsg = f'Estimated total time: {getFormatedTime(self.estim_total())}'
        Cursor.up()
        self.info.set_msg(progMsg)
        self.info.set_status(self.status)
        Cursor.down()
        flush()


class Info:
    """Class to display information with an optional status on the right"""
    def __init__(self, msg: str = '', status: str = '', width: int = SCREEN_WIDTH):
        self.msg = msg
        self.status = status
        self.width = width
        if msg:
            self.display()

    def set_msg(self, msg: str):
        self.msg = msg
        self.display()

    def set_status(self, status: str):
        self.status = status
        self.display()

    def display(self):
        write(' '*self.width)
        if self.status:
            Cursor.left(len(self.status) + 2)
            write(f'[{self.status}]')
            Cursor.left(self.width)
        else:
            Cursor.left(self.width)
        write(self.msg)
        Cursor.left(len(self.msg))
        flush()


class InfoWithTime(Info):
    """Inherits Info class but displays time taken after it is marked as done"""
    def __init__(self, msg: str = '', status: str = '', width: int = SCREEN_WIDTH):
        write('\n')
        self.start = time()
        self.time_taken = None
        super().__init__(msg, status, width)

    def set_done(self):
        self.status = 'Done'
        self.time_taken = time() - self.start
        self.display()

    def display(self):
        super().display()
        if self.time_taken:
            Cursor.up()
            progMsg = f'Time taken: {getFormatedTime(self.time_taken)}'
            write(progMsg)
            Cursor.left(len(progMsg))
            Cursor.down()
        flush()


# Demos
if __name__ == '__main__':
    from time import sleep

    Cursor.hide()
    try:

        # Title and subtitle
        write('\n')
        displayTitle('Demos of UI helpers')
        displayTubtitle('Progress bar demo')

        # Progress bar
        p = Progress(12)
        for i in range(13):
            p.set_prog(i)
            sleep(0.2)
        write('\n\n')

        # Info box
        displaySubtitle('Other demo')
        i = InfoWithTime('Info box demo', 'Starting')
        sleep(0.5)
        i.set_status('Finalizing')
        sleep(1)
        i.set_done()
        write('\n\n')

    finally:
        Cursor.show()

