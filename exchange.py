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
import datetime

api_key_file = "/home/corian/utils/exchange/api.key"
json_key_file = "/home/corian/utils/exchange/exchange.json"

def get_rates():
    """Get the current conversion rates from the online API    

    Returns: json object with the data
    """

    try:
        f = open(api_key_file)
        api_key = f.read()          
        f.close()
    except FileNotFoundError:
        print("Could not open API key file. Exiting")    
        exit()

    api = "https://api.currencyapi.com/v3/latest?apikey=" + api_key + "&currencies=EUR&base_currency=GBP"
    
    # Connect to the API
    print("Connecting to the api...")
    resp = requests.get(api)
    if(resp.status_code != 200):            
        print("Error connecting to the API!")
        exit()
    return json.loads(resp.text)


def convert(cur, val):    
    """Currency conversion

    This function gets the current rate conversion from GBP to EUR from an API and calculates the converted value
       
    Parameters:
    cur : str
        Currency for the supplied value. 'e' for EUR and 'p' for GBP
    val : float
        The value to convert

    Returns: the converted value
    """

    # Check if we have a local json file with up-to-date conversion values.

    try:
        f = open(json_key_file)
        file_contents = f.read()
        f.close()
        if(file_contents == ""): # File was empty
            print("File contained no data!")
            raise FileNotFoundError
        
        file_data = json.loads(file_contents)
        
        # Check if the last update was yesterday
        # Get today's date, subtract one day from it, format to Y-m-d
        yesterday = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y-%m-%d")        
        last_update = file_data["meta"]["last_updated_at"]

        if(yesterday in last_update):
            rates = file_data                    
        else:
            print("Conversion value is out of date. Updating...")
            raise FileNotFoundError
        
    except FileNotFoundError: # File was empty or not found, or data was not current, create a new file       
        rates = get_rates()
        try:
            f = open(json_key_file, "w")
            f.write(str(rates).replace("\'","\""))
            f.close()
        except:
            print("Could not write data to file")
            exit()
    

    # Get the current rate and use it to calculate and return the requested value
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
    

