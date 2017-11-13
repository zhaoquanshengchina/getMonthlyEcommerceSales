# getMonthlyEcommerceSales
Get monthly eCommerce Sales from Amazon, eBay, Walmart, Jet and ShipStation exports.

## What?
**Gather month to date eCommerce sales, for only specified products/skus.**
* Strip out any csv rows, line items, that are prior to current month or are not associated with desired product.
* Output the remaining line items (**matching** items) to an output csv that retains format/header of the original marketplace export.
* Append spreadsheet functions to marketplace's corresponding column, to do standard math on columns to be viewed via xlsx/gsheets later.

## Why?
**Reliable weekly sales reports. Despite each eCommerce platform using different export conventions.**
* Reliable sales. It's easy to mixup which **correct** indexes need to be added, ignored, multiplied, etc...
* Each eCommerce platform exports their sales in a different way and has it's own pros/cons when assessing.
    - Amazon/Walmart allow export of all sales in 30/60/90 day incriments (across months)
    - Ebay allows for scheduled export within a **range** of dates. Dates often times different from Amazon/Walmart, above.
    - ie: Shipstation records true shipping cost, whereas other marketplaces have 'Free Shipping' recorded.
* Total sales 'GUI' metrics aren't always reliable, sometimes are too general and/or don't offer filtering of sales by product/sku.

## TODO
* Pythonically add up totals of a column. Then output dictionary of {eBay: $TotalSales, Amazon: $X} to log file for easy (no gsheet/xlsx) reference
* Add shipstation/shipping cost feature.
  * Match order number, append shipping cost index to EOL of output csv.
