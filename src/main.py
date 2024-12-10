
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

# Overview: 
# This program takes the base consumption by taking the current records of your electricity bill
# and subtracting it to the previous record (if you have already set the record otherwise it is set 
# to 0 by default) and then calculates the total bill to be payed by multiplying the base consumption with the predetermined rates (generation, transmission, system loss, etc.). The program stores all data inside 2 .csv files, one is for the general information of the user, and the
# other one is for their records (which will be named after their ID).

# Additional Notes:
# All the variable declaration are right below the functions.
# You can run the run.bat file to run this program, '.\run'

import csv
import os
import tkinter as tk
import uuid
import time
from datetime import datetime
from tkinter import messagebox
from PIL import Image, ImageTk
import base64

# save user info
def save_user_info(first_name, last_name, address, curr_read, prev_read = 0):
    try:
        first_name_stringed = str(first_name)
        last_name_stringed = str(last_name)
        address_stringed = str(address)
        curr_read_float = float(curr_read)

        rows = []
        user_found = False
        user_id = ""

        try:
            with open("../data/user/data.csv", mode="r", newline="") as file:
                reader = csv.reader(file)
                rows = list(reader)
        except FileNotFoundError:
            pass 

        # look for prev read
        for i, row in enumerate(rows):
            if row[1] == first_name_stringed and row[2] == last_name_stringed:
                prev_read = float(row[5])  # Correct index for the previous reading
                rows[i] = [row[0], first_name_stringed, last_name_stringed, 
                           address_stringed, prev_read, curr_read_float]
                user_found = True
                user_id = row[0]
                break

        # if not found add entry w/ prev 0
        if not user_found:
            unique_id = base64.urlsafe_b64encode((uuid.uuid4()).bytes).rstrip(b'=').decode('utf-8')
            rows.append([unique_id, first_name_stringed, last_name_stringed, 
                         address_stringed, prev_read, curr_read_float])

        with open("../data/user/data.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        print("Data saved to data.csv")

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not user_id:
            rows2 = []
            with open("../data/user/data.csv", mode="r", newline="") as file:
                reader = csv.reader(file)
                rows2 = list(reader)

            for i, row in enumerate(rows2):
                if row[1] == first_name_stringed and row[2] == last_name_stringed:
                    user_id = row[0]
                    break

        file_name = f"{user_id}.csv"
        file_path = f"../data/records/{file_name}"

        try:
            with open(file_path, mode="a", newline="") as file:
                    
                writer = csv.writer(file)
                
                if file.tell() == 0:
                    writer.writerow(['Current Reading', 'Timestamp'])
                writer.writerow([curr_read_float, current_time])

            print(f"Data saved to {file_name}")
        except Exception as e:
            messagebox.showerror("Error", f"Error while creating records")
    except Exception as e:
        messagebox.showerror("Error", f"An error occured while saving the user info: {e}")

def calculate_bill():
    try:
        # rates 
        generation_rate = 4.5474
        transmission_rate = 1.2456
        system_loss_rate = 0.8921
        distribution_rate = 1.6393
        subsidies_rate = 0.0200
        government_tax_rate = 0.1250
        universal_charges_rate = 0.0513
        fit_all_renewable_rate = 0.2226
        total = 0
        prev_record = 0
        curr_record = float(entry_usage.get())

        rate_list = [round(generation_rate, 2), round(transmission_rate, 2), round(system_loss_rate, 2), round(distribution_rate, 2), round(subsidies_rate, 2), round(government_tax_rate, 2), round(universal_charges_rate, 2), round(fit_all_renewable_rate, 2)]

        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        address = entry_address.get()

        if user_exist(first_name, last_name):    
            prev_record = float(get_last_record(first_name, last_name)['Current Reading'])
            
        if curr_record <= prev_record:
            messagebox.showerror("Error", "Current record should be higher and doesn't equal to the previous one")
            return
        
        # gets the base consumption
        base_consumption = curr_record - prev_record

        print("Prev Record: ", prev_record)
        print("Curr Record: ", curr_record)
        print("Base Consumption: ", base_consumption)

        # calculate the base consumption and add them all with the rates
        for i in range(len(rate_list)):
            total += base_consumption * rate_list[i]

        print("Sum of total rates: ", total)

        save_user_info(first_name, last_name, address, curr_record)
        print("Im executed")

        if not first_name or not last_name or not address or not base_consumption:
            messagebox.showerror("Input Error", "Please fill in all customer or usage details.")
            return

        global bill_text
        bill_text = (
            f"Electricity Bill\n\n"
            f"Customer Name: {first_name} {last_name}\n"
            f"Address: {address}\n\n"
            f"Usage Details:\n"
            f" - Current Reading (kWh): {curr_record:.2f}\n"
            f" - Previous Reading (kWh): {prev_record:.2f}\n"
            f" - Base Consumption (kWh): {base_consumption:.2f}\n"
            f" - Generation Rate (PHP/kWh): {generation_rate:.2f}\n"
            f" - Transmission Rate (PHP/kWh): {transmission_rate:.2f}\n"
            f" - System Loss Rate (PHP/kWh): {system_loss_rate:.2f}\n"
            f" - Distribution Rate (PHP/kWh): {distribution_rate:.2f}\n"
            f" - Subsidies Rate (PHP/kWh): {subsidies_rate:.2f}\n"
            f" - Government Tax Rate (PHP/kWh): {government_tax_rate:.2f}\n"
            f" - Universal Charges Rate (PHP/kWh): {universal_charges_rate:.2f}\n"
            f" - Fit All Renewable Rate (PHP/kWh): {fit_all_renewable_rate:.2f}\n"
            f"Total Bill: PHP {total:.2f}\n"
            f"-----------------------------------"
        )
        label_bill.config(text=bill_text)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for usage and rate.")

def user_exist(first_name, last_name):
    user_data_file_path = "../data/user/data.csv"
    if(first_name and last_name):
        with open(user_data_file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["First Name"] == first_name and row["Last Name"] == last_name:
                    print(f"First Name: {row['First Name']} Last Name: {row['Last Name']} ID: {row['ID']}")
                    return True    
    return False


def get_last_record(first_name, last_name):
    user_data_file_path = "../data/user/data.csv"
    user_records_file_path = "../data/records"
    target_file_name = None
    latest_row = None
    latest_timestamp = None

     # open & read data.csv
    if(first_name and last_name):
        with open(user_data_file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["First Name"] == first_name and row["Last Name"] == last_name:
                    print(f"First Name: {row['First Name']} Last Name: {row['Last Name']} ID: {row['ID']}")
                    target_file_name = row['ID']
    
        # loop through dir 
        for root, dirs, files in os.walk(user_records_file_path):
            target_file_name += ".csv"
            if target_file_name in files:
                file_path = os.path.join(root, target_file_name)
                print(f"File found: {file_path}")
                
                # read .csv find latest row
                with open(file_path, mode="r") as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # timestamp to datetime obj
                        row_timestamp = datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S")
                        if not latest_timestamp or row_timestamp > latest_timestamp:
                            latest_timestamp = row_timestamp
                            latest_row = row
                
                break  # stops when found

    return latest_row

def clear_fields():
    try:
        entry_first_name.delete(0, tk.END)
        entry_last_name.delete(0, tk.END)
        entry_address.delete(0, tk.END)
        entry_usage.delete(0, tk.END)
        label_bill.config(text="Electricity Bill\n\n[Fill out details to calculate]")
    except Exception as e:
        messagebox.showerror("Error", f"An error occured while clearing the fields: {e}")

# ui part
root = tk.Tk()
root.title("Electrical Bill Profile")

# load logo
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "../assets/logo.png")
    ico = Image.open(icon_path)
    photo = ImageTk.PhotoImage(ico)

    # set icon
    root.wm_iconphoto(False, photo)
except FileNotFoundError:
    messagebox.showerror("Error", "File not found error, make sure the icon's path is correct (tkinter section)")
except Exception as e:
    messagebox.showerror("Error", f"An error occured while loading the image: {e}")

frame_customer = tk.LabelFrame(root, text="Customer Details", padx=10, pady=10)
frame_customer.grid(row=0, column=0, padx=10, pady=5)


tk.Label(frame_customer, text="First Name:").grid(row=0, column=0, sticky="e")
entry_first_name = tk.Entry(frame_customer, width=30)  
entry_first_name.grid(row=0, column=1)

tk.Label(frame_customer, text="Last Name:").grid(row=1, column=0, sticky="e")
entry_last_name = tk.Entry(frame_customer, width=30)  
entry_last_name.grid(row=1, column=1)

tk.Label(frame_customer, text="Address:").grid(row=2, column=0, sticky="e")
entry_address = tk.Entry(frame_customer, width=30)
entry_address.grid(row=2, column=1)

frame_usage = tk.LabelFrame(root, text="Usage Details", padx=10, pady=10)
frame_usage.grid(row=0, column=2, padx=10, pady=5)

tk.Label(frame_usage, text="Current Usage (kWh):").grid(row=0, column=0, sticky="e")
entry_usage = tk.Entry(frame_usage, width=10)
entry_usage.grid(row=0, column=1)

# buttons for action
frame_buttons = tk.Frame(root, padx=10, pady=10)
frame_buttons.grid(row=1, column=2)

button_calculate = tk.Button(frame_buttons, text="Generate Bill", command=calculate_bill)
button_calculate.grid(row=0, column=0, padx=5)

button_clear = tk.Button(frame_buttons, text="Clear", command=clear_fields)
button_clear.grid(row=0, column=1, padx=5)

# display bill
frame_bill = tk.LabelFrame(root, text="Generated Bill", padx=10, pady=10)
frame_bill.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

bill_text = ""
label_bill = tk.Label(frame_bill, text="Electricity Bill\n\n[Fill out details to calculate]", justify="left", font=("Courier", 12))
label_bill.grid(row=0, column=0)


# start loop
root.mainloop()
