# getMonthlyEcommerceSales
Get monthly eCommerce Sales from Amazon, eBay, Walmart, Jet and ShipStation exports.

## Usage
`python parseMonthlySales.py` will take **any** raw Amazon/Ebay/Walmart/ShipStation spreadsheet exports in the **SpreadsheetExports** folder and parse them. The resulting files will be created in the **output** folder. Each output will be a csv, with a name corresponding to the particular marketplace, todays date and will include only sales, for a particular SKU for the current month.
  
**Requirements:** None  
System agnostic and all imported libraries are native to default python installation. (`os, csv, datetime`)  
(csv could easily be removed for further minimilism)

## What?
**Gather month to date eCommerce sales, for only specified products/skus.**
* Strip out any csv rows, line items, that are prior to current month or are not associated with desired product.
* Output the remaining line items (**matching** items) to an output csv that retains format/header of the original marketplace export.
* Append spreadsheet functions to marketplace's corresponding column, to do standard math on columns to be viewed via xlsx/gsheets later.

## Why?
**Reliable weekly sales reports. Despite each eCommerce platform using different export conventions.**
* Reliable sales. It's easy to mixup which **correct** indexes need to be added, ignored, multiplied, etc...
* See '**TODO**'
* Each eCommerce platform exports their sales in a different way and has it's own pros/cons when assessing.
    - Amazon/Walmart allow export of all sales in 30/60/90 day incriments (across months)
    - Ebay allows for scheduled export within a **range** of dates. Dates often times different from Amazon/Walmart, above.
      * eBay exports also has duplicate line item entries when one order consists of multiple items. (archaic)
    - ie: Shipstation records true shipping cost, whereas other marketplaces have 'Free Shipping' recorded.
* Total sales 'GUI' metrics aren't always reliable, sometimes are too general and/or don't offer filtering of sales by product/sku.

## TODO
* Pythonically add up totals of a column. Then output dictionary of {eBay: $TotalSales, Amazon: $X} to log file for easy (no gsheet/xlsx) reference
* Add sys.argv[1] input to specify SKU prefix that gets parsed
  * Not needed but would remove personalized, hardcoded 'LUM' SKU prefix.
  * Incorporate tarps when finalizing Nov.  
* **Add shipstation/shipping cost feature.**
  * Match order number, append shipping cost index to index's row.
  * Purpose of this repo is based on 'whim' of bosses. This feature would add usefulness to more people.
* Port to ruby because it would be simple enough to do and Ocra is better than Py2Exe/Pyinstaller.
* **Add Sales Tax feature**
  * If sys.argv[2] == 'salestax' then if salestax index != None, append row to SalesTax-Month.csv
