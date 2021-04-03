import pandas as pd
import numpy as np

print("Hello World!")

# low_memory parameter to allow for mixed data types on a column in the dataframe
initial_training_set = pd.read_csv("comp3208-train.csv", low_memory=False, header=None, names=["user", "itemID",
                                                                                               "rating", "timestamp"])
print(initial_training_set)

# shuffle the rows in the data frame to make it unique with each run
initial_training_set = initial_training_set.sample(frac=1)
print(initial_training_set)

# splitting the training set into a training set (80%) and a validation set (20%) to use
training_set = initial_training_set.iloc[:80, :]
validation_set = initial_training_set.iloc[80:, :]

test_set = pd.read_csv("comp3208-test.csv", low_memory=False, header=None, names=["user", "itemID", "timestamp"])
