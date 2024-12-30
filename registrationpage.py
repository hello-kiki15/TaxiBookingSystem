from tkinter import *
from tkinter import messagebox
from loginpage import Login

import sqlite3


class Registration:
    def __init__(self, root):
        self.root=root
        self.root.title("Register")
        height=500
        width=540
        x=(root.winfo_screenwidth()//2)-(width//2)
        y=(root.winfo_screenheight()//2)-(height//2)
        self.root.geometry("{}x{}+{}+{}".format(width, height, x, y))

        #Database
        self.conn=sqlite3.connect("TaxiBooking.db")
        self.cursor=self.conn.cursor()

        #create table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS records
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            firstname TEXT,
                            lastname TEXT,
                            number TEXT,
                            address TEXT,
                            email TEXT,
                            username TEXT,
                            password TEXT,
                            role TEXT)''')
        self.conn.commit()

        #variables to store user input
        self.firstname_var=StringVar()
        self.lastname_var=StringVar()
        self.number_var=StringVar()
        self.address_var=StringVar()
        self.email_var=StringVar()
        self.username_var=StringVar()
        self.password_var=StringVar()

        #Title label
        titlelbl=Label(self.root, text="     REGISTRATION       ",font=('Lucida Sans',35,'bold'),fg='#111112',bg='#6cba96')
        titlelbl.place(x=0,y=0)

        #Name label and entry
        first_namelbl=Label(self.root,text='First Name:',font=('Lucida Sans',14,'bold'))
        first_namelbl.place(x=60,y=80)

        firstname_entry=Entry(self.root,font=("Lucida Sans",14), textvariable= self.firstname_var)
        firstname_entry.place(x=235,y=80)

        last_namelbl=Label(self.root,text='Last Name:',font=('Lucida Sans',14,'bold'))
        last_namelbl.place(x=60,y=120)

        lastname_entry=Entry(self.root,font=("Lucida Sans",14), textvariable= self.lastname_var)
        lastname_entry.place(x=235,y=120)

        #phone number label and entry
        numberlbl=Label(self.root,text='Mobile Number:',font=('Lucida Sans',14,'bold'))
        numberlbl.place(x=60,y=160)

        number_entry=Entry(self.root,font=("Lucida Sans",14),fg='#111112',bg="#f7fafa",textvariable= self.number_var)
        number_entry.place(x=235,y=160)

        #address label and entry
        addresslbl=Label(self.root,text='Address:',font=('Lucida Sans',14,'bold'))
        addresslbl.place(x=60,y=200)

        address_entry=Entry(self.root,font=("Lucida Sans",14),fg='#111112',bg="#f7fafa",textvariable= self.address_var)
        address_entry.place(x=235,y=200)

        #email label and entry
        emaillbl=Label(self.root,text='Email:',font=('Lucida Sans',14,'bold'))
        emaillbl.place(x=60,y=240)

        email_entry=Entry(self.root,font=("Lucida Sans",14), textvariable= self.email_var)
        email_entry.place(x=235,y=240)

        #username entry and label
        usernamelbl=Label(self.root,text='Username:',font=('Lucida Sans',14,'bold'))
        usernamelbl.place(x=60,y=280)

        username_entry=Entry(self.root,font=("Lucida Sans",14), textvariable=self.username_var)
        username_entry.place(x=235,y=280)

        # Password label and entry
        passwordlbl=Label(self.root,text="Password: ", font=('Lucida Sans',14,'bold'))
        passwordlbl.place(x=60,y=320)

        password_entry=Entry(self.root,font=("Lucida Sans",14), textvariable=self.password_var,show='*')
        password_entry.place(x=235,y=320)

        rolelbl=Label(self.root, text="Role:", font=('Lucida Sans',14,'bold'))
        rolelbl.place(x=60,y=360)
        list_of_role = ['Customer', 'Driver','Admin'] 
        self.role_var = StringVar()
        drplist = OptionMenu(root, self.role_var, *list_of_role)
        drplist.config(width=15)
        self.role_var.set('Select your Roles')
        drplist.place(x=235, y=360)

        # Register button
        registerbtn=Button(self.root, text="Register", command=self.create_record, font=('Lucida Sans',14,'bold'),fg='#111112',bg='#f7fafa')
        registerbtn.place(x=180,y=410)

         # Login button
        loginbtn=Button(self.root, text=" Back to Login", command=self.open_login_window,font=('Lucida Sans',12,'bold'),fg='#111112',bg='#f7fafa')
        loginbtn.place(x=360,y=460)

    def create_record(self):
        firstname = self.firstname_var.get()
        lastname = self.lastname_var.get()
        number = self.number_var.get()
        address = self.address_var.get()
        email = self.email_var.get()
        username = self.username_var.get()
        password = self.password_var.get()
        role=self.role_var.get()

        if firstname and lastname and number and address and email and username and password and role:
            self.cursor.execute('''INSERT INTO records (firstname, lastname, number, address, email, username, password, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''' , (firstname, lastname, number, address,email,username, password, role))
            self.conn.commit()  
            messagebox.showinfo('Success','Registration sucessfull!')
        else:
            messagebox.showerror('Error', 'Please fill in all the fields')

    def open_login_window(self):
        # Destroy the current registration window
        self.root.destroy()

        # Create the main Tkinter window for login
        login_root =Tk()

        # Create an instance of the Login class
        login_app = Login(login_root)

        # Start the Tkinter event loop for the login window
        login_root.mainloop()

if __name__ == "__main__":
    # Create the main Tkinter window for registration
    root =Tk()

    # Create an instance of the RegisterApp class
    app = Registration(root)

    # Start the Tkinter event loop
    root.mainloop()
