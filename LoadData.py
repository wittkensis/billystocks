import cgitb, string, urllib, time, sys, re

def historicalData(sym):
        data = [line.split(',') for line in open('data/history/'+sym+'-data.csv','r')]
        return { 'dates' : [x[0] for x in data if x[0] != "Date"],
                 'open' : [x[1] for x in data if x[1] != "Open"],
                 'high' : [x[2] for x in data if x[2] != "High"],
                 'low' : [x[3] for x in data if x[3] != "Low"],
                 'close' : [x[4] for x in data if x[4] != "Close"],
                 'volume' : [x[5] for x in data if x[5] != "Volume"],
                 'adj close' : [x[6] for x in data if x[6] != "Adj Close"]
        }

def _getSymbols():
        S = [line.split(',') for line in open('data/companylist-nasdaq.csv','r')]
        S.extend([line.split(',') for line in open('data/companylist-nyse.csv','r')])

        for sym in S: sym[0]=sym[0].replace('\"','')
        return S

def _downloadSymbols():
        print("Downloading NASDAQ symbols...")
        urllib.urlretrieve("http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download", "data/companylist-nasdaq.csv")
        print("Downloading NYSE symbols...")
        urllib.urlretrieve("http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download", "data/companylist-nyse.csv")

def _downloadStocks( market, fail=False ):
        stocks = []
        failed = []
        count = 0
 
        if fail is True:
                stocks = market
                print("Retrying failed downloads (" + str(len(stocks)) + " symbols)...")
        else:
                stocks = [line.split(',') for line in open('data/companylist-' + market.lower() + '.csv','r')]
                #del stocks[0]   # Remove the header row
                print("Downloading " + market.upper() + " company data (for " + str(len(stocks)) + " symbols)...")
        
        for sym in stocks:
                try:
                        if re.match( "^[A-Za-z0-9_-]*$", sym[0] ):
                                urllib.urlretrieve("http://ichart.finance.yahoo.com/table.csv?s="+sym[0].strip()+"&c=2011&g=w", "data/history/"+sym[0].strip()+"-data.csv")
                                count +=1
                                print ( sym[0].strip() + " - " + str(round((100*(count / len(stocks))),2)) + "% complete")
                except:
                        print( sym[0].strip() + " - FAILED. Will retry." )
                        failed.append(sym)
                        time.sleep(7)
        if (len(failed) > 0) and (fail is False):
                _downloadStocks(failed,True)
