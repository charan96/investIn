from django.shortcuts import render
from .forms import submitForm
import re, csv, urllib2

defOpts = "nophga2j3r2yl1"


def index(request):
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


# Make sure the ticker is 1 to 4 letters long
def sanitizeTicker(ticker):
	if re.match(r'^[A-Z]{1,5}$', ticker):
		return True
	return False


# Adds ticker and options to the base URL to create the request URL
def createReqURL(ticker, opts):
	baseURL = "http://finance.yahoo.com/d/quotes.csv?s="
	optionsURL = "&f="
	return baseURL + ticker + optionsURL + opts


# Uses codes.txt file to make a dict with codes and descriptions
def makeCodeDict():
	infile = 'investIn/static/codes.txt'
	reader = csv.reader(open(infile, 'r'))
	codeDict = {}
	for line in reader:
		code, desc = line
		codeDict[code] = desc
	return codeDict


# Runs the URL and gets a file object with CSV string of data
def getStockValueList(ticker, opts):
	requestURL = createReqURL(ticker, opts)

	# runs the URL and returns a file object with the stock
	# data in a CSV format
	fileObj = urllib2.urlopen(requestURL)

	# using CSV reader to split the file object data into a list
	# of the stock data values
	for stockDataList in csv.reader(fileObj):
		return stockDataList


# 1) Creates a list of option codes selected in the same order entered
# 2) Creates a dict with option and data from stockData (data from running URL)
#    and adds the previous list to the optDict
def readOptsAndCreateDict(opts, stockData):
	optDict = {}
	optionCodeList = []

	for index, option in enumerate(opts):
		if index + 1 > len(opts):
			break
		elif option.isdigit():
			continue
		elif opts[index + 1].isdigit():
			optionCodeList.append(option + opts[index + 1])
		else:
			optionCodeList.append(option)

	for index, option in enumerate(optionCodeList):
		optDict[option] = stockData[index]

	optDict['optCodeList'] = optionCodeList
	return optDict
