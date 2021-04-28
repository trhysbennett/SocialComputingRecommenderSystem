import math
import sqlite3
import codecs
import random

connection = sqlite3.connect('comp3208.db')

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

split = math.floor(len(listLines) * 0.8)
count = 0


cursor.execute('CREATE INDEX IF NOT EXISTS training_data_index on training_data (UserID, ItemID)')
cursor.execute('CREATE INDEX IF NOT EXISTS validation_data_index on validation_data (UserID, ItemID)')
connection.commit()

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
