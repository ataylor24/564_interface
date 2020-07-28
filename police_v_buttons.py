from tkinter import *
import pymysql
import credentials
import re

def dropdown_choices(attribute):
    connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name,
    cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = "SELECT distinct %s FROM officer" % (attribute)
        cursor.execute(sql)
        choices = {dict_[attribute] for dict_ in cursor.fetchall()}
        choices = sorted(choices)
    
    return choices

def dept_dropdown_choices():
    connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name,
    
    cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = "select distinct dept from department order by dept asc"
        cursor.execute(sql)
        choices = {dict_["dept"] for dict_ in cursor.fetchall()}
        choices = sorted(choices)

    return choices
   
#code for creating each of the police officer buttons and the subsequently created popup windows
def create_police_buttons(root):
    #Handles the creation of the popup window containing the search results
    def popup_search_res(search_result):
        #creates the popup window
        win = Toplevel(bg="black")
        win.wm_title("Search Result")
        win.geometry("1200x800")

        scrollbar = Scrollbar(win)
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox = Listbox(win, yscrollcommand=scrollbar.set,width=150,bg="black",fg="royalblue2")
        title_row = "DEAD_OFFICER_ID, OFFICER_NAME, DEPT, CAUSE_OF_DEATH, DEATH_DATE, LOC OF DEATH (STATE)"
        listbox.insert(END, title_row)
        for result_dict in search_result:
            row = ""+str(result_dict['dead_officer_id'])+", "+result_dict['officer_name']+", "\
            +str(result_dict['d.dept'])+", "+result_dict['cause_short']+", "+result_dict['death_date']+", "+result_dict['state_abbr']
            listbox.insert(END, row)
        listbox.pack(side=LEFT, fill=BOTH)

    #Handles the creation of the labels/entry boxes for delete
    def write_label_delete(win):
        row = 0
        #NOT SURE IF THIS SHOULD BE UP TO THE USER
        id_ = Entry(win,width=30,bg="royalblue2")
        id_.grid(row=row,column=1,padx=20)
        id_label = Label(win, text="ID",bg="royalblue2")
        id_label.grid(row=row,column=0)

        return id_

    #Handles the creation of the labels/entry boxes for search/insert
    def write_label(win):
        row = 0
        # creates label for officer name and the text box for user 
        # to input the desired insert/search criterion
        name = Entry(win,width=30,bg="royalblue2")
        name.grid(row=row,column=1)
        name_label = Label(win, text="Name",bg="royalblue2")
        name_label.grid(row=row,column=0)
        row+=1

        # creates label for civilian date of death and the text box for user 
        # to input the desired insert/search criterion
        dod = Entry(win,width=30,bg="royalblue2")
        dod.grid(row=row,column=1)
        dod_label = Label(win, text="Date of Death (mm/dd/yyyy)",bg="royalblue2")
        dod_label.grid(row=row,column=0)
        row+=1

        # creates dropdown for officer cause of death and queries the DB so the user 
        # may select their desired insert/search criterion
        cause = StringVar(root)
        cause.set('Unspecified') # set the default option
        cause_dropdown = OptionMenu(win, cause, *dropdown_choices("cause_short"))
        cause_dropdown.grid(row = row, column =1)
        cause_label = Label(win, text="Cause of Death",bg="royalblue2")
        cause_label.grid(row=row,column=0)
        row+=1

        # creates label for officer department of employment and the text box for user 
        # to input the desired insert/search criterion
        dept = StringVar(root)
        dept.set('')
        dept_dropdown = OptionMenu(win, dept, *dept_dropdown_choices())
        dept_dropdown.grid(row=row,column=1)
        dept_label = Label(win, text="Worked For (Department)",bg="royalblue2")
        dept_label.grid(row=row,column=0)
        row+=1 

        # creates label for officer location of death (state) and the text box for user 
        # to input the desired insert/search criterion
        # state_abbr = Entry(win,width=30,bg="royalblue2")
        # state_abbr.grid(row=row,column=1)
        # state_abbr_label = Label(win, text="State Abbreviation",bg="royalblue2")
        # state_abbr_label.grid(row=row,column=0)
        # row+=1

        state_abbr = StringVar(root)
        state_abbr.set('Unspecified') # set the default option
        state_abbr_dropdown = OptionMenu(win, state_abbr, *dropdown_choices("state_abbr"))
        state_abbr_dropdown.grid(row = row, column =1)
        state_abbr_label = Label(win, text="State Abbreviation",bg="royalblue2")
        state_abbr_label.grid(row=row,column=0)
        row+=1

        return name,dod,cause,dept,state_abbr

    #creates the popup window for the 'insert new officer victim' button
    def pop_up_insert():
        #creates the window itself
        win = Toplevel(bg="black")
        win.wm_title("Insert Police Victim")
        win.geometry("600x400")

        #writes the labels/entry boxes in the window
        name,dod,cause,dept,state_abbr = write_label(win)

        def insert():
            #retrieves the text from the boxes
            name_text = name.get()
            date_of_death_text = dod.get()
            cause_text = cause.get() if "Unspecified" in cause.get() else ""
            dept_text = dept.get()
            state_abbr_text = state_abbr.get()

            r = re.compile('../../....')
            if len(date_of_death_text) > 0 and r.match(date_of_death_text) is None:
                win = Toplevel(bg="black")
                win.wm_title("Incorrect Formatting")
                win.geometry("700x350")

                title = Label(win, text="Incorrect formatting of the date, should be 'mm/dd/yyyy'",fg="red",bg="black")
                title.grid(row=1,column=0,columnspan=2,ipadx=50)
                title.config(font=("Times New Roman", 20))
                return

            #establishes the connection with the db
            connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name)
            try:
                with connection.cursor() as cursor:
                    retrieve_max_id = "select max(dead_officer_id) from officer"
                    cursor.execute(retrieve_max_id)
                    id_text = int(cursor.fetchall()[0][0]) + 1
                    print(id_text)

                    find_dept_id = "select dept_id from department where dept = \"%s\"" %(dept_text)
                    cursor.execute(find_dept_id)
                    dept_id = cursor.fetchall()[0][0]
                    # Create a new record
                    sql = "INSERT INTO officer (dead_officer_id,officer_name,dept,\
                        cause_short,death_date,state_abbr) VALUES (%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (id_text,name_text,dept_id,cause_text,date_of_death_text,state_abbr_text))
                    connection.commit()
                # connection is not autocommit by default. So you must commit to save
                # your changes.
            finally:
                connection.close()
                #clears the text from the boxes
                name.delete(0, END)
                dod.delete(0, END)
                #cause.delete(0, END)
                
                #state_abbr.delete(0,END)
        
        #establishes the button to insert the provided info into the db
        a = Button(win, text="Insert into database", command=insert,highlightbackground="royalblue2")
        a.grid(row=12, column=0)

    #Establishes the popup window for the 'search for police victim' button
    def pop_up_search():
        #creates the window
        win = Toplevel(bg="black")
        win.wm_title("Search Police Victim")
        win.geometry("600x400")

        #writes the labels/entry boxes
        name,dod,cause,dept,state_abbr = write_label(win)

        def search():
            #retrieves the text from the boxes
            name_text = name.get()
            date_of_death_text = dod.get()
            cause_text = cause.get() if "Unspecified" not in cause.get() else ""
            dept_text = dept.get()
            state_abbr_text = state_abbr.get()  if "Unspecified" not in state_abbr.get() else ""

            r = re.compile('../../....')
            if len(date_of_death_text) > 0 and r.match(date_of_death_text) is None:
                win = Toplevel(bg="black")
                win.wm_title("Incorrect Formatting")
                win.geometry("700x350")

                title = Label(win, text="Incorrect formatting of the date, should be 'mm/dd/yyyy'",fg="red",bg="black")
                title.grid(row=1,column=0,columnspan=2,ipadx=50)
                title.config(font=("Times New Roman", 20))
                return

            try:
                #establishes connection with db
                connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name,
                cursorclass=pymysql.cursors.DictCursor)
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM officer o,department d WHERE (o.officer_name like '%"
                    name_list = name_text.split(' ')
                    dept_list = dept_text.split('\'')
                    sql = sql +name_list[0] + "%'"
                    for i in range(1,len(name_list)):
                        sql = sql + "or o.officer_name like '%" + name_list[i] + "%'"
                    sql = sql+") and o.dept like d.dept_id and d.dept like '%" + dept_list[0] + "%'"\
                    + "and o.death_date like '%" + date_of_death_text + "%'" + \
                    "and o.cause_short like '%" + cause_text + "%'" + "and o.state_abbr like '%" + state_abbr_text + "%'"
                    cursor.execute(sql)
                    print(sql)
                    search_result = cursor.fetchall()
                   
                    connection.commit()
                # connection is not autocommit by default. So you must commit to save
                # your changes.
            finally:
                connection.close()
                #clears the text from the boxes
                name.delete(0, END)
                dod.delete(0, END)
                
                popup_search_res(search_result)

        #establishes the button for searching the database
        c = Button(win, text="Search in database", command=search,highlightbackground="royalblue2")
        c.grid(row=12, column=0)
    
    #Establishes the popup window for the 'delete police victim from records' button
    def pop_up_delete():
        #establishes the popup window
        win = Toplevel(bg="black")
        win.wm_title("Delete Police Victim")
        win.geometry("600x200")

        #writes the label/entry box
        id_ = write_label_delete(win)

        def delete():
            #retrives the text from the boxes
            id_text = id_.get()
            try:
                connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name)
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "DELETE FROM officer WHERE officer.dead_officer_id=%s"
                    cursor.execute(sql, (id_text))
                    connection.commit()
                # connection is not autocommit by default. So you must commit to save
                # your changes.
                
            finally:
                #closes connection and clears text from the box
                connection.close()
                id_.delete(0, END)
            
        #establishes the button for deleting from the databsase
        b = Button(win, text="Delete from database", command=delete,highlightbackground="royalblue2")
        b.grid(row=6, column=0)

    row =11
    #establishes the insert button on the root window
    insert_btn = Button(root, text="Insert new Police Victim", command=pop_up_insert,highlightbackground="royalblue2")
    insert_btn.grid(row=row,column=0,columnspan=2, pady=20,padx=10,ipadx=50)
    
    row+=1
    #establishes the search button on the root window
    search_btn = Button(root, text="Search for Police Victim", command=pop_up_search,highlightbackground="royalblue2")
    search_btn.grid(row=row,column=0,columnspan=2, pady=20,padx=10,ipadx=50)
    
    row+=1
    #establishes the delete button on the root window
    delete_btn = Button(root, text="Delete Police Victim from Records", command=pop_up_delete,highlightbackground="royalblue2")
    delete_btn.grid(row=row,column=0,columnspan=2, pady=20,padx=10,ipadx=50)