import re, csv, urllib2, sys, json


def getCoreDataFromJSON():
	"""
	:return: returns dictionary of coreData JSON file after reading it
	"""
	with open('investIn/static/coreData.json', 'r') as core:
		coreData = json.load(core)
		return coreData


def getBasicStatsOpts(additionalOpts):
	"""
	:param additionalOpts: string of additional options
	:return: string of all options
	"""
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


def createReqURL(ticker, opts, baseURL, optionsURL):
	"""
	Adds ticker and options to the base URL to create the request URL
	:param baseURL: base url from coreData JSON
	:param optionsURL: options url from coreData JSON
	:param ticker: sanitized ticker from user
	:param opts: option codes entered by user
	:return: URL string with ticker and option codes
	"""
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


def getStockValueList(ticker, opts, baseURL, optsURL):
	"""
	Runs the URL and gets a file object with CSV string of data
	:param baseURL: string of base URL from coreData JSON
	:param optsURL: string of options URL from coreData JSON
	:param ticker: sanitized ticker from user
	:param opts: option codes entered by user
	:return: a list of values for option codes from running URL
	"""
	requestURL = createReqURL(ticker, opts, baseURL, optsURL)

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


def getIndicesValuesDict(indexOpts, strOfIndices, baseURL, optsURL):
	"""

	:param indexOpts: index options from coreData JSON
	:param strOfIndices: string of indices from coreData JSON
	:param baseURL: base url from coreData JSON
	:param optsURL: options url from coreData JSON
	:return: dictionary of each index and its values
	"""
	fullDict = {}
	obj = urllib2.urlopen(baseURL + strOfIndices + optsURL + indexOpts)

	for indexList in csv.reader(obj):
		fullDict[indexList[0]] = readOptsAndCreateDict(indexOpts, indexList)
	fullDict["indexList"] = strOfIndices.split(",")

	return fullDict
