import sys
import controller
import updatecsvs
import insertdb
import os


# TODO: Add help argument to print out possible arguments and uses.
def main():
    args = sys.argv[1:]
    if len(args) == 0:
        updatecsvs.update_csvs()
        controller.scrapper_controller("ASIItem")
    elif len(args) == 3 and args[0] == '-i':
        insertdb.insert_db(args[1], args[2])
    elif len(args) == 1 and args[0] == '-clean':
        test = os.listdir("/Users/thomaslangston/PycharmProjects/pythonProject")
        for item in test:
            if item.endswith(".csv"):
                os.remove(item)
    elif len(args) == 1 and args[0] == '-csvs':
        updatecsvs.update_csvs()
    else:
        print("Please check format of arguments.")


if __name__ == "__main__":
    main()
