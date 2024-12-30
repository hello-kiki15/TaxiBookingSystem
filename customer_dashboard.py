from tkinter import*
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

import sqlite3

class Booking:
    def __init__(self,root):
        self.root=root
        self.root.title('Customer Dashboard')
        height=550
        width=1020
        x=(root.winfo_screenwidth()//2)-(width//2)
        y=(root.winfo_screenheight()//2)-(height//2)
        self.root.geometry("{}x{}+{}+{}".format(width, height, x, y))

        #Database
        self.conn=sqlite3.connect("TaxiBooking.db")
        self.cursor=self.conn.cursor()

        #create table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS booking
                            (bookingid INTEGER PRIMARY KEY AUTOINCREMENT, 
                            pickup TEXT, 
                            dropoff TEXT, 
                            date TEXT, 
                            time TEXT,
                            status TEXT,
                            driverid INTEGER,
                            FOREIGN KEY (driverid) REFERENCES driver(driverid))''')
        self.conn.commit()

        #GUI
        #Title label
        titlelbl=Label(self.root, text="                       BOOK A RIDE!                       ",font=('Lucida Sans',35,'bold'),fg='#111112',bg='#6cba96')
        titlelbl.place(x=0,y=0)

        self.pickuplbl = Label(self.root, text='Pickup Address:', font=('Lucida Sans',14,'bold'))
        self.pickuplbl.place(x=120,y=80)
        self.pickup_entry=Entry(self.root, font=('Lucida Sans',14,'bold'))
        self.pickup_entry.place(x=300,y=80)

        self.dropofflbl=Label(self.root, text='Dropoff Address:', font=('Lucida Sans',14,'bold'))
        self.dropofflbl.place(x=120,y=130)
        self.dropoff_entry=Entry(self.root, font=('Lucida Sans',14,'bold'))
        self.dropoff_entry.place(x=300,y=130)

        self.datelbl=Label(self.root, text='Date:', font=('Lucida Sans',14,'bold'))
        self.datelbl.place(x=200,y=180)
        self.date_entry=DateEntry(self.root, font=('Lucida Sans',14,'bold'))
        self.date_entry.place(x=300,y=180)

        self.timelbl=Label(self.root, text='Time:', font=('Lucida Sans',14,'bold'))
        self.timelbl.place(x=200,y=230)
        self.time_entry=Entry(self.root, font=('Lucida Sans',14,'bold'))
        self.time_entry.place(x=300,y=230)

        #Treeview
        columns = ("ID", "Pickup", "Dropoff", "Date", "Time", "Status")
        self.tree=ttk.Treeview(self.root, columns=columns, show = 'headings', height=12)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Pickup", text="Pickup")
        self.tree.heading("Dropoff", text="Dropoff")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Status", text="Status")
        for column in columns:
            self.tree.heading(column, text=column, anchor="center")
            self.tree.column(column, anchor="center", width=165)
        self.tree.place(x=15,y=280)

        # Buttons
        self.bookbtn = Button(self.root, text="Request", command=self.create_record, font=('Lucida Sans',14,'bold'))
        self.bookbtn.place(x=650,y=110)

        self.updatebtn = Button(self.root, text="Update", command=self.update_record, font=('Lucida Sans',14,'bold'))
        self.updatebtn.place(x=800,y=110)

        self.deletebtn = Button(self.root, text="Delete", command=self.delete_record, font=('Lucida Sans',14,'bold'))
        self.deletebtn.place(x=650,y=180)

        self.btn_logout = Button(root, text="Logout", command=self.logout, font=('Lucida Sans',10,'bold'), fg='#c42323')
        self.btn_logout.place(x=800,y=190)

        self.read_records()

    def create_record(self):
        pickup = self.pickup_entry.get()
        dropoff = self.dropoff_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        status='Pending'

        if pickup and dropoff and date and time:
            self.cursor.execute('''INSERT INTO booking (pickup, dropoff, date, time, status) VALUES (?, ?, ?, ?, ?)''' , (pickup, dropoff, date, time,status))
            self.conn.commit()
            self.read_records()
            messagebox.showinfo('Success','Requested booking!')
            self.clear_entries()
            
        else:
            messagebox.showerror('Error', 'Please fill in all the fields')
    
    def read_records(self):
        self.tree.delete(*self.tree.get_children())

        self.cursor.execute('''SELECT * FROM booking''')
        booking=self.cursor.fetchall()

        if booking:
            for record in booking:
                self.tree.insert("","end",values=record)
        else:
                messagebox.showinfo("No Records", "No records found.")
    
    def update_record(self):
        selected_item=self.tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a record to update.")
            return
        
        selected_id = self.tree.item(selected_item, "values")[0]
        
        pickup=self.pickup_entry.get()
        dropoff = self.dropoff_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        status='Pending'

        self.cursor.execute('''UPDATE booking SET pickup=?, dropoff=?, date=?, time=?, status=? WHERE bookingid=?''', ( pickup, dropoff, date, time,status, selected_id))
        self.conn.commit()
        self.read_records()
        messagebox.showinfo("Success", "Record updated successfully!")
        self.clear_entries()
        

    def delete_record(self):
        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete.")
            return

        selected_id = self.tree.item(selected_item, "values")[0]

        self.cursor.execute('''DELETE FROM booking WHERE bookingid=?''', (selected_id,))
        self.conn.commit()
        self.read_records()
        messagebox.showinfo("Success", "Record deleted successfully!")
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
        self.pickup_entry.delete(0, END)
        self.dropoff_entry.delete(0, END)
        self.date_entry.delete(0, END)
        self.time_entry.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    app = Booking(root)
    root.mainloop()