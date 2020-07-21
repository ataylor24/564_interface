from tkinter import *

import pymysql
import civ_v_buttons
import police_v_buttons
import spec_query_btns

#Creates a connection
db = pymysql.connect("localhost","root","password","pdviolence" )

def main():
    root = Tk()
    root.title('564 GUI')
    root.geometry("1200x800")
    root.configure(background="black")

    im_frame = Frame(root, width=500, height=400)
    im_frame.grid(row=0, column=0)
    db_im= PhotoImage(file="image0.png")
    db_im_label= Label(im_frame, image=db_im,bg="black")
    db_im_label.grid(row=0,column=2)

    title = Label(root, text="Deaths related to Law Enforcement",fg="royalblue2",bg="black")
    title.grid(row=1,column=0,columnspan=2,ipadx=50)
    title.config(font=("Times New Roman", 36))
    interact_nudge = Label(root, text="Click one of the following options to interact with the database...",fg="royalblue2",bg="black")
    interact_nudge.grid(row=2,column=0,columnspan=2,ipadx=50)
    interact_nudge.config(font=("Times New Roman italic", 20))
    
    civ_label = Label(root, text="Civilian Records",fg="darkgoldenrod3",bg="black")
    civ_label.grid(row=5,column=0,columnspan=2,ipadx=50)
    civ_label.config(font=("Times New Roman", 20))

    pd_label = Label(root, text="Police Department Records",fg="darkgoldenrod3",bg="black")
    pd_label.grid(row=10,column=0,columnspan=2,ipadx=50)
    pd_label.config(font=("Times New Roman", 20))

    spec_label = Label(root, text="Special Queries",fg="darkgoldenrod3",bg="black")
    spec_label.grid(row=5,column=2,columnspan=2,ipadx=50)
    spec_label.config(font=("Times New Roman", 20))

    #establish civilian query buttons
    civ_v_buttons.create_civ_v_buttons(root)
    #establish police query buttons
    police_v_buttons.create_police_buttons(root)
    #establish special query buttons
    spec_query_btns.create_special_query_btns(root)

    root.mainloop()

if __name__ == "__main__":
    main()

