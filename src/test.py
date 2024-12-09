def generation_charge(base_kwh, rate):
    return base_kwh * rate

def transmission_charge(base_kwh, rate):
    return base_kwh * rate

def system_loss_charge(base_kwh, rate):
    return base_kwh * rate

def distribution_charge(base_kwh, rate):
    return base_kwh * rate

def subsidies(base_kwh, rate):
    return base_kwh * rate

def government_tax(base_kwh, rate):
    return base_kwh * rate

def universal_charges(base_kwh, rate):
    return base_kwh * rate

def fit_all_renewable(base_kwh, rate):
    return base_kwh * rate

def calculate_electric_bill(base_kwh, generation_rate, transmission_rate, system_loss_rate, distribution_rate,
                            subsidies_rate, government_tax_rate, universal_charges_rate, fit_all_renewable_rate):
    bill_1st = generation_charge(base_kwh, generation_rate)
    bill_2nd = transmission_charge(base_kwh, transmission_rate)
    bill_3rd = system_loss_charge(base_kwh, system_loss_rate)
    bill_4th = distribution_charge(base_kwh, distribution_rate)
    bill_5th = subsidies(base_kwh, subsidies_rate)
    bill_6th = government_tax(base_kwh, government_tax_rate)
    bill_7th = universal_charges(base_kwh, universal_charges_rate)
    bill_8th = fit_all_renewable(base_kwh, fit_all_renewable_rate)

    print(f'Generation charge: base {base_kwh} * rates {generation_rate} = {bill_1st: .2f}')
    print(f'Transmission charge: base {base_kwh} * rates {transmission_rate} = {bill_2nd: .2f}')
    print(f'System loss charge: base {base_kwh} * rates {system_loss_rate} = {bill_3rd: .2f}')
    print(f'Distribution charge: base {base_kwh} * rates {distribution_rate} = {bill_4th: .2f}')
    print(f'Subsidies charge: base {base_kwh} * rates {subsidies_rate} = {bill_5th: .2f}')
    print(f'Government tax: base {base_kwh} * rates {government_tax_rate} = {bill_6th: .2f}')
    print(f'Universal charge: base {base_kwh} * rates {universal_charges_rate} = {bill_7th: .2f}')
    print(f'FiT-All renewable: base {base_kwh} * rates {fit_all_renewable_rate} = {bill_8th: .2f}')

    total_bill = bill_1st + bill_2nd + bill_3rd + bill_4th + bill_5th + bill_6th + bill_7th + bill_8th
    print(f'Total bill: {total_bill: .2f}')

    return total_bill

def main():
    while True:
        base_kwh = float(input("Enter the base consumption in kWh: "))
        print("Note: The rates are the fixed price.")

        generation_rate = 4.5474
        transmission_rate = 1.2456
        system_loss_rate = 0.8921
        distribution_rate = 1.6393
        subsidies_rate = 0.0200
        government_tax_rate = 0.1250
        universal_charges_rate = 0.0513
        fit_all_renewable_rate = 0.2226

        total_amount = calculate_electric_bill(
            base_kwh,
            generation_rate,
            transmission_rate,
            system_loss_rate,
            distribution_rate,
            subsidies_rate,
            government_tax_rate,
            universal_charges_rate,
            fit_all_renewable_rate
        )

        while total_amount > 0:
            payment_bill = input("Enter 'Pay' to make a payment or 'Exit' to quit: ")

            if payment_bill == 'Exit':
                print("Thank you and have a nice day!.")
                return

            elif payment_bill == 'Pay':
                payment = float(input(f"\nYour total bill is ₱{total_amount:.2f}. Enter your payment amount: ₱"))

                if payment >= total_amount:
                    change = payment - total_amount
                    print(f"Payment successful! Your change is: ₱{change:.2f}")
                    total_amount = 0
                else:
                    total_amount -= payment
                    print(f"Partial payment received. Remaining balance: ₱{total_amount:.2f}")

            else:
                print("Invalid input. Please enter 'Pay' to make a payment or 'Exit' to quit.")

        print("Thank you for your payment!")

main()
