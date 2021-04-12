import pandas as pd
import numpy as np
import math

# low_memory parameter to allow for mixed data types on a column in the dataframe
initial_training_set = pd.read_csv("comp3208-train.csv", low_memory=False, header=None, names=["user", "itemID",
                                                                                               "rating", "timestamp"])

# shuffle the rows in the data frame to make it unique with each run
initial_training_set = initial_training_set.sample(frac=1)

# splitting the training set into a training set (80%) and a validation set (20%) to use
training_set = initial_training_set.iloc[:80, :]
validation_set = initial_training_set.iloc[80:, :]

test_set = pd.read_csv("comp3208-test.csv", low_memory=False, header=None, names=["user", "itemID", "timestamp"])


# u1 and u2 are lists of ratings for the same items from user1 and user2
# Returns the similarity measure for user1 and user2
def sim(u1, u2):
    mean_u1 = sum(u1) / len(u1)
    mean_u2 = sum(u2) / len(u2)

    sum_u1 = 0
    sum_u2 = 0

    sum_sqr_u1 = 0
    sum_sqr_u2 = 0

    for i in u1:
        sum_u1 += i - mean_u1
        sum_sqr_u1 += (i - mean_u1) ^ 2

    for i in u2:
        sum_u2 += i - mean_u2
        sum_sqr_u2 += (i - mean_u2) ^ 2

    return (sum_u1 * sum_u2) / (math.sqrt(sum_sqr_u1) * math.sqrt(sum_sqr_u2))


# ToDo
# Given two users user1 and user2 create a list of ratings for items that both user1 and user2 have reviewed
def calculate_sim(user1, user2):
    u1 = {}
    u2 = {}

    return sim(u1, u2)


# ToDo Function to get ratings for a given user
def get_ratings(user):
    ratings = training_set.loc[training_set['user' == user], ['ratings']].iloc[0]
    # Need to test exactly what data type this variable is, may need to add an extra argument to the command

    print(ratings)

    return ratings


# ToDo Function to get rating for a specific item from a specific user
def get_single_rating(user, item):
    single_rating = training_set.loc[training_set['user' == user], training_set['item' == item]].iloc[0].item()
    # need to check what index in the iloc to give the right rating

    print(single_rating)

    return single_rating


def get_neighbours(user, item):
    neighbours = {}

    return neighbours


# Given a user, item and list of neighbours
# Returns a predicted rating for the item by the user
def pred(user, item):
    user_ratings = get_ratings(user)

    mean_user_rating = sum(user_ratings) / len(user_ratings)

    numerator = 0

    denominator = 0

    neighbours = get_neighbours(user, item)

    for neighbour in neighbours:
        neighbour_ratings = get_ratings(neighbour)
        mean_neighbour_rating = sum(neighbour_ratings) / len(neighbour_ratings)
        numerator += (calculate_sim(user, neighbour) * (get_single_rating(neighbour, item) - mean_neighbour_rating))
        denominator += calculate_sim(user, neighbour)

    return mean_user_rating + (numerator / denominator)


get_ratings(2)
