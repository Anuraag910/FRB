import pandas as pd
from astropy.time import Time
from itertools import product

# Load the data
input_file = r"/home/arya/Downloads/B_team_coords_MJDs.csv"
df = pd.read_csv(input_file)

# Clean the RA and DEC columns by removing the text prefix
# and converting the values to float with 8 decimal places
df['RA'] = df['RA'].str.extract(r'([-+]?\d*\.\d+)').astype(float).round(8)
df['DEC'] = df['DEC'].str.extract(r'([-+]?\d*\.\d+)').astype(float).round(8)

# Extract the MJD values from the `TOA` column
df['MJD'] = df['TOA'].str.extract(r'(\d+\.\d+)').astype(float)

# Convert MJD to UTC using astropy
times = Time(df['MJD'], format='mjd')
df['UTC TOA'] = times.iso  # Convert to ISO format for readability

# Extract date part from UTC TOA and add a column for the date
df['DATE'] = df['UTC TOA'].str[:10]  # Format: YYYY-MM-DD
df['YYYYMMDD'] = df['DATE'].str.replace("-", "")  # Format: YYYYMMDD

df['UTC TOA'] = df['UTC TOA'].str.replace(" ", "T")  # Format: YYYYMMDD

# Function to generate a sequence of alphabet tags (A-Z, AA-ZZ, etc.)
def generate_alphabet_sequence():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for size in range(1, 4):  # Extend to 3-letter combinations if needed
        for combo in product(alphabet, repeat=size):
            yield "".join(combo)

# Assign a unique name for each row within a group
def assign_alphabet_sequence(group):
    sequence = generate_alphabet_sequence()
    return pd.Series([f"FRB{date}{next(sequence)}" for date in group['YYYYMMDD']], index=group.index)

# Apply the function to create the 'Name' column
df['Name'] = df.groupby('YYYYMMDD', group_keys=False).apply(assign_alphabet_sequence)

# Remove unnecessary columns
df = df.drop(columns=['TOA', 'DATE', 'YYYYMMDD'])

# Rearrange the column order
df = df[['Name', 'RA', 'DEC', 'MJD', 'UTC TOA']]

# Specify the output file name and save the updated DataFrame
output_file = r"/home/arya/Downloads/B_team_coords_MJDs_with_UTC_and_Name.csv"
df.to_csv(output_file, index=False)

# Display the first few rows to verify
print(df.head())
