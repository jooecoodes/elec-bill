
# Group 2 
# Members-------------------------------------------------------        
# Villacorta                |  Computer Programming 1.
# Ello                      |  
# Bologa                    |  Final PIT for 1st semester.
# Recopelacion              |  Instructor: Kim Serenuela Pagal
# Gomez                     |  Section: CS1B
# Moneva                    |
# Tangarocan                |   
#----------------------------------------------------------------
#---------------------Electrical Bill----------------------------

# Additional Notes:

# When you cloned this from my repository, it is recommended to create a virtual environment
# and then install all the dependencies, look for 'guide.md' file in the root dir to know how.

# All the variable declaration are right below the functions. This is to ensure the readability
# of the program. It has been always recommended to put the functions above or use function prototypes
# to easily track the flow.

# You can run the run.bat file to run this program, '.\run'

# External dependencies used:
# Tkinter
# FPDF

import os
import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
from PIL import Image, ImageTk

def calculate_bill():
    try:
        name = entry_name.get()
        address = entry_address.get()
        usage = float(entry_usage.get())
        rate = float(entry_rate.get())
        total = usage * rate

        if not name or not address:
            messagebox.showerror("Input Error", "Please fill in all customer details.")
            return

        global bill_text
        bill_text = (
            f"Electricity Bill\n\n"
            f"Customer Name: {name}\n"
            f"Address: {address}\n\n"
            f"Usage Details:\n"
            f" - Usage (kWh): {usage:.2f}\n"
            f" - Rate (PHP/kWh): {rate:.2f}\n\n"
            f"Total Bill: PHP {total:.2f}\n"
            f"-----------------------------------"
        )
        label_bill.config(text=bill_text)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for usage and rate.")

def save_to_pdf():
    try:
        if not bill_text:
            messagebox.showerror("Error", "No bill generated to save. Please calculate the bill first.")
            return
        
        name = entry_name.get()
        file_name = f"{name.replace(' ', '_')}_electricity_bill.pdf"

        # Create a PDF object
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add content to the PDF
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, txt="Electricity Bill", ln=True, align='C')
        pdf.ln(10)

        pdf.set_font("Arial", size=12)
        lines = bill_text.split("\n")
        for line in lines:
            pdf.cell(0, 10, txt=line, ln=True)

        # Save the PDF
        pdf.output(file_name)
        messagebox.showinfo("Success", f"Bill saved as {file_name}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving: {e}")

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_usage.delete(0, tk.END)
    entry_rate.delete(0, tk.END)
    label_bill.config(text="Electricity Bill\n\n[Fill out details to calculate]")


# Create the main application window
root = tk.Tk()
root.title("Electrical Bill Profile")

# This gets the absolute path of the main.py file,
# C:\Users\<User>\OneDrive\Desktop\elec_bill\src\main.py
script_dir = os.path.dirname(os.path.abspath(__file__))

# This will be equivalent to the absolute path of the logo,
# C:\Users\<User>\OneDrive\Desktop\elec_bill\assets\logo.png
icon_path = os.path.join(script_dir, "../assets/logo.png")

# Load the image
ico = Image.open(icon_path)
photo = ImageTk.PhotoImage(ico)

# Set the window icon
root.wm_iconphoto(False, photo)


# Customer details section
frame_customer = tk.LabelFrame(root, text="Customer Details", padx=10, pady=10)
frame_customer.grid(row=0, column=0, padx=10, pady=5)

tk.Label(frame_customer, text="Name:").grid(row=0, column=0, sticky="e")
entry_name = tk.Entry(frame_customer, width=30)
entry_name.grid(row=0, column=1)

tk.Label(frame_customer, text="Address:").grid(row=1, column=0, sticky="e")
entry_address = tk.Entry(frame_customer, width=30)
entry_address.grid(row=1, column=1)


# Usage details section
frame_usage = tk.LabelFrame(root, text="Usage Details", padx=10, pady=10)
frame_usage.grid(row=1, column=0, padx=10, pady=5)

tk.Label(frame_usage, text="Electricity Usage (kWh):").grid(row=0, column=0, sticky="e")
entry_usage = tk.Entry(frame_usage, width=10)
entry_usage.grid(row=0, column=1)

tk.Label(frame_usage, text="Rate per kWh (PHP):").grid(row=1, column=0, sticky="e")
entry_rate = tk.Entry(frame_usage, width=10)
entry_rate.grid(row=1, column=1)


# Buttons for actions
frame_buttons = tk.Frame(root, padx=10, pady=10)
frame_buttons.grid(row=2, column=0)

button_calculate = tk.Button(frame_buttons, text="Generate Bill", command=calculate_bill)
button_calculate.grid(row=0, column=0, padx=5)

button_save_pdf = tk.Button(frame_buttons, text="Save to PDF", command=save_to_pdf)
button_save_pdf.grid(row=0, column=1, padx=5)

button_clear = tk.Button(frame_buttons, text="Clear", command=clear_fields)
button_clear.grid(row=0, column=2, padx=5)


# Display bill section
frame_bill = tk.LabelFrame(root, text="Generated Bill", padx=10, pady=10)
frame_bill.grid(row=3, column=0, padx=10, pady=10)

bill_text = ""  # Global variable to store bill text
label_bill = tk.Label(frame_bill, text="Electricity Bill\n\n[Fill out details to calculate]", justify="left", font=("Courier", 12))
label_bill.grid(row=0, column=0)


# Start the main loop
root.mainloop()
