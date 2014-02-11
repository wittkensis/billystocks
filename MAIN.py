'''#!/usr/bin/python'''

import cgi, cgitb, sys, re, os, inspect
import LoadData
import PatProcess

cgitb.enable()

SYMBOLS = []

def testPatterns(data):
        print(data)

def UpdateStocks(getSyms=False, getQuotes=False):
        global SYMBOLS
        
        if getSyms is True:
                LoadData.downloadSymbols()        
        if getQuotes is True:
                LoadData._downloadStocks('nasdaq')
                LoadData._downloadStocks('nyse')

        SYMBOLS = LoadData._getSymbols()

def AS(sym=None):
        global SYMBOLS
        
        UpdateStocks()
        if len(SYMBOLS) < 1 and sym is None:
                print("Not enough stocks loaded.")
                return
        
        # If a single stock symbol has been passed, only test that symbol.
        if isinstance(sym, str):
                print("Will test: " + sym)
                tester = PatProcess.Test(LoadData.historicalData(sym))
                tester.parse()

        # Otherwise, test them all.
        else:
                for s in SYMBOLS[1:20]:
                        print("Will test:" + s[0])
                        #Patterns.test(LoadData.historicalData(s[0]))
                
AS("TEST")

'''

Get historical data:
http://ichart.finance.yahoo.com/table.csv?s=AAPL&c=1962
Details: http://etraderzone.com/free-scripts/47-historical-quotes-yahoo.html

Get complete stock quote list:
http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download
(replace exchange=nasdaq with exchange=nyse for nyse symbols).

More info:
http://benjisimon.blogspot.com/2009/01/truly-simple-stock-api.html

# ------------------------------------------
# Disable buffering for live AJAX feed

class Unbuffered:
        def __init__(self, stream):
                self.stream = stream
        def write(self, data):
                self.stream.write(data)
                self.stream.flush()
        def __getattr__(self, attr):
                return getattr(self.stream, attr)

sys.stdout=Unbuffered(sys.stdout)

'''
