import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

# import requests
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"), encoding="utf8"))

DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT")
TABLE_NAME = os.getenv("TABLE_NAME")


def render_index():
    dynamodb = boto3.resource("dynamodb", endpoint_url=DYNAMODB_ENDPOINT)
    table = dynamodb.Table(TABLE_NAME)

    res = table.scan()
    items = res["Items"]

    template = env.get_template("index.html")
    html = template.render(items=items)

    return  {
        "statusCode": 200,
        "body": html,
        "headers": {
            "Content-Type": "text/html"
        }
    }


def lambda_handler(event, context):
    path = event["path"]

    if path == "/console":
        return render_index()

    return {
        "statusCode": 400,
        "body": json.dumps({ "message": "Page not found" }),
    }
