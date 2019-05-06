# -*- coding: utf-8 -*-

import io
import boto3
import time
import sys


def batch(seq, batch_size):
    seq_len = len(seq)
    for ndx in range(0, seq_len, batch_size):
        yield seq[ndx:min(ndx + batch_size, seq_len)]

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("provide file path (source of data) and dynamodb table name (destination)")
        exit(1)

    file_path = sys.argv[1]
    table_name = sys.argv[2]

    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(table_name)




    # small documents (size is much smaller than 400kb)  



    items = []
    with open(file_path) as user_data:
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
        time.sleep(2)


