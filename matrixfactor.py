import pandas as pd
import numpy as np

train_df = pd.read_csv("comp3208-train.csv", low_memory=False, header=None, names=["user", "itemID", "rating", "timestamp"])
train_df = train_df.apply(pd.to_numeric, errors='coerce')
train_df['rating'] = train_df['rating'].astype(float)
train_df = train_df[(train_df > 0).all(axis=1)]

np.random.seed(0)

n_users = train_df.user.unique().shape[0]
n_items = train_df.itemID.unique().shape[0]
ratings = np.zeros((n_users, n_items), np.half)

for row in train_df.itertuples():
    ratings[row[1]-1, row[2]-1] = row[3]

print(ratings)

n_factors = 40
learning_rate = 0.1
reg = 0.0
n_pairs = 20

user_vectors = np.random.random((n_users, n_factors))
item_vectors = np.random.random((n_items, n_factors))

for i in range(0, 20):
    rand_users = np.random.randint(0, n_users, n_pairs)
    rand_items = np.random.randint(0, n_items, n_pairs)

    for j in range(0, n_pairs - 1):
        pred_rating = user_vectors[rand_users[j], :].dot(item_vectors[rand_items[j], :].T)
        print(pred_rating)
        actual_rating = ratings[rand_users[j], rand_items[j]]
        error = actual_rating - pred_rating

        user_vectors[j, :] += learning_rate * ((error * item_vectors[j, :]) - (reg * user_vectors[j, :]))
        item_vectors[j, :] += learning_rate * ((error * user_vectors[j, :]) - (reg * item_vectors[j, :]))


test_df = pd.read_csv("comp3208-test.csv", low_memory=False, header=None, names=["user", "itemID", "timestamp"])
test_df.insert(2, 'predRatings')

for i in range(0, test_df.size):
    user = test_df.iloc[i, i]
    item = test_df.iloc[i, i + 1]

    pred_rating = user_vectors[user].dot(item_vectors[item].T)
    print(pred_rating)

    test_df.loc[i, "pred_rating"] = pred_rating

print(test_df)
