import pandas as pd

# read csv file
df = pd.read_csv('example.csv')

# delete the rows that all values are NaN
df = df.dropna(how='all')

# get the  12th column names
f12_name = df.columns[12]

# change the 12th column to float and round to 0
df[f12_name] = df[f12_name].astype(float).round(0)

# get the 15th column names
f15_name = df.columns[15]

# change the 15th column to float and round to 3
df[f15_name] = df[f15_name].astype(float).round(3)

# get the 0th and 11th column names
f0_name = df.columns[0]
f11_name = df.columns[10]

# change the 0th column to numeric, if error, change to NaN
df[f0_name] = pd.to_numeric(df[f0_name], errors='coerce')

# delete the rows that the 0th column is NaN
df = df.dropna(subset=[f0_name])

# change the 0th and 11th column to int
df[f0_name] = df[f0_name].astype(int)
df[f11_name] = df[f11_name].astype(int)

# get the 3rd and 4th column names
f3_name = df.columns[3]
f4_name = df.columns[4]

# change the 3rd and 4th column to float and round to 6
df[f3_name] = df[f3_name].astype(float).round(6)
df[f4_name] = df[f4_name].astype(float).round(6)


# write to csv file
df.to_csv('result.csv', index=False)