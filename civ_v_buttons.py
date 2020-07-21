from tkinter import *
import pymysql
import credentials

def create_civ_v_buttons(root):
    def write_label_delete(win):
        row = 0
        #NOT SURE IF THIS SHOULD BE UP TO THE USER
        id_ = Entry(win,width=30,bg="royalblue2")
        id_.grid(row=row,column=1,padx=20)
        id_label = Label(win, text="ID",bg="royalblue2")
        id_label.grid(row=row,column=0)

        return id_

    def write_labels(win):
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

        age = Entry(win,width=30,bg="royalblue2")
        age.grid(row=row,column=1)
        age_label = Label(win, text="Age",bg="royalblue2")
        age_label.grid(row=row,column=0)
        row+=1

        race = Entry(win,width=30,bg="royalblue2")
        race.grid(row=row,column=1)
        race_label = Label(win, text="Race",bg="royalblue2")
        race_label.grid(row=row,column=0)
        row+=1

        date_of_death = Entry(win,width=30,bg="royalblue2")
        date_of_death.grid(row=row,column=1)
        dod_label = Label(win, text="Date of Death",bg="royalblue2")
        dod_label.grid(row=row,column=0)
        row+=1

        gender = Entry(win,width=30,bg="royalblue2")
        gender.grid(row=row,column=1)
        gender_label = Label(win, text="Gender",bg="royalblue2")
        gender_label.grid(row=row,column=0)
        row+=1

        cause = Entry(win,width=30,bg="royalblue2")
        cause.grid(row=row,column=1)
        cause_label = Label(win, text="Cause of Death",bg="royalblue2")
        cause_label.grid(row=row,column=0)
        row+=1

        city_name = Entry(win,width=30,bg="royalblue2")
        city_name.grid(row=row,column=1)
        city_name_label = Label(win, text="Location of Death (City)",bg="royalblue2")
        city_name_label.grid(row=row,column=0)
        row+=1

        state_name = Entry(win,width=30,bg="royalblue2")
        state_name.grid(row=row,column=1)
        state_name_label = Label(win, text="Location of Death (State)",bg="royalblue2")
        state_name_label.grid(row=row,column=0)
        row+=1

        return id_,name,age,race,date_of_death,gender,cause,city_name,state_name

    def pop_up_insert():
        win = Toplevel(bg="black")
        win.wm_title("Insert Civilian Victim")
        win.geometry("500x350")

        id_,name,age,race,date_of_death,gender,cause,city_name,state_name = write_labels(win)
        
        
        def submit():
            
            #clears the text from the boxes
            id_text = id_.get()
            name_text = name.get()
            age_text = age.get()
            race_text = race.get()
            date_of_death_text = date_of_death.get()
            gender_text = gender.get()
            cause_text = cause.get()
            city_name_text = city_name.get()
            state_name_text= state_name.get()
            
            try:
                connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name)
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "INSERT INTO civilian (dead_civilian_id,cname,\
                        age,gender,race,death_date,city_name,state_abbr,cause) \
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (id_text,name_text,age_text, 
                    gender_text,race_text,date_of_death_text,city_name_text,state_name_text,cause_text))
                    connection.commit()
                # connection is not autocommit by default. So you must commit to save
                # your changes.

            finally:
                connection.close()
                id_.delete(0, END)
                name.delete(0, END)
                age.delete(0, END)
                race.delete(0, END)
                date_of_death.delete(0, END)
                gender.delete(0, END)
                cause.delete(0, END)
                city_name.delete(0,END)
                state_name.delete(0,END)


        a = Button(win, text="Insert into database", command=submit,highlightbackground="royalblue2")
        a.grid(row=10, column=0)

    def pop_up_search():
        win = Toplevel(bg="black")
        win.wm_title("Search Civilian Victim")
        win.geometry("500x350")

        id_,name,age,race,date_of_death,gender,cause,city_name,state_name = write_labels(win)

        def search():
            #clears the text from the boxes
            id_.delete(0, END)
            name.delete(0, END)
            age.delete(0, END)
            race.delete(0, END)
            date_of_death.delete(0, END)
            gender.delete(0, END)
            cause.delete(0, END)
            city_name.delete(0,END)
            state_name.delete(0,END)
        b = Button(win, text="Search in database", command=search,highlightbackground="royalblue2")
        b.grid(row=10, column=0)

    def pop_up_delete():
        win = Toplevel(bg="black")
        win.wm_title("Delete Civilian Victim")
        win.geometry("500x350")

        id_= write_label_delete(win)
        def delete():
            #clears the text from the boxes
            id_text = id_.get()
            
            try:
                connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name)
                with connection.cursor() as cursor:
                    # Create a new record
                    sql = "DELETE FROM civilian WHERE dead_civilian_id=%s"
                    cursor.execute(sql, (id_text))
                    connection.commit()
                # connection is not autocommit by default. So you must commit to save
                # your changes.

            finally:
                connection.close()
                id_.delete(0, END)

            
        c = Button(win, text="Delete from database", command=delete,highlightbackground="royalblue2")
        c.grid(row=8, column=0)
    
        
    row=6
    insert_btn = Button(root, text="Insert new Civilian Victim", command=pop_up_insert,highlightbackground="royalblue2")
    insert_btn.grid(row=row,column=0,columnspan=2, pady=20,padx=10,ipadx=50)
    row+=1
    
    delete_btn = Button(root, text="Search for Civilian Victim", command=pop_up_search,highlightbackground="royalblue2")
    delete_btn.grid(row=row,column=0,columnspan=2, pady=20,padx=10,ipadx=50)
    row+=1
    
    search_btn = Button(root, text="Delete Civilian Victim from Records", command=pop_up_delete,highlightbackground="royalblue2")
    search_btn.grid(row=row,column=0,columnspan=2, pady=20,padx=10,ipadx=50)
    row+=1