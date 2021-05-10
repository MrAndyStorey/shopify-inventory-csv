# Shopify Inventory to CSV
## Introduction
Every year my accountant asks for a inventory run down of [my online store](https://www.prendas.co.uk/) that runs on Shopify.  So I decided to make my life easier on June 30th and write this Python script to do all the hard work for me.  

It uses a variety of GraphQL calls to get the data.  The [reference of which is available here](https://shopify.dev/docs/admin-api/graphql/reference) and I used the [Shopify GraphiQL App Docs sidebar](https://shopify-graphiql-app.shopifycloud.com/) which I found to be a useful tool during development.

It takes a single argument for the output file (-out).  The default is inventory.csv.
```
inventory.py -out 
```

## Packages Used
We will be using:
* [Progress](https://github.com/verigak/progress) to display the progress of the scrip to the user.
* [python-dotenv](https://github.com/theskumar/python-dotenv) to read and use the environment variables
* [Shopify API](https://github.com/Shopify/shopify_python_api) to access the Shopify Admin API in Python.


To install these packages, you should use Python's package installer, pip3.  On the MacOS CLI you can use these commands:
```
pip3 install progress
pip3 install python-dotenv
pip3 install ShopifyAPI
```

## Environment variables
This project includes an example of a .env files that you need to create to allow you to acccess your private Shopify App.  You need to fill out your API key and API secret KEY before copying it to .env.
```
cp .env.local .env
```


## MacOS - SSL Certificate Error messages
If this is the first time you are running requests using SSL, you might numerous errors on the CLI when running the Python file such as:
```
SSLError: [SSL: CERTIFICATE_VERIFY_FAILED]
```
If this is the case, as it was for me, check out the following [stackoverflow.com answer](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify/42098127#42098127) that helped solve the issue for me.
