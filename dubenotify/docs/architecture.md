📣 DubeNotify – Smart AWS Notification System
DubeNotify is a lightweight, serverless alerting system built on AWS.
It monitors file uploads to an S3 bucket and sends email notifications when specific types of files (e.g. .csv) are uploaded.
The system is designed to be modular, cost-effective, and easy to extend.

📚 Table of Contents
Real-World Analogy
Tech Stack
How It Works
Lambda Function Code
Version 1: Basic Lambda
Version 2: Triggered by S3
Version 3: With File Type Filtering
IAM Policy
SNS Setup
S3 Setup
Architecture Diagram
Testing
Future Enhancements
Final Notes
🧠 Real-World Analogy (For Non-Tech Folks)
Imagine you run a small office.
Every time someone drops a report into the "Important Documents" tray, you want to get an email alert — but only if it’s a spreadsheet, not random notes or images.

DubeNotify is like a smart assistant that watches that tray (S3 bucket), checks if the document is a spreadsheet (.csv), and sends you an email if it is.
It ignores everything else — quietly and efficiently.

🛠️ Tech Stack
AWS S3 – Stores uploaded files
Bucket Name: dube-notify-bucket
Folder (Prefix): Files uploaded to root or under uploads/
AWS Lambda – Processes file upload events
Function Name: DubeNotifyHandler
AWS SNS – Sends email alerts
Topic Name: DubeNotifyTopic
IAM Roles – Secure access between services
Role Name: LambdaSNSPublishRole
🚀 How It Works
A file is uploaded to the S3 bucket
S3 triggers the Lambda function
Lambda checks if the file ends with .csv
If yes, Lambda publishes a message to the SNS topic
SNS sends an email to the configured recipient
📜 Lambda Function Code (dubenotify.py)
🧪 Version 1: Basic Lambda
Used for manual testing via the Lambda console.

import boto3
import os

sns = boto3.client('sns')

def lambda_handler(event, context):
    message = event.get('message', 'Default alert message')
    topic_arn = os.environ['SNS_TOPIC_ARN']

    response = sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='DubeNotify Alert'
    )

    return {
        'statusCode': 200,
        'body': f"Message sent to SNS: {response['MessageId']}"
    }
🧪 How to Test This Version In the Lambda console:

Click Test

Create a test event with the following JSON:

{
  "message": "🚨 Alert: Something important happened!"
}
Run the test → You should receive an email alert.
📁 Version 2: Triggered by S3

Used when Lambda was connected to S3. Sends alerts for any file type.

import boto3
import os

sns = boto3.client('sns')

def lambda_handler(event, context):
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    message = f"📁 New file uploaded to S3:\nBucket: {bucket}\nKey: {key}"
    topic_arn = os.environ['SNS_TOPIC_ARN']

    response = sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='DubeNotify S3 Alert'
    )

    return {
        'statusCode': 200,
        'body': f"Alert sent for S3 upload: {response['MessageId']}"
    }
✅ Sends alerts for any file type uploaded to the bucket.

🧠 Version 3: With File Type Filtering

Final version — only sends alerts for .csv files.


import boto3
import os

sns = boto3.client('sns')

def lambda_handler(event, context):
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    # Filter: Only alert for .csv files
    if not key.lower().endswith('.csv'):
        print(f"Ignored file: {key}")
        return {
            'statusCode': 200,
            'body': f"Ignored file: {key}"
        }

    message = f"📊 CSV file uploaded:\nBucket: {bucket}\nKey: {key}"
    topic_arn = os.environ['SNS_TOPIC_ARN']

    response = sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='DubeNotify CSV Alert'
    )

    return {
        'statusCode': 200,
        'body': f"CSV alert sent: {response['MessageId']}"
    }


✅ This version is used in the final setup and only sends alerts for .csv uploads.

🔐 IAM Inline Policy for Lambda Execution Role Attach this inline policy to your Lambda’s IAM role:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sns:Publish",
      "Resource": "arn:aws:sns:your-region:your-account-id:DubeNotifyTopic"
    }
  ]
}
📧 SNS Setup (via AWS CLI) bash

aws sns create-topic --name DubeNotifyTopic

aws sns subscribe \
  --topic-arn arn:aws:sns:your-region:your-account-id:DubeNotifyTopic \
  --protocol email \
  --notification-endpoint your.email@example.com
📩 You’ll receive a confirmation email — click the link to activate the subscription.

🪣 S3 Event Notification Setup (JSON Format)

{
  "LambdaFunctionConfigurations": [
    {
      "Id": "NotifyOnCSVUpload",
      "LambdaFunctionArn": "arn:aws:lambda:your-region:your-account-id:function:DubeNotifyHandler",
      "Events": ["s3:ObjectCreated:*"],
      "Filter": {
        "Key": {
          "FilterRules": [
            {
              "Name": "suffix",
              "Value": ".csv"
            }
          ]
        }
      }
    }
  ]
}
You can apply this via the AWS Console or using the put-bucket-notification-configuration CLI command.

🧱 Architecture Diagram

S3 Bucket ──▶ Lambda Function ──▶ SNS Topic ──▶ Email Notification

Visualize this using tools like Lucidchart, Draw.io, or Excalidraw.

🧪 Testing

✅ Upload a .csv file → Email alert received

❌ Upload a .jpg or .txt file → No alert sent

🧭 Future Enhancements (Optional)

Add Slack or SMS alerts

Filter based on file size or content

Use CloudWatch for logging and metrics

Deploy via CloudFormation or Terraform

🙌 Final Notes This project was built as a hands-on exploration of AWS event-driven architecture. It demonstrates how to connect core AWS services in a modular, secure, and scalable way.