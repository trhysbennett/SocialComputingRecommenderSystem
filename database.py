import math
import sqlite3
import codecs
import random

global connection
global c

connection = sqlite3.connect('comp3208.db')
connection.row_factory = lambda cursor, row: row[0]

readHandle = codecs.open('comp3208-train.csv', 'r', 'utf-8', errors='replace')
listLines = readHandle.readlines()
readHandle.close()

c = connection.cursor()
c.execute('CREATE TABLE IF NOT EXISTS training_data '
               '(UserID INT, ItemID INT, Rating FLOAT, PredRating FLOAT, TmSmp INT)')
connection.commit()
c.execute('CREATE TABLE IF NOT EXISTS predictions (UserID INT, ItemID INT, PredRating FLOAT, '
               'TmSmp INT)')
connection.commit()
c.execute('CREATE TABLE IF NOT EXISTS similarities (Item1 INT, Item2 INT, Similarity FLOAT)')
connection.commit()

'''
split = math.floor(len(listLines) * 0.8)
count = 0
'''

c.execute('SELECT COUNT(UserID) From training_data')
if int(c.fetchone()) == 0:
    for strLine in listLines:
        if len(strLine.strip()) > 0:
            listParts = strLine.strip().split(',')
            if len(listParts) == 4:
                c.execute('INSERT INTO training_data VALUES (?,?,?,?,?)',
                          (listParts[0], listParts[1], listParts[2], random.random() * 5.0, listParts[3]))
            else:
                raise Exception('failed to parse csv: ' + repr(listParts))

    connection.commit()


c.execute('CREATE INDEX IF NOT EXISTS training_data_index on training_data (UserID, ItemID)')
connection.commit()


readHandle = codecs.open('comp3208-test.csv', 'r', 'utf-8', errors='replace')
listLines = readHandle.readlines()
readHandle.close()

c.execute('SELECT COUNT(UserID) From predictions')
if int(c.fetchone()) == 0:
    for strLine in listLines:
        if len(strLine.strip()) > 0:
            listParts = strLine.strip().split(',')
            if len(listParts) == 3:
                c.execute('INSERT INTO predictions VALUES (?,?,?,?)',
                          (listParts[0], listParts[1], -1.0, listParts[2]))
            else:
                raise Exception('failed to parse csv: ' + repr(listParts))

    connection.commit()

c.execute('CREATE INDEX IF NOT EXISTS predictions_index on predictions (UserID, ItemID)')
connection.commit()

# u1 and u2 are lists of ratings for the same items from user1 and user2
# Returns the similarity measure for user1 and user2
def sim(u1, u2):
    mean_u1 = sum(u1) / len(u1)
    mean_u2 = sum(u2) / len(u2)

    sum_us = 0

    sum_sqr_u1 = 0
    sum_sqr_u2 = 0

    for i in range(len(u1)):
        sum_us += (u1[i] - mean_u1) * (u2[i] - mean_u2)
        sum_sqr_u1 += (u1[i] - mean_u1) ** 2
        sum_sqr_u2 += (u2[i] - mean_u2) ** 2

    sqrt_sum_sqr_u1 = math.sqrt(sum_sqr_u1)
    sqrt_sum_sqr_u2 = math.sqrt(sum_sqr_u2)

    if (sqrt_sum_sqr_u1 == 0.0) | (sqrt_sum_sqr_u2 == 0.0):
        return 0
    else:
        similarity = sum_us / (sqrt_sum_sqr_u1 * sqrt_sum_sqr_u2)
        return similarity


# Given two users user1 and user2 create a list of ratings for items that both user1 and user2 have reviewed
def calculate_sim(user1, user2):
    '''
    c.execute('SELECT SUM((u1Rating - AVG(u1Rating)) * (u2Rating - AVG(u2Rating))) FROM '
              '(SELECT A.ItemID, A.Rating AS u1Rating, B.Rating AS u2Rating FROM training_data A, training_data B '
              'WHERE A.UserID=' + str(user1) + ' AND B.UserID=' + str(user2) + ' AND A.ItemID=B.ItemID')
    sum_us = c.fetchone()
    '''

    c.execute('SELECT Rating FROM training_data WHERE UserID=' + str(user1) +
                   ' AND ItemID IN (SELECT ItemID FROM training_data WHERE UserID=' + str(user2) + ')')
    u1 = c.fetchall()

    if len(u1) == 0:
        return 0
    else:

        c.execute('SELECT Rating FROM training_data WHERE UserID=' + str(user2) +
                  ' AND ItemID IN (SELECT ItemID FROM training_data WHERE UserID=' + str(user1) + ')')
        u2 = c.fetchall()

        return sim(u1, u2)


# Function to get ratings for a given user
def get_ratings(user):
    c.execute('SELECT Rating FROM training_data WHERE UserID=' + str(user))
    ratings_list = c.fetchall()

    return ratings_list


# Function to get rating for a specific item from a specific user
def get_single_rating(user, item):
    c.execute('SELECT Rating FROM training_data WHERE UserID=' + str(user) + ' AND ItemID=' + str(item))
    single_rating = float(c.fetchone())

    return single_rating


def get_neighbours(user, item):
    c.execute('SELECT UserID FROM training_data WHERE ItemID=' + str(item) + ' AND UserID<>' + str(user))
    neighbour_list = c.fetchall()

    return neighbour_list


# Given a user, item and list of neighbours
# Returns a predicted rating for the item by the user
def pred(user, item):
    user_ratings = get_ratings(user)

    mean_user_rating = sum(user_ratings) / len(user_ratings)

    numerator = 0

    denominator = 0

    neighbours = get_neighbours(user, item)

    for neighbour in neighbours:
        c.execute('SELECT AVG(Rating) FROM training_data WHERE UserID=' + str(neighbour))
        mean_neighbour_rating = float(c.fetchone())
        similarity = calculate_sim(user, neighbour)
        numerator += (similarity * (get_single_rating(neighbour, item) - mean_neighbour_rating))
        denominator += similarity

    prediction = mean_user_rating + (numerator / denominator)

    c.execute('UPDATE predictions SET PredRating=' + str(prediction) + ' WHERE UserID=' + str(user) + ' AND ItemID='
              + str(item))
    connection.commit()

    return prediction

def item_sim(i1, i2):
    mean_i1 = sum(i1) / len(i1)
    mean_i2 = sum(i2) / len(i2)

    sum_i = 0

    sum_sqr_i1 = 0
    sum_sqr_i2 = 0

    for rating in range(len(i1)):
        sum_i += (i1[rating] - mean_i1) * (i2[rating] - mean_i2)
        sum_sqr_i1 += (i1[rating] - mean_i1) ** 2
        sum_sqr_i2 += (i2[rating] - mean_i2) ** 2

    sqrt_sum_sqr_i1 = math.sqrt(sum_sqr_i1)
    sqrt_sum_sqr_i2 = math.sqrt(sum_sqr_i2)

    if (sqrt_sum_sqr_i1 == 0.0) | (sqrt_sum_sqr_i2 == 0.0):
        return 0
    else:
        similarity = sum_i / (sqrt_sum_sqr_i1 * sqrt_sum_sqr_i2)
        return similarity


def calculate_item_sim(item1, item2):
    c.execute('SELECT Rating FROM training_data WHERE ItemID=' + str(item1) +
              ' AND UserID IN (SELECT UserID FROM training_data WHERE ItemID=' + str(item2) + ')')
    i1 = c.fetchall()

    if len(i1) == 0:
        return 0
    else:

        c.execute('SELECT Rating FROM training_data WHERE ItemID=' + str(item2) +
                  ' AND UserID IN (SELECT UserID FROM training_data WHERE ItemID=' + str(item1) + ')')
        i2 = c.fetchall()

        return item_sim(i1, i2)

def get_item_ratings(item):
    c.execute('SELECT Rating FROM training_data WHERE ItemID=' + str(item))
    ratings_list = c.fetchall()

    return ratings_list

def item_pred(user, item):
    c.execute('SELECT ItemID FROM training_data WHERE UserID=' + str(user))
    user_ratings = c.fetchall()
    numerator = 0
    denominator = 0

    for rating in user_ratings:
        c.execute('SELECT Rating FROM training_data WHERE UserID=' + str(user) + ' AND ItemID=' + str(rating))
        item_rating = c.fetchone()
        similarity = calculate_item_sim(item, rating)
        numerator += similarity * item_rating
        denominator += similarity

    return numerator/denominator


'''
cursor.execute('SELECT AVG(ABS(Rating-PredRating)) FROM training_data WHERE PredRating IS NOT NULL')
row = cursor.fetchone()
nMSE = float(row[0])

print('example MSE for random prediction = ' + str(nMSE))

cursor.execute('SELECT AVG(ABS(Rating-3.53)) FROM training_data WHERE PredRating IS NOT NULL')
row = cursor.fetchone()
nMSE = float(row[0])

print('example MSE for user average of 3.53 prediction = ' + str(nMSE))
'''

'''
cursor.execute('SELECT UserID, ItemID FROM predictions')
pred_list = cursor.fetchall()
predictions = []

for item in pred_list:
    predictions.append([item[0], item[1]])

for prediction in predictions:
    pred(prediction[0], prediction[1])
'''

# cursor.execute('SELECT UserID FROM training_data WHERE ItemID=113')
# print(cursor.fetchall())

# print(calculate_sim(1, 5))
# print(pred(1, 46886))
'''
c.execute('SELECT SUM((u1Rating - AVG(u1Rating)) * (u2Rating - AVG(u2Rating))) FROM '
              '(SELECT A.ItemID, A.Rating AS u1Rating, B.Rating AS u2Rating FROM training_data A, training_data B '
              'WHERE A.UserID=6 AND B.UserID=15 AND A.ItemID=B.ItemID)')
print(c.fetchone())
'''

c.execute('SELECT DISTINCT ItemID FROM training_data')
sim_list = c.fetchall()

i = 0

for item in range(0,len(sim_list)):
    i = item + 1
    if i == 1:
        i = 5845
    while i < len(sim_list):
        first_item = sim_list[item]
        second_item = sim_list[i]
        c.execute('INSERT INTO similarities VALUES(' + str(first_item) + ', ' + str(second_item) + ', ' + str(calculate_item_sim(first_item, second_item)) + ')')
        connection.commit()
        i += 1

'''
for similarity in sim_list:
    c.execute('UPDATE similarities SET Similarity=' + str(calculate_item_sim()) + ' WHERE ItemID=' + str(similarity[1]))
'''
c.close()
connection.close()
