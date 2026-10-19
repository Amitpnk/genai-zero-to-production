# AWS CLI and Bedrock setup

Get from "I have an AWS account" to a working Bedrock call: install the AWS CLI, sign in with a profile, pick a region, enable model access, and fix the usual errors.

> **Draft** · Used in Episode 2 and Module 10 · Not run live while drafting (no AWS profile on the build machine); commands follow the AWS CLI v2 docs.

## The big picture

```text
Your code (boto3)  ──uses──▶  AWS profile "genai-course"  ──signs requests──▶  Bedrock (in one region)
                                (SSO or access keys)                            └─ only models you've enabled
```

Three things must line up: **who you are** (profile), **where** (region) and **what you're allowed to call** (model access + IAM).

## 1. Install the AWS CLI (v2)

| OS | How |
| --- | --- |
| **Windows** | Download the MSI from the [AWS CLI install guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html), or `winget install Amazon.AWSCLI` |
| **macOS** | The `.pkg` installer from the same page, or `brew install awscli` |
| **Linux** | The zip installer from the same page |

```bash
aws --version          # aws-cli/2.x.x ...
```

## 2. Sign in with a named profile

This course uses a profile called **`genai-course`**, matching `AWS_PROFILE` in `.env`.

**Option A: IAM Identity Center / SSO (recommended)**: short-lived credentials, nothing secret stored long-term.

```bash
aws configure sso --profile genai-course       # follow the prompts (start URL, region, account, role)
aws sso login --profile genai-course           # run again whenever the session expires
```

**Option B: access keys (personal dev account only)**

```bash
aws configure --profile genai-course           # paste access key ID + secret, set region
```

> Prefer SSO. If you must use access keys: an IAM user with Bedrock-only permissions, never your root account, and never commit the keys.

**Check who you are:**

```bash
aws sts get-caller-identity --profile genai-course
```

## 3. Pick a region and check model access

- Bedrock isn't in every region, and **each region has its own model list**. This course uses `us-east-1`.
- Open the **Bedrock console → Model access** (or the model catalog) in that region and make sure the models you want are available to your account. Some providers ask for a one-time use-case form.
- Copy the **model ID** (or **inference profile ID**, often starting with a region prefix like `us.`) into `.env` as `BEDROCK_MODEL_ID`.

List what you can see from the command line:

```bash
aws bedrock list-foundation-models --region us-east-1 --profile genai-course \
    --query "modelSummaries[].modelId" --output table
```

## 4. Minimum IAM permissions

For calling models, the role or user needs at least:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
    "Resource": "*"
  }]
}
```

The Converse API is authorised through these same `InvokeModel` actions. Tighten `Resource` to specific model ARNs for production.

## 5. Test it

```bash
uv run python ep02-setup/hello_bedrock.py
```

## Troubleshooting

| Error | Cause | Fix |
| --- | --- | --- |
| `The config profile (genai-course) could not be found` | Profile not created, or a typo | `aws configure sso --profile genai-course`; check `AWS_PROFILE` in `.env` |
| `Token has expired` / `SSO session ... expired` | SSO sessions last hours | `aws sso login --profile genai-course` |
| `UnrecognizedClientException` | Bad or deleted access keys | Re-run `aws configure --profile genai-course` |
| `AccessDeniedException` | No model access, or IAM missing `bedrock:InvokeModel` | Enable the model in the console; check IAM |
| `ValidationException: ... model identifier is invalid` | Wrong model ID, or the model needs an **inference profile** ID | Copy the exact ID from the catalog in your region |
| `ResourceNotFoundException` / model not found | Model not offered in this region | Switch region or model |
| `ThrottlingException` | Too many requests | Back off and retry ([API errors guide](../api-errors/)) |

## Useful commands

```bash
aws configure list-profiles                      # which profiles exist?
aws configure list --profile genai-course        # what does this profile use?
aws sso logout                                   # end SSO sessions
aws sts get-caller-identity --profile genai-course
```

> Never paste account IDs or keys into screenshots, issues or videos. Blur them.
