from django.shortcuts import render
from .forms import submitForm, doubleStockForm
import stockdata

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
	"""
	:param request: HTML request for comparing two stocks
	:return: appropriate template with dictionary
	"""
	formClass = doubleStockForm
	defOpts = coreData['defOpts']
	baseURL = coreData['baseURL']
	optsURL = coreData['optsURL']

	if request.method == 'POST':
		form = formClass(data=request.POST)

		if form.is_valid():
			ticker1 = str(request.POST.get('ticker1', '')).upper()
			ticker2 = str(request.POST.get('ticker2', '')).upper()

			if stockdata.sanitizeTicker(ticker1) and stockdata.sanitizeTicker(ticker2):
				stockData1 = stockdata.getStockValueList(ticker1, defOpts, baseURL, optsURL)
				stockData2 = stockdata.getStockValueList(ticker2, defOpts, baseURL, optsURL)

				templateOpts1 = stockdata.readOptsAndCreateDict(defOpts, stockData1)
				templateOpts2 = stockdata.readOptsAndCreateDict(defOpts, stockData2)

				return render(request, 'investIn/doubleStockDisplay.html',
						  {'ticker1': ticker1, 'ticker2': ticker2, 'opts1': templateOpts1,
						   'opts2': templateOpts2,
						   'codeDict': codeDict})
			else:
				errTickerStr = ticker1 + " and/or " + ticker2
				return render(request, 'investIn/error.html', {'ticker': errTickerStr})

	return render(request, 'investIn/stockCompare.html', {'form': doubleStockForm})
