import MySQLdb
import curses
from curses import wrapper

def get_dbName(list, page, y_pos):

     for x in list:
	  if x[1] == page and x[2] == y_pos:
	       return x[0]

     return -1

def db_overview(stdscr, db):

     curses.noecho() #do not display keyboard input

     cur_page = 1 #for future pagination implementation

     cursor = db.cursor()
     cursor.execute("SHOW DATABASES")
     data = cursor.fetchall()

     stdscr.clear()
     stdscr.border(0)
     stdscr.addstr(4, 34, "DATABASES OVERVIEW", curses.A_STANDOUT)
     
     db_list = []
     i = 0
     for x in data:
	  #Append 3-tuple: (database, page number, y-pos of printed line)
	  db_list.append((x[0], cur_page, i + 6))
	  i += 1
     
     k = 1
     for y in db_list:
	  stdscr.addstr(y[2], 34, str(k) + " " + y[0])
	  k += 1
	  

     stdscr.addstr(22, 2, "U - USE    D - DROP    C - CREATE NEW DATABASE        Q - QUIT")
     stdscr.refresh()

     #handle key presses
     stdscr.move(6, 34)

     while 1:
	  input = stdscr.getch()
	  cur_pos = stdscr.getyx()
	  if input == curses.KEY_UP:
	       stdscr.move(cur_pos[0] - 1, cur_pos[1])
	  elif input == curses.KEY_DOWN:
	       stdscr.move(cur_pos[0] + 1, cur_pos[1])
	  elif chr(input) == "u":
	       db_name = get_dbName(db_list, cur_page, cur_pos[0])
	       table_overview(stdscr, db, db_name)
	       return
	  elif chr(input) == "d":
	       db_name = get_dbName(db_list, cur_page, cur_pos[0])
	       stdscr.addstr(21, 2, "Are you sure you want to DROP " + db_name + "? (y/n)")
	       res = stdscr.getch()
	       if chr(res) == "y":
		    cursor.execute("DROP DATABASE  " + db_name)
		    db_overview(stdscr, db)
		    return
	       else:
		    db_overview(stdscr, db)
		    return


	  elif chr(input) == "q":
	       curses.endwin()
	       exit()
	 
     


def table_overview(stdscr, db, db_name):

     cur_page = 1 #for future pagination implementation

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
	  #Append 3-tuple: (table name, page, printed line)
	  table_list.append((x[0], cur_page, i + 6))
	  i += 1
     k = 1
     for y in table_list:
	  stdscr.addstr(y[2], 34, str(k) + " " + y[0])
	  k += 1
     
     stdscr.addstr(22, 2, "V - VIEW    D - DELETE    C - CREATE TABLE    B - BACK    Q - QUIT")
     stdscr.refresh()
     
     #handle key presses
     stdscr.move(6, 34)

     while 1:
	  input = stdscr.getch()
	  cur_pos = stdscr.getyx()
	  if input == curses.KEY_UP:
	       stdscr.move(cur_pos[0] - 1, cur_pos[1])
	  elif input == curses.KEY_DOWN:
	       stdscr.move(cur_pos[0] + 1, cur_pos[1])
	  elif chr(input) == "v":
	       #view
	       temp = 1
	  elif chr(input) == "d":
	       #delete
	       temp = 1
	  elif chr(input) == "c":
	       #create
	       temp = 1
	  elif chr(input) == "b":
	       #back
	       db_overview(stdscr, db)
	       
	  elif chr(input) == "q":
	       #quit
	       curses.endwin()
	       exit()



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
	hostname_db = "45.49.78.62"

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
