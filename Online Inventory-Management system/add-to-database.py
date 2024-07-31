#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import all the modules

#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python
# coding: utf-8

#!/usr/bin/env python
# coding: utf-8

from tkinter import *
from tkinter import ttk
import sqlite3
import tkinter.messagebox

conn = sqlite3.connect("storedb.db")
c = conn.cursor()
result = c.execute("SELECT Max(id) from inventory")
for r in result:
    id = r[0]

class Database:
    def __init__(self, master, *args, **kwargs):
        self.master = master
        self.master.title("Inventory Database Management")
        self.master.geometry("1366x768+0+0")
        self.master.config(bg="#f0f0f0")

        # Styling
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 16), background="#f0f0f0")
        self.style.configure("TButton", font=("Arial", 14), background="#004080", foreground="white")
        self.style.configure("TEntry", font=("Arial", 14))
        self.style.map("TButton", background=[("active", "#0059b3")])

        self.heading = Label(master, text="Add to the Inventory Database", font=('Arial 40 bold'), fg='#004080', bg='#f0f0f0')
        self.heading.pack(pady=20)

        # Frame for form
        self.form_frame = Frame(master, bg="#f0f0f0")
        self.form_frame.pack(pady=10)

        # Labels and Entries
        labels = [
            ("Enter Product Name", 0),
            ("Enter Stocks", 1),
            ("Enter Cost Price", 2),
            ("Enter Selling Price", 3),
            ("Enter Vendor Name", 4),
            ("Enter Vendor Phone Number", 5),
            ("Enter Product Id", 6)
        ]
        self.entries = {}
        for text, row in labels:
            label = ttk.Label(self.form_frame, text=text)
            label.grid(row=row, column=0, padx=10, pady=5, sticky=W)
            entry = ttk.Entry(self.form_frame, width=30)
            entry.grid(row=row, column=1, padx=10, pady=5)
            self.entries[text] = entry

        # Buttons
        self.button_frame = Frame(master, bg="#f0f0f0")
        self.button_frame.pack(pady=20)

        self.btn_add = ttk.Button(self.button_frame, text='Add to Inventory Database', command=self.get_items)
        self.btn_add.grid(row=0, column=0, padx=10, pady=10)

        self.btn_clear = ttk.Button(self.button_frame, text="Clear All Fields", command=self.clear_all)
        self.btn_clear.grid(row=0, column=1, padx=10, pady=10)

        # Text box for the log
        self.log_frame = Frame(master, bg="#f0f0f0")
        self.log_frame.pack(pady=10)

        self.log_label = ttk.Label(self.log_frame, text="Log", font=('Arial 18 bold'))
        self.log_label.pack()

        self.tbBox = Text(self.log_frame, width=80, height=15, font=("Arial", 12), bg="#ffffff", fg="#000000", borderwidth=2, relief="groove")
        self.tbBox.pack(padx=10, pady=10)
        self.tbBox.insert(END, "Product Id has reached up to: " + str(id))

        self.master.bind('<Return>', self.get_items)
        self.master.bind('<Up>', self.clear_all)

    def get_items(self, *args, **kwargs):
        # Get values from entries
        data = {key: entry.get() for key, entry in self.entries.items()}
        name, stock, cp, sp, vendor, vendor_phone, prod_id = data.values()

        # Validate entries
        if not all([name, stock, cp, sp, vendor, vendor_phone, prod_id]):
            tkinter.messagebox.showinfo("Error", "Please fill all the entries.")
            return

        # Dynamic entries
        try:
            totalcp = float(cp) * float(stock)
            totalsp = float(sp) * float(stock)
            assumed_profit = float(totalsp - totalcp)
        except ValueError:
            tkinter.messagebox.showinfo("Error", "Please enter valid numeric values for Stocks, Cost Price, and Selling Price.")
            return

        sql = "INSERT INTO inventory (name, stock, cp, sp, totalcp, totalsp, assumed_profit, vendor, vendor_phoneno) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        c.execute(sql, (name, stock, cp, sp, totalcp, totalsp, assumed_profit, vendor, vendor_phone))
        conn.commit()

        # Textbox insert
        self.tbBox.insert(END, f"\n\nInserted {name} into the database with code {prod_id}")
        tkinter.messagebox.showinfo("Success", "Successfully added to the database")

    def clear_all(self, *args, **kwargs):
        for entry in self.entries.values():
            entry.delete(0, END)

root = Tk()
b = Database(root)
root.mainloop()
