import csv, sys
from datetime import datetime

file = sys.argv[1]

def EbaySales(file): # Get only monthly sales for Amazon Marketplace sales list export
	x = 1
	with open(file, 'r') as inCsv:
		reader = csv.reader(inCsv, delimiter=',') # Amazon only exports as tab delimited txt
		header = reader.next() # headers
		currentTime = datetime.now() # Current day/month/year to be used later

		with open('ebaySales-%s.csv' % currentTime.strftime("%m-%d-%Y"), 'a+') as output: # Start datestamped log file
			for each in header: # Write header to log file
				output.write('%s,' % each) # comma delimited
			output.write('\n') # newline escaped
			print header

			for index in reader: # For each index in Amazon export
				if index[31][0:3] != "LUM": # If index contents is not Luminara SKU, pass
					pass # Can add later function for various SKUs, ie tarps.

				elif index[31][0:3] == "LUM": # If sku IS Luminara, continue.
					purchaseDate = index[25]
					if purchaseDate != "":
						purchaseDate = datetime.strptime(purchaseDate, '%b-%d-%y')
						if currentTime.strftime('%b') == purchaseDate.strftime('%b'):
							x += 1
							print x

							for each in index:
								output.write('%s,' % each.replace(",", ""))
							output.write('\n')
							print index
						else:
							pass
			output.write(",,,,,,,,,,,,,,,=sum(P2:P%s),,,,,=sum(U2:U%s),,,,,,,,,,,,,,,,,,,,," % (x, x))
							
EbaySales(file)

#Ebay Header
#['Sales Record Number,User Id,Buyer Fullname,Buyer Phone Number,Buyer Email,Buyer Address 1,Buyer Address 2,Buyer City,Buyer State,Buyer Zip,
#Buyer Country,Order ID,Item ID,Transaction ID,Item Title,Quantity,Sale Price,Shipping And Handling,Sales Tax,Insurance,Total Price,Payment Method,
#PayPal Transaction ID,Sale Date,Checkout Date,Paid on Date,Shipped on Date,Shipping Service,Feedback Left,Feedback Received,Notes to Yourself,
#Custom Label,Listed On,Sold On,Private Notes,Product ID Type,Product ID Value,Product ID Value 2,Variation Details,Product Reference ID,Tracking Number']

#Item Title: 14, quantity: 15, sale price: 16, total price: 20, sale date: 23, paid on date:25 customLabel: 31, sold on (site): 33