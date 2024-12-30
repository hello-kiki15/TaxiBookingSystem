from tkinter import*
from tkinter import ttk, messagebox

import sqlite3

class DriverDashboard:
    def __init__(self, root):
        self.root=root
        self.root.title("Driver Dashboard")
        height=550
        width=900
        x=(root.winfo_screenwidth()//2)-(width//2)
        y=(root.winfo_screenheight()//2)-(height//2)
        self.root.geometry("{}x{}+{}+{}".format(width, height, x, y))

        #Database
        self.conn=sqlite3.connect("TaxiBooking.db")
        self.cursor=self.conn.cursor()

        self.conn.commit()

        #GUI Components
        self.acceptbtn = Button(root, text="Accept Ride", font=('Lucida Sans',14,'bold'), command=self.accept)
        self.acceptbtn.place(x=500,y=20)

        self.btn_view = Button(root, text=" View assigned rides", command=self.view_records, font=('Lucida Sans',14,'bold'))
        self.btn_view.place(x=150,y=20)

        self.btn_logout = Button(root, text="Logout", command=self.logout, font=('Lucida Sans',10,'bold'), fg='#c42323')
        self.btn_logout.place(x=720,y=25)

        # Create a Treeview to display records
        columns= ("ID", "Pickup", "Dropoff", "Date", "Time", "Status", "Driver ID")
        self.tree = ttk.Treeview(self.root, columns= columns, show="headings", height=20)
        
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
            self.tree.column(column, anchor="center", width=125)  

        self.tree.place(x=12, y=100)

    def view_records(self):
        # Fetch records from the database
            self.cursor.execute('SELECT * FROM booking')
            records = self.cursor.fetchall()

        # Insert records into the Treeview
            for record in records:
                self.tree.insert("", "end", values=record)

    def accept(self):
        selected_item=self.tree.selection()

        if selected_item:
            messagebox.showinfo("Success", "You accepted the ride!")
        else:
            messagebox.showerror("Error", "Please select a record.")

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
            
if __name__ == "__main__":
    root = Tk()
    app = DriverDashboard(root)
    root.mainloop()