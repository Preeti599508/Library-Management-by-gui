import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv
import os

# Initialize library with predefined books (name, price, amount)
library = {
    "Harry Potter": {"price": 20, "amount": 5},
    "The Great Gatsby": {"price": 15, "amount": 3},
    "Moby Dick": {"price": 10, "amount": 7},
    "Pride and Prejudice": {"price": 12, "amount": 6},
    "1984": {"price": 18, "amount": 4},
    "To Kill a Mockingbird": {"price": 22, "amount": 2},
    "The Hobbit": {"price": 25, "amount": 3},
    "War and Peace": {"price": 30, "amount": 1},
    "The Catcher in the Rye": {"price": 17, "amount": 8},
    "The Odyssey": {"price": 14, "amount": 5}
}

# Store user activities
user_data = {}

# CSV file name
csv_file_name = "library_activity.csv"

# Function to write data to CSV
def write_to_csv(user_name, issued_books, donated_books, added_books):
    file_exists = os.path.isfile(csv_file_name)
    with open(csv_file_name, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Name", "Issued Books", "Donated Books", "Added Books"])
        writer.writerow([user_name, ", ".join(issued_books), ", ".join(donated_books), ", ".join(added_books)])

# Function to donate a book
def donate_book():
    donate_window = tk.Toplevel(root)
    donate_window.title("Donate Book")
    donate_window.geometry("400x300")
    
    book_name_label = tk.Label(donate_window, text="Select Book to Donate:", font=("Arial", 12))
    book_name_label.pack(pady=5)
    
    book_names = list(library.keys())
    book_combo = ttk.Combobox(donate_window, values=book_names, width=30, font=("Arial", 12))
    book_combo.pack(pady=5)
    
    amount_label = tk.Label(donate_window, text="Enter Amount to Donate:", font=("Arial", 12))
    amount_label.pack(pady=5)
    
    amount_entry = tk.Entry(donate_window, font=("Arial", 12))
    amount_entry.pack(pady=5)
    
    user_name_label = tk.Label(donate_window, text="Enter Your Name:", font=("Arial", 12))
    user_name_label.pack(pady=5)
    
    user_name_entry = tk.Entry(donate_window, font=("Arial", 12))
    user_name_entry.pack(pady=5)
    
    def confirm_donation():
        book_name = book_combo.get()
        try:
            amount = int(amount_entry.get())
            user_name = user_name_entry.get().strip()
            
            if book_name and amount > 0 and user_name:
                if book_name in library:
                    library[book_name]["amount"] += amount
                else:
                    library[book_name] = {"price": 0, "amount": amount}
                
                # Store donation activity
                if user_name not in user_data:
                    user_data[user_name] = {"issued": [], "donated": [], "added": []}
                user_data[user_name]["donated"].append(book_name)

                # Write donation activity to CSV
                write_to_csv(user_name, [], [book_name], [])

                messagebox.showinfo("Success", f"Thank you {user_name}! The book '{book_name}' has been donated.")
                update_book_list()
                donate_window.destroy()
            else:
                messagebox.showerror("Error", "Please fill all fields correctly!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
    
    donate_button = tk.Button(donate_window, text="Donate", font=("Arial", 12), command=confirm_donation)
    donate_button.pack(pady=10)

# Function to issue a book
def issue_book():
    issue_window = tk.Toplevel(root)
    issue_window.title("Issue Book")
    issue_window.geometry("400x300")
    
    book_name_label = tk.Label(issue_window, text="Select Book:", font=("Arial", 12))
    book_name_label.pack(pady=5)
    
    book_names = list(library.keys())
    book_combo = ttk.Combobox(issue_window, values=book_names, width=30, font=("Arial", 12))
    book_combo.pack(pady=5)
    
    amount_label = tk.Label(issue_window, text="Enter Amount:", font=("Arial", 12))
    amount_label.pack(pady=5)
    
    amount_entry = tk.Entry(issue_window, font=("Arial", 12))
    amount_entry.pack(pady=5)
    
    user_name_label = tk.Label(issue_window, text="Enter Your Name:", font=("Arial", 12))
    user_name_label.pack(pady=5)
    
    user_name_entry = tk.Entry(issue_window, font=("Arial", 12))
    user_name_entry.pack(pady=5)
    
    total_price_label = tk.Label(issue_window, text="Total Price: 0", font=("Arial", 12))
    total_price_label.pack(pady=5)
    
    def calculate_total_price():
        try:
            selected_book = book_combo.get()
            amount = int(amount_entry.get())
            if selected_book in library:
                book_price = library[selected_book]["price"]
                total_price = book_price * amount
                total_price_label.config(text=f"Total Price: {total_price}")
        except ValueError:
            pass

    amount_entry.bind("<KeyRelease>", lambda event: calculate_total_price())
    
    def confirm_issue():
        selected_book = book_combo.get()
        try:
            amount = int(amount_entry.get())
            user_name = user_name_entry.get().strip()

            if selected_book and amount > 0 and user_name:
                if selected_book in library and library[selected_book]["amount"] >= amount:
                    library[selected_book]["amount"] -= amount
                    
                    # Store issue activity
                    if user_name not in user_data:
                        user_data[user_name] = {"issued": [], "donated": [], "added": []}
                    user_data[user_name]["issued"].append(selected_book)

                    # Write issue activity to CSV
                    write_to_csv(user_name, [selected_book], [], [])

                    messagebox.showinfo("Success", f"The book '{selected_book}' has been issued to {user_name}!")
                    update_book_list()
                    issue_window.destroy()
                else:
                    messagebox.showwarning("Warning", "Not enough copies available or invalid input!")
            else:
                messagebox.showerror("Error", "Please fill all fields correctly!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
    
    issue_button = tk.Button(issue_window, text="Issue Book", font=("Arial", 12), command=confirm_issue)
    issue_button.pack(pady=10)

# Function to add data (new window)
def add_data():
    add_window = tk.Toplevel(root)
    add_window.title("Add Data")
    add_window.geometry("400x200")
    
    # Buttons for adding existing or new book
    add_existing_button = tk.Button(add_window, text="Add Existing Book", font=("Arial", 12), command=add_existing_book)
    add_existing_button.pack(pady=10)

    add_new_button = tk.Button(add_window, text="Add New Book", font=("Arial", 12), command=add_new_book)
    add_new_button.pack(pady=10)

def add_existing_book():
    existing_window = tk.Toplevel(root)
    existing_window.title("Add Existing Book")
    existing_window.geometry("400x200")

    book_name_label = tk.Label(existing_window, text="Select Book:", font=("Arial", 12))
    book_name_label.pack(pady=5)

    book_names = list(library.keys())
    book_combo = ttk.Combobox(existing_window, values=book_names, width=30, font=("Arial", 12))
    book_combo.pack(pady=5)

    amount_label = tk.Label(existing_window, text="Enter Amount:", font=("Arial", 12))
    amount_label.pack(pady=5)

    amount_entry = tk.Entry(existing_window, font=("Arial", 12))
    amount_entry.pack(pady=5)

    user_name_label = tk.Label(existing_window, text="Enter Your Name:", font=("Arial", 12))
    user_name_label.pack(pady=5)

    user_name_entry = tk.Entry(existing_window, font=("Arial", 12))
    user_name_entry.pack(pady=5)

    def confirm_add_existing_book():
        book_name = book_combo.get()
        user_name = user_name_entry.get().strip()
        try:
            amount = int(amount_entry.get())
            if book_name and amount > 0:
                if book_name in library:
                    library[book_name]["amount"] += amount
                    
                    # Write addition of existing book to CSV
                    write_to_csv(user_name, [], [], [book_name])

                    messagebox.showinfo("Success", f"Added {amount} copies of '{book_name}'!")
                    update_book_list()
                    existing_window.destroy()
                else:
                    messagebox.showwarning("Warning", f"The book '{book_name}' does not exist!")
            else:
                messagebox.showerror("Error", "Please fill all fields correctly!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    add_button = tk.Button(existing_window, text="Add Book", font=("Arial", 12), command=confirm_add_existing_book)
    add_button.pack(pady=10)

def add_new_book():
    new_book_window = tk.Toplevel(root)
    new_book_window.title("Add New Book")
    new_book_window.geometry("400x300")

    book_name_label = tk.Label(new_book_window, text="Book Name:", font=("Arial", 12))
    book_name_label.pack(pady=5)

    book_name_entry = tk.Entry(new_book_window, font=("Arial", 12))
    book_name_entry.pack(pady=5)

    price_label = tk.Label(new_book_window, text="Price:", font=("Arial", 12))
    price_label.pack(pady=5)

    price_entry = tk.Entry(new_book_window, font=("Arial", 12))
    price_entry.pack(pady=5)

    amount_label = tk.Label(new_book_window, text="Amount:", font=("Arial", 12))
    amount_label.pack(pady=5)

    amount_entry = tk.Entry(new_book_window, font=("Arial", 12))
    amount_entry.pack(pady=5)

    user_name_label = tk.Label(new_book_window, text="Enter Your Name:", font=("Arial", 12))
    user_name_label.pack(pady=5)

    user_name_entry = tk.Entry(new_book_window, font=("Arial", 12))
    user_name_entry.pack(pady=5)

    def confirm_add_new_book():
        book_name = book_name_entry.get().strip()
        user_name = user_name_entry.get().strip()  # Get the user name here
        try:
            price = int(price_entry.get().strip())
            amount = int(amount_entry.get().strip())
            if book_name and price > 0 and amount > 0:
                if book_name not in library:
                    library[book_name] = {"price": price, "amount": amount}

                    # Write addition of new book to CSV
                    write_to_csv(user_name, [], [], [book_name])

                    messagebox.showinfo("Success", f"The book '{book_name}' has been added to the library!")
                    update_book_list()  # Update the book list after adding
                    new_book_window.destroy()
                else:
                    messagebox.showwarning("Warning", f"The book '{book_name}' already exists!")
            else:
                messagebox.showerror("Error", "Please fill in all fields correctly!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for price and amount.")

    add_button = tk.Button(new_book_window, text="Add Book", font=("Arial", 12), command=confirm_add_new_book)
    add_button.pack(pady=10)

# Function to update the book list display
def update_book_list():
    for row in tree.get_children():
        tree.delete(row)
    for book, details in library.items():
        tree.insert("", tk.END, values=(book, details['price'], details['amount']))

# Function to exit the application
def exit_application():
    root.destroy()

# Main application window
root = tk.Tk()
root.title("Library Management System")
root.geometry("600x500")
root.config(bg="light blue")

# Create a Treeview for the book list
tree = ttk.Treeview(root, columns=("Book", "Price", "Amount"), show='headings')
tree.heading("Book", text="Book")
tree.heading("Price", text="Price")
tree.heading("Amount", text="Amount")
tree.column("Book", width=250)
tree.column("Price", width=100)
tree.column("Amount", width=100)
tree.pack(pady=20)

# Frame for buttons
button_frame = tk.Frame(root, bg="light blue")
button_frame.pack(pady=10)

# Buttons to perform actions
donate_button = tk.Button(button_frame, text="Donate Book", font=("Arial", 15), command=donate_book)
donate_button.pack(side=tk.LEFT, padx=5)

issue_button = tk.Button(button_frame, text="Issue Book", font=("Arial", 15), command=issue_book)
issue_button.pack(side=tk.LEFT, padx=5)

add_data_button = tk.Button(button_frame, text="Add Data", font=("Arial", 15), command=add_data)
add_data_button.pack(side=tk.LEFT, padx=5)

# Exit button
exit_button = tk.Button(button_frame, text="Exit", font=("Arial", 15), command=exit_application)
exit_button.pack(side=tk.LEFT, padx=5)

# Initialize the book list
update_book_list()

# Start the GUI event loop
root.mainloop()
