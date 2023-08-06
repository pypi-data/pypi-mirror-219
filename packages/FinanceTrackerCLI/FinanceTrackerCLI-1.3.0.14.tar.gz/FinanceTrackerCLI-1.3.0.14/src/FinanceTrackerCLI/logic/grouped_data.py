from datetime import datetime
from decimal import Decimal, ROUND_DOWN
from forex_python.converter import CurrencyRates

c = CurrencyRates()


def group_by_month(finances_list, currency_choice):
    if currency_choice != 'USD':
        print('Loading...\n')
    grouped_data = {}
    for item in finances_list:
        parts = item.split('---')
        date_str, expense_income, value, *rest = parts
        date_parts = date_str.split('-')
        month = datetime.strptime(date_parts[1], "%m").strftime("%B")
        year = date_parts[0]
        month_year = f"{month} {year}"
        description = ''
        value = Decimal(value)
        if expense_income == 'Expense':
            value = -value
        value = c.convert('USD', currency_choice, value)
        value = value.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        if rest:
            description = '---'.join(rest[1:])
        if month_year not in grouped_data:
            grouped_data[month_year] = []
        grouped_data[month_year].append(
            f"{date_parts[2]}---{expense_income}---{value}---{currency_choice}---{description}")
    return grouped_data


def display_grouped_data(grouped_data):
    overall_sum = Decimal('0.0')
    overall_expense = Decimal('0.0')
    overall_income = Decimal('0.0')
    sorted_months = sorted(grouped_data.keys(), key=lambda x: datetime.strptime(x, "%B %Y"), reverse=False)
    currency = ''
    for month in sorted_months:
        values = grouped_data[month]
        print(f"{month}:")

        for value in values:
            parts = value.split('---')
            date, expense_income, amount, *rest = parts
            currency = rest[0] if rest else currency
            print(f"{date}---{expense_income}---{amount}---{currency}---{rest[1] if len(rest) > 1 else ''}")
            amount = Decimal(amount)
            if expense_income == 'Expense':
                overall_expense += amount
            else:
                overall_income += amount
        sum_value = sum(Decimal(value.split('---')[2]) for value in values)
        print("Sum:", sum_value if sum_value >= Decimal('0') else f"-{abs(sum_value)}", currency)
        overall_sum += sum_value
        print()
    print('Expenses:', abs(overall_expense), currency)
    print("Income:", abs(overall_income), currency)
    print("Total:", overall_sum.quantize(Decimal('0.00'), rounding=ROUND_DOWN), currency)


def grouped_final(finances_list, currency_list):
    if not finances_list:
        print('List is empty!')
        return
    print('Displaying grouped data\nList of all available currencies can be found in the main menu')
    currency_choice = input('Enter currency (Or leave for USD): ').upper()
    print()
    if not currency_choice:
        currency_choice = 'USD'
    while currency_choice not in currency_list:
        print('Entered currency is not in the currency list\nYou can view all available currencies in the main menu\n')
        currency_choice = input('Enter currency again: ').upper()
        print()
    if currency_choice == 'RUB':
        print('Your currency is not available at this moment.\nWill be used USD\n')
        currency_choice = 'USD'
    grouped_data = group_by_month(finances_list, currency_choice)
    display_grouped_data(grouped_data)
