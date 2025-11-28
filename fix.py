import pandas as pd

dataFile = pd.read_csv('cleaned_data.csv') #read the dataset and store it

dataFile['Price'] = dataFile['Price'].astype(float).round(2)

dataFile.to_csv('dataset_with_float_prices.csv', index=False)
