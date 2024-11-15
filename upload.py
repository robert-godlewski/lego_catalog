import pandas as pd # type: ignore


# Need to figure out how to connect to SQLite
filename = input('What is the name of the csv file? ')

try:
    data = pd.read_csv(filename, header=0).values
    print(type(data))
    print(data)
except:
    print('There is nothing to upload here.')
