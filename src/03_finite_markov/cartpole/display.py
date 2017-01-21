import curses
import atexit


class Display:
    def __init__(self, use_curses=False):
        self.__use_curses = use_curses
        self.__stdscr = None
        self.__curse_cleaned = True
        if self.__use_curses:
            self.__init_curses()

    def __init_curses(self):
        if not self.__use_curses:
            return

        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.__stdscr = stdscr
        self.__curse_cleaned = False

        atexit.register(self.__terminate_curses)

    def free_curses(self):
        if self.__curse_cleaned:
            return

        curses.nocbreak()
        curses.echo()
        curses.endwin()
        self.__curse_cleaned = True

    def __terminate_curses(self):
        self.free_curses()

    def print(self, msg, row=0, clear_all=False, clear_row=True):
        if not self.__use_curses:
            print(msg)
            return

        stdscr = self.__stdscr
        if clear_all:
            stdscr.clear()

        if clear_row:
            stdscr.addstr(row, 0, ' '*80)
        stdscr.addstr(row, 0, msg)
        stdscr.refresh()



