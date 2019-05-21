import json
import os
import shutil

import registrars.query

CORS_ORIGIN = os.getenv("CORS_ORIGIN")


def initialize():
    global index
    shutil.copyfile("rtree.idx", "/tmp/rtree.idx")
    shutil.copyfile("rtree.dat", "/tmp/rtree.dat")
    index = registrars.query.open_index("/tmp/rtree")


def lambda_handler(event, context):
    global index
    if event["httpMethod"] == "POST":
        body = json.loads(event["body"])
        gps_location = (body["longitude"], body["latitude"])
        payload = [
            {
                "osm_name": registrar_dict["osm_name"],
                "url": registrars.query.format_url(registrar_dict,
                                                   gps_location),
            }
            for registrar_dict in registrars.query.search_index(gps_location,
                                                                index)
        ]
        return {
            "statusCode": "200",
            "body": json.dumps(payload) + "\n",
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": CORS_ORIGIN,
            },
        }
    elif event["httpMethod"] == "OPTIONS":
        return {
            "statusCode": "200",
            "headers": {
                "Access-Control-Allow-Origin": CORS_ORIGIN,
            }
        }
    else:
        return {
            "statusCode": "500",
        }


initialize()
