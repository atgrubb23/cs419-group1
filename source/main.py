import math
import MySQLdb
import curses
from curses import wrapper

def get_name(list, page, y_pos):

     for x in list:
	  if x[1] == page and x[2] == y_pos:
	       return x[0]

     return -1

def draw_list(list, cur_page, window):

     k = 1 + (cur_page - 1) * 10
     for y in list:
	  if y[1] == cur_page:
	       window.addstr(y[2], 0, str(k) + " " + y[0])
	       k += 1
     if cur_page > 1:
	  window.addstr(12, 0, "<- Prev Page")
     if cur_page < math.ceil(len(list) / 10.0):
	  window.addstr(13, 0, "-> Next Page")
     window.move(0, 0)

def db_overview(stdscr, db):

     curses.noecho() #do not display keyboard input

     cur_page = 1 
     page_num = 1

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
	  db_list.append((x[0], page_num, i))
	  i += 1
	  if i == 10: 
	       page_num += 1
	       i = 0
    
     #10 listings per page
     num_pages = math.ceil(len(db_list) / 10.0)

     begin_x = 34
     begin_y = 6
     height = 15
     width = 40
     list_win = curses.newwin(height, width, begin_y, begin_x)
     list_win.keypad(1)
     
     #draw list
     draw_list(db_list, cur_page, list_win)
	  

     stdscr.addstr(22, 2, "U - USE    D - DROP    C - CREATE NEW DATABASE        Q - QUIT")
     stdscr.refresh()
     list_win.refresh()
     
     #handle key presses

     while 1:
	  input = list_win.getch()
	  cur_pos = list_win.getyx()
	  #stdscr.addstr(1,1, str(input))
	  if input == curses.KEY_UP:
	       if cur_pos[0] > 0:
		    list_win.move(cur_pos[0] - 1, cur_pos[1])
	  elif input == curses.KEY_DOWN: 
	       if cur_pos[0] < 9 and cur_pos[0] < (len(db_list) - (cur_page - 1) * 10) - 1:
		    list_win.move(cur_pos[0] + 1, cur_pos[1])
	       
	  elif input == curses.KEY_LEFT:
	       if cur_page > 1:
		    cur_page -= 1
		    list_win.erase()
		    draw_list(db_list, cur_page, list_win)


	  elif input == curses.KEY_RIGHT:
	       if cur_page < num_pages:
		    cur_page += 1
		    list_win.erase()
		    draw_list(db_list, cur_page, list_win)
	  elif input == ord('u'): 
	       db_name = get_name(db_list, cur_page, cur_pos[0])
	       table_overview(stdscr, db, db_name)
	       return
	  elif input == ord('d'): 
	       db_name = get_name(db_list, cur_page, cur_pos[0])
	       stdscr.addstr(21, 2, "Are you sure you want to DROP " + db_name + "? (y/n)")
	       res = stdscr.getch()
	       if res == ord('y'):
		    cursor.execute("DROP DATABASE  " + db_name)
		    db_overview(stdscr, db)
		    return
	       else:
		    db_overview(stdscr, db)
		    return


	  elif input == ord('q'): 
	       curses.endwin()
	       exit()

	  stdscr.refresh()
	  list_win.refresh()
    
     


def table_overview(stdscr, db, db_name):

     cur_page = 1
     page_num = 1

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
	  table_list.append((x[0], page_num, i))
	  i += 1
	  if i == 10:
	       page_num += 1
	       i = 0
     
     
     #10 listings per page
     num_pages = math.ceil(len(table_list) / 10.0)

     begin_x = 34
     begin_y = 6
     height = 15
     width = 40
     list_win = curses.newwin(height, width, begin_y, begin_x)
     list_win.keypad(1)
     
     draw_list(table_list, cur_page, list_win)
      
     stdscr.addstr(22, 2, "V - VIEW    D - DELETE    C - CREATE TABLE    B - BACK        Q - QUIT")
     stdscr.refresh()
     list_win.refresh()
     
     #handle key presses

     while 1:
	  input = list_win.getch()
	  cur_pos = list_win.getyx()
	  
	  if input == curses.KEY_UP:
	       if cur_pos[0] > 0:
		    list_win.move(cur_pos[0] - 1, cur_pos[1])
	  elif input == curses.KEY_DOWN:
	       if cur_pos[0] < 9 and cur_pos[0] < (len(table_list) - (cur_page - 1) * 10) - 1:
		    list_win.move(cur_pos[0] + 1, cur_pos[1])
	  elif input == curses.KEY_LEFT:
	       if cur_page > 1:
		    cur_page -= 1
		    list_win.erase()
		    draw_list(table_list, cur_page, list_win)
	  elif input == curses.KEY_RIGHT:
	       if cur_page < num_pages:
		    cur_page += 1
		    list_win.erase()
		    draw_list(table_list, cur_page, list_win)
	       
	  elif input == ord('v'):
	       #view
	       temp = 1
	  elif input == ord('d'): #delete table 
	       table_name = get_name(table_list, cur_page, cur_pos[0])
	       stdscr.addstr(21, 2, "Are you sure you want to DROP " + table_name + "? (y/n)")
	       res = stdscr.getch()
	       if res == ord('y'):
		    cursor.execute("DROP TABLE  " + table_name)
		    table_overview(stdscr, db, db_name)
		    return
	       else:
		    table_overview(stdscr, db, db_name)
		    return
	  elif input == ord('c'): 
	       #create
	       temp = 1
	  elif input == ord('b'):
	       #back
	       db_overview(stdscr, db)
	       
	  elif input == ord('q'):
	       #quit
	       curses.endwin()
	       exit()

	  stdscr.refresh()
	  list_win.refresh()



    


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

	db = MySQLdb.connect(host=hostname_db, user=username_db, passwd=password_db)
	if db.cursor():
		stdscr.addstr(20, 30, "Connected!")
		db_overview(stdscr, db)

	#incorrect credentials produce ugly traceback. does not fail gracefully.
	else:
		stdscr.addstr(20, 30, "Connection failed.")
	
	#stdscr.addstr(21, 30, "", curses.A_BLINK)
	
	db.close()

	stdscr.getch()

	curses.endwin()

wrapper(main)
