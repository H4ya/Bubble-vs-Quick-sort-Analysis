"""اضفت كل ذا عشان نرتب ونسهل التيبل علينا """

import pandas as pd
path = 'cleaneDataset.csv'
dataFile = pd.read_csv(path)
dataFile.insert(0, 'id', [str(i) for i in range(1, len(dataFile) + 1)])
dataFile['Price'] = dataFile['Price'].astype(float).round(2)
dataFile['Date of Purchase'] = dataFile['Date of Purchase'].astype(str).str.zfill(8)
dataFile['Time of Purchase'] = dataFile['Time of Purchase'].astype(str).str.zfill(6)
dataFile['Date of Journey'] = dataFile['Date of Journey'].astype(str).str.zfill(8)
dataFile['Time of Purchase'] = dataFile['Time of Purchase'].astype(str).str.zfill(6)
dataFile['Departure Time'] = dataFile['Departure Time'].astype(str).str.zfill(6)
dataFile['Arrival Time'] = dataFile['Arrival Time'].astype(str).str.zfill(6)
dataFile['Actual Arrival Time'] = dataFile['Actual Arrival Time'].astype(str).str.zfill(6)

dataFile.to_csv('cleaneDataset.csv', index=False)



