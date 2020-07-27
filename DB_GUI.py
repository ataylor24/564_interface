from tkinter import *
import pymysql
import civ_v_buttons
import police_v_buttons
import spec_query_btns
import credentials #credentials for accessing the database, separate for each member

def main():
    #sets up the root frame on which the other GUI elements are placed
    root = Tk()
    root.title('564 GUI')
    root.geometry("1200x800")
    root.configure(background="black")
    
    #sets up the image above the title
    im_frame = Frame(root, width=500, height=400)
    im_frame.grid(row=0, column=0)
    db_im= PhotoImage(file="scotch_job1.png")
    db_im_label= Label(im_frame, image=db_im,bg="black")
    db_im_label.grid(row=0,column=1)

   
    #sets up the title in the top lefthand corner of the screen
    title = Label(root, text="Deaths related to Law Enforcement",fg="royalblue2",bg="black")
    title.grid(row=0,column=1,columnspan=2,ipadx=50)
    title.config(font=("Times New Roman", 36))
     
    
    #sets up the labels for the Civilian section of the GUI
    civ_label = Label(root, text="Civilian Records",fg="darkgoldenrod3",bg="black")
    civ_label.grid(row=5,column=0,columnspan=2,ipadx=50)
    civ_label.config(font=("Times New Roman", 20))

    #sets up the labels for the Police Officer section of the GUI
    pd_label = Label(root, text="Police Department Records",fg="darkgoldenrod3",bg="black")
    pd_label.grid(row=10,column=0,columnspan=2,ipadx=50)
    pd_label.config(font=("Times New Roman", 20))

    #sets up the labels for the Special Query section of the GUI
    spec_label = Label(root, text="Special Queries",fg="darkgoldenrod3",bg="black")
    spec_label.grid(row=5,column=2,columnspan=2,ipadx=50)
    spec_label.config(font=("Times New Roman", 20))

    #establish civilian query buttons
    civ_v_buttons.create_civ_v_buttons(root) #farms button creation out to civ_v_buttons.py
    #establish police query buttons
    police_v_buttons.create_police_buttons(root) #farms button creation out to police_v_buttons.py
    #establish special query buttons
    spec_query_btns.create_special_query_btns(root) #farms button creation out to spec_query_btns.py

    #establishes the GUI
    root.mainloop()

if __name__ == "__main__":
    main()

