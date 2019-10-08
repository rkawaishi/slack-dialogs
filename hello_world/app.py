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
    user_id = "test user"

    template = env.get_template("index.html")
    html = template.render(user_id=user_id)

    return  {
        "statusCode": 200,
        "body": html,
        "headers": {
            "Content-Type": "text/html"
        }
    }


def lambda_handler(event, context):
    print(DYNAMODB_ENDPOINT)
    print(TABLE_NAME)

    dynamodb = boto3.resource("dynamodb", endpoint_url=DYNAMODB_ENDPOINT)
    table = dynamodb.Table(TABLE_NAME)

    res = table.query(KeyConditionExpression=Key("name").eq("sasaki-daisuke"))
    items = res["Items"]

    print(items)

    return items
    # return {
    #     "statusCode": 200,
    #     "body": json.dumps({
    #         "message": render_index(),
    #         # "location": ip.text.replace("\n", "")
    #     }),
    # }
