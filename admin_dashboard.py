from tkinter import*
from tkinter import ttk, messagebox

import sqlite3

class Administrator:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        height=580
        width=920
        x=(root.winfo_screenwidth()//2)-(width//2)
        y=(root.winfo_screenheight()//2)-(height//2)
        self.root.geometry("{}x{}+{}+{}".format(width, height, x, y))

        # Database
        self.conn = sqlite3.connect("TaxiBooking.db")
        self.cursor = self.conn.cursor()

        self.conn.commit()

        # GUI Components
        #Title label
        titlelbl=Label(self.root, text="                       Assign Driver                       ",font=('Lucida Sans',35,'bold'),fg='#111112',bg='#6cba96')
        titlelbl.place(x=0,y=0)

        self.driverlbl = Label(root, text="Driver ID:", font=('Lucida Sans',14,'bold'))
        self.driverlbl.place(x=170,y=100)

        list_of_driver=self.fetch_driver_id()

        self.driver_id_var=StringVar()
        self.driver_id_var.set("Select a driver.")

        self.drplist=OptionMenu(root, self.driver_id_var, *list_of_driver)       
        self.drplist.config(width=15)
        self.drplist.place(x=300,y=100)
        
        self.btn_view = Button(root, text=" View booking requests", command=self.view_records, font=('Lucida Sans',14,'bold'))
        self.btn_view.place(x=550,y=80)

        self.btn_assign = Button(root, text="Assign Driver", command=self.assign_driver, font=('Lucida Sans',14,'bold'))
        self.btn_assign.place(x=220,y=160)

        self.btn_cancel = Button(root, text="Decline Request", command=self.cancel_booking, font=('Lucida Sans',14,'bold'))
        self.btn_cancel.place(x=580,y=130)

        self.btn_logout = Button(root, text="Logout", command=self.logout, font=('Lucida Sans',10,'bold'), fg='#c42323')
        self.btn_logout.place(x=620,y=180)


        # Create a Treeview to display records
        columns= ("ID", "Pickup", "Dropoff", "Date", "Time","Status", "Driver ID")
        self.tree = ttk.Treeview(self.root, columns= columns, show="headings", height=15)

        # Define column headings
        self.tree.heading("ID", text="Booking ID")
        self.tree.heading("Pickup", text="Pickup")
        self.tree.heading("Dropoff", text="Dropoff")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Driver ID", text="Driver ID")
        
        for column in columns:
            self.tree.heading(column, text=column, anchor="center")
            self.tree.column(column, anchor="center", width=130)  

        self.tree.place(x=5, y=230)

    def view_records(self):
        # Fetch records from the database
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute('SELECT * FROM booking')
        booking = self.cursor.fetchall()

        # Insert records into the Treeview
        if booking:
            for record in booking:
                self.tree.insert("", "end", values=record)
        else:
                messagebox.showinfo("No Records", "No records found.")

    def assign_driver(self):
        selected_item=self.tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a record to update.")
            return
        
        selected_id = self.tree.item(selected_item, "values")[0]
        status='Assigned'
        selected_driver_id = self.driver_id_var.get()

        # Update the booking table with the selected driver ID
        self.cursor.execute('''UPDATE booking SET driverid=?, status=? WHERE bookingid=?''', (selected_driver_id, status, selected_id))
        self.conn.commit()
        self.view_records()
        messagebox.showinfo("Success", "Driver assigned successfully!")
        self.clear_entries()
              
        
    def fetch_driver_id(self):
        # Connect to SQLite database
        conn = sqlite3.connect("TaxiBooking.db")
        cursor = conn.cursor()

        # Fetch driver IDs from the database
        cursor.execute('SELECT driverid FROM driver')
        list_of_driver = [str(row[0]) for row in cursor.fetchall()]
    
        conn.commit()

        return list_of_driver
    
    def cancel_booking(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a record.")
            return

        selected_id = self.tree.item(selected_item, "values")[0]
        status = 'Declined'

        # Update the booking table with the decline status
        self.cursor.execute('''UPDATE booking SET status=? WHERE bookingid=?''', (status, selected_id))
        self.conn.commit()
        self.view_records()
        messagebox.showinfo("Success", "Request declined successfully!")
        self.clear_entries()
          
    def logout(self):
        from loginpage import Login
        result = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if result:
            print("Logging out...")

        # Destroy the current registration window
            self.root.destroy()

        # Create the main Tkinter window for login
            login_root =Tk()

        # Create an instance of the Login class
            login_app = Login(login_root)

        # Start the Tkinter event loop for the login window
            login_root.mainloop()

        else:
            print("Logout canceled.")

    def clear_entries(self):
        self.driver_id_var.get()
        
if __name__ == "__main__":
    root = Tk()
    app = Administrator(root)
    root.mainloop()