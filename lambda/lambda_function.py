import base64
import json
import os
import shutil

import requests

import registrars.query

CORS_ORIGIN = os.getenv("CORS_ORIGIN")


def initialize():
    global index
    AWS_EXECUTION_ENV = os.getenv("AWS_EXECUTION_ENV")
    if ((AWS_EXECUTION_ENV and AWS_EXECUTION_ENV.startswith("AWS_Lambda_")) or
            os.getenv("AWS_SAM_LOCAL") == "true"):
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
        if event.get("isBase64Encoded"):
            raw_body = base64.b64decode(event["body"])
        else:
            raw_body = event["body"]
        body = json.loads(raw_body)
        if "longitude" in body and "latitude" in body:
            location = (body["longitude"], body["latitude"])
            if "accuracy" in body:
                try:
                    accuracy = float(body["accuracy"])
                except ValueError:
                    accuracy = 0
            else:
                accuracy = 0
        elif "query" in body:
            location = nominatim(body["query"])
            if location is None:
                return {
                    "statusCode": "200",
                    "body": json.dumps({
                        "error": ("The search query couldn't be resolved to a "
                                  "location.")
                    }),
                    "headers": {
                        "Content-Type": "application/json",
                        "Access-Control-Allow-Origin": CORS_ORIGIN,
                    },
                }
            accuracy = 0
        else:
            return {
                "statusCode": "200",
                "body": json.dumps({
                    "error": ("Neither a search query nor a location was "
                              "specified.")
                }),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": CORS_ORIGIN,
                },
            }
        results = list(registrars.query.search_index(
            location,
            accuracy,
            index
        ))
        if not results:
            return {
                "statusCode": "200",
                "body": json.dumps({
                    "error": "No results were found for this location."
                }),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": CORS_ORIGIN,
                },
            }
        payload = {
            "results": [
                {
                    "osm_name": registrar_dict["osm_name"],
                    "url": registrars.query.format_url(registrar_dict,
                                                       location),
                }
                for registrar_dict in results
            ]
        }
        return {
            "statusCode": "200",
            "body": json.dumps(payload),
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
