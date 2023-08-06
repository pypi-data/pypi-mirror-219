def delete_string(finances_list):
    def print_data():
        if len(finances_list) == 0:
            print('List is empty!')
        else:
            print('---------Displaying all strings:----------\n')
            for i, item in enumerate(finances_list, start=1):
                print(f"{i}. {item}")
            print()

    print_data()
    choice = input('Delete string? (y/n): ')
    while choice.lower() in ['yes', 'y']:
        index = int(input('Choose index: '))
        if 1 <= index <= len(finances_list):
            finances_list.pop(index - 1)
            print('String deleted successfully!\n')
            print_data()
            choice = input('Delete another one? (y/n): ')
        else:
            print('Invalid index!')
    print('\nReturning...')
