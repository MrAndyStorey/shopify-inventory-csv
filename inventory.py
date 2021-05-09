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
    csv_writer.writerow(['Product', 'Product Type', 'Unit Cost', 'Quantity', 'Line Total'])

    # Connect to Shopify, and get a list of products.
    with shopify.Session.temp(apiURL, apiVersion, apiPasswd):
      print(shopify.GraphQL().execute("{ shop { name id } }"))

    # Showing a progress bar to the user.
    with Bar('Processing products.', max=100) as bar:
      
      productName = ""
      productType = ""
      productCost = 0
      productQty = 0
      productTotal = 0

      # Write the data for this row to the csv file.
      csv_writer.writerow([productName, productType, productCost, productQty, productTotal])
      bar.next()

    # Close the output file
    output_file.close()
