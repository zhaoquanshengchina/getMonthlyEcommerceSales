import csv, os
from datetime import datetime

currentTime = datetime.now() # One global for current time/month. Used basically everywhere.

def replacePrint(output, index): # repetitive commands ran during each marketplace function call.
	for each in index:
		output.write('%s,' % each.replace(",", "")) # replace any rogue commas in product title, customer address, etc...
	print index # print each row that matched monthly/SKU requirements
	#Note: default spreadsheet header format of original marketplace spreadsheet is retained.

def eBayIndexes(reader, output, x): # Run on ebay Spreadsheet
	for index in reader:
		if index[31][0:3] != "LUM": # index 31 == 'Custom SKU'
			pass # Is not a product we want total sales of

		elif index[31][0:3] == "LUM": # Is product we want total sales of
			purchaseDate = index[25]
					
			if purchaseDate != "": # Ebay has some lines (multiple item orders) that are blank. Disclude them.
				purchaseDate = datetime.strptime(purchaseDate, '%b-%d-%y') # make datetime instance using date format string from spreadsheet.
				if currentTime.strftime('%b') == purchaseDate.strftime('%b'): # Match month abbreviation to current. ie: Nov, Dec, etc...
					replacePrint(output, index) # See above
					x += 1
	output.write(",,,,,,,,,,,,,,,=sum(P2:P%s),,,,,=sum(U2:U%s),,,,,,,,,,,,,,,,,,,,," % (x, x))
	# Ugly code for last line in csv with spreadsheet functions in their respective columns.

def amazonIndexes(reader, output, x):
	for index in reader:
		if index[2][0:3] != "LUM":
			pass

		elif index[2][0:3] == "LUM":
			purchaseDate = index[5].split(" ")[0] 
			purchaseDate = datetime.strptime(purchaseDate, '%Y-%m-%d') 

			if currentTime.strftime('%m') == purchaseDate.strftime('%m'): # Match numerical month string in spreadsheet, with current month. ie: 11, 12, etc...
				replacePrint(output, index)
				x += 1

				output.write("=sum(D%s*K%s)" % (x, x)) # Amazon has line items, regardless of multi item orders. Multiply 'Quantity' with 'Sale price.'
				output.write('\n') # new line escaped

	output.write(",,,=sum(D2:D%s),,,,,,,,=sum(L2:L%s)" % (x, x))

def wallyIndexes(reader, output, x):
	for index in reader:
		if index[20][0:3] != "LUM":
			pass

		elif index[20][0:3] == "LUM":		
			purchaseDate = index[2]
			purchaseDate = datetime.strptime(purchaseDate, '%Y-%m-%d')

			if currentTime.strftime('%m') == purchaseDate.strftime('%m'):
				replacePrint(output, index)
				x += 1

	output.write(",,,,,,,,,,,,,,,,,,,=SUM(T2:T%s),,=SUM(V2:V%s),,,,,,,," % (x, x))
	# Ugly code for last line in csv with spreadsheet functions in their respective columns.

def parseBasedOn(storeName, reader, output): # We quick check which store the spreadsheet belongs to
	x = 1

	if storeName == 'eBay':
		eBayIndexes(reader, output, x)
	elif storeName == 'Amazon':
		amazonIndexes(reader, output, x)
	elif storeName == 'Wally':
		wallyIndexes(reader, output, x)
	elif storeName == 'ShipStation':
		print 'FINISH SHIPSTATION PARSING'
	else:
		return 'BROKEN!'

def makeFile(file, outputFolder): # Input file, output file
	with open(file, 'r') as inCsv:

		if file.endswith('.txt'):
			reader = csv.reader(inCsv, delimiter='\t') # If txt file (Amazon is) tab delimited
			# A little redundant code but necessary for reading header (full spreadsheet) properly later on

		else:
			reader = csv.reader(inCsv, delimiter=',')
		header = reader.next()

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

			parseBasedOn(storeName, reader, output)

inputFolder = './SpreadsheetExports/' # hardcoded location of input files
outputFolder = './output/' # hardcoded file for output, converted files.

inCWD = next(os.walk('%s' % inputFolder))[2] # Get each spreadsheet filename
print inCWD

for eachFile in inCWD: #Run script on each file
	makeFile('./%s%s' % (inputFolder, eachFile), outputFolder)
