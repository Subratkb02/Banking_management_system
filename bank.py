import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
from datetime import date

class BankingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Banking System")
        self.master.geometry("400x300")

        # Database connection
        self.mydb = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="subrat",
            auth_plugin="mysql_native_password"
        )
        self.mycursor = self.mydb.cursor()

        # Create and use database
        self.mycursor.execute("CREATE DATABASE IF NOT EXISTS subrat_bank")
        self.mycursor.execute("USE subrat_bank")

        # Create required tables
        self.mycursor.execute("CREATE TABLE IF NOT EXISTS bank_master (acno CHAR(4) PRIMARY KEY, name VARCHAR(30), city CHAR(20), mobileno CHAR(10), balance INT(6))")
        self.mycursor.execute("CREATE TABLE IF NOT EXISTS bank_trans (acno CHAR(4), amount INT(6), dot DATE, ttype CHAR(10), FOREIGN KEY(acno) REFERENCES bank_master(acno))")
        self.mydb.commit()

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self.master, text="Create Account", command=self.create_account).pack(pady=10)
        tk.Button(self.master, text="Deposit Money", command=self.deposit_money).pack(pady=10)
        tk.Button(self.master, text="Withdraw Money", command=self.withdraw_money).pack(pady=10)
        tk.Button(self.master, text="Display Account", command=self.display_account).pack(pady=10)
        tk.Button(self.master, text="Exit", command=self.master.quit).pack(pady=10)

    def create_account(self):
        acno = simpledialog.askstring("Input", "Enter account number:")
        name = simpledialog.askstring("Input", "Enter name (limit 35 characters):")
        city = simpledialog.askstring("Input", "Enter city name:")
        mobileno = simpledialog.askstring("Input", "Enter mobile no.:")
        balance = 0

        try:
            self.mycursor.execute("INSERT INTO bank_master VALUES (%s, %s, %s, %s, %s)", 
                                  (acno, name, city, mobileno, balance))
            self.mydb.commit()
            messagebox.showinfo("Success", "Account is successfully created!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")

    def deposit_money(self):
        acno = simpledialog.askstring("Input", "Enter account number:")
        amount = simpledialog.askinteger("Input", "Enter amount to be deposited:")
        dot = date.today().isoformat()
        ttype = "deposited"

        try:
            self.mycursor.execute("INSERT INTO bank_trans VALUES (%s, %s, %s, %s)", 
                                  (acno, amount, dot, ttype))
            self.mycursor.execute("UPDATE bank_master SET balance = balance + %s WHERE acno = %s", 
                                  (amount, acno))
            self.mydb.commit()
            messagebox.showinfo("Success", "Money has been deposited successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")

    def withdraw_money(self):
        acno = simpledialog.askstring("Input", "Enter account number:")
        amount = simpledialog.askinteger("Input", "Enter amount to be withdrawn:")
        dot = date.today().isoformat()
        ttype = "withdrawn"

        try:
            self.mycursor.execute("INSERT INTO bank_trans VALUES (%s, %s, %s, %s)", 
                                  (acno, amount, dot, ttype))
            self.mycursor.execute("UPDATE bank_master SET balance = balance - %s WHERE acno = %s", 
                                  (amount, acno))
            self.mydb.commit()
            messagebox.showinfo("Success", "Money has been withdrawn successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")

    def display_account(self):
        acno = simpledialog.askstring("Input", "Enter account number:")
        try:
            self.mycursor.execute("SELECT * FROM bank_master WHERE acno = %s", (acno,))
            account_info = self.mycursor.fetchone()
            if account_info:
                info_str = f"Account Number: {account_info[0]}\nName: {account_info[1]}\nCity: {account_info[2]}\nMobile: {account_info[3]}\nBalance: {account_info[4]}"
                messagebox.showinfo("Account Information", info_str)
            else:
                messagebox.showinfo("Info", "Account not found")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"An error occurred: {err}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()
