import csv, os
from datetime import datetime

currentTime = datetime.now()
x = 1

def replaceWritePrint(output, index, x):
	x += 1
	for each in index:
		output.write('%s,' % each.replace(",", ""))
	output.write('\n')
	print index

def eBayIndexes(reader, output, x):
	for index in reader:
		if index[31][0:3] != "LUM":
			pass #

		elif index[31][0:3] == "LUM":
			purchaseDate = index[25]
					
			if purchaseDate != "":
				purchaseDate = datetime.strptime(purchaseDate, '%b-%d-%y')
				if currentTime.strftime('%b') == purchaseDate.strftime('%b'):
					replaceWriteAndPrint(output, index, x)
	output.write(",,,,,,,,,,,,,,,=sum(P2:P%s),,,,,=sum(U2:U%s),,,,,,,,,,,,,,,,,,,,," % (x, x))

def amazonIndexes(reader, output, x):
	for index in reader:
		if index[2][0:3] != "LUM":
			pass

		elif index[2][0:3] == "LUM":
			purchaseDate = index[5].split(" ")[0] 
			purchaseDate = datetime.strptime(purchaseDate, '%Y-%m-%d') 

			if currentTime.strftime('%m') == purchaseDate.strftime('%m'): 
				replaceWriteAndPrint(output, index, x)

				output.write("=sum(D%s*K%s)" % (x, x))
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
				replaceWriteAndPrint(output, index, x)
	output.write(",,,,,,,,,,,,,,,,,,,=SUM(T2:T%s),,=SUM(V2:V%s),,,,,,," % (x, x))

def parseBasedOnStore(storeName, reader, output):
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

def makeFile(file, outputFolder):
	with open(file, 'r') as inCsv:

		if file.endswith('.txt'):
			reader = csv.reader(inCsv, delimiter='\t')
		else:
			reader = csv.reader(inCsv, delimiter=',')
		header = reader.next()

		if header[0:3] == ['item-name', 'listing-id', 'sku']:
			storeName = 'Amazon'
		elif header[0:3] == ['Sales Record Number', 'User Id', 'Buyer Fullname']:
			storeName = 'eBay'
		elif header[0:3] == ['PO#', 'Order#', 'Order Date']:
			storeName = 'Wally'
		elif header[0:3] == ['AmountPaid', 'BatchID', 'BillDutiesToSender']:
			storeName = 'ShipStation'

		print "%s: Finished" % storeName

		with open('%s/%s-%s.csv' % (outputFolder, storeName, currentTime.strftime("%m-%d-%Y")), 'a+') as output:
			for each in header:
				output.write('%s,' % each) 
			output.write('\n')

			parseBasedOnStore(storeName, reader, output)

inputFolder = './SpreadsheetExports/' 
outputFolder = './output/'

filesInCWD = next(os.walk('%s' % inputFolder))[2]
print filesInCWD

for eachFile in filesInCWD:
	makeFile('./%s%s' % (inputFolder, eachFile), outputFolder)