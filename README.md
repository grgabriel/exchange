Simple script that converts between GBP and EUR

Usage:

```exchange.py currency value```

currency: e or p
	e: converts Euro to Pound
	p: converts Pound to Euro

value: float value to be converted

Example: ```exchange.py p 1000```

The script will check for an existing exchange.json file with up to date information. If the file does not exist or the data is not from today, it will fetch new data. This will prevent calls to the API if the retrieved information is from today. Because the exchange value is calculated at 23:59:59 we need to subtract one day from today.
