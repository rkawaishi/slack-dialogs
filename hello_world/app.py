import json
import os

# import requests
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"), encoding="utf8"))


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

    return render_index()
    # return {
    #     "statusCode": 200,
    #     "body": json.dumps({
    #         "message": render_index(),
    #         # "location": ip.text.replace("\n", "")
    #     }),
    # }
