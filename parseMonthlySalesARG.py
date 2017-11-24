# Parse all csv spreadsheets in specific folder. Generate output SalesReport.csv's in export folder
# Will parse sales based on online SKU prefix, seperated by a dash.
# ie: COMPUTER-MODEL, COMPUTER-MODELZ are same 'category' of item, therefor will be parsed from items not in same category but with different colors, models, variations...
# Add sales of all SKU's in same category, specified as arguement to this script. >> python parseMonthlySales.py COMPUTER

import sys, csv, os
from datetime import datetime

currentTime = datetime.now() # One global for current time/month. Used basically everywhere.
SKU = sys.argv[1]

def totalSalesLog(sales):
	with open('totalSalesLog.txt', 'a+') as salesLog:
		salesLog.write("%s \n" % sales)

def replacePrint(output, index): # repetitive commands ran during each marketplace function call.
	for each in index:
		output.write('%s,' % each.replace(",", "")) # replace any rogue commas in product title, customer address, etc...
	print index # print each row that matched monthly/SKU requirements
	#Note: default spreadsheet header format of original marketplace spreadsheet is retained.

def eBayIndexes(inputz, output, x): # Run on ebay Spreadsheet
	total = 0
	for index in inputz:
		if index[31].split('-')[0] != SKU: # index 31 == 'Custom SKU' Split on first '-'
			pass # Is not a product we want total sales of

		elif index[31].split('-')[0] == SKU: # Is product we want total sales of
			purchaseDate = index[25]
					
			if purchaseDate != "": # Ebay has some lines (multiple item orders) that are blank. Disclude them.
				purchaseDate = datetime.strptime(purchaseDate, '%b-%d-%y') # make datetime instance using date format string from spreadsheet.
				if currentTime.strftime('%b') == purchaseDate.strftime('%b'): # Match month abbreviation to current. ie: Nov, Dec, etc...
					replacePrint(output, index) # See above

					x += 1
					total += float(index[20].replace("$", ""))
					print total
					output.write('\n')
					
	output.write(",,,,,,,,,,,,,,,=SUM(P2:P%s),,,,,=sum(U2:U%s),,,,,,,,,,,,,,,,,,,,," % (x, x))
	totalSalesLog("eBay: $%s" % total)

	# Ugly code for last line in csv with spreadsheet functions in their respective columns.

def amazonIndexes(inputz, output, x):
	total = 0
	for index in inputz:
		if index[2].split('-')[0] != SKU:
			pass

		elif index[2].split('-')[0] == SKU:
			purchaseDate = index[5].split(" ")[0] 
			purchaseDate = datetime.strptime(purchaseDate, '%Y-%m-%d') 

			if currentTime.strftime('%m') == purchaseDate.strftime('%m'): # Match numerical month string in spreadsheet, with current month. ie: 11, 12, etc...
				replacePrint(output, index)

				x += 1
				total += float(index[3]) * float(index[10])
				print total
				output.write("=sum(D%s*K%s)" % (x, x)) # Amazon has line items, regardless of multi item orders. Multiply 'Quantity' with 'Sale price.'
				output.write('\n') # new line escaped

	output.write(",,,=sum(D2:D%s),,,,,,,,=sum(L2:L%s)" % (x, x))
	totalSalesLog("Amazon: $%s" % total)

def wallyIndexes(inputz, output, x):
	total = 0
	for index in inputz:
		if index[20].split('-')[0] != SKU:
			pass

		elif index[20].split('-')[0] == SKU:		
			purchaseDate = index[2]
			purchaseDate = datetime.strptime(purchaseDate, '%Y-%m-%d')

			if currentTime.strftime('%m') == purchaseDate.strftime('%m'):
				replacePrint(output, index)
				
				x += 1
				total += float(index[21])
				print total
				output.write('\n')

	output.write(",,,,,,,,,,,,,,,,,,,=SUM(T2:T%s),,=SUM(V2:V%s),,,,,,,," % (x, x))
	totalSalesLog("Wally: $%s" % total)
	# Ugly code for last line in csv with spreadsheet functions in their respective columns.

def shipStationIndexes(inputz, output, x):
	total = 0
	for index in inputz:
		if index[88].split('-')[0] != SKU:
			pass

		elif index[88].split('-')[0] == SKU:
			purchaseDate = index[68].split(" ")[0]
			purchaseDate = datetime.strptime(purchaseDate, '%m/%d/%Y')

			if currentTime.strftime('%m') == purchaseDate.strftime('%m'):
				replacePrint(output, index)

				x += 1
				total += float(index[96]) * float(index[75])
				print total
				output.write('\n')

	output.write(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,=SUM(BX2:BX%s),,,,,,,,,,,,,,,,,,,,,=SUM(CS2:CS%s),,,,,,,,,") # BX = QTY, CS = unitprice
	totalSalesLog("ShipStation: $%s" % total)

def parseBasedOn(storeName, inputz, output): # We quick check which store the spreadsheet belongs to
	x = 1

	if storeName == 'eBay':
		eBayIndexes(inputz, output, x)
	elif storeName == 'Amazon':
		amazonIndexes(inputz, output, x)
	elif storeName == 'Wally':
		wallyIndexes(inputz, output, x)
	elif storeName == 'ShipStation':
		shipStationIndexes(inputz, output, x)

def makeFile(file, outputFolder): # Input file, output file
	with open(file, 'r') as inCsv:

		if file.endswith('.txt'):
			inputz = csv.reader(inCsv, delimiter='\t') # If txt file (Amazon is) tab delimited
			# A little redundant code but necessary for reading header (full spreadsheet) properly later on

		else:
			inputz = csv.reader(inCsv, delimiter=',')
		header = inputz.next()

		if header[0:3] == ['item-name', 'listing-id', 'sku']: # Amazon header
			storeName = 'Amazon'
		elif header[0:3] == ['Sales Record Number', 'User Id', 'Buyer Fullname']: # Ebay header
			storeName = 'eBay'
		elif header[0:3] == ['PO#', 'Order#', 'Order Date']: # Wally header
			storeName = 'Wally'
		elif header[0:3] == ['AmountPaid', 'BatchID', 'BillDutiesToSender']: # Shipstation header
			storeName = 'ShipStation'

		with open('%s/%s-%s.csv' % (outputFolder, storeName, currentTime.strftime("%m-%d-%Y")), 'a+') as output: # Output CSV
			for each in header: # Keep original marketplace header intact.
				output.write('%s,' % each) # Comma dlimited
			output.write('\n') # New line escaped

			parseBasedOn(storeName, inputz, output)

inputFolder = './SpreadsheetExports/' # hardcoded location of input files
outputFolder = './output/' # hardcoded file for output, converted files.

currentDirectory = next(os.walk('%s' % inputFolder))[2] # Get each spreadsheet filename
print currentDirectory

with open('totalSalesLog.txt', 'w+') as deleteExistingLog:
	pass

for eachFile in currentDirectory: #Run script on each file
	makeFile('./%s%s' % (inputFolder, eachFile), outputFolder)
