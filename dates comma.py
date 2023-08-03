import pandas as pd
data = pd.read_csv('output.csv')
data['Date'] = data['Date'].str.replace(",", '')
data.to_csv('output.csv', index=False)