import MySQLdb
import curses
from curses import wrapper

def db_overview(stdscr, db):

     cursor = db.cursor()
     cursor.execute("SHOW DATABASES")
     data = cursor.fetchall()

     stdscr.clear()
     stdscr.border(0)
     stdscr.addstr(4, 34, "DATABASES OVERVIEW", curses.A_STANDOUT)
     
     db_list = []
     i = 0
     for x in data:
	  db_list.append(x[0])
     
     for name in db_list:
	  stdscr.addstr(i + 6, 34, str(i + 1) + " " + name)
	  i += 1

     stdscr.addstr(i + 6, 10, "Select a database by inputting its number and hit ENTER")
     stdscr.refresh()

     list_idx = int(stdscr.getstr()) - 1
     stdscr.addstr(i + 7, 10, str(list_idx))
     db_name = db_list[list_idx]

     table_overview(stdscr, db, db_name)
     


def table_overview(stdscr, db, db_name):


     cursor = db.cursor()
     sql = "USE " + db_name
     cursor.execute(sql)
     cursor.execute("SHOW TABLES")
     data = cursor.fetchall()

     stdscr.clear()
     stdscr.border(0)
     stdscr.addstr(4, 34, "TABLES IN " + db_name, curses.A_STANDOUT)

     table_list = []
     i = 0
     for x in data:
	  table_list.append(x[0])
     for name in table_list:
	  stdscr.addstr(i + 6, 34, str(i + 1) + " " + name)
	  i += 1
     
     stdscr.refresh()

     #stdscr.getch()
     #curses.endwin()
     



def main(stdscr):

	stdscr = curses.initscr()
	curses.echo()
	stdscr.border(0)

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

	username_db = win.getstr()
	win.move(5, 18)
	win.refresh()
	password_db = win.getstr()
	hostname_db = "76.103.139.98"

	#db = MySQLdb.connect(host=hostname_db, user=username_db, passwd=password_db, db="cs419db")
	db = MySQLdb.connect(host=hostname_db, user=username_db, passwd=password_db)
	if db.cursor():
		stdscr.addstr(20, 30, "Connected!")
		db_overview(stdscr, db)
		#table_overview(stdscr, db)

	#incorrect credentials produce ugly traceback. does not fail gracefully.
	else:
		stdscr.addstr(20, 30, "Connection failed.")
	
	#stdscr.addstr(21, 30, "", curses.A_BLINK)
	
	db.close()

	stdscr.getch()

	curses.endwin()

wrapper(main)
