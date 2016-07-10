from django.shortcuts import render
from .forms import submitForm
import stockdata

coreData = stockdata.getCoreDataFromJSON()
codeDict = stockdata.makeCodeDict()


def index(request):
	"""
	:param request: HTML request
	:return: appropriate template with dictionary
	"""
	formClass = submitForm

	if request.method == 'POST':
		form = formClass(data=request.POST)

		if form.is_valid():
			ticker = str(request.POST.get('ticker', '')).upper()
			if stockdata.sanitizeTicker(ticker):
				stockData = stockdata.getStockValueList(ticker, coreData["defOpts"], coreData['baseURL'],
										    coreData['optsURL'])
				templateOpts = stockdata.readOptsAndCreateDict(coreData["defOpts"], stockData)
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
	stockData = stockdata.getStockValueList(ticker, coreData["defOpts"], coreData['baseURL'], coreData['optsURL'])
	templateOpts = stockdata.readOptsAndCreateDict(coreData["defOpts"], stockData)

	return render(request, 'investIn/demoDisplayTicker.html',
			  {'ticker': ticker, 'opts': templateOpts, 'codeDict': codeDict})


def keyStats(request, ticker):
	"""
	:param request: HTML request for key stats
	:param ticker: sanitized ticker from user
	:return: appropriate template with dictionary
	"""
	keyStatOpts = stockdata.getBasicStatsOpts("p2poabyr1m6m8m3m4ms6wdee7j4rr6s7p5")
	stockData = stockdata.getStockValueList(ticker, keyStatOpts, coreData['baseURL'], coreData['optsURL'])
	templateOpts = stockdata.readOptsAndCreateDict(keyStatOpts, stockData)

	return render(request, 'investIn/keyStatsDisplay.html',
			  {'ticker': ticker, 'opts': templateOpts, 'codeDict': codeDict})


def charts(request, ticker):
	"""
	:param request: HTML request for charts
	:param ticker: sanitized ticker from user
	:return: appropriate template with dictionary
	"""
	stockData = stockdata.getStockValueList(ticker, coreData["defOpts"], coreData['baseURL'], coreData['optsURL'])
	templateOpts = stockdata.readOptsAndCreateDict(coreData["defOpts"], stockData)

	return render(request, 'investIn/charts.html',
			  {'ticker': ticker, 'opts': templateOpts, 'codeDict': codeDict})


def stockIndexes(request):
	"""
	:param request: HTML request for stock indices
	:return: appropriate template with dictionary
	"""
	indexOpts = coreData['indexOpts']
	strOfIndices = coreData['indicesStr']
	obj = urllib2.urlopen(coreData['baseURL'] + strOfIndices + coreData['optsURL'] + indexOpts)

	fullDict = {}

	for indexList in csv.reader(obj):
		fullDict[indexList[0]] = stockdata.readOptsAndCreateDict(indexOpts, indexList)
	fullDict["indexList"] = strOfIndices.split(",")

	return render(request, 'investIn/stockIndices.html', {'opts': fullDict, 'codeDict': codeDict})


def stockCompare(request):
	pass


def customStats(request):
	pass
