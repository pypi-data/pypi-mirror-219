mainMessage = """
------------Expense tracker---------------
0. Help
1. Add string
2. Find month
3. Display all
4. Display grouped data
5. Currencies
6. Local convertor
7. Clear data
8. Quit
------------------------------------------
"""
helpMessage = """
----Description for all commands here:----
0. Help
1. Add a new value for finance array
2. Find all items based on month in array
3. Display all items in array
4. Display grouped data by months
5. List of all available currencies \n  at Forex exchange at current moment
6. Local currency convertor
7. Clear all data from array
8. Quit app
9. Credits
------------------------------------------
"""
creditsMessage = """
------------------------------------------
  Expense tracker python CLI app made by
            Vladimir Kobranov
            
    https://github.com/VladimirKobranov
------------------------------------------
        Release Date: 2023-07-10
          Version Number: 1.4.0
             Release Notes:
--added conversion at Forex Exchange Market
--added local currency convertor
--added input checks
--added program name title
--added delete string functionality 
--overhaul, fixes
--packed to pip
------------------------------------------
"""
availableCurrencies = """
---------------------------------------------------------
             Available currencies:
EUR - Euro Member Countries    CHF - Switzerland Franc
IDR - Indonesia Rupiah         KRW - Korea (South) Won
BGN - Bulgaria Lev             CNY - China Yuan Renminbi
ILS - Israel Shekel            TRY - Turkey Lira
GBP - United Kingdom Pound     HRK - Croatia Kuna
DKK - Denmark Krone            NZD - New Zealand Dollar
CAD - Canada Dollar            THB - Thailand Baht
JPY - Japan Yen                USD - United States Dollar
HUF - Hungary Forint           NOK - Norway Krone
RON - Romania New Leu          RUB - Russia Ruble --not available
MYR - Malaysia Ringgit         INR - India Rupee
SEK - Sweden Krona             MXN - Mexico Peso
SGD - Singapore Dollar         CZK - Czech Republic Koruna
HKD - Hong Kong Dollar         BRL - Brazil Real
AUD - Australia Dollar         PLN - Poland Zloty
PHP - Philippines Peso         ZAR - South Africa Rand
---------------------------------------------------------
"""
currency_list = ['EUR', 'IDR', 'BGN', 'ILS', 'GBP', 'DKK', 'CAD', 'JPY', 'HUF', 'RON',
                 'MYR', 'SEK', 'SGD', 'HKD', 'AUD', 'CHF', 'KRW', 'CNY', 'TRY', 'HRK',
                 'NZD', 'THB', 'USD', 'NOK', 'RUB', 'INR', 'MXN', 'CZK', 'BRL', 'PLN', 'PHP', 'ZAR']
