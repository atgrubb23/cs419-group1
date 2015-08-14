import MySQLdb
import curses
from curses import wrapper

def create_table(stdscr, db, cursor, db_name):
	curses.echo()

	#Create outer screen with title
	stdscr.clear()
	stdscr.border(0)
	stdscr.addstr(1, 34, "CREATE NEW TABLE", curses.A_STANDOUT)
	stdscr.refresh()

	#Create inner window for entry of database name
	begin_x = 22
	begin_y = 2
	height = 20
	width = 40
	win = curses.newwin(height, width, begin_y, begin_x)
	win.border(0)
	win.addstr(1, 8, "NAME: ")
	win.addstr(2, 8, "COL 1: ")
	win.move(1, 18)
	win.refresh()

	#Get initial input for name and mandatory column 1
	table_name = win.getstr()
	win.move(2, 18)
	column = win.getstr()

	while 1:
		col_input_y = 3
		col_num = 2
		input = win.getch()
		if chr(input) == "a":
			win.addstr(col_input_y, 8, "COL " + str(col_num) + ": ")
			win.move(col_input_y, 18)
			win.refresh()
			col_input_y += 1
			col_num += 1
	 	else:
	 		break

	#query = 'CREATE TABLE ' + tb_name
	#query += '( foo VARCHAR(50) DEFAULT NULL ) ENGINE=InnoDb;'
	#cursor.execute(query)

	table_overview(stdscr, db, db_name)


def create_db(stdscr, db):
	#Allow user to see typed text
	curses.echo()

	#Create outer screen with title
	stdscr.clear()
	stdscr.border(0)
	stdscr.addstr(4, 34, "CREATE NEW DATABASE", curses.A_STANDOUT)
	stdscr.refresh()

	#Create inner window for entry of database name
	begin_x = 22
	begin_y = 8
	height = 10
	width = 40
	win = curses.newwin(height, width, begin_y, begin_x)
	win.border(0)
	win.addstr(6, 8, "NAME: ")
	win.move(6, 18)
	win.refresh()

	#Get user input for database name
	db_name = win.getstr()
	cursor = db.cursor()

	#Create new database
	cursor.execute('CREATE DATABASE ' + db_name + ';')

	#Navigate back to database overview
	db_overview(stdscr, db)

def db_overview(stdscr, db):

     curses.noecho()


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
	  

     #stdscr.addstr(i + 6, 10, "Select a database by inputting its number and hit ENTER")
     stdscr.addstr(22, 2, "U - USE    D - DELETE    N - NEW")
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
	       for x in db_list:
		    if x[1] == cur_page and x[2] == cur_pos[0]:
			 db_name = x[0]
			 table_overview(stdscr, db, db_name)
			 break
	       break
	  elif chr(input) == "n":
	  	create_db(stdscr, db)
	  	break
	 

     #list_idx = int(stdscr.getstr()) - 1
     #stdscr.addstr(i + 7, 10, str(list_idx))
     #db_name = db_list[list_idx]

     #table_overview(stdscr, db, db_name)
     


def table_overview(stdscr, db, db_name):


     cursor = db.cursor()
     sql = "USE " + db_name
     cursor.execute(sql)
     cursor.execute("SHOW TABLES")
     data = cursor.fetchall()

     stdscr.clear()
     stdscr.border(0)
     stdscr.addstr(4, 34, "TABLES IN " + db_name, curses.A_STANDOUT)
     stdscr.addstr(22, 2, "N - NEW")

     table_list = []
     i = 0
     for x in data:
	  table_list.append(x[0])
     for name in table_list:
	  stdscr.addstr(i + 6, 34, str(i + 1) + " " + name)
	  i += 1
     
     stdscr.refresh()
     while 1:
     	userInput = stdscr.getch()
     	if chr(userInput) == "n":
     		create_table(stdscr, db, cursor, db_name)
     
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