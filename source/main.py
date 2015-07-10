import curses
from curses import wrapper

def main(stdscr):

	stdscr = curses.initscr()
	curses.echo()
	#stdscr.border(0)

	stdscr.addstr(4, 34, "[INSERT TITLE]", curses.A_STANDOUT)

	begin_x = 22
	begin_y = 8
	height = 10
	width = 40
	win = curses.newwin(height, width, begin_y, begin_x)

	win.border(0)
	

	win.addstr(0, 0, "ENTER LOGIN CREDENTIALS")
	win.addstr(3, 8, "Username: ")
	win.addstr(5, 8, "Password: ")
	win.move(3, 18)
	stdscr.refresh()
	win.refresh()

	un_input = win.getstr()
	win.move(5, 18)
	win.refresh()
	pw_input = win.getstr()
	
	stdscr.addstr(20, 30, "omg i'm blinking", curses.A_BLINK)

	
	stdscr.getch()

	curses.endwin()

wrapper(main)
