from typing import List

import asi
import csv
import ingram


def main():
    file = open('SKUs.csv')
    csvreader = csv.reader(file)
    skus = []
    for row in csvreader:
        skus.append(row)

    print("Collecting prices.. please wait")
    asi.asi_price_grabber(skus)

    # file = open('ingramSKUs.csv')
    # csvreader = csv.reader(file)
    # skus = []
    # for row in csvreader:
    #     skus.append(row)
    #
    # print("Collecting prices.. please wait")
    # ingram.ingram_price_grabber(skus)

if __name__ == "__main__":
    main()
