import sys
def display():
    if sys.argv[0] != "jayshreeram" and len(sys.argv) >= 0  or sys.argv[1] != "-u" or sys.argv[2] != "-p" or sys.argv[3] != "-db":
        print("॥ जय श्री राम ॥")
        raise Exception("To run RESTfulApiGen run RESTfulApiGen -u <username> -p <password> -db <database_name>")
        exit()
    else:
        print("HELL Yeah ")
    

display()
