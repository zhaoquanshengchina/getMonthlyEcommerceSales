import csv, sys
from datetime import datetime

file = 'Walmart-PO_Data_2017-11-02_08-56-40PST.csv'#sys.argv[1]

def WallySales(file): # Get only monthly sales for Amazon Marketplace sales list export
	x = 1
	with open(file, 'r') as inCsv:
		reader = csv.reader(inCsv, delimiter=',') # Amazon only exports as tab delimited txt
		header = reader.next() # headers
		currentTime = datetime.now() # Current day/month/year to be used later

		with open('wallySales-%s.csv' % currentTime.strftime("%m-%d-%Y"), 'a+') as output: # Start datestamped log file
			for each in header: # Write header to log file
				output.write('%s,' % each) # comma delimited
			output.write('\n') # newline escaped
			print header

			for index in reader: # For each index in Amazon export
				if index[20][0:3] != "LUM": # If index contents is not Luminara SKU, pass
					pass # Can add later function for various SKUs, ie tarps.

				elif index[20][0:3] == "LUM": # If sku IS Luminara, continue.			
					purchaseDate = index[2]
					purchaseDate = datetime.strptime(purchaseDate, '%Y-%m-%d')

					if currentTime.strftime('%m') == purchaseDate.strftime('%m'):
						x += 1
						print x
						print purchaseDate

						for each in index:
							output.write('%s,' % each.replace(",", ""))
						output.write('\n')
						print index
					else:
						pass
			output.write(",,,,,,,,,,,,,,,,,,,=SUM(T2:T%s),,=SUM(V2:V%s),,,,,,," % (x, x))
			
WallySales(file)

#2: Order Date, 19: qty, 20: SKU, 21: Item cost

#Walmart Headers
#['PO#', 'Order#', 'Order Date', 'Ship By', 'Customer Name', 'Customer Shipping Address',
#'Customer Phone Number', 'Customer Email ID', 'Ship to Address 1', 'Ship to Address 2', 'City', 'State',
#'Zip', 'FLIDS', 'Line#', 'UPC', 'Status', 'Item Description', 'Shipping Method', 'Qty', 'SKU', 'Item Cost',
#'Shipping Cost', 'Tax', 'Update Status', 'Update Qty', 'Carrier', 'Tracking Number', 'Tracking Url']