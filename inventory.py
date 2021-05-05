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
# os.environ or os.getenv

if __name__ == '__main__':

  # Open the output file and loop through each keyword one by one
  with open(args.output, 'w+', encoding='utf-8') as output_file:
    csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['Product', 'Product Type', 'Unit Cost', 'Quantity', 'Line Total'])

    # Showing a progress bar to the user.
    with Bar('Processing products.', max=100) as bar:



      # Write the data for this row to the csv file.
      csv_writer.writerow([keyword, builtResults, builtFree, builtPaid, builtAvgRating, builtAvgReviews, builtTopX.rstrip('|')])
      bar.next()
  output_file.close()
