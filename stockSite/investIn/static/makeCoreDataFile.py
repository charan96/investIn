#!/usr/bin/python

import json

defOpts = "nj1l1c1p2poma2r"
indexOpts = "snl1c1p2m"
keyStatsOpts = "p2poabyr1m6m8m3m4ms6wdee7j4rr6s7p5"
quandl_KEY = "d9c2StRA1P6VRoQFAdL2"
strOfIndices = "^NYA,^XAX,^IXIC,^GSPC,^OEX,^SPSUPX,^VIX,^RUT,^FTSE,^FCHI,^GDAXI,^N225,^HSI,^STI"
baseURL = "http://download.finance.yahoo.com/d/quotes.csv?s="
optsURL = "&f="

jsonDict = {"defOpts": defOpts, "indexOpts": indexOpts, "quandlKEY": quandl_KEY, "indicesStr": strOfIndices,
		"baseURL": baseURL, "optsURL": optsURL, "keyStatsOpts": keyStatsOpts}

jsonFile = "coreData.json"

with open(jsonFile, 'w') as outfile:
	json.dump(jsonDict, outfile)
