import sqlite3

def connect_db():
    conn = sqlite3.connect("billing.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            bill_no INTEGER PRIMARY KEY,
            customer_name TEXT,
            product_name TEXT,
            quantity INTEGER,
            total_amount REAL,
            payment_mode TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_bill(bill_no, customer, product, qty, total, payment):
    conn = sqlite3.connect("billing.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO bills VALUES (?, ?, ?, ?, ?, ?)",
        (bill_no, customer, product, qty, total, payment)
    )
    conn.commit()
    conn.close()

def fetch_bills():
    conn = sqlite3.connect("billing.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM bills")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_bill(bill_no):
    conn = sqlite3.connect("billing.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM bills WHERE bill_no=?", (bill_no,))
    conn.commit()
    conn.close()

def update_bill(customer, product, qty, total, payment, bill_no):
    conn = sqlite3.connect("billing.db")
    cur = conn.cursor()
    cur.execute("""
        UPDATE bills SET
        customer_name=?,
        product_name=?,
        quantity=?,
        total_amount=?,
        payment_mode=?
        WHERE bill_no=?
    """, (customer, product, qty, total, payment, bill_no))
    conn.commit()
    conn.close()