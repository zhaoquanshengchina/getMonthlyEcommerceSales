import csv, sys

file = "fd163957-c77b-4157-80c2-ecdcf1ce39df.csv"#sys.argv[1]
outputArray = []

theGoodColumns = [9, 21, 68, 75, 88, 90, 96] # CARRIER FEE, SKU, PAYDATE, UNITPRICE, STORE, QTY

with open(file, 'r') as inCsv:
	content = csv.reader(inCsv, delimiter=',')
	header = content.next()
	header = content.next()

	for each in theGoodColumns:
		print header[each],

	for index in content:
		scratchArray = []
		for each in theGoodColumns:
			scratchArray.append(index[each])
		outputArray.append(scratchArray)

	print outputArray

with open('SalesAnalysis.csv', 'wb') as outputCsv:
	writer = csv.writer(outputCsv)
	#writer.write(header[each],)
	writer.writerows(outputArray)