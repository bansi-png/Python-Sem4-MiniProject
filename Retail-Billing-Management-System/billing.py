from tkinter import *
from tkinter import ttk, messagebox
import database

database.connect_db()

root = Tk()
root.title("Retail Billing Management System")
root.geometry("1100x700")
root.resizable(True, True)

# Variables
bill_no = StringVar()
customer_name = StringVar()
product_name = StringVar()
quantity = StringVar()
total_amount = StringVar()
payment_mode = StringVar()
search_text = StringVar()

# Helpers
def safe_int(value, fallback=0):
    try:
        return int(value)
    except ValueError:
        return fallback

def safe_float(value, fallback=0.0):
    try:
        return float(value)
    except ValueError:
        return fallback

# Business functions
def validate_fields(require_bill_no=False):
    if require_bill_no and not bill_no.get().strip():
        messagebox.showerror("Validation Error", "Bill Number is required for this action.")
        return False

    if not customer_name.get().strip():
        messagebox.showerror("Validation Error", "Customer Name is required.")
        return False
    if not product_name.get().strip():
        messagebox.showerror("Validation Error", "Product Name is required.")
        return False
    if safe_int(quantity.get()) <= 0:
        messagebox.showerror("Validation Error", "Quantity must be a positive integer.")
        return False
    if safe_float(total_amount.get()) <= 0:
        messagebox.showerror("Validation Error", "Total Amount must be a positive number.")
        return False
    if payment_mode.get().strip() == "":
        messagebox.showerror("Validation Error", "Payment Mode is required.")
        return False
    return True


def get_next_bill_no():
    rows = database.fetch_bills()
    if not rows:
        return 1
    return max(row[0] for row in rows) + 1


def set_next_bill_no():
    bill_no.set(str(get_next_bill_no()))


def add_bill():
    if not validate_fields():
        return
    current_bill_no = bill_no.get().strip()
    if current_bill_no == "":
        current_bill_no = str(get_next_bill_no())

    try:
        database.insert_bill(
            int(current_bill_no),
            customer_name.get().strip(),
            product_name.get().strip(),
            safe_int(quantity.get()),
            safe_float(total_amount.get()),
            payment_mode.get().strip()
        )
        status_label.config(text=f"Added bill #{current_bill_no}.", fg="green")
    except Exception as ex:
        messagebox.showerror("Database Error", f"Could not add bill: {ex}")
        status_label.config(text="Could not add bill.", fg="red")
    view_bills()
    clear_fields()


def view_bills(filtered=None):
    bill_list.delete(*bill_list.get_children())
    rows = filtered if filtered is not None else database.fetch_bills()
    total = 0
    cash_total = 0
    upi_total = 0
    card_total = 0
    for row in rows:
        bill_list.insert("", END, values=row)
        try:
            amount = float(row[4])
            total += amount
            payment = str(row[5]).lower()
            if payment == "cash":
                cash_total += amount
            elif payment == "upi":
                upi_total += amount
            elif payment == "card":
                card_total += amount
        except Exception:
            pass
    total_label.config(text=f"Total Revenue: ₹{total:,.2f}")
    cash_label.config(text=f"Cash: ₹{cash_total:,.2f}")
    upi_label.config(text=f"UPI: ₹{upi_total:,.2f}")
    card_label.config(text=f"Card: ₹{card_total:,.2f}")


def export_csv():
    try:
        import csv
        rows = database.fetch_bills()
        with open("bills_export.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Bill No", "Customer", "Product", "Quantity", "Total", "Payment Mode"])
            writer.writerows(rows)
        messagebox.showinfo("Export", "Bills exported to bills_export.csv")
        status_label.config(text="Exported bills to bills_export.csv", fg="green")
    except Exception as ex:
        messagebox.showerror("Export Error", f"Could not export CSV: {ex}")
        status_label.config(text="Export failed", fg="red")


def print_invoice():
    if not bill_no.get().strip() or not customer_name.get().strip() or not product_name.get().strip():
        messagebox.showerror("Invoice Error", "Fill bill, customer, and product to print invoice.")
        return
    invoice = (
        f"*** Retail Billing Invoice ***\n"
        f"Bill #: {bill_no.get()}\n"
        f"Customer: {customer_name.get()}\n"
        f"Product: {product_name.get()}\n"
        f"Qty: {quantity.get()}\n"
        f"Total: ₹{float(total_amount.get()):,.2f}\n"
        f"Payment: {payment_mode.get()}\n"
        f"\nThank you for your purchase!"
    )
    messagebox.showinfo("Invoice", invoice)
    status_label.config(text=f"Invoice ready for bill #{bill_no.get()}", fg="blue")


def delete_bill():
    selected = bill_list.focus()
    if not selected:
        messagebox.showerror("Error", "Please select a bill to delete.")
        return
    data = bill_list.item(selected)["values"]
    if messagebox.askyesno("Confirm", f"Delete bill #{data[0]}?"):
        database.delete_bill(data[0])
        view_bills()
        clear_fields()


def update_bill():
    if not validate_fields(require_bill_no=True):
        return
    try:
        database.update_bill(
            customer_name.get().strip(),
            product_name.get().strip(),
            safe_int(quantity.get()),
            safe_float(total_amount.get()),
            payment_mode.get().strip(),
            int(bill_no.get().strip())
        )
        messagebox.showinfo("Success", "Bill updated successfully!")
    except Exception as ex:
        messagebox.showerror("Database Error", f"Could not update bill: {ex}")
    view_bills()
    clear_fields()


def clear_fields():
    set_next_bill_no()
    customer_name.set("")
    product_name.set("")
    quantity.set("")
    total_amount.set("")
    payment_mode.set("Cash")
    status_label.config(text="Ready", fg="black")


def fill_form_from_selection(event=None):
    selected = bill_list.focus()
    if not selected:
        return
    data = bill_list.item(selected)["values"]
    bill_no.set(str(data[0]))
    customer_name.set(data[1])
    product_name.set(data[2])
    quantity.set(str(data[3]))
    total_amount.set(str(data[4]))
    payment_mode.set(data[5])
    status_label.config(text=f"Editing bill #{data[0]}", fg="blue")


def search_bills():
    q = search_text.get().strip().lower()
    if not q:
        view_bills()
        return
    filtered = [row for row in database.fetch_bills()
                if q in str(row[0]).lower()
                or q in str(row[1]).lower()
                or q in str(row[2]).lower()
                or q in str(row[5]).lower()]
    view_bills(filtered)


# UI Layout
header = Label(root, text="Retail Billing System", font=("Arial", 22, "bold"))
header.pack(pady=8)

main_frame = PanedWindow(root, orient=HORIZONTAL, sashrelief=RAISED)
main_frame.pack(fill=BOTH, expand=True)

left = Frame(main_frame, padx=10, pady=10)
right = Frame(main_frame, padx=10, pady=10)
main_frame.add(left)
main_frame.add(right)

Label(left, text="Bill No:").grid(row=0, column=0, sticky=W, pady=2)
Entry(left, textvariable=bill_no, width=25).grid(row=0, column=1, pady=2)
Label(left, text="Customer Name:").grid(row=1, column=0, sticky=W, pady=2)
Entry(left, textvariable=customer_name, width=25).grid(row=1, column=1, pady=2)
Label(left, text="Product Name:").grid(row=2, column=0, sticky=W, pady=2)
Entry(left, textvariable=product_name, width=25).grid(row=2, column=1, pady=2)
Label(left, text="Quantity:").grid(row=3, column=0, sticky=W, pady=2)
Entry(left, textvariable=quantity, width=25).grid(row=3, column=1, pady=2)
Label(left, text="Total Amount:").grid(row=4, column=0, sticky=W, pady=2)
Entry(left, textvariable=total_amount, width=25).grid(row=4, column=1, pady=2)
Label(left, text="Payment Mode:").grid(row=5, column=0, sticky=W, pady=2)
combo = ttk.Combobox(left, textvariable=payment_mode, values=["Cash", "UPI", "Card"], state="readonly", width=23)
combo.grid(row=5, column=1, pady=2)

btn_frame = Frame(left, pady=8)
btn_frame.grid(row=6, column=0, columnspan=2)
Button(btn_frame, text="Add Bill", width=10, command=add_bill).grid(row=0, column=0, padx=4)
Button(btn_frame, text="Update", width=10, command=update_bill).grid(row=0, column=1, padx=4)
Button(btn_frame, text="Delete", width=10, command=delete_bill).grid(row=0, column=2, padx=4)
Button(btn_frame, text="Clear", width=10, command=clear_fields).grid(row=0, column=3, padx=4)

status_label = Label(left, text="Ready", fg="black", font=("Arial", 9, "italic"))
status_label.grid(row=7, column=0, columnspan=2, pady=6)

# Right side with search and table
search_frame = Frame(right)
search_frame.pack(fill=X, pady=(0, 6))
Entry(search_frame, textvariable=search_text, width=30).pack(side=LEFT)
Button(search_frame, text="Search", width=10, command=search_bills).pack(side=LEFT, padx=4)
Button(search_frame, text="Show All", width=10, command=lambda: view_bills()).pack(side=LEFT)

columns = ("bill_no", "customer", "product", "qty", "total", "payment")
bill_list = ttk.Treeview(right, columns=columns, show="headings", height=14)
for col, label_text in zip(columns, ["Bill No", "Customer", "Product", "Qty", "Total", "Payment"]):
    bill_list.heading(col, text=label_text)
    bill_list.column(col, width=110, anchor=CENTER)
bill_list.pack(fill=BOTH, expand=True)
bill_list.bind("<Double-1>", fill_form_from_selection)

summary_frame = Frame(right, pady=8)
summary_frame.pack(fill=X)
total_label = Label(summary_frame, text="Total Revenue: ₹0.00", font=("Arial", 12, "bold"))
total_label.pack(side=LEFT, padx=(0, 18))
cash_label = Label(summary_frame, text="Cash: ₹0.00", font=("Arial", 11))
cash_label.pack(side=LEFT, padx=(0, 8))
upi_label = Label(summary_frame, text="UPI: ₹0.00", font=("Arial", 11))
upi_label.pack(side=LEFT, padx=(0, 8))
card_label = Label(summary_frame, text="Card: ₹0.00", font=("Arial", 11))
card_label.pack(side=LEFT)

more_frame = Frame(right, pady=6)
more_frame.pack(fill=X)
Button(more_frame, text="Export CSV", width=10, command=export_csv).pack(side=LEFT, padx=3)
Button(more_frame, text="Print Invoice", width=10, command=print_invoice).pack(side=LEFT, padx=3)

set_next_bill_no()
payment_mode.set("Cash")
view_bills()
root.mainloop()