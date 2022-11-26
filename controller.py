import asi
import ingram
import csv


# Handles the webscrapers and calls them individually.
# Updates the SKU csvs with data delivered from the Database.

def init_webscrape():
    print("Collecting prices and stock.. please wait")
    #   ASI Web Scraper
    asi_controller()
    # Ingram Web Scraper
    ingram_controller()


# noinspection PyBroadException
def asi_controller():
    file = open('ASIItem.csv')
    csvreader = csv.reader(file)
    skus = []
    for row in csvreader:
        if row[0] != "itemSKU":
            skus.append(row)
    file.close()
    print("Collecting prices from ASI.. please wait")
    asi.asi_price_grabber(skus)


# noinspection PyBroadException
def ingram_controller():
    file = open('ingramSKUs.csv')
    csvreader = csv.reader(file)
    skus = []
    for row in csvreader:
        skus.append(row)
    file.close()
    print("Collecting prices from Ingram.. please wait")
    try:
        ingram.ingram_price_grabber(skus)
    except:
        print("Exception thrown while attempting to gather Ingram prices. Please inspect.")


def scrapper_controller(table_name):
    if table_name == 'ASIItem':
        asi_controller()
    elif table_name == 'IngramItem':
        ingram_controller()
