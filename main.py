import pandas as pd
import numpy as np

print("Hello World!")

# low_memory parameter to allow for mixed data types on a column in the dataframe
training_set = pd.read_csv("comp3208-train.csv", low_memory=False, header=None, names=["user", "itemID", "rating",
                                                                                       "timestamp"])

print(training_set)
