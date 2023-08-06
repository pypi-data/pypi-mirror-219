import sys
import os
def display():
    if len(sys.argv) == 1 or sys.argv[1] != "-u" or sys.argv[3] != "-p" or sys.argv[5] != "-db":
        print("॥ जय श्री राम ॥")
        raise Exception("To run RESTfulApiGen run RESTfulApiGen -u <username> -p <password> -db <database_name>")
        exit()
    else:
        print("HELL Yeah ")
        if not os.environ.get(sys.argv[4]):
            print(sys.argv[4])
        else:
            print(os.environ.get(sys.argv[4]))
        
    

display()
#  or sys.argv[5] != "--demo" or sys.argv[5] != "--demo-gunincorn" or sys.argv[5] != "--demo-react" or sys.argv[5] != "-react"
