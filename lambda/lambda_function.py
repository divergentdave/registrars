import json
import os
import requests
import shutil

import registrars.query

CORS_ORIGIN = os.getenv("CORS_ORIGIN")


def initialize():
    global index
    AWS_EXECUTION_ENV = os.getenv("AWS_EXECUTION_ENV")
    if AWS_EXECUTION_ENV and AWS_EXECUTION_ENV.startswith("AWS_Lambda_"):
        shutil.copyfile("rtree.idx", "/tmp/rtree.idx")
        shutil.copyfile("rtree.dat", "/tmp/rtree.dat")
        index = registrars.query.open_index("/tmp/rtree")
    else:
        index = registrars.query.open_index("rtree")


def nominatim(query):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "https://github.com/divergentdave/registrars"
    })
    resp = session.get("https://nominatim.openstreetmap.org/search",
                       params={"q": query, "limit": 1, "format": "json"})
    body = resp.json()
    if not body:
        return None
    result = body[0]
    bounding_box = result["boundingbox"]
    bb_south, bb_north, bb_west, bb_east = [float(x) for x in bounding_box]
    longitude = (bb_west + bb_east) / 2
    latitude = (bb_south + bb_north) / 2
    return (longitude, latitude)


def lambda_handler(event, context):
    global index
    if event["httpMethod"] == "POST":
        body = json.loads(event["body"])
        if "longitude" in body and "latitude" in body:
            location = (body["longitude"], body["latitude"])
        elif "query" in body:
            location = nominatim(body["query"])
        else:
            return {
                "statusCode": "500",
                "body": json.dumps({
                    "error": ("Neither a search query nor a location was "
                              "specified")
                }),
            }
        if location:
            payload = [
                {
                    "osm_name": registrar_dict["osm_name"],
                    "url": registrars.query.format_url(registrar_dict,
                                                       location),
                }
                for registrar_dict
                in registrars.query.search_index(location, index)
            ]
        else:
            payload = []
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
            },
        }
    else:
        return {
            "statusCode": "500",
        }


initialize()
