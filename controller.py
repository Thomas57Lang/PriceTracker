import asi
import ingram
import csv


def init_webscrape():
    print("Collecting prices and stock.. please wait")
    #   ASI Web Scraper
    asi_controller()
    # Ingram Web Scraper
    ingram_controller()


def asi_controller():
    file = open('SKUs.csv')
    csvreader = csv.reader(file)
    skus = []
    for row in csvreader:
        skus.append(row)
    file.close()
    print("Collecting prices from ASI.. please wait")
    asi.asi_price_grabber(skus)


def ingram_controller():
    file = open('ingramSKUs.csv')
    csvreader = csv.reader(file)
    skus = []
    for row in csvreader:
        skus.append(row)
    file.close()
    print("Collecting prices from Ingram.. please wait")
    ingram.ingram_price_grabber(skus)
