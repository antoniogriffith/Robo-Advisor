# this is the "app/robo_advisor.py" file

#Modules
import os
import requests
import json
import datetime
from dotenv import load_dotenv

# Accessing Secret API Key Value
load_dotenv()
api_key = os.getenv("ALPHAVANTAGE_API_KEY")


# utility function to convert float or integer to USD-formatted string (for printing)
# ... adapted from: https://github,com/s2t2/shopping-cart-screencast/blob/30c2a2873a796b8766
def to_usd(my_price):
        return "${0:,.2f}".format(my_price) #>$12,000.71

time_of_request = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

symbolList = []
last_refreshed_list = []
latest_close_list = []
recent_high_list = []
recent_low_list = []


#
# INFO INPUTS
#


#Welcome Message
print("\n\nWelcome to Planalytics LLC. Securities Manangement Software!")
print(
'''
The following program will recieve an entry of one or more stock tickers
(ex, IBM, AAPL, MSFT) and produce a Buy, Sell, or Hold recommendation for each.

The historical data (from the previous 100 days) will be written to a .csv file
corresponding to each stock entered.

Please be sure to enter an accurate symbol to avoid receiving an error message.

-——————————————————————————————————————————————————————————————————————————————
If at any point you wish to exit the program prematurely, please enter 'quit'.

'''
)

while True:
    symbol = input("Please enter stock symbol(s) or 'quit' to exit: ")
    symbol = symbol.upper()

    if(symbol == 'QUIT'):
        print("Exiting program now. Please come back soon! Goodbye...\n")
        quit()

    if (len(symbol) > 5 or  symbol.isalpha() == False):
        print("Oh, expecting a properly-formed stock symbol like 'MSFT'. Please try again.\n")
    else:
        request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol + "&apikey=" + api_key

        response = requests.get(request_url)
        # print(type(response)) #> 'requests.models.Response'>
        # print(response.status_code) #> 200
        # print(response.text)

        parsed_response = json.loads(response.text)

        errorCheck = list(parsed_response.keys())

        if ("Error Message" in errorCheck):
            print("Sorry, couldn't find any trading data for that stock symbol. Please try again. \n")
        else:

            last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

            last_refreshed_list.append(last_refreshed)

            tsd = parsed_response['Time Series (Daily)']

            dates = list(tsd.keys()) # TODO: assumes first day is on top, but consider sorting to ensure

            latest_day = dates[0] #> "2021-03-05"

            high_prices = []
            low_prices = []

            for item in dates:
                high_price = tsd[item]["2. high"]
                high_prices.append(float(high_price))
                low_price = tsd[item]["3. low"]
                low_prices.append(float(low_price))

            #
            # Variables to Output
            #

            latest_close = tsd[latest_day]["4. close"] #> $1,000.00

            latest_close_list.append(latest_close)

            # maximum of all high prices
            recent_high = max(high_prices)

            recent_high_list.append(recent_high)

            # manimum of all low prices
            recent_low = min(low_prices)

            recent_low_list.append(recent_low)

            multipleEntries = input("\nWould you like to enter another stock? Enter 'yes' or 'no': ")
            multipleEntries = multipleEntries.upper()

            while (multipleEntries != "YES" and multipleEntries != "NO"):
                print("\nINVALID  ENTRY! Please try again!")
                multipleEntries = input("Would you like to enter another stock? Enter 'yes' or 'no': ")
                multipleEntries = multipleEntries.upper()

            if (multipleEntries == "YES"):
                symbolList.append(symbol)

            elif (multipleEntries == "NO"):
                symbolList.append(symbol)
                break




#
# INFO OUTPUTS
#

print("\n-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {time_of_request}") #> using datetime module
print("-------------------------\n")

index = 0
for stock in symbolList:
    print("\n-------------------------")
    print(f"SELECTED SYMBOL: {stock}")
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed_list[index]}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close_list[index]))}")
    print(f"RECENT HIGH: {to_usd(float(recent_high_list[index]))}")
    print(f"RECENT LOW: {to_usd(float(recent_low_list[index]))}")
    print("-------------------------")
    print("RECOMMENDATION: BUY!")
    print("RECOMMENDATION REASON: TODO")
    print("-------------------------")

    index += 1



print("HAPPY INVESTING!")
print("-------------------------\n\n")