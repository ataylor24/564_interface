from tkinter import *
import pymysql
import credentials

def create_police_buttons(root):
    def write_label_delete(win):
        row = 0
        #NOT SURE IF THIS SHOULD BE UP TO THE USER
        id_ = Entry(win,width=30,bg="royalblue2")
        id_.grid(row=row,column=1,padx=20)
        id_label = Label(win, text="ID",bg="royalblue2")
        id_label.grid(row=row,column=0)

        return id_

    def write_label(win):
        row = 0
        #NOT SURE IF THIS SHOULD BE UP TO THE USER
        id_ = Entry(win,width=30,bg="royalblue2")
        id_.grid(row=row,column=1,padx=20)
        id_label = Label(win, text="ID",bg="royalblue2")
        id_label.grid(row=row,column=0)
        row+=1

        name = Entry(win,width=30,bg="royalblue2")
        name.grid(row=row,column=1)
        name_label = Label(win, text="Name",bg="royalblue2")
        name_label.grid(row=row,column=0)
        row+=1

        date_of_death = Entry(win,width=30,bg="royalblue2")
        date_of_death.grid(row=row,column=1)
        dod_label = Label(win, text="Date of Death",bg="royalblue2")
        dod_label.grid(row=row,column=0)
        row+=1

        cause = Entry(win,width=30,bg="royalblue2")
        cause.grid(row=row,column=1)
        cause_label = Label(win, text="Cause of Death",bg="royalblue2")
        cause_label.grid(row=row,column=0)
        row+=1

        dept = Entry(win,width=30,bg="royalblue2")
        dept.grid(row=row,column=1)
        dept_label = Label(win, text="Worked For (Department)",bg="royalblue2")
        dept_label.grid(row=row,column=0)
        row+=1 

        state_abbr = Entry(win,width=30,bg="royalblue2")
        state_abbr.grid(row=row,column=1)
        state_abbr_label = Label(win, text="State Abbreviation",bg="royalblue2")
        state_abbr_label.grid(row=row,column=0)
        row+=1

        return id_,name,date_of_death,cause,dept,state_abbr

    def pop_up_insert():
        win = Toplevel(bg="black")
        win.wm_title("Insert Police Victim")
        win.geometry("600x200")

        id_,name,date_of_death,cause,dept,state_abbr = write_label(win)

        def insert():
            id_text = id_.get()
            name_text = name.get()
            date_of_death_text = date_of_death.get()
            cause_text = cause.get()
            dept_text = dept.get()
            state_abbr_text = state_abbr.get()
            connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name)
            try:
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO officer (dead_officer_id,officer_name,dept,\
                        cause_short,death_date,state_abbr) VALUES (%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (id_text,name_text,dept_text,cause_text,date_of_death_text,state_abbr_text))
                    connection.commit()
                # connection is not autocommit by default. So you must commit to save
                # your changes.
            finally:
                connection.close()
                #clears the text from the boxes
                id_.delete(0, END)
                name.delete(0, END)
                date_of_death.delete(0, END)
                cause.delete(0, END)
                dept.delete(0,END)
                state_abbr.delete(0,END)
        a = Button(win, text="Insert into database", command=insert,highlightbackground="royalblue2")
        a.grid(row=7, column=0)

    def pop_up_search():
        win = Toplevel(bg="black")
        win.wm_title("Search Police Victim")
        win.geometry("600x200")

        id_,name,date_of_death,cause,dept,state_abbr = write_label(win)
        def search():
            #clears the text from the boxes
            id_.delete(0, END)
            name.delete(0, END)
            date_of_death.delete(0, END)
            cause.delete(0, END)
            dept.delete(0,END)
            state_abbr.delete(0,END)
        c = Button(win, text="Search in database", command=search,highlightbackground="royalblue2")
        c.grid(row=7, column=0)
            
    def pop_up_delete():
        win = Toplevel(bg="black")
        win.wm_title("Delete Police Victim")
        win.geometry("600x200")

        id_ = write_label_delete(win)
        def delete():
            #clears the text from the boxes
            id_.delete(0, END)
        
        b = Button(win, text="Delete from database", command=delete,highlightbackground="royalblue2")
        b.grid(row=6, column=0)

    row =11
    insert_btn = Button(root, text="Insert new Police Victim", command=pop_up_insert,highlightbackground="royalblue2")
    insert_btn.grid(row=row,column=0,columnspan=2, pady=20,padx=10,ipadx=50)
    
    row+=1
    
    search_btn = Button(root, text="Search for Police Victim", command=pop_up_search,highlightbackground="royalblue2")
    search_btn.grid(row=row,column=0,columnspan=2, pady=20,padx=10,ipadx=50)
    
    row+=1
        
    delete_btn = Button(root, text="Delete Police Victim from Records", command=pop_up_delete,highlightbackground="royalblue2")
    delete_btn.grid(row=row,column=0,columnspan=2, pady=20,padx=10,ipadx=50)
    
    row+=1