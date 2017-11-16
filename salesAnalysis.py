import csv, sys

file = sys.argv[1]

outputArray = []
theGoodColumns = [9, 21, 68, 75, 88, 90, 96] # Remove all columns, except these ones.
# CARRIER FEE, SKU, PAYDATE, UNITPRICE, STORE, QTY

with open(file, 'r') as inCsv: # input hella long spreadsheet (Shipstation export = 100+ columns)
	content = csv.reader(inCsv, delimiter=',')
	header = content.next() # Headers

	for each in theGoodColumns:
		print header[each],

	for index in content: # For every row in csv, do the following
		row = [] # Scratch pad array for retaining only desired info/rows
		for each in theGoodColumns: # For each specified index, do the following.
			row.append(index[each]) # Append scratch pad array
		outputArray.append(row) # Append static, master array with entire row
	print outputArray # Print completed row

with open('SalesAnalysis.csv', 'wb') as outputCsv: # WB because Windows appends /r/n's like an idiot.
	writer = csv.writer(outputCsv) # To write pythonic arrays as comma delimited csv's
	writer.writerows(outputArray) # Write each row without array bracket and quote characters.