#!/usr/bin/python

import json

defOpts = "nj1l1c1p2poma2r"
indexOpts = "snl1c1p2m"
quandl_KEY = "d9c2StRA1P6VRoQFAdL2"
strOfIndices = "^NYA,^XAX,^IXIC,^GSPC,^OEX,^SPSUPX,^VIX,^RUT,^FTSE,^FCHI,^GDAXI,^N225,^HSI,^STI"
baseURL = "http://download.finance.yahoo.com/d/quotes.csv?s="
optsURL = "&f="

jsonDict = {"defOpts": defOpts, "indexOpts": indexOpts, "quandlKEY": quandl_KEY, "indicesStr": strOfIndices,
		"baseURL": baseURL, "optsURL": optsURL}

jsonFile = "coreData.json"

with open(jsonFile, 'w') as outfile:
	json.dump(jsonDict, outfile)
