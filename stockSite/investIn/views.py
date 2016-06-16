from django.shortcuts import render
from .forms import submitForm
import re, csv

optionCodes = {'y0': 'Trailing Annual Dividend Yield In Percent', 'd2': 'Trade Date', 'x0': 'Stock Exchange',
		   'd0': 'Trailing Annual Dividend Yield', 'd1': 'Last Trade Date', 'q0': 'Ex Dividend Date',
		   'g6': 'Holdings Gain (Realtime)', 'g5': 'Holdings Gain Percent (Realtime)', 'g4': 'Holdings Gain',
		   'g3': 'Annualized Gain', 'g1': 'Holdings Gain Percent', 'g0': 'Days Low', 't8': 'Oneyr Target Price',
		   't6': 'Trade Links', 't7': 'Ticker Trend', 't1': 'Last Trade Time', 'l2': 'High Limit',
		   'l3': 'Low Limit', 'l0': 'Last Trade With Time', 'l1': 'Last Trade Price Only', 'j4': 'E B I T D A',
		   'j5': 'Change From Year Low', 'j6': 'Percent Change From Year Low', 'j0': 'Year Low',
		   'j1': 'Market Capitalization', 'j2': 'Shares Outstanding', 'j3': 'Market Cap (Realtime)',
		   'b4': 'Book Value Per Share', 'b6': 'Bid Size', 'w4': 'Days Value Change (Realtime)', 'b0': 'Bid',
		   'w1': 'Days Value Change', 'b3': 'Bid (Realtime)', 'o0': 'Open', 'e9': 'E P S Estimate Next Quarter',
		   'e8': 'E P S Estimate Next Year', 'e7': 'E P S Estimate Current Year', 'e0': 'Diluted E P S',
		   'r5': 'P E G Ratio', 'r6': 'Price E P S Estimate Current Year', 'r7': 'Price E P S Estimate Next Year',
		   'r0': 'P E Ratio', 'r1': 'Dividend Pay Date', 'r2': 'P E Ratio (Realtime)', 'v1': 'Holdings Value',
		   'h0': 'Days High', 'm5': 'Change From Two Hundredday Moving Average',
		   'm4': 'Two Hundredday Moving Average', 'm7': 'Change From Fiftyday Moving Average',
		   'm6': 'Percent Change From Two Hundredday Moving Average', 'm0': 'Days Range',
		   'm3': 'Fiftyday Moving Average', 'm2': 'Days Range (Realtime)',
		   'm8': 'Percent Change From Fiftyday Moving Average', 'c8': 'After Hours Change (Realtime)',
		   'c3': 'Commission', 'c1': 'Change', 'c0': 'Change<i> Change In Percent', 'c6': 'Change (Realtime)',
		   'c4': 'Currency', 'p2': 'Change In Percent', 'p0': 'Previous Close', 'p1': 'Price Paid',
		   'p6': 'Price Book', 'p5': 'Price Sales', 'f0': 'Trade Links Additional', 'b2': 'Ask (Realtime)',
		   'f6': 'Shares Float', 'w0': 'Year Range', 's1': 'Shares Owned', 's0': 'Symbol', 's7': 'Short Ratio',
		   's6': 'Revenue', 'k3': 'Last Trade Size', 'k2': 'Change In Percent (Realtime)',
		   'k1': 'Last Trade (Realtime) With Time', 'k0': 'Year High', 'k5': 'Change In Percent From Year High',
		   'k4': 'Change From Year High', 'i0': 'More Info', 'i5': 'Order Book (Realtime)', 'v0': 'Volume',
		   'a0': 'Ask', 'a2': 'Average Daily Volume', 'a5': 'Ask Size', 'v7': 'Holdings Value (Realtime)',
		   'n0': 'Name', 'n4': 'Notes'}
defOpts = "nophga2j3r2yba"


def index(request):
	formClass = submitForm

	if request.method == 'POST':
		form = formClass(data=request.POST)

		if form.is_valid():
			ticker = str(request.POST.get('ticker', '')).upper()
			if sanitizeTicker(ticker):
				requestURL = createReqURL(ticker, defOpts)
				return render(request, 'investIn/demoDisplayTicker.html', {'ticker': ticker, 'url': requestURL})
			else:
				return render(request, 'investIn/error.html', {'ticker': ticker})

	return render(request, 'investIn/index.html', {'form': submitForm})


def sanitizeTicker(ticker):
	if re.match(r'^[A-Z]{1,5}$', ticker):
		return True
	return False


def createReqURL(ticker, opts):
	baseURL = "http://finance.yahoo.com/d/quotes.csv?s="
	optionsURL = "&f="
	return baseURL + ticker + optionsURL + opts
