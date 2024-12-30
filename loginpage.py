from tkinter import *
from tkinter import messagebox
from customer_dashboard import Booking
from driver_dashboard import DriverDashboard
from admin_dashboard import Administrator

import sqlite3 

class Login:
    def __init__(self, root):
        self._root = root
        self._root.title("Login")
        height=310
        width=430
        x=(root.winfo_screenwidth()//2)-(width//2)
        y=(root.winfo_screenheight()//2)-(height//2)
        self._root.geometry("{}x{}+{}+{}".format(width, height, x, y))

        # Database
        self.conn = sqlite3.connect("TaxiBooking.db")
        self.cursor = self.conn.cursor()

        self.conn.commit()

        # Variables to store user input
        self.username_var = StringVar()
        self.password_var = StringVar()

        # Create and set up the GUI
        self.create_widgets()

    def create_widgets(self):
        #Title label
        titlelbl=Label(self._root, text="         LOGIN          ",font=('Lucida Sans',35,'bold'),fg='#111112',bg='#6cba96')
        titlelbl.place(x=0,y=0)

        # Username label and entry
        usernamelbl=Label(self._root, text="Username:",font=('Lucida Sans',14,'bold'))
        usernamelbl.place(x=40,y=90)

        username_enrty=Entry(self._root, textvariable=self.username_var,font=("Lucida Sans",14))
        username_enrty.place(x=160,y=90)

        # Password label and entry
        passwordlbl=Label(self._root, text="Password:",font=('Lucida Sans',14,'bold'))
        passwordlbl.place(x=40,y=150)

        password_entry=Entry(self._root, textvariable=self.password_var, show="*",font=("Lucida Sans",14))
        password_entry.place(x=160,y=150)

        # Login button
        loginbtn=Button(self._root, text="  Login  ", command=self.login, font=('Lucida Sans',16,'bold'),fg='#111112',bg='#f7fafa')
        loginbtn.place(x=150,y=200)

        registerlbl=Label(self._root, text="Don't have an account?",font=('Lucida Sans',14,'bold'))
        registerlbl.place(x=10,y=270)

        registerbtn=Button(self._root, text="Register here!", command=self.open_registrationpage, font=('Lucida Sans',14,'bold'),fg='#254ce8',bg='#f7fafa')
        registerbtn.place(x=260,y=260)


    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        cus_role="Customer"
        driv_role="Driver"
        admin_role="Admin"
        # Validate input
        if not username or not password or not cus_role or not driv_role or not admin_role:
            messagebox.showwarning("Error", "Please enter both username and password.")
            return
        self.cursor.execute('SELECT * FROM records WHERE username=? and password=? and role=?', (username, password,cus_role))
        user=self.cursor.fetchone()
        self.cursor.execute('SELECT * FROM records WHERE username=? and password=? and role=?', (username, password,driv_role))
        driver=self.cursor.fetchone()
        self.cursor.execute('SELECT * FROM records WHERE username=? and password=? and role=?', (username, password,admin_role))
        admin=self.cursor.fetchone()

        if driver:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.open_driver_dashboard_window()
        elif admin:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.open_admin_dashboard_window()
        elif user:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.open_customer_dashboard_window()
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    def open_customer_dashboard_window(self):
        # Destroy the current login window
            self._root.destroy()

        # Create the main Tkinter window for login
            customer_root =Tk()

        # Create an instance of the Login class
            customer_app = Booking(customer_root)

        # Start the Tkinter event loop for the login window
            customer_root.mainloop()
        
    def open_driver_dashboard_window(self):
        # Destroy the current login window
            self._root.destroy()

        # Create the main Tkinter window for login
            driver_root =Tk()

        # Create an instance of the Login class
            driver_app = DriverDashboard(driver_root)

        # Start the Tkinter event loop for the login window
            driver_root.mainloop()
    
    def open_admin_dashboard_window(self):
            
        # Destroy the current login window
            self._root.destroy()

        # Create the main Tkinter window for login
            admin_root =Tk()

        # Create an instance of the Login class
            admin_app = Administrator(admin_root)

        # Start the Tkinter event loop for the login window
            admin_root.mainloop()

    def open_registrationpage(self):
            from registrationpage import Registration
        # Destroy the current login window
            self._root.destroy()

        # Create the main Tkinter window for login
            register_root =Tk()

        # Create an instance of the Login class
            register_app = Registration(register_root)

        # Start the Tkinter event loop for the login window
            register_root.mainloop()

    
if __name__ == "__main__":
    # Create the main Tkinter window for login
    root = Tk()

    # Create an instance of the LoginApp class
    app = Login(root)

    # Start the Tkinter event loop
    root.mainloop()