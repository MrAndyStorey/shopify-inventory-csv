#!/usr/bin/env python3
import sys
import os
import csv
import time
import logging

import argparse

from dotenv import load_dotenv

from progress.bar import Bar

import shopify

# Logging Setup
logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s', filename='inventory.log', filemode='w', level=logging.INFO)

# Allow the user to pass the output CSV file via a CLI argument.
parser = argparse.ArgumentParser(description='')
parser.add_argument("--out", default="inventory.csv", type=str, help="Output filename - default = inventory.csv.")
parser.add_argument("--suppress", default=True, type=bool, help="Suppress products from the output filename that have zero inventory, makes for a tidier csv file - default = True.")
parser.add_argument("--factor", default=1, type=int, help="Sometimes it is helpful to increase/decrease the stock level to make projections - default = 1.")
parser.add_argument("--location", default="shopify", type=str, help="Only include stock that is handled by shopify - default = shopify.")
parser.add_argument("--delay", default=2, type=int, help="Unless you are on Shopify Plus, your API Rates will be limited, so a small delay is made inbetween calls.  Default = 2")

args = parser.parse_args()

# Load the environment variables from .env.
load_dotenv()

# Private applications authenticate with Shopify through basic HTTP authentication, 
# using the URL format https://{apikey}:{password}@{hostname}/admin/api/{version}/{resource}.json
apiKey = os.getenv("SHOPIFY_API_KEY")
apiPasswd = os.getenv("SHOPIFY_API_SECRET")
apiURL = os.getenv("SHOPIFY_URL")
apiVersion = os.getenv("SHOPIFY_API_VERSION")

if __name__ == '__main__':
  # Create a dictionary to store summary data
  counts = dict()

  # Open the output file and loop through each keyword one by one
  with open(args.out, 'w+', encoding='utf-8') as output_file:
    csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['ID', 'Name', 'Type', 'Cost', 'Quantity', 'Total'])

    # Connect to Shopify
    session = shopify.Session(apiURL, apiVersion, apiPasswd)
    shopify.ShopifyResource.activate_session(session)

    runningQty = 0
    runningTotal = 0

    # First get a total count of the products from shopify.  This gives a maxcount figure for the progress bar.
    maxCount = shopify.Product.count()
    currentCount = 0
    logging.info(f'Processing {maxCount} products.')

    # Showing a progress bar to the user.
    with Bar('Processing ' + str(maxCount) + ' products.', max=maxCount) as bar:
      
      products = shopify.Product.find()
      while currentCount < maxCount:
      
        for product in products:
          time.sleep(args.delay)

          currentCount += 1
          productID = product.id
          productName = product.title
          productLocation = ""
          productType = product.product_type
          productCost = 0
          productQty = 0

          for variant in product.variants:
            productLocation = variant.inventory_management
            if productLocation == args.location:
              if productCost == 0:
                # Unforetunately, the product cost is not held along with the rest of the variant data.
                # It is held as an inventory item.   So we will have to get it via a separate API call.
                inv_item = shopify.InventoryItem.find(variant.inventory_item_id)
                if inv_item.cost is not None:
                  productCost = float(inv_item.cost)
              productQty += round(int(variant.inventory_quantity) * args.factor,0)
          
          productTotal = round(productCost * productQty,2)

          #Update the Summary dictionary
          if productType in counts:
              counts[productType] += productTotal
          else:
              counts[productType] = productTotal

          # Write the product data for this row to the csv file.
          if productLocation == args.location:
            runningQty += productQty
            runningTotal += productTotal

            if productQty > 0:
              csv_writer.writerow([productID, productName, productType, productCost, productQty, productTotal])
            else:
              if args.suppress is False:
                csv_writer.writerow([productID, productName, productType, productCost, productQty, productTotal])

          bar.next()

        next_url = products.next_page_url
        products = shopify.Product.find(from_=next_url)

    csv_writer.writerow(["", "", "", "", runningQty, round(runningTotal,2)])
    logging.info(f'Product Count: {maxCount}.')
    logging.info(f'Total Variant Count: {runningQty}.')
    logging.info(f'Inventory Total: {round(runningTotal,2)}.')

    for key, val in counts.items():
      logging.info(f'{key}: {round(val,2)}.')

    # Close the Shopify session
    shopify.ShopifyResource.clear_session()

    # Close the output file
    output_file.close()
