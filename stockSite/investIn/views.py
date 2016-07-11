from django.shortcuts import render
from .forms import submitForm
import stockdata, urllib2, csv

coreData = stockdata.getCoreDataFromJSON()
codeDict = stockdata.makeCodeDict()


def index(request):
	"""
	:param request: HTML request
	:return: appropriate template with dictionary
	"""
	formClass = submitForm
	defOpts = coreData['defOpts']
	baseURL = coreData['baseURL']
	optsURL = coreData['optsURL']

	if request.method == 'POST':
		form = formClass(data=request.POST)

		if form.is_valid():
			ticker = str(request.POST.get('ticker', '')).upper()
			if stockdata.sanitizeTicker(ticker):
				stockData = stockdata.getStockValueList(ticker, defOpts, baseURL, optsURL)
				templateOpts = stockdata.readOptsAndCreateDict(defOpts, stockData)
				return render(request, 'investIn/demoDisplayTicker.html',
						  {'ticker': ticker, 'opts': templateOpts, 'codeDict': codeDict})
			else:
				return render(request, 'investIn/error.html', {'ticker': ticker})

	return render(request, 'investIn/index.html', {'form': submitForm})


def display(request, ticker):
	"""
	:param request: HTML request for display
	:param ticker: sanitized ticker from user
	:return: appropriate template with dictionary
	"""
	defOpts = coreData['defOpts']
	baseURL = coreData['baseURL']
	optsURL = coreData['optsURL']

	stockData = stockdata.getStockValueList(ticker, defOpts, baseURL, optsURL)
	templateOpts = stockdata.readOptsAndCreateDict(defOpts, stockData)

	return render(request, 'investIn/demoDisplayTicker.html',
			  {'ticker': ticker, 'opts': templateOpts, 'codeDict': codeDict})


def keyStats(request, ticker):
	"""
	:param request: HTML request for key stats
	:param ticker: sanitized ticker from user
	:return: appropriate template with dictionary
	"""
	baseURL = coreData['baseURL']
	optsURL = coreData['optsURL']
	keyStatsOpts = coreData['keyStatsOpts']

	fullKeyStatsOpts = stockdata.getBasicStatsOpts(keyStatsOpts)
	stockData = stockdata.getStockValueList(ticker, fullKeyStatsOpts, baseURL, optsURL)
	templateOpts = stockdata.readOptsAndCreateDict(fullKeyStatsOpts, stockData)

	return render(request, 'investIn/keyStatsDisplay.html',
			  {'ticker': ticker, 'opts': templateOpts, 'codeDict': codeDict})


def charts(request, ticker):
	"""
	:param request: HTML request for charts
	:param ticker: sanitized ticker from user
	:return: appropriate template with dictionary
	"""
	defOpts = coreData['defOpts']
	baseURL = coreData['baseURL']
	optsURL = coreData['optsURL']

	stockData = stockdata.getStockValueList(ticker, defOpts, baseURL, optsURL)
	templateOpts = stockdata.readOptsAndCreateDict(defOpts, stockData)

	return render(request, 'investIn/charts.html',
			  {'ticker': ticker, 'opts': templateOpts, 'codeDict': codeDict})


def stockIndexes(request):
	"""
	:param request: HTML request for stock indices
	:return: appropriate template with dictionary
	"""
	indexOpts = coreData['indexOpts']
	strOfIndices = coreData['indicesStr']
	baseURL = coreData['baseURL']
	optsURL = coreData['optsURL']

	fullDict = stockdata.getIndicesValuesDict(indexOpts, strOfIndices, baseURL, optsURL)

	return render(request, 'investIn/stockIndices.html', {'opts': fullDict, 'codeDict': codeDict})


def stockCompare(request):
	return render(request, 'investIn/stockCompare.html', {})
