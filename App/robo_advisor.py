# this is the "app/robo_advisor.py" file

#Modules
import csv
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
    symbol = input("Please enter stock symbol or enter 'quit' to exit: ")
    symbol = symbol.upper()

    if(symbol == 'QUIT'):
        print("Exiting program now. Please come back soon! Goodbye...\n")
        quit()

    elif (symbol in symbolList):
        print("\nYou have already entered this symbol!")
        
        multipleEntries = input("\nWould you like to enter another stock? Enter 'yes' or 'no': ")
        multipleEntries = multipleEntries.upper()

        while (multipleEntries != "YES" and multipleEntries != "NO"):
            print("\nINVALID  ENTRY! Please try again!")
            multipleEntries = input("Would you like to enter another stock? Enter 'yes' or 'no': ")
            multipleEntries = multipleEntries.upper()

        if (multipleEntries == "NO"):
            break

    else:
        if (len(symbol) > 5 or  (symbol.isalpha() == False  and "." not in symbol)): # Stock symbols can contain periods!
            print("Oh, expecting a properly-formed stock symbol like 'MSFT'.\n")
        else:
            request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=" + symbol + "&apikey=" + api_key

            response = requests.get(request_url)

            parsed_response = json.loads(response.text)

            errorCheck = list(parsed_response.keys())

            if ("Error Message" in errorCheck):
                print("Sorry, couldn't find any trading data for that stock symbol.\n")

            elif ("Note" in errorCheck):
                print('''
                Alpha Vantage has a standard API call frequency of 5 calls per minute and 500 calls per day.
                Please wait 30 seconds, then begin entering the data at a rate less than 5 symbols per minute.
                ''')

            else:

                symbolList.append(symbol)

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

                # Writing Data to CSV Files

                csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"{symbol}_prices.csv")

                with open(csv_file_path, "w") as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames = ["Timestamp", "Open", "High", "Low", "Close", "Volume"])
                    writer.writeheader()

                    for date in tsd:
                        writer.writerow({"Timestamp": date, "Open": tsd[date]["1. open"] , 
                                         "High": tsd[date]["2. high"], "Low": tsd[date]["3. low"], 
                                         "Close": tsd[date]["4. close"], "Volume": tsd[date]["5. volume"]})




        multipleEntries = input("\nWould you like to enter another stock? Enter 'yes' or 'no': ")
        multipleEntries = multipleEntries.upper()

        while (multipleEntries != "YES" and multipleEntries != "NO"):
            print("\nINVALID  ENTRY! Please try again!")
            multipleEntries = input("Would you like to enter another stock? Enter 'yes' or 'no': ")
            multipleEntries = multipleEntries.upper()

        if (multipleEntries == "NO"):
            if not symbolList:
                emptyListCheck = input("No valid data has been entered. Are you sure? Please enter 'yes' or 'no': ")
                emptyListCheck = emptyListCheck.upper()

                while (emptyListCheck != "YES" and emptyListCheck != "NO"):
                    print("\nINVALID  ENTRY! Please try again!")
                    emptyListCheck = input("No valid data has been entered. Are you sure? Please enter 'yes' or 'no': ")
                    emptyListCheck = emptyListCheck.upper()

                if (emptyListCheck == 'YES'):
                    print("Exiting program now. Please come back soon! Goodbye...\n")
                    quit()

            elif (len(symbolList) > 0 ):
                break   


# Investor Risk Tolerance
print('''

                                               INVESTMENT STRATEGY


In order for us to determine an investment strategy, we must first know the investor's risk tolerance.

        Aggressive: Maximizing returns by taking a high degree of risk. This strategy will focus on capital appreciation
                    by recommending the purchase of what are commonly know as "high-growth" stocks and the liquidation of stocks
                    with low growth opportunity.


          Moderate: This strategy attempts to find a balance between aggressive and conservative strategies by suggesting
                    allocation toward so-called "value" stocks. These stocks have moderate growth potential and
                    are typically undervalued by the market. Returns on this strategy are fairly volatile in the short-term
                    but are favorable in the long-term

        
      Conservative: Maximizing the safety of the principal investment by accepting little-to-zero risk. This strategy will
                    suggest allocation to "sturdy" stocks - i.e. companies with a history of stable cash flows. Returns are
                    considerably lower under this strategy.

''')

risk_tolerance = input("Please select an investment strategy. Enter 'Aggressive', 'Moderate, or 'Conservative': ")
risk_tolerance = risk_tolerance.upper()

while (risk_tolerance != 'AGGRESSIVE' and  risk_tolerance != 'MODERATE' and risk_tolerance != 'CONSERVATIVE'):
    risk_tolerance = input("Invalid Entry! Please enter 'Aggressive', 'Moderate, or 'Conservative': ")
    risk_tolerance = risk_tolerance.upper()


#
# INFO OUTPUTS
#

print("\n-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print(f"REQUEST AT: {time_of_request}") #> using datetime module
print("PRINTING STOCK MARKET DATA...")
print(f"INVESTMENT STRATEGY: {risk_tolerance}")
print("-------------------------")

index = 0
for stock in symbolList:

    # Recommendation
    rec = ""
    reason = ""

    if (risk_tolerance == 'AGGRESSIVE'):
       
        if (float(latest_close_list[index]) >= (1.10 * float(recent_high_list[index]))):
            rec = "Buy"
            reason = "Because the Stock is Hot"
        elif (float(latest_close_list[index]) <= (0.80 * float(recent_high_list[index]))):
            rec = "Sell"
            reason = "Because the Stock is Cold"
        else:
            rec = "Hold"
            reason = "Because the stock is neither cold nor hot"

    elif (risk_tolerance == 'MODERATE'):
        
        if (float(latest_close_list[index]) >= (1.10 * float(recent_high_list[index]))):
            rec = "Buy"
            reason = "Because the Stock is Hot"
        elif (float(latest_close_list[index]) <= (0.80 * float(recent_high_list[index]))):
            rec = "Sell"
            reason = "Because the Stock is Cold"
        else:
            rec = "Hold"
            reason = "Because the stock is neither cold nor hot"
    
    else:
        
        if (float(latest_close_list[index]) >= (1.10 * float(recent_high_list[index]))):
            rec = "Buy"
            reason = "Because the Stock is Hot"
        elif (float(latest_close_list[index]) <= (0.80 * float(recent_high_list[index]))):
            rec = "Sell"
            reason = "Because the Stock is Cold"
        else:
            rec = "Hold"
            reason = "Because the stock is neither cold nor hot"



    print("\n-------------------------")
    print(f"SELECTED SYMBOL: {stock}")
    print("-------------------------")
    print(f"LATEST DAY: {last_refreshed_list[index]}")
    print(f"LATEST CLOSE: {to_usd(float(latest_close_list[index]))}")
    print(f"RECENT HIGH: {to_usd(float(recent_high_list[index]))}")
    print(f"RECENT LOW: {to_usd(float(recent_low_list[index]))}")
    print("-------------------------")
    print(f"RECOMMENDATION: {rec}")
    print(f"RECOMMENDATION REASON: {reason}")
    print("-------------------------")

    index += 1

print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("HAPPY INVESTING!")
print("-------------------------\n\n")