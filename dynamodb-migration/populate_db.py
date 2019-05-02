# -*- coding: utf-8 -*-

import io
import boto3
import time

dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('users')


def batch(seq, batch_size):
    seq_len = len(seq)
    for ndx in range(0, seq_len, batch_size):
        yield seq[ndx:min(ndx + batch_size, seq_len)]

# small documents (size is much smaller than 400kb)  



items = []
with open("dummy_user_data.csv") as user_data:
    for user in user_data:
        if not user:
            continue

        parts = user.split(",")

        item = {
            'id': parts[0],
            'first_name': parts[1],
            'last_name': parts[2],
            'email': parts[3].strip()
        }

        items.append(item)

batches = [b for b in batch(items, 25)]

print(str(batches[0]))


for batch in batches:
    with table.batch_writer() as writer:
        for item in batch:
            writer.put_item(item)

