#!/usr/bin/env python3
import sys
import os
import csv

import argparse

from dotenv import load_dotenv

from progress.bar import Bar

import shopify


# Allow the user to pass the output CSV file via a CLI argument.
parser = argparse.ArgumentParser(description='')
parser.add_argument("--out", default="inventory.csv", type=str, help="Output filename - default = inventory.csv.")
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

  # Open the output file and loop through each keyword one by one
  with open(args.out, 'w+', encoding='utf-8') as output_file:
    csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['ID', 'Name', 'Type', 'Cost', 'Quantity', 'Total'])

    # Connect to Shopify, and get a list of products.
    session = shopify.Session(apiURL, apiVersion, apiPasswd)
    shopify.ShopifyResource.activate_session(session)

    runningQty = 0
    runningTotal = 0

    # Showing a progress bar to the user.
    with Bar('Processing products:') as bar:
      
      for product in shopify.Product.find():
        productID = product.id
        productName = product.title
        productType = product.product_type
        productCost = 0
        productQty = 0
        productTotal = 0
        for variant in product.variants:
          productCost =+ float(variant.price)
          productQty =+ int(variant.inventory_quantity)
          productTotal =+ round(productCost * productQty,2)

        runningQty =+ productQty
        runningTotal =+ productTotal

        # Write the data for this row to the csv file.
        csv_writer.writerow([productID, productName, productType, productCost, productQty, productTotal])

        bar.next()

    csv_writer.writerow(["", "", "", "", runningQty, runningTotal])

    # Close the Shopify session
    shopify.ShopifyResource.clear_session()

    # Close the output file
    output_file.close()
