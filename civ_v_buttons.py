from tkinter import *
import pymysql
import credentials

#Queries the civilian table for the passed attribute and returns a dict
def dropdown_choices(attribute):
    connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name,
    cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = "SELECT distinct %s FROM civilian" % (attribute)
        cursor.execute(sql)
        choices = {dict_[attribute] for dict_ in cursor.fetchall()}
    
    return choices

#code for creating each of the civilian buttons and the subsequently created popup windows
def create_civ_v_buttons(root):
    #Handles the creation of the popup window containing the search results
    def popup_search_res(search_result):
        #creates the popup window
        win = Toplevel(bg="black")
        win.wm_title("Search Result")
        win.geometry("1200x800")
        #creates the category labels
        scrollbar = Scrollbar(win)
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox = Listbox(win, yscrollcommand=scrollbar.set,width=150,bg="black",fg="royalblue2")
        title_row = "DEAD_CIVILIAN_ID, CIVILIAN_NAME, AGE, GENDER, RACE, DEATH_DATE, LOC OF DEATH (CITY), LOC OF DEATH (STATE), CAUSE"
        listbox.insert(END, title_row)
        for result_dict in search_result:
            row = ""+str(result_dict['dead_civilian_id'])+", "+result_dict['cname']+", "\
            +result_dict['age']+", "+result_dict['gender']+", "+result_dict['race']+\
            ", "+result_dict['death_date']+", "+result_dict['city_name']+", "+result_dict['state_abbr']\
            +", "+result_dict['cause']
            listbox.insert(END, row)
        listbox.pack(side=LEFT, fill=BOTH)

        scrollbar.config(command=listbox.yview)

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
    def write_labels(win):
        row = 0
        
        # creates label for civilian ID and the text box for user 
        # to input the desired insert/search criterion
        id_ = Entry(win,width=30,bg="royalblue2")
        id_.grid(row=row,column=1,padx=20)
        id_label = Label(win, text="ID",bg="royalblue2")
        id_label.grid(row=row,column=0)
        row+=1

        # creates label for civilian name and the text box for user 
        # to input the desired insert/search criterion
        name = Entry(win,width=30,bg="royalblue2")
        name.grid(row=row,column=1)
        name_label = Label(win, text="Name",bg="royalblue2")
        name_label.grid(row=row,column=0)
        row+=1

        # creates label for civilian age and the text box for user 
        # to input the desired insert/search criterion
        age = Entry(win,width=30,bg="royalblue2")
        age.grid(row=row,column=1)
        age_label = Label(win, text="Age",bg="royalblue2")
        age_label.grid(row=row,column=0)
        row+=1

        # creates dropdown for civilian race and queries the DB so the user 
        # may select their desired insert/search criterion
        race = StringVar(root)
        race.set('Unspecified') # set the default option
        race_dropdown = OptionMenu(win, race, *dropdown_choices("race"))
        race_dropdown.grid(row = row, column =1)
        race_label = Label(win, text="Race",bg="royalblue2")
        race_label.grid(row=row,column=0)
        row+=1

        # creates label for civilian ID and the text box for user 
        # to input the desired insert/search criterion
        dod = Entry(win,width=30,bg="royalblue2")
        dod.grid(row=row,column=1)
        dod_label = Label(win, text="Date of Death",bg="royalblue2")
        dod_label.grid(row=row,column=0)  
        row+=1

        # creates dropdown for civilian gender and queries the DB so the user 
        # may select their desired insert/search criterion
        gender = StringVar(root)
        gender.set('Unspecified') # set the default option
        gender_dropdown = OptionMenu(win, gender, *dropdown_choices("gender"))
        gender_dropdown.grid(row = row, column =1)
        gender_label = Label(win, text="Gender",bg="royalblue2")
        gender_label.grid(row=row,column=0)
        row+=1

        # creates label for civilian cause of death and the text box for user 
        # to input the desired insert/search criterion
        cause = Entry(win,width=30,bg="royalblue2")
        cause.grid(row=row,column=1)
        cause_label = Label(win, text="Cause of Death",bg="royalblue2")
        cause_label.grid(row=row,column=0)
        row+=1

        # creates label for civilian location of death (city) and the text box for user 
        # to input the desired insert/search criterion
        city_name = Entry(win,width=30,bg="royalblue2")
        city_name.grid(row=row,column=1)
        city_name_label = Label(win, text="Location of Death (City)",bg="royalblue2")
        city_name_label.grid(row=row,column=0)
        row+=1

        # creates label for civilian location of death (state) and the text box for user 
        # to input the desired insert/search criterion
        state_name = Entry(win,width=30,bg="royalblue2")
        state_name.grid(row=row,column=1)
        state_name_label = Label(win, text="Location of Death (State)",bg="royalblue2")
        state_name_label.grid(row=row,column=0)
        row+=1

        return id_,name,age,race,dod,gender,cause,city_name,state_name

    #creates the popup window for the 'insert new civilian victim' button
    def pop_up_insert():
        #creates the window itself
        win = Toplevel(bg="black")
        win.wm_title("Insert Civilian Victim")
        win.geometry("500x350")

        #writes the labels/entry boxes in the window
        id_,name,age,race,dod,gender,cause,city_name,state_name= write_labels(win)
        
        
        def submit():
            #retrieves the text from the boxes
            id_text = id_.get()
            name_text = name.get()
            age_text = age.get()
            race_text = race.get()
            date_of_death_text = dod.get()
            gender_text = gender.get()
            cause_text = cause.get()
            city_name_text = city_name.get()
            state_name_text= state_name.get()
            
            try:
                #establishes the connection with the db
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
                #closes connection to the db
                connection.close()
                
                #clears the text from the boxes to ready it for a new query
                id_.delete(0, END)
                name.delete(0, END)
                age.delete(0, END)
                dod.delete(0, END)
                cause.delete(0, END)
                city_name.delete(0,END)
                state_name.delete(0,END)

        #establishes the button to insert the provided info into the db
        a = Button(win, text="Insert into database", command=submit,highlightbackground="royalblue2")
        a.grid(row=14, column=0)

    #Establishes the popup window for the 'search for civilian victim' button
    def pop_up_search():
        #creates the window
        win = Toplevel(bg="black")
        win.wm_title("Search Civilian Victim")
        win.geometry("500x350")

        #writes the labels/entry boxes
        id_,name,age,race,dod,gender,cause,city_name,state_name = write_labels(win)

        def search():
            #retrieves the text from the boxes
            id_text = id_.get()
            name_text = name.get()
            age_text = age.get()
            race_text = race.get() if "Unspecified" not in race.get() else ""
            date_of_death_text = dod.get()
            gender_text = gender.get() if "Unspecified" not in gender.get() else ""
            cause_text = cause.get()
            city_name_text = city_name.get()
            state_name_text= state_name.get()
            try:
                #establishes connection with db
                connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name,
                cursorclass=pymysql.cursors.DictCursor)
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM civilian WHERE dead_civilian_id LIKE '%" + id_text + "%'" + \
                    "and cname like '%"
                    name_list = name_text.split(' ')
                    sql = sql + name_list[0] + "%'"
                    for i in range(1,len(name_list)):
                        sql = sql + "or cname like '%" + name_list[i] + "%'"
                    sql = sql + "and age like '%" + age_text + "%'" + \
                    "and race like '%" + race_text + "%'" + "and death_date like '%" + date_of_death_text + "%'" + \
                    "and gender like '%" + gender_text + "%'" + "and cause like '%" + cause_text + "%'" + \
                    "and city_name like '%" + city_name_text + "%'" + "and state_abbr like '%" + state_name_text + "%'"
                    print(sql)
                    cursor.execute(sql)
                    search_result = cursor.fetchall()
                    
                    print(search_result)
                    connection.commit()
                # connection is not autocommit by default. So you must commit to save
                # your changes.
            finally:
                #clears the text from the boxes
                connection.close()
                id_.delete(0, END)
                name.delete(0, END)
                age.delete(0, END)
                dod.delete(0, END)
                cause.delete(0, END)
                city_name.delete(0,END)
                state_name.delete(0,END)
                popup_search_res(search_result)
                
        #establishes the button for searching the database
        b = Button(win, text="Search in database", command=search,highlightbackground="royalblue2")
        b.grid(row=14, column=0)

    #Establishes the popup window for the 'delete civilian victim from records' button
    def pop_up_delete():
        #establishes the popup window
        win = Toplevel(bg="black")
        win.wm_title("Delete Civilian Victim")
        win.geometry("500x350")
        #writes the label/entry box
        id_= write_label_delete(win)
        def delete():
            #retrieves the text from the boxes
            id_text = id_.get()
            
            try:
                #Establishes a conenction with the db
                connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name)
                with connection.cursor() as cursor:
                    # removes a record
                    sql = "DELETE FROM civilian WHERE dead_civilian_id=%s"
                    cursor.execute(sql, (id_text))
                    connection.commit()
                # connection is not autocommit by default. So you must commit to save
                # your changes.

            finally:
                #clears the text from the boxes and closes the connection to the db
                connection.close()
                id_.delete(0, END)

        
        #establishes the button for deleting from the databsase
        c = Button(win, text="Delete from database", command=delete,highlightbackground="royalblue2")
        c.grid(row=8, column=0)
    
    #establishes the insert button on the root window
    row=6
    insert_btn = Button(root, text="Insert new Civilian Victim", command=pop_up_insert,highlightbackground="royalblue2")
    insert_btn.grid(row=row,column=0,columnspan=2, pady=20,padx=10,ipadx=50)
    row+=1
    #establishes the delete button on the root window
    delete_btn = Button(root, text="Search for Civilian Victim", command=pop_up_search,highlightbackground="royalblue2")
    delete_btn.grid(row=row,column=0,columnspan=2, pady=20,padx=10,ipadx=50)
    row+=1
    #establishes the search button on the root window
    search_btn = Button(root, text="Delete Civilian Victim from Records", command=pop_up_delete,highlightbackground="royalblue2")
    search_btn.grid(row=row,column=0,columnspan=2, pady=20,padx=10,ipadx=50)