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


# breakpoint()

tsd = parsed_response['Time Series (Daily)']

dates = list(tsd.keys()) # TODO: assumes first day is on top, but consider sorting to ensure

latest_day = dates[0] #> "2021-03-05"

latest_close = tsd[latest_day]["4. close"] #> $1,000.00


high_prices = []
low_prices = []

for item in dates:
    high_price = tsd[item]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[item]["3. low"]
    low_prices.append(float(low_price))

# maximum of all high prices
recent_high = max(high_prices)

# manimum of all low prices
recent_low = min(low_prices)

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
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")