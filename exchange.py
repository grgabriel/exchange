"""Currency Converter

This script will convert EUR to GBP or vice-versa

Usage: exchange.py <e|p> <val>

Arguments:
cur : str
    The direction for conversion
    e -> convert Euro to Pound
    p -> convert Pound to Euro
val : float
    The value to be converted

Examples:

exchange.py e 50
    Converts 50€ to £

exchange.py p 50
    Converts 50£ to €   
"""

import json
import requests
import sys

def convert(cur, val):    
    """Currency conversion

    This function gets the current rate conversion from GBP to EUR from an API and calculates the converted value
       
    Parameters:
    cur : str
        Currency for the supplied value. 'e' for EUR and 'p' for GBP
    val : float
        The value to convert
    """

    api = "https://api.currencyapi.com/v3/latest?apikey=cur_live_VoiSjxU2rbs7JxXjGtzbjcfYdk4jVS1fHXPIQr03&currencies=EUR&base_currency=GBP"
    #tmp = '{  "meta": {    "last_updated_at": "2024-06-08T23:59:59Z"  },  "data": {    "EUR": {      "code": "EUR",      "value": 1.1774525048    }  }}'
    
    # Connect to the API
    resp = requests.get(api)

    if(resp.status_code != 200):            
        print("Error connecting to the API!")
        return False
    
    # Load json data
    rates = json.loads(resp.text)
    r = float(rates["data"]["EUR"]["value"])
    if(cur == "p"):    
        return format(float(val)*r, ".2f")
    elif(cur == "e"):
        return format(float(val)/r, ".2f")

if(len(sys.argv) == 3):
    val = sys.argv[2]
    
    # Test if the supplied value to convert is valid
    try:
        float(val)
    except ValueError:
        print("Invalid value for conversion")
        exit()

    if(sys.argv[1] == "p"): # Converting a £ value to €
        conv = convert("p", val)
        print(val + "£ is " + conv + "€")
    elif(sys.argv[1] == "e"): # Converting a € value to £
        conv = convert("e", val)
        print(val + "€ is " + conv + "£")
    else: # Supplied currency was invalid
        print("Invalid Currency. Use p to convert pounds to euro, and e to convert euro to pounds.")
else:
    print("Arguments: <p|e> <val>")
    

