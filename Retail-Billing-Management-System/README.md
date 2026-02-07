# Retail Billing Management System


## Problem Statement
Develop a Retail Billing Management System using Python and Tkinter. Design a GUI to manage billing details such as Bill Number, Customer Name, Product Name, Quantity, Total Amount, and Payment Mode. Implement CRUD operations.


## Project Overview
The Retail Billing Management System is a desktop-based application developed using Python and Tkinter that helps manage retail billing records efficiently with CRUD operations.  
The system allows users to create, view, update, and delete billing records through a simple and user-friendly graphical interface. All data is stored locally using an SQLite database.


## Features
- Add new billing records
- View all existing bills
- Update billing details
- Delete billing records
- Store data persistently using SQLite
- Simple and intuitive Tkinter GUI


## Objectives
- To automate the retail billing process
- To reduce manual errors in billing records
- To provide a simple GUI-based billing management system
- To implement complete CRUD operations using a database


## Technologies Used
- **Python** – Core programming language
- **Tkinter** – GUI development
- **SQLite** – Database management


## System Modules
- **GUI Module**: Handles user interaction using Tkinter
- **Database Module**: Manages data storage and CRUD operations using SQLite


## Database Structure
Table Name: `bills`

| Field Name      | Data Type             |
|---------------- |-----------------------|
| bill_no         | INTEGER (Primary Key) |
| customer_name   | TEXT                  |
| product_name    | TEXT                  |
| quantity        | INTEGER               |
| total_amount    | REAL                  |
| payment_mode    | TEXT                  |

---


## How to Run the Project

### Prerequisites
- Python 3.x installed on your system

### Steps to Execute
1. Clone the repository:
   git clone https://github.com/your-username/Retail-Billing-Management-System.git

2. Navigate to project folder:
   cd Retail-Billing-Management-System

3. Run the application:
   python billing.py