from datetime import datetime


def search_by_month(finances_list):
    keyword = input("Enter month (leave empty for current month): ")
    print()
    if not keyword:
        keyword = datetime.now().strftime("%B")

    matched_strings = []
    for string in finances_list:
        date_str = string.split('---')[0]
        date = datetime.strptime(date_str, "%Y-%m-%d")
        month = date.strftime("%B")
        month_number = date.strftime("%m")
        if month.lower() == keyword.lower() or month.startswith(
                keyword.capitalize()) or month_number == keyword:
            matched_strings.append(string)

    if len(matched_strings) == 0:
        print('No matching strings found')
    else:
        print(f"Matched strings for month '{keyword}':\n")
        for i, string in enumerate(matched_strings, start=1):
            print(f"{i:2}. {string}")
    print()
