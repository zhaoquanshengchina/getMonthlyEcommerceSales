import csv, sys
from datetime import datetime

#Amazon Header
#['item-name', 'listing-id', 'sku', 'price', 'shipping-fee', 'purchase-date', 'buyer-email', 'buyer-nick-name', 'date-listed', 'item-is-marketplace', 'quantity']

file = 'Amazon-Sold+Listings+Report+11-02-2017 - Copy.txt'#sys.argv[1]

def AmazonSales(file): # Get only monthly sales for Amazon Marketplace sales list export
	x = 1
	with open(file, 'r') as amznTxt:
		reader = csv.reader(amznTxt, delimiter='\t') # Amazon only exports as tab delimited txt
		header = reader.next() # headers
		currentTime = datetime.now() # Current day/month/year to be used later

		with open('amazonSales-%s.csv' % currentTime.strftime("%m-%d-%Y"), 'a+') as amazonOutput: # Start datestamped log file
			for each in header: # Write header to log file
				amazonOutput.write('%s,' % each) # comma delimited
			amazonOutput.write('\n') # newline escaped
			print header

			for index in reader: # For each index in Amazon export
				if index[2][0:3] != "LUM": # If index contents is not Luminara SKU, pass
					pass # Can add later function for various SKUs, ie tarps.
				elif index[2][0:3] == "LUM": # If sku IS Luminara, continue.
					purchaseDate = index[5].split(" ")[0] # Figure out purchase date month
					purchaseDate = datetime.strptime(purchaseDate, '%Y-%m-%d') # Exclude the time, only year-month-day

					if currentTime.strftime('%m') == purchaseDate.strftime('%m'): # If month of purchase date is current month
						x += 1
						print x

						for each in index: # For each in row
							amazonOutput.write("%s," % each) # Write entire rows contents to log file, comma delimited
						amazonOutput.write("=sum(D%x*K%x)" % (x, x))
						amazonOutput.write('\n') # new line escaped
						print index
					else: # Otherwise, from a previous month.
						pass # pass.
			amazonOutput.write(",,,=sum(D2:D%x),,,,,,,,=sum(L2:L%x)" % (x, x))
			#amazonOutput.write("=sum(L2:L%x)" % x)
AmazonSales(file)