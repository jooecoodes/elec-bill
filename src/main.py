
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
# PIL

import csv
import os
import tkinter as tk
import uuid
import time
from datetime import datetime
from tkinter import messagebox
from fpdf import FPDF
from PIL import Image, ImageTk

# Function to read user data from the CSV file
def read_user_data():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(script_dir, "../data")
        file_path = os.path.join(folder_path, "data.csv")
        if not os.path.isfile(file_path):
            raise FileNotFoundError

        user_data = {}
        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                unique_id, first_name, last_name, address, prev_reading, current_reading = row
                user_data[unique_id] = {'firstName': str(first_name), 'lastName': last_name, 
                                        'address': address, 'previous': float(prev_reading), 
                                        'current': float(current_reading)}
        return user_data
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found at {file_path}, make sure the path of the csv is correct (read_user_data)")
    except Exception as e:
        messagebox.showerror("Error", f"An error occured while reading the data: {e}")

# Function to save user info to the CSV file
def save_user_info(first_name, last_name, address, curr_read, prev_read = 0):
    try:
        # Convert inputs to proper types
        first_name_stringed = str(first_name)
        last_name_stringed = str(last_name)
        address_stringed = str(address)
        curr_read_float = float(curr_read)


        # Read existing data from the CSV file
        rows = []
        user_found = False
        user_id = ""

        try:
            with open("data/user/data.csv", mode="r", newline="") as file:
                reader = csv.reader(file)
                rows = list(reader)
        except FileNotFoundError:
            pass  # No file, will create a new one

        # Look for the existing user to get their previous reading
        for i, row in enumerate(rows):
            if row[1] == first_name_stringed and row[2] == last_name_stringed:
                prev_read = float(row[5])  # Correct index for the previous reading
                rows[i] = [row[0], first_name_stringed, last_name_stringed, 
                           address_stringed, prev_read, curr_read_float]
                user_found = True
                user_id = row[0]
                break

        # If the user is not found, add a new entry with prev_read as 0
        if not user_found:
            unique_id = uuid.uuid4()
            rows.append([unique_id, first_name_stringed, last_name_stringed, 
                         address_stringed, prev_read, curr_read_float])

        # Write the updated data back to the CSV file
        with open("data/user/data.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        print("Data saved to data.csv")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        file_name = f"{user_id}.csv"
        file_path = f"data/records/{file_name}"

        # Check if the file already exists. If it does, append the new data. If it doesn't, create a new file.
        try:
            # Check if the file exists (to create a header for the first time)
            with open(file_path, mode="a", newline="") as file:
                writer = csv.writer(file)
                
                # If the file is empty, add the header
                if file.tell() == 0:
                    writer.writerow(['Current Reading', 'Timestamp'])
                
                # Append the new record to the file
                writer.writerow([curr_read_float, current_time])

            print(f"Data saved to {file_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Error while creating records")

    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found, make sure the csv is present inside the data folder (save_user_info)")
    except Exception as e:
        messagebox.showerror("Error", f"An error occured while saving the user info: {e}")

# Function to calculate the bill
def calculate_bill():
    try:
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        address = entry_address.get()
        usage = float(entry_usage.get())
        rate = float(entry_rate.get())
        total = usage * rate

        save_user_info(first_name, last_name, address, usage)

        if not first_name or not last_name or not address or not usage or not rate:
            messagebox.showerror("Input Error", "Please fill in all customer or usage details.")
            return

        global bill_text
        bill_text = (
            f"Electricity Bill\n\n"
            f"Customer Name: {first_name} {last_name}\n"
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

# Function to save to pdf
def save_to_pdf():
    try:
        if not bill_text:
            messagebox.showerror("Error", "No bill generated to save. Please calculate the bill first.")
            return
        
        # Gets the name of the user, and then append it to the file name.
        first_name = entry_first_name.get()
        file_name = f"{first_name.replace(' ', '_')}_electricity_bill.pdf"
        dir = os.path.join(script_dir, "../outputs")
        file_path = os.path.join(dir, file_name)

        # Create a PDF object
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)

        # Add content to the PDF
        pdf.set_font("Helvetica", style="B", size=16)
        pdf.cell(200, 10, txt="Electricity Bill", align='C')
        pdf.ln(10)

        pdf.set_font("Helvetica", size=12)
        lines = bill_text.split("\n")
        print(lines)
        for line in lines:
            pdf.cell(0, 10, txt=line,)

        # Save the PDF
        pdf.output(file_path)
        messagebox.showinfo("Success", f"Bill saved as {file_name}")
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found, make sure the paths are correct in the (save_to_pdf)")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while saving : {e}")

def clear_fields():
    try:
        entry_first_name.delete(0, tk.END)
        entry_last_name.delete(0, tk.END)
        entry_address.delete(0, tk.END)
        entry_usage.delete(0, tk.END)
        entry_rate.delete(0, tk.END)
        label_bill.config(text="Electricity Bill\n\n[Fill out details to calculate]")
    except Exception as e:
        messagebox.showerror("Error", f"An error occured while clearing the fields: {e}")

# Tkinter section
root = tk.Tk()
root.title("Electrical Bill Profile")

# Load the image
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "../assets/logo.png")
    ico = Image.open(icon_path)
    photo = ImageTk.PhotoImage(ico)

    # Set the window icon
    root.wm_iconphoto(False, photo)
except FileNotFoundError:
    messagebox.showerror("Error", "File not found error, make sure the icon's path is correct (tkinter section)")
except Exception as e:
    messagebox.showerror("Error", f"An error occured while loading the image: {e}")

# Customer details section
frame_customer = tk.LabelFrame(root, text="Customer Details", padx=10, pady=10)
frame_customer.grid(row=0, column=0, padx=10, pady=5)

# First Name
tk.Label(frame_customer, text="First Name:").grid(row=0, column=0, sticky="e")
entry_first_name = tk.Entry(frame_customer, width=30)  # Changed variable name for clarity
entry_first_name.grid(row=0, column=1)

# Last Name
tk.Label(frame_customer, text="Last Name:").grid(row=1, column=0, sticky="e")  # Adjusted row
entry_last_name = tk.Entry(frame_customer, width=30)  # Changed variable name for clarity
entry_last_name.grid(row=1, column=1)

# Address
tk.Label(frame_customer, text="Address:").grid(row=2, column=0, sticky="e")  # Adjusted row
entry_address = tk.Entry(frame_customer, width=30)
entry_address.grid(row=2, column=1)


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

bill_text = ""
label_bill = tk.Label(frame_bill, text="Electricity Bill\n\n[Fill out details to calculate]", justify="left", font=("Courier", 12))
label_bill.grid(row=0, column=0)


# Start the main loop
root.mainloop()
