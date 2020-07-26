from tkinter import *
import pymysql
import credentials

def dropdown_choices(attribute):
    connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name,
    cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = "SELECT distinct %s FROM civilian" % (attribute)
        #sql = "SELECT distinct state_name FROM state ORDER BY state_name"
        cursor.execute(sql)
        choices = {dict_[attribute] for dict_ in cursor.fetchall()}
        choices = sorted(choices)
    
    return choices

def create_special_query_btns(root):
    def popup_acts_res(act_result):
        win = Toplevel(bg="black")
        win.wm_title("Search Result")
        win.geometry("1200x800")
        scrbar = Scrollbar(win)
        scrbar.pack(side=RIGHT, fill = Y)
        lsbox = Listbox(win, yscrollcommand = scrbar.set,width=150, bg="black",fg="royalblue2")
        #Label(win, text = 'Department', borderwidth = 1,bg="royalblue2").grid(row = 0, column = 0)
        #Label(win, text = 'City', borderwidth = 1,bg="royalblue2").grid(row = 0, column = 1)
        #Label(win, text = 'State', borderwidth = 1,bg="royalblue2").grid(row = 0, column = 2)
        title = "Department, City, State"
        lsbox.insert(END, title)
        for result_dict in act_result:
            row = ""+result_dict['dept']+\
            ", "+result_dict['city_name']+", "+result_dict['state_abbr']
            lsbox.insert(END, row)
        lsbox.pack(side=LEFT, fill=BOTH)
        scrbar.config(command=lsbox.yview)
    def popup_dept_death_res(pd_st_result):
        win = Toplevel(bg="black")
        win.wm_title("Search Result")
        win.geometry("1200x800")
        sbar = Scrollbar(win)
        sbar.pack(side = RIGHT, fill = Y)
        lbox = Listbox(win, yscrollcommand=sbar.set,width=150,bg="black",fg="royalblue2")
        title = "Department, State"
        #Label(win, text = 'Department', borderwidth = 1,bg="royalblue2").grid(row = 0, column = 0)
        #Label(win, text = 'State', borderwidth = 1,bg="royalblue2").grid(row = 0, column = 1)
        lbox.insert(END, title)
        for result_dict in pd_st_result:
           row = ""+result_dict['dept'] +","+result_dict['state_abbr']
           lbox.insert(END, row)
        lbox.pack(side=LEFT, fill=BOTH)
        sbar.config(command=lbox.yview)
    def popup_search_res(search_result):
        win = Toplevel(bg="black")
        win.wm_title("Search Result")
        win.geometry("1200x800")
        Label(win, text = 'Dead Officer ID', borderwidth = 1,bg="royalblue2").grid(row = 0, column = 0)
        Label(win, text = 'Officer Name', borderwidth = 1,bg="royalblue2").grid(row = 0, column = 1)
        Label(win, text = 'Department', borderwidth = 1,bg="royalblue2").grid(row = 0, column = 2)
        Label(win, text = 'Cause', borderwidth = 1,bg="royalblue2").grid(row = 0, column = 3)
        Label(win, text = 'Date of Death', borderwidth = 1,bg="royalblue2").grid(row = 0, column = 4)
        Label(win, text = 'State', borderwidth = 1,bg="royalblue2").grid(row = 0, column = 5)
        i = 0
        for result_dict in search_result:
            i += 1
            Label(win, text = result_dict['dead_officer_id'], borderwidth = 1,bg="royalblue2").grid(row = i, column = 0)
            Label(win, text = result_dict['officer_name'], borderwidth = 1,bg="royalblue2").grid(row = i, column = 1)
            Label(win, text = result_dict['dept'], borderwidth = 1,bg="royalblue2").grid(row = i, column = 3)
            Label(win, text = result_dict['cause_short'], borderwidth = 1,bg="royalblue2").grid(row = i, column = 3)
            Label(win, text = result_dict['death_date'], borderwidth = 1,bg="royalblue2").grid(row = i, column = 4)
            Label(win, text = result_dict['state_abbr'], borderwidth = 1,bg="royalblue2").grid(row = i, column = 5)
    
    def state_result_popup(search_result):
        win = Toplevel(bg="black")
        win.wm_title("Search result")
        win.geometry("1200x800")
        Label(win, text= 'State Abbreviation', borderwidth = 1, bg="royalblue2").grid(row = 0, column = 0)
        Label(win, text= 'State Name', borderwidth = 1, bg="royalblue2").grid(row = 0, column = 1)
        Label(win, text= 'Population 2010', borderwidth = 1, bg="royalblue2").grid(row = 0, column = 2)
        Label(win, text= 'Population 2019', borderwidth = 1, bg="royalblue2").grid(row = 0, column = 3)
        i = 0
        for result_dict in search_result:
            i += 1
            Label(win, text = result_dict['state_abbr'], borderwidth = 1, bg="royalblue2").grid(row = i, column = 0)
            Label(win, text = result_dict['state_name'], borderwidth = 1, bg="royalblue2").grid(row = i, column = 1)
            Label(win, text = result_dict['population_2010'], borderwidth = 1, bg="royalblue2").grid(row = i, column = 2)
            Label(win, text = result_dict['population_2019'], borderwidth = 1, bg="royalblue2").grid(row = i, column = 3)
    
    def write_label(win):
        row = 0

        pd_name = Entry(win,width=30,bg="royalblue2")
        pd_name.grid(row=row,column=1)
        pd_name_label = Label(win, text="Name of Police Department",bg="royalblue2")
        pd_name_label.grid(row=row,column=0)
        row+=1

        return pd_name
    
    def write_label_state(win):
        row = 0
        # gender.set('Unspecified') # set the default option
        # gender_dropdown = OptionMenu(win, gender, *dropdown_choices("gender"))
        # gender_dropdown.grid(row = row, column =1)
        # pd_name = Entry(win,width=30,bg="royalblue2")
        # pd_name.grid(row=row,column=1)

        states = {'Alabama'}

        pd_name = StringVar(root)
        pd_name.set('Unspecified')
        pd_name_dropdown = OptionMenu(win, pd_name, *dropdown_choices("state_abbr"))
        pd_name_dropdown.grid(row = row, column=1)
        pd_name_label = Label(win, text="Name of State",bg="royalblue2")
        pd_name_label.grid(row=row,column=0)
        row+=1

        print(pd_name)
        return pd_name

    def pop_up_acts():
        win = Toplevel(bg="black")
        win.wm_title("Find Where Specific Police Departments Act")
        win.geometry("600x200")

        pd_name = write_label(win)

        def search():
            #clears the text from the boxes
            pd_text = pd_name.get()
            try:
                connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name,
                cursorclass=pymysql.cursors.DictCursor)
                with connection.cursor() as cursor:
                    sql = "select a.city_name, a.state_abbr, d.dept from acts_in a, department d where a.dept_id = d.dept_id and d.dept like '%" + pd_text +"%';"
                    cursor.execute(sql)
                    act_result = cursor.fetchall()
                    print(act_result)
                    connection.commit()
            finally:
                connection.close()
                pd_name.delete(0,END)
                popup_acts_res(act_result)

            
        a = Button(win, text="Search Database", command=search,highlightbackground="royalblue2")
        a.grid(row=2, column=0)

    def pop_up_deaths():
        win = Toplevel(bg="black")
        win.wm_title("Find where Members of Police Departments have Died")
        win.geometry("600x200")

        pd_name = write_label(win)
        def search():
            #clears the text from the boxes
            pd_text = pd_name.get()
            try:
                connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name,
                cursorclass=pymysql.cursors.DictCursor)
                with connection.cursor() as cursor:
                    sql = "select d.dept, e.state_abbr from department d, dept_deaths_in e where e.dept_id = d.dept_id and d.dept like '%" + pd_text + "%';"
                    cursor.execute(sql)
                    pd_st_result = cursor.fetchall()
                    print(pd_st_result)
                    connection.commit()
            finally:
                connection.close()
                pd_name.delete(0,END)
                popup_dept_death_res(pd_st_result)
            
        a = Button(win, text="Search Database", command=search,highlightbackground="royalblue2")
        a.grid(row=2, column=0)
            
    def pop_up_victims():
        win = Toplevel(bg="black")
        win.wm_title("Find information on States")
        win.geometry("600x200")

        pd_name = write_label_state(win)
        def search():
            pd_text = pd_name.get()

            try:
                connection = pymysql.connect(credentials.host,credentials.username,credentials.password,credentials.db_name,
                cursorclass=pymysql.cursors.DictCursor)
                with connection.cursor() as cursor:
                    sql = "select * from state where state_abbr like '%" + pd_text + "%';"
                    cursor.execute(sql)
                    state_result = cursor.fetchall()
                    print(state_result)
                    connection.commit()
            finally:
                connection.close()
                #pd_name.delete(0,END)
                state_result_popup(state_result)

            #clears the text from the boxes
            #pd_name.delete(0, END)
        
        a = Button(win, text="Search Database", command=search,highlightbackground="royalblue2")
        a.grid(row=2, column=0)

    row = 6
    insert_btn = Button(root, text="Find where Specific Police Departments have killed", 
    command=pop_up_acts,highlightbackground="royalblue2")
    insert_btn.grid(row=row,column=2,columnspan=2, pady=20,padx=10,ipadx=50)
    row+=1
    
    search_btn = Button(root, text="Find where Members of Police Departments have Died", 
    command=pop_up_deaths,highlightbackground="royalblue2")
    search_btn.grid(row=row,column=2,columnspan=2, pady=20,padx=10,ipadx=50)
    
    row+=1
        
    delete_btn = Button(root, text="Find information on States", 
    command=pop_up_victims,highlightbackground="royalblue2")
    delete_btn.grid(row=row,column=2,columnspan=2, pady=20,padx=10,ipadx=50)
    
    row+=1