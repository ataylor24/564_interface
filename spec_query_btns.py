from tkinter import *
import pymysql
import credentials

def create_special_query_btns(root):
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
    def write_label(win):
        row = 0

        pd_name = Entry(win,width=30,bg="royalblue2")
        pd_name.grid(row=row,column=1)
        pd_name_label = Label(win, text="Name of Police Department",bg="royalblue2")
        pd_name_label.grid(row=row,column=0)
        row+=1

        return pd_name

    def pop_up_acts():
        win = Toplevel(bg="black")
        win.wm_title("Find where specific Police Departments act")
        win.geometry("600x200")

        pd_name = write_label(win)

        def search():
            #clears the text from the boxes
            pd_name.delete(0, END)
            
        a = Button(win, text="Search Database", command=search,highlightbackground="royalblue2")
        a.grid(row=2, column=0)

    def pop_up_deaths():
        win = Toplevel(bg="black")
        win.wm_title("Find where Members of Police Departments have Died")
        win.geometry("600x200")

        pd_name = write_label(win)
        def search():
            #clears the text from the boxes
            pd_name.delete(0, END)
            
        a = Button(win, text="Search Database", command=search,highlightbackground="royalblue2")
        a.grid(row=2, column=0)
            
    def pop_up_victims():
        win = Toplevel(bg="black")
        win.wm_title("Find Names of those killed by Specific Police Departments")
        win.geometry("600x200")

        pd_name = write_label(win)
        def search():
            #clears the text from the boxes
            pd_name.delete(0, END)
        
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
        
    delete_btn = Button(root, text="Find Names of those killed by Specific Police Departments", 
    command=pop_up_victims,highlightbackground="royalblue2")
    delete_btn.grid(row=row,column=2,columnspan=2, pady=20,padx=10,ipadx=50)
    
    row+=1