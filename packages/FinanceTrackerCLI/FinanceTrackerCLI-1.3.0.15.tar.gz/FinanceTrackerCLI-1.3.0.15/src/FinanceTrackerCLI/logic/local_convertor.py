import math

from forex_python.converter import CurrencyRates

c = CurrencyRates()


def local_convertor(currency_list):

    first_input = input('First currency: ').upper()
    while first_input not in currency_list:
        print()
        print('Entered currency is not in currency list\nYou can watch all available currencies in main menu')
        first_input = input('Enter currency again: ').upper()
        print()
    else:
        if first_input == 'RUB':
            print()
            print('You currency is not available at this moment\nUSD will be used\n')
            first_input = 'USD'
        else:
            first_input = first_input
    second_input = input('Second currency: ').upper()
    while second_input not in currency_list:
        print()
        print('Entered currency is not in currency list\nYou can watch all available currencies in main menu')
        second_input = input('Enter currency again: ').upper()
        print()
    else:
        if second_input == 'RUB':
            print()
            print('You currency is not available at this moment\nUSD will be used\n')
            second_input = 'USD'
        else:
            second_input = second_input

    while True:
        amount = input('Amount: ')
        try:
            float(amount)
            break
        except ValueError:
            print('Enter only numbers\n')
    print()

    print('Loading...\n')
    first_currency = str(first_input).upper()
    second_currency = str(second_input).upper()
    first_amount = amount

    second_amount = c.convert(first_currency, second_currency, float(first_amount))
    second_amount = math.floor(second_amount * 100) / 100

    conversion_rate = c.get_rate(first_currency, second_currency)
    conversion_rate = math.floor(conversion_rate * 100) / 100

    print(f'{first_currency}: {first_amount}')
    print(f'{second_currency}: {second_amount}')
    print(f'Conversion rate: {conversion_rate}')
