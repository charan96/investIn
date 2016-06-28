from django.shortcuts import render
from .forms import submitForm
import re, csv, urllib2, sys

defOpts = "nj1l1c1p2poma2r"
quandl_KEY = "d9c2StRA1P6VRoQFAdL2"


def index(request):
	"""
	:param request: HTML request
	:return: appropriate template with dictionary
	"""
	formClass = submitForm
	codeDict = makeCodeDict()

	if request.method == 'POST':
		form = formClass(data=request.POST)

		if form.is_valid():
			ticker = str(request.POST.get('ticker', '')).upper()
			if sanitizeTicker(ticker):
				stockData = getStockValueList(ticker, defOpts)
				templateOpts = readOptsAndCreateDict(defOpts, stockData)
				return render(request, 'investIn/demoDisplayTicker.html',
						  {'ticker': ticker, 'opts': templateOpts, 'codeDict': codeDict})
			else:
				return render(request, 'investIn/error.html', {'ticker': ticker})

	return render(request, 'investIn/index.html', {'form': submitForm})


def display(request, ticker):
	codeDict = makeCodeDict()
	stockData = getStockValueList(ticker, defOpts)
	templateOpts = readOptsAndCreateDict(defOpts, stockData)
	return render(request, 'investIn/demoDisplayTicker.html',
			  {'ticker': ticker, 'opts': templateOpts, 'codeDict': codeDict})


def keyStats(request, ticker):
	keyStatOpts = getBasicStatsOpts("p2poabyr1m6m8m3m4ms6wdee7j4rr6s7p5")
	codeDict = makeCodeDict()
	stockData = getStockValueList(ticker, keyStatOpts)
	templateOpts = readOptsAndCreateDict(keyStatOpts, stockData)
	return render(request, 'investIn/keyStatsDisplay.html',
			  {'ticker': ticker, 'opts': templateOpts, 'codeDict': codeDict})


def charts(request, ticker):
	codeDict = makeCodeDict()
	stockData = getStockValueList(ticker, defOpts)
	templateOpts = readOptsAndCreateDict(defOpts, stockData)
	return render(request, 'investIn/charts.html',
			  {'ticker': ticker, 'opts': templateOpts, 'codeDict': codeDict})


def stockIndexes(request):
	codeDict = makeCodeDict()
	indexOpts = "snl1c1p2m"
	obj = urllib2.urlopen(
		"http://download.finance.yahoo.com/d/quotes.csv?s=^NYA,^XAX,^IXIC,^GSPC,^OEX,^SPSUPX,^VIX,^RUT,^FTSE,^N225,^GDAXI,^HSI,^AORD,^STI&f=" + indexOpts)
	fullDict = {}
	for indexList in csv.reader(obj):
		fullDict[indexList[0]] = readOptsAndCreateDict(indexOpts, indexList)
	fullDict["indexList"] = ['^NYA', '^XAX', '^IXIC', '^GSPC', '^OEX', '^SPSUPX', '^VIX', '^RUT', '^FTSE', '^N225',
					 '^GDAXI', '^HSI', '^AORD', '^STI']
	return render(request, 'investIn/stockIndices.html', {'opts': fullDict, 'codeDict': codeDict})


def stockCompare(request):
	pass


def customStats(request):
	pass


def getBasicStatsOpts(additionalOpts):
	return "nj1l1c1" + additionalOpts


def sanitizeTicker(ticker):
	"""
	Make sure the ticker is 1 to 4 letters long
	:param ticker: raw ticker entered by user
	:return: true if ticker is 1 to 5 uppercase alphabets; else false
	"""
	if re.match(r'^[A-Z]{1,5}$', ticker):
		return True
	return False


def createReqURL(ticker, opts):
	"""
	Adds ticker and options to the base URL to create the request URL
	:param ticker: sanitized ticker from user
	:param opts: option codes entered by user
	:return: URL string with ticker and option codes
	"""
	baseURL = "http://finance.yahoo.com/d/quotes.csv?s="
	optionsURL = "&f="
	return baseURL + ticker + optionsURL + opts


def makeCodeDict():
	"""
	Uses codes.txt file to make a dict with codes and descriptions
	:return: dict with keys of option codes and values of code descriptions
	"""
	infile = 'investIn/static/codes.txt'
	reader = csv.reader(open(infile, 'r'))
	codeDict = {}
	for line in reader:
		code, desc = line
		codeDict[code] = desc
	return codeDict


def getStockValueList(ticker, opts):
	"""
	Runs the URL and gets a file object with CSV string of data
	:param ticker: sanitized ticker from user
	:param opts: option codes entered by user
	:return: a list of values for option codes from running URL
	"""
	requestURL = createReqURL(ticker, opts)

	# runs the URL and returns a file object with the stock
	# data in a CSV format
	fileObj = urllib2.urlopen(requestURL)

	# using CSV reader to split the file object data into a list
	# of the stock data values
	for stockDataList in csv.reader(fileObj):
		return stockDataList


def readOptsAndCreateDict(opts, stockData):
	"""
	1) Creates a list of option codes selected in the same order entered
	2) Creates a dict with option and data from stockData (data from running URL)
	   and adds the previous list to the optDict
	:param opts: string of options selected by user
	:param stockData: list of values for respective options obtained from running URL
	:return: dict of option and values and a key of 'optCodeList' is mapped to a list
		   of options in the ordered entered by user
	"""
	optDict = {}
	optionCodeList = []

	for index, option in enumerate(opts):
		if index + 1 == len(opts):
			if not option.isdigit():
				optionCodeList.append(option)
			break
		elif option.isdigit() and opts[index + 1].isdigit():
			print "Invalid Options: Multiple numbers"
			sys.exit()
		elif option.isdigit():
			continue
		elif opts[index + 1].isdigit():
			optionCodeList.append(option + opts[index + 1])
		else:
			optionCodeList.append(option)

	for index, option in enumerate(optionCodeList):
		optDict[option] = stockData[index]

	optDict['optsString'] = opts
	optDict['optCodeList'] = optionCodeList
	return optDict
