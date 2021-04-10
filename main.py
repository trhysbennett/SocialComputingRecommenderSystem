import pandas as pd
import numpy as np
import math

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

#u1 and u2 are lists of ratings for the same items from user1 and user2
#Returns the similarity measure for user1 and user2
def sim(u1, u2):

    mean_u1 = sum(u1)/len(u1)
    mean_u2 = sum(u2)/len(u2)

    sum_u1 = 0
    sum_u2 = 0

    sum_sqr_u1 = 0
    sum_sqr_u2 = 0

    for i in u1:
        sum_u1 += i - mean_u1
        sum_sqr_u1 += (i-mean_u1) ^ 2

    for i in u2:
        sum_u2 += i - mean_u2
        sum_sqr_u2 += (i - mean_u2) ^ 2

    return (sum_u1*sum_u2)/(math.sqrt(sum_sqr_u1)*math.sqrt(sum_sqr_u2))

#ToDo
#Given two users user1 and user2 create a list of ratings for items that both user1 and user2 have reviewed
def calculate_sim(user1, user2):

    u1 = {}
    u2 = {}

    return sim(u1, u2)

#ToDo Function to get ratings for a given user
def get_ratings(user):

#ToDo Function to get rating for a specific item from a specific user
def get_single_rating(user, item):

#Given a user, item and list of neighbours
#Returns a predicted rating for the item by the user
def pred(user, item, neighbours):

    user_ratings = get_ratings(user)

    mean_user_rating = sum(user_ratings)/len(user_ratings)

    numerator = 0

    denominator = 0

    for neighbour in neighbours:
        neighbour_ratings = get_ratings(neighbour)
        mean_neighbour_rating = sum(neighbour_ratings)/len(neighbour_ratings)
        numerator += (calculate_sim(user, neighbour) * (get_single_rating(neighbour, item) - mean_neighbour_rating))
        denominator += calculate_sim(user, neighbour)

    return mean_user_rating + (numerator/denominator)