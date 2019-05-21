import json
import shutil

import registrars.query


def initialize():
    global index
    shutil.copyfile("rtree.idx", "/tmp/rtree.idx")
    shutil.copyfile("rtree.dat", "/tmp/rtree.dat")
    index = registrars.query.open_index("/tmp/rtree")


def lambda_handler(event, context):
    global index
    payload = [
    ]
    return {
        "statusCode": "200",
        "body": json.dumps(payload),
    }


initialize()
