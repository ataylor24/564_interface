from tkinter import *
import pymysql
import credentials
#returns choices needed for the dropdown menu
def dropdown_choices(attribute):
    #open connection using mysql credentials in order to access database - uses credentials.py
    connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name,
    cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        #Find possible choices for dropdown
        sql = "SELECT distinct %s FROM civilian" % (attribute)
        cursor.execute(sql)
        #grab each possible choice and sort
        choices = {dict_[attribute] for dict_ in cursor.fetchall()}
        choices = sorted(choices)
    #return list of choices    
    return choices
#creates the special query buttons
def create_special_query_btns(root):
    #Pop up created from searching using the Find Where Specific Police Departments Act query
    def popup_acts_res(act_result):
        #create window
        win = Toplevel(bg="black")
        win.wm_title("Search Result")
        win.geometry("1200x800")
        #create scrollbar on the right side of the screen
        scrbar = Scrollbar(win)
        scrbar.pack(side=RIGHT, fill = Y)
        #create listbox to display results
        lsbox = Listbox(win, yscrollcommand = scrbar.set,width=150, bg="black",fg="royalblue2")
        #insert title to listbox
        title = "Department, City, State"
        lsbox.insert(END, title)
        #iterate through results of query and add them to the listbox
        for result_dict in act_result:
            row = ""+result_dict['dept']+\
            ", "+result_dict['city_name']+", "+result_dict['state_abbr']
            lsbox.insert(END, row)
        #pack listbox to the left and associate scrollbar and listbox
        lsbox.pack(side=LEFT, fill=BOTH)
        scrbar.config(command=lsbox.yview)

    #Pop up created from searching using the Find where Members of Police Departments have Died query
    def popup_dept_death_res(pd_st_result):
        #create window
        win = Toplevel(bg="black")
        win.wm_title("Search Result")
        win.geometry("1200x800")
        #create scrollbar on the right side of the screen
        sbar = Scrollbar(win)
        sbar.pack(side = RIGHT, fill = Y)
        #create listbox to display results
        lbox = Listbox(win, yscrollcommand=sbar.set,width=150,bg="black",fg="royalblue2")
        title = "Department, State"
        #insert title to listbox
        lbox.insert(END, title)
        #iterate through results of query and add them to the listbox
        for result_dict in pd_st_result:
           row = ""+result_dict['dept'] +","+result_dict['state_abbr']
           lbox.insert(END, row)
        #pack listbox to the left and associate scrollbar and listbox
        lbox.pack(side=LEFT, fill=BOTH)
        sbar.config(command=lbox.yview)
    #Pop up created from searching using the Find information on States query
    def state_result_popup(search_result):
        #create new window
        win = Toplevel(bg="black")
        win.wm_title("Search result")
        win.geometry("600x300")
        #Display titles of each column
        Label(win, text= 'State Abbreviation', borderwidth = 1, bg="royalblue2").grid(row = 0, column = 0)
        Label(win, text= 'State Name', borderwidth = 1, bg="royalblue2").grid(row = 0, column = 1)
        Label(win, text= 'Population 2010', borderwidth = 1, bg="royalblue2").grid(row = 0, column = 2)
        Label(win, text= 'Population 2019', borderwidth = 1, bg="royalblue2").grid(row = 0, column = 3)
        #iterate through results and display all relevant information
        i = 0
        for result_dict in search_result:
            i += 1
            Label(win, text = result_dict['state_abbr'], borderwidth = 1, bg="royalblue2").grid(row = i, column = 0)
            Label(win, text = result_dict['state_name'], borderwidth = 1, bg="royalblue2").grid(row = i, column = 1)
            Label(win, text = result_dict['population_2010'], borderwidth = 1, bg="royalblue2").grid(row = i, column = 2)
            Label(win, text = result_dict['population_2019'], borderwidth = 1, bg="royalblue2").grid(row = i, column = 3)
    
    #writes police department label and create the corresponding search box
    def write_label(win):
        row = 0
        pd_name = Entry(win,width=30,bg="royalblue2")
        pd_name.grid(row=row,column=1)
        pd_name_label = Label(win, text="Name of Police Department",bg="royalblue2")
        pd_name_label.grid(row=row,column=0)
        row+=1

        return pd_name
    
    #write state label and create the corresponding search box
    def write_label_state(win):
        row = 0

        pd_name = StringVar(root)
        pd_name.set('Unspecified')
        pd_name_dropdown = OptionMenu(win, pd_name, *dropdown_choices("state_abbr"))
        pd_name_dropdown.grid(row = row, column=1)
        pd_name_label = Label(win, text="Name of State",bg="royalblue2")
        pd_name_label.grid(row=row,column=0)
        row+=1

        return pd_name

    #Pop up for when user clicks on Find Where Specific Police Departments Have Killed button
    def pop_up_acts():
        #create window
        win = Toplevel(bg="black")
        win.wm_title("Find Where Specific Police Departments Act")
        win.geometry("600x200")
        #set up search box
        pd_name = write_label(win)
        #search function activated when user clicks the search button
        def search():
            #get the user's search details
            pd_text = pd_name.get()
            try:
                #open a connection using mysql credentials
                connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name,
                cursorclass=pymysql.cursors.DictCursor)
                with connection.cursor() as cursor:
                    #create sql query: query uses user input to find the location(city name and state name) where a police department
                    #acts in (using department to match department with a dept_id and acts_in to get relevant information)
                    sql = "select a.city_name, a.state_abbr, d.dept from acts_in a, department d where a.dept_id = d.dept_id and d.dept like '%" + pd_text +"%';"
                    cursor.execute(sql)
                    #get results from query as a list of dictionaries
                    act_result = cursor.fetchall()
                    connection.commit()
            finally:
                #close connection and open up the relevant pop up
                connection.close()
                pd_name.delete(0,END)
                popup_acts_res(act_result)
        #add button to search the database and bind it to the above search function
        a = Button(win, text="Search Database", command=search,highlightbackground="royalblue2")
        a.grid(row=2, column=0)
    #Pop up for when user clicks on Find where Members of Police Departments have Died button
    def pop_up_deaths():
        #create window
        win = Toplevel(bg="black")
        win.wm_title("Find where Members of Police Departments Have Died")
        win.geometry("600x200")
        #set up search box
        pd_name = write_label(win)
        #search function activated when user clicks the search button
        def search():
            #get user's input
            pd_text = pd_name.get()
            try:
                #open a connection using mysql credentials
                connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name,
                cursorclass=pymysql.cursors.DictCursor)
                with connection.cursor() as cursor:
                    #create sql query: query takes department name, matches it with the appropriate dept_id and uses relavent information
                    #from dept_deaths_in
                    sql = "select d.dept, e.state_abbr from department d, dept_deaths_in e where e.dept_id = d.dept_id and d.dept like '%" + pd_text + "%';"
                    cursor.execute(sql)
                    #get results of query as list of dictionaries
                    pd_st_result = cursor.fetchall()
                    connection.commit()
            finally:
                #close connection and open up relevant pop up window
                connection.close()
                pd_name.delete(0,END)
                popup_dept_death_res(pd_st_result)
        #add button to search the database and bind it to the above search function   
        a = Button(win, text="Search Database", command=search,highlightbackground="royalblue2")
        a.grid(row=2, column=0)
    #Pop up for when user clicks on Find Information on States button        
    def pop_up_states():
        #create window
        win = Toplevel(bg="black")
        win.wm_title("Find Information on States")
        win.geometry("600x200")
        #set up search box
        pd_name = write_label_state(win)
        #search function activated when user clicks the search button
        def search():
            #get user input from the search box
            pd_text = pd_name.get()
            try:
                #open up a connection using mysql credentials
                connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name,
                cursorclass=pymysql.cursors.DictCursor)
                with connection.cursor() as cursor:
                    #create sql query: takes a state abbreviation and provides relevant information
                    sql = "select * from state where state_abbr like '%" + pd_text + "%';"
                    cursor.execute(sql)
                    #get results of query as list of dictionaries
                    state_result = cursor.fetchall()
                    connection.commit()
            finally:
                #close connection and open relevant pop up
                connection.close()
                state_result_popup(state_result)
        #create button to search using above search function
        a = Button(win, text="Search Database", command=search,highlightbackground="royalblue2")
        a.grid(row=2, column=0)

    #Create the special query buttons and associate them with the relevant pop ups
    row = 6
    insert_btn = Button(root, text="Find Where Specific Police Departments Have Killed", 
    command=pop_up_acts,highlightbackground="royalblue2")
    insert_btn.grid(row=row,column=2,columnspan=2, pady=20,padx=10,ipadx=50)
    row+=1
    
    search_btn = Button(root, text="Find Where Members of Police Departments Have Died", 
    command=pop_up_deaths,highlightbackground="royalblue2")
    search_btn.grid(row=row,column=2,columnspan=2, pady=20,padx=10,ipadx=50)
    
    row+=1
        
    delete_btn = Button(root, text="Find Information on States", 
    command=pop_up_states,highlightbackground="royalblue2")
    delete_btn.grid(row=row,column=2,columnspan=2, pady=20,padx=10,ipadx=50)
    
    row+=1