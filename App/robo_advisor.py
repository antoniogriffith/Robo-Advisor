# this is the "app/robo_advisor.py" file

#Modules
import requests
import json


# utility function to convert float or integer to USD-formatted string (for printing)
# ... adapted from: https://github,com/s2t2/shopping-cart-screencast/blob/30c2a2873a796b8766
def to_usd(my_price):
        return "${0:,.2f}".format(my_price) #>$12,000.71


#
# INFO INPUTS
#


request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo"

response = requests.get(request_url)
# print(type(response)) #> 'requests.models.Response'>
# print(response.status_code) #> 200
# print(response.text)

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

latest_close = parsed_response['Time Series (Daily)']["2021-03-05"]["4. close"] #> $1,000.00




# breakpoint()



#
# INFO OUTPUTS
#




print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm") #> using datetime module
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")