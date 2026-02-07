from tkinter import *
from tkinter import ttk, messagebox
import database

database.connect_db()

root = Tk()
root.title("Retail Billing Management System")
root.geometry("800x500")

# Variables
bill_no = IntVar()
customer_name = StringVar()
product_name = StringVar()
quantity = IntVar()
total_amount = DoubleVar()
payment_mode = StringVar()

# Functions
def add_bill():
    if bill_no.get() == 0:
        messagebox.showerror("Error", "Bill Number required")
        return
    database.insert_bill(
        bill_no.get(),
        customer_name.get(),
        product_name.get(),
        quantity.get(),
        total_amount.get(),
        payment_mode.get()
    )
    view_bills()
    clear_fields()

def view_bills():
    bill_list.delete(*bill_list.get_children())
    for row in database.fetch_bills():
        bill_list.insert("", END, values=row)

def delete_bill():
    selected = bill_list.focus()
    if not selected:
        messagebox.showerror("Error", "Select a bill")
        return
    data = bill_list.item(selected)["values"]
    database.delete_bill(data[0])
    view_bills()

def update_bill():
    database.update_bill(
        customer_name.get(),
        product_name.get(),
        quantity.get(),
        total_amount.get(),
        payment_mode.get(),
        bill_no.get()
    )
    view_bills()

def clear_fields():
    bill_no.set(0)
    customer_name.set("")
    product_name.set("")
    quantity.set(0)
    total_amount.set(0)
    payment_mode.set("")

# UI Layout
Label(root, text="Retail Billing System", font=("Arial", 20)).pack(pady=10)

frame = Frame(root)
frame.pack()

Label(frame, text="Bill No").grid(row=0, column=0)
Entry(frame, textvariable=bill_no).grid(row=0, column=1)

Label(frame, text="Customer Name").grid(row=1, column=0)
Entry(frame, textvariable=customer_name).grid(row=1, column=1)

Label(frame, text="Product Name").grid(row=2, column=0)
Entry(frame, textvariable=product_name).grid(row=2, column=1)

Label(frame, text="Quantity").grid(row=3, column=0)
Entry(frame, textvariable=quantity).grid(row=3, column=1)

Label(frame, text="Total Amount").grid(row=4, column=0)
Entry(frame, textvariable=total_amount).grid(row=4, column=1)

Label(frame, text="Payment Mode").grid(row=5, column=0)
ttk.Combobox(frame, textvariable=payment_mode,
             values=["Cash", "UPI", "Card"]).grid(row=5, column=1)

# Buttons
Button(frame, text="Add", command=add_bill).grid(row=6, column=0)
Button(frame, text="Update", command=update_bill).grid(row=6, column=1)
Button(frame, text="Delete", command=delete_bill).grid(row=7, column=0)
Button(frame, text="Clear", command=clear_fields).grid(row=7, column=1)

# Table
bill_list = ttk.Treeview(root, columns=(1,2,3,4,5,6), show="headings")
for i, col in enumerate(["Bill No","Customer","Product","Qty","Total","Payment"]):
    bill_list.heading(i+1, text=col)
bill_list.pack(fill=BOTH, expand=True)

view_bills()
root.mainloop()