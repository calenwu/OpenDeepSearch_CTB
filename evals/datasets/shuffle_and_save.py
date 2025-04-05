import pandas as pd
import numpy as np

# Read the original CSV file
df = pd.read_csv('frames_test_set.csv')

# Shuffle the dataframe
df_shuffled = df.sample(frac=1, random_state=42)

# Take the first 100 rows
df_sample = df_shuffled.head(100)

# Save to a new CSV file
df_sample.to_csv('frames_test_set_sample.csv', index=False)

print(f"Successfully saved 100 shuffled rows to frames_test_set_sample.csv") 