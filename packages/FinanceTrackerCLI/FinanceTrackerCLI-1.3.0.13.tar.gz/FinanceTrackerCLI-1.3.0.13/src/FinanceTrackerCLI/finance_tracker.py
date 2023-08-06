import json
import os
import os.path

from logic.grouped_data import grouped_final
from logic.input_data import input_string
from logic.local_convertor import local_convertor
from logic.search_by_month_data import search_by_month
from logic.show_all_delete_string import delete_string
from logic.terminal_name import set_terminal_title, get_terminal_title
from logic.text_prompts import mainMessage, helpMessage, creditsMessage, \
    availableCurrencies, currency_list

new_title = 'Finance tracker'
original_title = get_terminal_title()
set_terminal_title(new_title)

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "FinanceList.json")


def main():
    try:
        with open(file_path, "r") as infile:
            finances_list = json.load(infile)
    except FileNotFoundError:
        print("The 'finances.json' file is not found\nStarting a new finance list!")
        finances_list = []

    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    choice = ''
    currency = 'USD'
    while choice not in ['8', 'exit', 'quit', 'q', 'e']:
        print(mainMessage)
        choice = input('Enter index: ')
        match choice:
            case '0' | 'help' | 'h':
                clear()
                print(helpMessage)
            case '1' | 'add' | 'a':
                clear()
                print('Adding new string\n')
                input_string(finances_list, currency)
            case '2' | 'find' | 'f':
                clear()
                if len(finances_list) == 0:
                    print('List is empty!')
                else:
                    print('Looking for existing strings\n')
                    search_by_month(finances_list)
            case '3' | 'all' | 'aa':
                clear()
                if len(finances_list) == 0:
                    print('List is empty!')
                else:
                    delete_string(finances_list)
            case '4' | 'grouped' | 'g':
                clear()
                grouped_final(finances_list, currency_list)
            case '5' | 'currency' | 'cur' | 'cr':
                clear()
                print(availableCurrencies)
            case '6' | 'convertor' | 'conv' | 'c':
                clear()
                print('---------Local currency convertor---------\n')
                local_convertor(currency_list)
            case '7' | 'clear' | 'cl':
                clear()
                clear_question = input('Do you want to clean all data? y/n: ')
                if clear_question == 'y':
                    finances_list.clear()
                    print('Cleared!')
            case '8' | 'exit' | 'quit' | 'q' | 'e':
                clear()
                print('Quiting\n')
            case '9' | 'info' | 'credits' | 'i':
                clear()
                print(creditsMessage)
            case _:
                print('Wrong command\n')
    with open(file_path, "w") as outfile:
        json.dump(finances_list, outfile, indent=4)
    set_terminal_title(original_title)
    print("Program Terminated!\n")


if __name__ == "__main__":
    main()
