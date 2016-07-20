################################################################################
#
# Copyright (c) 2016 Nicholas Vinson
#
# This file is part of libzilla
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################

import curses

class ShellCommand:
    def _define_term_colors(self):
        """ Define the color pairs so shell colors can be used. """
        curses.init_pair(1, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_BLUE, -1)
        curses.init_pair(5, curses.COLOR_MAGENTA, -1)
        curses.init_pair(6, curses.COLOR_CYAN, -1)
        curses.init_pair(7, curses.COLOR_WHITE, -1)

    def _draw_border(self):
        self.screen.attron(curses.color_pair(3))
        y, x, = self.screen.getmaxyx()
        self.screen.hline(1, 1, curses.ACS_HLINE, x - 2)
        self.screen.hline(y - 1, 1, curses.ACS_HLINE, x - 2)
        self.screen.vline(2, x - 1, curses.ACS_VLINE, y - 3)
        self.screen.vline(2, 0, curses.ACS_VLINE, y - 3)
        self.screen.addch(1, 0, curses.ACS_ULCORNER)
        self.screen.addch(1, x - 1, curses.ACS_URCORNER)
        self.screen.addch(y - 1, 0, curses.ACS_LLCORNER)
        # Writing to the LR corner with addch() will trigger an exception
        # because addch() will try to advance to the next line (i.e. out of
        # bounds).
        try:
            self.screen.addch(y - 1, x - 1, curses.ACS_LRCORNER)
        except curses.error:
            pass
        self.screen.attroff(curses.color_pair(3))

    def _draw_menu(self):
        pass

    def _write_title(self):
        y, x = self.screen.getmaxyx()
        self.screen.addstr(0, (x - len(self.title))//2,
                           " {0} ".format(self.title),
                           curses.color_pair(5) | curses.A_BOLD)

    def _write_menu_title(self):
        y, x = self.screen.getmaxyx()
        max_width = x - 4
        if len(title) > max_width:
            ### Title is too long.
            title = title[:max_width - 3] + "..."
        self.screen.addstr(1, 2, title,
            curses.color_pair(2) | curses.A_BOLD)

    def _write_text(self, y, x, text):
        maxy, maxx = self.screen.getmaxyx()
        line_len = min(len(text), maxx - x - 1)
        self.screen.addstr(y, 1, " " * (maxx - 2))
        self.screen.addstr(y, x, text[:line_len], curses.A_BOLD)

    def __init__(self, title):
        self.screen = curses.initscr()
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        self._define_term_colors()

        self.menus = []
        self.title = title

    def __enter__(self):
        curses.cbreak()
        curses.noecho()
        self.screen.keypad(1)
        return self

    def __exit__(self, etype, value, tb):
        self.screen.keypad(True)
        curses.echo()
        curses.nocbreak()
        self.screen.keypad(0)
        curses.endwin()
        return False

    def run(self):
        curses.ungetch(curses.KEY_RESIZE)
        while True:
            try:
                c = self.screen.getch()
                if c == curses.KEY_RESIZE:
                    self.screen.clear()
                if c == 4:
                    self._write_text(3, 4, "EOF")
                    break
                if c == 27:
                    self._write_text(3, 4, "ESCAPE")
                    continue
                if c == curses.KEY_UP:
                    self._write_text(3, 4, "UP")
                    continue
                if c == curses.KEY_LEFT:
                    self._write_text(3, 4, "LEFT")
                    continue
                if c == curses.KEY_DOWN:
                    self._write_text(3, 4, "DOWN")
                    continue
                if c == curses.KEY_RIGHT:
                    self._write_text(3, 4, "RIGHT")
                    continue
                if c == curses.KEY_PPAGE:
                    self._write_text(3, 4, "PAGE-UP")
                    continue
                if c == curses.KEY_NPAGE:
                    self._write_text(3, 4, "PAGE-DOWN")
                    continue
                if c == curses.KEY_HOME:
                    self._write_text(3, 4, "HOME")
                    continue
                if c == curses.KEY_END:
                    self._write_text(3, 4, "END")
                    continue
            except KeyboardInterrupt:
                break
            self._write_text(3, 4, str(c) + " ")
            self._draw_border()
            self._write_title()
            self._draw_menu()
