#!/usr/bin/env python
# -*- coding: utf-8 -*-

import boto3
import time
import sys
from boto3.dynamodb.conditions import Attr


def scan_all(table, filter):

    lastEvaluatedKey = {}

    while True:

        scanResp = table.scan(FilterExpression=filter,
                              ExclusiveStartKey=lastEvaluatedKey) \
                    if lastEvaluatedKey \
                    else table.scan(FilterExpression=filter)

        items = scanResp["Items"]
        if not items:
            print("No more items to process")
            break

        print("Scan fetched {0} items".format(len(items)))

        for item in items:
            yield item

        if "LastEvaluatedKey" in scanResp:
            lastEvaluatedKey = scanResp["LastEvaluatedKey"]
        else:
            print("No more items to process")
            break

    print("End of scanning")


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("provide dynamodb table name")
        exit(1)

    dynamoDB = boto3.resource("dynamodb")
    table = dynamoDB.Table(sys.argv[1])

    migration_no = 5
    not_migrated = Attr('migration').ne(migration_no)

    count = 0
    for item in scan_all(table, not_migrated):

        # processing items goes here
        print(str(item))

        table.update_item(
            Key={'id': item['id']},
            UpdateExpression='SET email = :val, migration = :mig',
            ExpressionAttributeValues={
                ':val': 'updated_' + item['email'],
                ':mig': migration_no
            }
        )
        time.sleep(1)
        count += 1

    print("Items processed: {0}".format(count))
