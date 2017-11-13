import os

def Contents(filez):
	for each in filez.readlines():
		return each
	
def PassIndexParams():
	# put repetetive lines here
	# replace index variables (respective to market's exported spreadsheet index) with passed param
	return

cwd = os.getcwd()
for dirPath, dirNames, fileNames in os.walk(cwd):
	for each in fileNames:
		with open('%s' % each, 'r') as fileIn:
			if each.endswith(".csv"): # Ebay, SS, Walmart(ish), exports as csv.
				print "CSV File: %s" % each
				print Contents(fileIn) + '\n'

			elif each.endswith('.txt'): # Amazon exports as .txt with tab deliniation.
				print "TXT File: %s" % each
				print Contents(fileIn) + '\n'
