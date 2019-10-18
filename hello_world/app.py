import json
import os
import urllib
import boto3
from boto3.dynamodb.conditions import Key, Attr

# import requests
import slack
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"), encoding="utf8"))

DYNAMODB_ENDPOINT = os.getenv("DYNAMODB_ENDPOINT")
TABLE_NAME = os.getenv("TABLE_NAME")

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_BOT_VERIFY_TOKEN = os.getenv("SLACK_BOT_VERIFY_TOKEN")


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


def render_dialogs(payload):
    client = slack.WebClient(SLACK_BOT_TOKEN)
    user_id = payload["user"]["id"]

    try:
        client.dialog_open(
            trigger_id=payload["trigger_id"],
            dialog={
                "title": "Request a coffee",
                "submit_label": "Submit",
                "callback_id": f"{user_id}cofee_order_from",
                "elements": [
                    {
                        "label": "Coffeee Type",
                        "type": "select",
                        "name": "meal_preferences",
                        "placeholder": "Select a drink",
                        "options": [
                            {
                                "label": "Cappuccino",
                                "value": "cappuccino"
                            },
                            {
                                "label": "Latte",
                                "value": "latte"
                            }
                        ]
                    }
                ]
            }
        )
    except Exception as e:
        print(e)

    return { "statusCode": 200, "body": "" }


def is_verify_token(event):
    token = event.get("token")
    return token == SLACK_BOT_VERIFY_TOKEN


def lambda_handler(event, context):
    path = event["path"]

    if path == "/console":
        return render_index()

    elif path == "/slack/api/events":
        payload = json.loads(urllib.parse.unquote(event["body"][8:]))
        print(payload)

        if "challenge" in payload:
            return payload["challenge"]

        if not is_verify_token(payload):
            return "Token not verified"

        return render_dialogs(payload)

    return {
        "statusCode": 400,
        "body": json.dumps({ "message": "Page not found" }),
    }
