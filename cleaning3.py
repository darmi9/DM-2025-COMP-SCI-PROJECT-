import pandas as pd

# Import the CSV file
df = pd.read_csv('salaries-by-college-type.csv')

# Handling missing data: Drop rows with any missing values
df = df.dropna(axis=0)
print(df.columns)
# Remove commas from numeric columns (to handle cases like '1,000')
df = df.replace(',', '', regex=True)
numerical_columns = [
    'Starting Median Salary',
    'Mid-Career Median Salary',
    'Mid-Career 10th Percentile Salary',
    'Mid-Career 25th Percentile Salary',
    'Mid-Career 75th Percentile Salary',
    'Mid-Career 90th Percentile Salary'
]

for salaries in numerical_columns:
        df[salaries] = df[salaries].str[1:]
# converted to integers.
df[numerical_columns] = df[numerical_columns].astype(float)

df.to_csv('updated-salaries-by-college-type.csv', index=False)
