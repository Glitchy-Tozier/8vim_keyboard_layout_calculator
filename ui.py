from sys import stdout
from time import time

from config import SCREEN_WIDTH


def write(text: str):
    stdout.write(text)


def flush():
    stdout.flush()


class Cursor:
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


def formatTime(seconds: float):
    if seconds < 0:
        return 'N/A'
    minutes = int(seconds//60)
    seconds %= 60
    hours = minutes//60
    minutes %= 60
    return f'{str(hours) + "h " if hours else ""}{str(minutes) + "m " if minutes else ""}{seconds:.2f}s'


def padding(text: str, width: int, left: bool = False):
    pad = ' '*(width - len(text))
    if left:
        return pad + text
    return text + pad

def separator(width: int = SCREEN_WIDTH, char: str = '─'):
    write(f'{char*width}\n')
    flush()


def title(title: str, width: int = SCREEN_WIDTH, char: str = '━'):
    spaceLeft = width - len(title) - 2
    line = char*(spaceLeft//2)
    write(f'{line} {title} {line}')
    if spaceLeft % 2:
        write(char)
    write('\n\n')
    flush()


def subtitle(subtitle: str, width: int = SCREEN_WIDTH):
    title(subtitle, width, '─')


class Progress:
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

    def estim_total(self):
        if not self.prog:
            return -1
        return (self.last_update - self.start)*self.total/self.prog

    def display(self):
        msg = f'[{self.prog}/{self.total}]'
        width = self.width - len(msg) - 2
        if self.prog == self.total:
            write(f'{msg}⦗{"╍"*width}⦘')
        else:
            barLen = int((self.width - len(msg) - 2)*self.prog/self.total)
            write(f'{msg}⦗{"╍"*barLen}{" "*(width - barLen)}⦘')
        Cursor.left(self.width)
        if self.time_taken:
            progMsg = f'Time taken: {formatTime(self.estim_total())}'
        else:
            progMsg = f'Estimated total time: {formatTime(self.estim_total())}'
        Cursor.up()
        self.info.set_msg(progMsg)
        self.info.set_status(self.status)
        Cursor.down()
        flush()


class Info:
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
            progMsg = f'Time taken: {formatTime(self.time_taken)}'
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
        title('Demos of UI helpers')
        subtitle('Progress bar demo')

        # Progress bar
        p = Progress(12)
        for i in range(13):
            p.set_prog(i)
            sleep(0.2)
        write('\n\n')

        # Info box
        subtitle('Other demo')
        i = InfoWithTime('Info box demo', 'Starting')
        sleep(0.5)
        i.set_status('Finalizing')
        sleep(1)
        i.set_done()
        write('\n\n')

    finally:
        Cursor.show()
