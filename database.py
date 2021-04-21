import math
import sqlite3
import codecs
import random

connection = sqlite3.connect('comp3208.db')

readHandle = codecs.open('comp3208-train.csv', 'r', 'utf-8', errors='replace')
listLines = readHandle.readlines()
readHandle.close()


cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS training_data (UserID INT, ItemID INT, Rating FLOAT, PredRating FLOAT,'
               'TmSmp INT)')
cursor.execute('CREATE TABLE IF NOT EXISTS validation_data (UserID INT, ItemID INT, Rating FLOAT, PredRating FLOAT, '
               'TmSmp INT)')
connection.commit()

split = math.floor(len(listLines) * 0.8)
count = 0

for strLine in listLines:
    if len(strLine.strip()) > 0:
        listParts = strLine.strip().split(',')
        if len(listParts) == 4:
            if count <= split:
                cursor.execute('INSERT INTO training_data VALUES (?,?,?,?,?)',
                               (listParts[0], listParts[1], listParts[2], random.random() * 5.0, listParts[3]))
                count += 1
            else:
                cursor.execute('INSERT INTO validation_data VALUES (?,?,?,?)',
                               (listParts[0], listParts[1], listParts[2], random.random() * 5.0, listParts[3]))
                count += 1
        else:
            raise Exception('failed to parse csv: ' + repr(listParts))

connection.commit()

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

cursor.close()
connection.close()

