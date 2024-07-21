"""
Program:    Debt Freedom Planner
Assignment: Student Choice Program
Class:      Programming with Functions (CSE 111), BYU-Idaho
Author:     Traek Malan
Updated:    2024-07-20
GitHub:     https://github.com/traek/debt-freedom-planner
"""

from datetime import datetime, timedelta as td
import csv, os, sqlite3 as sql
import amortization.period as amort

# DATABASE_FILE = "debts.db"
# DATABASE_INIT = [
#     "CREATE TABLE debt(debt, debtor, current_balance, interest_rate, minimum_payment, last_updated)",
#     "CREATE TABLE plan(name, seq_num, account)",
#     "CREATE TABLE customizations(plan,)",
#     "CREATE TABLE ",
#     "CREATE TABLE "
# ]

debts = {}
plans = {}

# Used for testing until I implement SQLite or another saving feature
debts = {
    'VentureOne VISA':  [['CapitalOne', 4000, 0.0899,  85.00, datetime.now()]],
    'Best Buy MC':      [['Citibank',   6500, 0.1599, 225.00, datetime.now()]],
    'Costco VISA':      [['Citibank',   1500, 0.1899,  70.00, datetime.now()]],
    'Timmy\'s Bill':    [['Dr. Smith',   500, 0.1,     25.00, datetime.now()]],
    'Personal Loan':    [['Mom & Dad', 25000, 0.01,    250.00, datetime.now()]],
    'Corolla Loan':     [['Chase',      8500, 0.0525, 200.00, datetime.now()]]
}

DEBTOR_INDEX = 0
BALANCE_INDEX = 1
INTEREST_INDEX = 2
PAYMENT_INDEX = 3
UPDATE_INDEX = 4
STATES = [' (OFF)',' (ON)']

# place to implement translation(s)
MENU_IMPORT_DEBT = "Import debts from CSV template"
MENU_ADD_DEBT = "Add Debt"
MENU_REMOVE_DEBT = "Remove Debts"
MENU_LIST_DEBT = "List Debts"
MENU_GENERATE_PLAN = "Generate Repayment Plan"
MENU_LIST_PLANS = "View repayment plans"
MENU_EXPORT_PLANS = "Export repayment plans to CSV"
MENU_INSTRUCTIONS = "Toggle Instructions"
MENU_EXIT = "Exit"
MENU_HEADER = "Please select one of the following options"
MENU_PROMPT = "Enter selection"

DISPLAY_DEBT = "Debt Name"
DISPLAY_DEBTOR = "Debtor"
DISPLAY_BALANCE = "Current Balance"
DISPLAY_INTEREST = "Interest Rate"
DISPLAY_PAYMENT = "Minimum Payment"
DISPLAY_ACCELERATION = "Acceleration Amount"
DISPLAY_DEBT_SELECTION = "Debt Plan Type"

INSTRUCTIONS_ADD_DEBT = f"{MENU_ADD_DEBT.upper()}:\n[{DISPLAY_DEBT}] You will need a unique name for each account, which could be a nickname, an account number, or anything else that would help you easily identify the debt.\n[{DISPLAY_DEBTOR}] Name of the institution or individual to whom you owe this debt.\n[{DISPLAY_BALANCE}] Current balance as of today's date.\n[{DISPLAY_INTEREST}] Current APR (e.g. 15.99).\n[{DISPLAY_PAYMENT}] Enter the minimum payment required by the debtor."
INSTRUCTIONS_GENERATE_PLAN = f"{MENU_GENERATE_PLAN.upper()}:\n[{DISPLAY_ACCELERATION}] You will need to provide the monthly amount you can add from your current budget to accelerate your debt repayment plan. This amount will be added to your total debt payments throughout the plan.\n[{DISPLAY_DEBT_SELECTION}] You can choose one or both of the following debt repayment plan options:\n1. Debt Snowball (most common):\nthis repayment plan focuses on early success by paying off your lowest balances before moving to higher balances. As you progress through your repayment plan, your paid off debt payment amounts are cumulatively added to your next debt. As you reach the larger balance debts, you will have more money to pay them off.\n2. Debt Avalanch (saves the most money):\nthis repayment plan focuses on saving as much interest as possible, usually helping you pay off your debts faster.\n3. Why not generate both and see which you prefer?\nNOTE: it is critical you continue to make all of you minimum payments until the plan shows you to increase your payment amount. Once completed, you will add that payment to the next debt."
INSTRUCTIONS_REMOVE_DEBT = f"{MENU_REMOVE_DEBT.upper()}:\nA summarized list of debts will show with a corresponding number for each. Please select which record you would like to remove by entering the corresponding number."

ERROR_INVALID_CHOICE = "Invalid choice"
ERROR_FEATURE_INCOMPLETE = "Feature not yet implemented"

EXIT_MESSAGE = "Good bye"

def main():
    running = True
    display_instructions = True
    while running == True:
        menu = []
        toggle = STATES[display_instructions]
        if len(debts) < 1:
            menu.append(MENU_IMPORT_DEBT)
            menu.append(MENU_ADD_DEBT)
        else:
            menu.append(MENU_ADD_DEBT)
            menu.append(MENU_REMOVE_DEBT)
            menu.append(MENU_LIST_DEBT)
        if len(plans) < 1 and len(debts) > 1:
            menu.append(MENU_GENERATE_PLAN)
        elif len(plans) > 1:
            menu.append(MENU_GENERATE_PLAN)
            menu.append(MENU_LIST_PLANS)
            menu.append(MENU_EXPORT_PLANS)
        menu.append(MENU_INSTRUCTIONS+toggle)
        menu.append(MENU_EXIT)
        choices = menu_choices(menu)
        print(f"{MENU_HEADER}:\n")
        for key, value in choices.items():
            print(f"{key}. {value}")
        print()
        valid_choice = False
        while valid_choice == False:
            choice = input(f"{MENU_PROMPT}: ")
            try:
                index = int(choice)
                if choices[index]:
                    valid_choice = True
                else:
                    print(ERROR_INVALID_CHOICE)
            except:
                print(f"{ERROR_INVALID_CHOICE} '{choice}'")
        if choices[index] == MENU_IMPORT_DEBT:
            print(f"\n{ERROR_FEATURE_INCOMPLETE}\n")
        elif choices[index] == MENU_ADD_DEBT:
            if display_instructions:
                print(f"{INSTRUCTIONS_ADD_DEBT}\n")
            enter = True
            while enter == True:
                reenter = False
                duplicated = True # set for initial check of unique debt name
                while not reenter:
                    while duplicated:
                        debt = data_entry(prompt="Debt Name", data_type="str")
                        if debt in debts.keys(): # check for duplicate record
                            print(f"Existing record found for '{debt}'. Please reenter.")
                            duplicated = True
                        else:
                            duplicated = False
                    debtor = data_entry(prompt="Debtor", data_type="str")
                    balance = data_entry(prompt="Current Balance", data_type="money")
                    interest = data_entry(prompt="Interest Rate", data_type="interest")
                    payment = data_entry(prompt="Minimum Payment", data_type="money")
                    print("\nPlease review:\n")
                    print(f"DEBT NAME:          {debt}")
                    print(f"   Debtor:          {debtor}")
                    print(f"   Current Balance: {format_money(balance)}")
                    print(f"   Interest Rate:   {format_percentage(interest)}")
                    print(f"   Minimum Payment: {format_money(payment)}")
                    reenter=data_entry(prompt="Is this correct?", data_type="boolean")
                debts[debt] = [[debtor, balance, interest, payment, datetime.now()]]
                enter = data_entry(prompt="Enter another debt?", data_type="boolean")
        elif choices[index] == MENU_REMOVE_DEBT:
            if display_instructions:
                print(f"{INSTRUCTIONS_REMOVE_DEBT}\n")
            counter = 0
            records = []
            for debt, attributes in debts.items():
                for _, balance, interest, payment, _ in attributes:
                    records.append(f"{debt}, ({format_money(balance)} @ {format_percentage(interest)}) {format_money(payment)}/mo")
            records.append(f"Cancel")
            selection = menu_choices(records)
            for key, value in selection.items():
                print(f"{key}. {value}")
            print()
        elif choices[index] == MENU_LIST_DEBT:
            print(f"\nDebts found: {len(debts)}")
            for debt, attributes in debts.items():
                for debtor, balance, interest, payment, updated in attributes:
                    print(f"DEBT NAME:          {debt}")
                    print(f"   Debtor:          {debtor}")
                    print(f"   Current Balance: {format_money(balance)}")
                    print(f"   Interest Rate:   {format_percentage(interest)}")
                    print(f"   Minimum Payment: {format_money(payment)}")
                    print(f"   Last Updated on: {updated}\n")
        elif choices[index] == MENU_GENERATE_PLAN:
            if display_instructions:
                print(f"{INSTRUCTIONS_GENERATE_PLAN}\n")
            list_snowball = []
            list_avalanch = []
            plans.clear()
            plan_types = ["snowball", "avalanch"]
            for debt, attributes in debts.items():
                for _, balance, interest, _, _ in attributes:
                    list_snowball.append([balance, debt])
                    list_avalanch.append([interest, debt])
            list_snowball.sort() # sort by asc balance
            list_avalanch.sort(reverse=True) # sort by dsc interest
            accelerate_amount = data_entry(f"{DISPLAY_ACCELERATION}", "money")
            for plan_type in plan_types:
                print(f"\n{plan_type.capitalize()} Debt Plan:\n")
                if plan_type == "snowball":
                    plan_list = list_snowball
                else:
                    plan_list = list_avalanch
                plans[plan_type] = generate_plan(plan_type=plan_type, plan_list=plan_list, debts=debts, acceleration=accelerate_amount)
                for _, output in plans[plan_type].items():
                    for row in output:
                        print(row)
        elif choices[index] == MENU_LIST_PLANS:
            print(f"\n{ERROR_FEATURE_INCOMPLETE}\n")
        elif choices[index] == MENU_EXPORT_PLANS:
            print(f"\n{ERROR_FEATURE_INCOMPLETE}\n")
        elif choices[index] == MENU_INSTRUCTIONS+toggle:
            # toggle value for display instructions
            display_instructions = not display_instructions
        elif choices[index] == MENU_EXIT:
            running = False
            print(f"\n{EXIT_MESSAGE}!\n")

def data_entry(prompt, data_type):
    """Basic data entry prompt with retry until
    correct data type is entered
    Parameters:
        prompt: string to prompt user for input.
            If the prompt ends in a '?', a space
            will be placed after the prompt before
            allowing input. Otherwise, a ':' will
            be inserted before the space.
        data_type: one of the following values is
            accepted:
                "str" - string
                "money" - real, currency format
                "interest" - real, interest format
                "boolean" - boolean, y or n prompt
    Returns:
        User-entered, data-type-forced type
    """
    if prompt[len(prompt) - 1] == "?":
        end_character = ""
    else:
        end_character = ":"
    if data_type == "money":
        entry_prefix = "$"
    else:
        entry_prefix = ""
    valid = False
    while not valid:
        entry = input(f"{prompt}{end_character} {entry_prefix}")
        try:
            match data_type:
                case "str":
                    data = entry
                    valid = True
                case "money":
                    data = float(entry)
                    valid = True
                case "interest":
                    data = float(entry)/100
                    valid = True
                case "boolean" | "Y or N":
                    data_type = "Y or N"
                    if entry.lower() == "y":
                        data = True
                        valid = True
                    elif entry.lower() == "n":
                        data = False
                        valid = True
                    else:
                        valid = False
                        raise TypeError
        except:
            print(f"Invalid data. Expected '{data_type}'")
            entry = ""
            valid = False
    return data

def generate_plan(plan_type, plan_list, debts, acceleration):
    plan = {}
    rows = []
    running_date = datetime.now()
    cumulative_debt_payment = acceleration
    for _, debt in plan_list:
        for row in debts[debt]:
            debtor = row[DEBTOR_INDEX]
            balance = row[BALANCE_INDEX]
            interest = row[INTEREST_INDEX]
            payment = row[PAYMENT_INDEX]
            updated = row[UPDATE_INDEX]
            # print(f"{debtor} {balance} {interest} {payment} {updated}")
        cumulative_debt_payment += payment
        # calculate number of months at new payment
        payoff = calculate_payoff(balance, interest, cumulative_debt_payment, running_date)
        rows.append(f"{debt} {format_money(payment)} + {format_money(cumulative_debt_payment-payment)} ({format_money(cumulative_debt_payment)}) to {debtor} until {payoff}")
        running_date = payoff
    plan[plan_type] = rows
    return plan

def calculate_payoff(balance, interest, payment, start_date):
    months = amort.calculate_amortization_period(balance, interest, payment)
    payoff = add_months(start_date, months)
    return payoff

def menu_choices(options):
    dictionary = {}
    counter = 0
    for item in options:
        counter += 1
        dictionary[counter] = item
    return dictionary

# def import_debts(debts, filename):
#     with open(filename) as file:
#         data = csv.reader(file)
#         next(data)
#         for line in data:
#             key = data[0]
#             debts[key] = line

# def init_database(connector):
#     cur = connector.cursor()

# def load_debts(connector):
#     cur = connector.cursor()

# def load_plan(connector):
#     cur = connector.cursor()

def add_months(current_date, months_to_add):
    new_date = datetime(current_date.year + (current_date.month + months_to_add - 1) // 12,
                        (current_date.month + months_to_add - 1) % 12 + 1,
                        current_date.day, current_date.hour, current_date.minute, current_date.second)
    return new_date

def format_money(money):
    """Display float as money, with negative before
    the dollar sign.
    Parameter:
        money: float to be converted to money format
    Return:
        string formatted with $ddd.cc, negative values
        precede the $ sign
    """
    if money >= 0:
        return f"${money:.2f}"
    else:
        return f"-${abs(money):.2f}"

def format_percentage(rate, decimals=2):
    """Display float as percentage
    Parameter:
        rate: float to be converted to percentage
        decimals: number of decimals to return,
            defaults to 2. Pass -1 to switch to general
            number format (% is still appended).
    Return:
        string formatted with rate * 100 with % appended
    """
    if decimals == -1:
        return f"{rate * 100:g}%"
    else:
        return f"{rate:.{decimals}%}"

if __name__ == "__main__":
    main()