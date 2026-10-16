import os

import boto3
from dotenv import load_dotenv

load_dotenv()
session = boto3.Session(  # reads AWS_PROFILE credentials (SSO or IAM)
    profile_name=os.getenv("AWS_PROFILE"),
    region_name=os.environ["AWS_REGION"],
)
client = session.client("bedrock-runtime")

# Converse API: one request shape for every Bedrock model
response = client.converse(
    modelId=os.environ["BEDROCK_MODEL_ID"],
    messages=[{"role": "user", "content": [{"text": "Say hello in one sentence."}]}],
    inferenceConfig={"maxTokens": 200},
)
print(response["output"]["message"]["content"][0]["text"])
