import csv, sys
from datetime import datetime

file = 'ShipStation-3e7d41a5-6fc1-4468-a536-10b7a8803a1c.csv'#sys.argv[1]

def ShipStationSales(file): # Get only monthly sales for Amazon Marketplace sales list export
	x = 0
	with open(file, 'r') as inCsv:
		reader = csv.reader(inCsv, delimiter=',') # Amazon only exports as tab delimited txt
		header = reader.next() # headers
		currentTime = datetime.now() # Current day/month/year to be used later

		with open('shipStationSales-%s.csv' % currentTime.strftime("%m-%d-%Y"), 'a+') as output: # Start datestamped log file
			for each in header: # Write header to log file
				output.write('%s,' % each) # comma delimited
			output.write('\n') # newline escaped

			for index in reader: # For each index in Amazon export
				if index[88][0:3] != "LUM": # If index contents is not Luminara SKU, pass
					pass # Can add later function for various SKUs, ie tarps.

				elif index[88][0:3] == "LUM": # If sku IS Luminara, continue.
					purchaseDate = index[68].split(" ")[0]
					purchaseDate = datetime.strptime(purchaseDate, '%m/%d/%Y')

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
			#output.write(",,,,,,,,,,,,,,,,,,,=SUM(T2:T%s),,=SUM(V2:V%s),,,,,,," % (x, x))
		
ShipStationSales(file)

#0: AmountPaid
#1: BatchID
#2: BillDutiesToSender
#3: BillToAccount
#4: BillToCountryCode
#5: BillToParty
#6: BillToPostalCode
#7: BuyerEmail
#8: Carrier
#9: CarrierFee
#10: CarrierTransactionID
#11: City
#12: Company
#13: ConfirmationServiceID
#14: CountryCode
#15: CreateDate
#16: DeclaredValue
#17: Delivered
#18: DeliveryDate
#19: DeliveryMessage
#20: DeliveryStatusDate
#21: Description
#22: EmailErrorMessage
#23: EmailNote
#24: EmailNotificationRequested
#25: EmailNotificationSent
#26: ExtendedPrice
#27: ExternalID
#28: ExternalTrackingID
#29: ForwardTo
#30: Height
#31: HidePostage
#32: InsuranceBillingTransactionID
#33: InsuranceClaimCode
#34: InsuranceClaimDate
#35: InsuranceClaimFiled
#36: InsuranceClaimNumber
#37: InsuranceErrorMessage
#38: InsuranceFee
#39: InsuranceProviderID
#40: InsurancePurchased
#41: InsuranceRequested
#42: InsuranceTransactionID
#43: InsuranceVoided
#44: InsuranceVoidErrorMessage
#45: InsuredValue
#46: InternalTransactionID
#47: IsReturnLabel
#48: Items
#49: LabelCreateDate
#50: LabelErrorMessage
#51: LabelInfoMessage
#52: LabelMessage
#53: Length
#54: MarketplaceNotified
#55: ModifyDate
#56: Name
#57: NonMachinable
#58: NoPostage
#59: NotifyErrorMessage
#60: OrderDate
#61: OrderID
#62: OrderItemID
#63: OrderNumber
#64: OrderTotal
#65: Package
#66: PackageCount
#67: PackageTypeID
#68: PayDate
#69: PaymentMethod
#70: Phone
#71: PostalCode
#72: ProductID
#73: ProviderID
#74: ProviderName
#75: Quantity
#76: ReturnReceivedDate
#77: RMANumber
#78: SellerID
#79: ServiceCode
#80: ShipDate
#81: ShipmentID
#82: Shipped
#83: ShippingContentTypeID
#84: ShippingPaid
#85: ShippingServiceCode
#86: ShippingServiceID
#87: ShowPostage
#88: SKU
#89: State
#90: StoreName
#91: Street1
#92: Street2
#93: Street3
#94: TaxAmount
#95: TrackingNumber
#96: UnitPrice
#97: UserID
#98: Username
#99: VoidDate
#100: Voided
#101: WarehouseID
#102: WarehouseName
#103: WeightOz
#104: Width
#105: BatchNumber