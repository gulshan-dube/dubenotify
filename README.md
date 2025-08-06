# 📣 DubeNotify – Smart AWS Notification System

DubeNotify is a lightweight, serverless alerting system built on AWS.  
It monitors file uploads to an S3 bucket and sends email notifications when specific types of files (e.g. `.csv`) are uploaded.  
The system is designed to be modular, cost-effective, and easy to extend.

---

## 🧠 Real-World Analogy (For Non-Tech Folks)

Imagine you run a small office.  
Every time someone drops a report into the "Important Documents" tray, you want to get an email alert — but only if it’s a spreadsheet, not random notes or images.

**DubeNotify** is like a smart assistant that watches that tray (S3 bucket), checks if the document is a spreadsheet (`.csv`), and sends you an email if it is.  
It ignores everything else — quietly and efficiently.

---

## 🛠️ Tech Stack

- **AWS S3** – Stores uploaded files
- **AWS Lambda** – Processes file upload events
- **AWS SNS (Simple Notification Service)** – Sends email alerts
- **IAM Roles** – Secure access between services

---

## 🚀 How It Works

1. A file is uploaded to a specific S3 bucket
2. S3 triggers a Lambda function
3. Lambda checks if the file ends with `.csv`
4. If yes, Lambda publishes a message to an SNS topic
5. SNS sends an email to the configured recipient

---






## 📜 Lambda Function Code (`dubenotify.py`)



---

## 🧠 Lambda Function Evolution

Below are the three versions of the Lambda function used throughout the project. Each version reflects a different phase of development.

---

### 🧪 Version 1: Basic Lambda for Manual Testing

This version was used to test SNS alerts manually by sending a message via the Lambda console.

```python
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

```

🧪 How to Test This Version

In the Lambda console:

Click Test

Create a test event with the following JSON:

``` json
{
  "message": "🚨 Alert: Something important happened!"
}

```

📁 Version 2: Lambda Triggered by S3 Uploads

This version was used when the Lambda was connected to an S3 bucket to an S3 bucket. It extracts the. It extracts the bucket name and file key from the bucket name and file key from the event and sends event and sends an alert.



```python
import boto3
import os

sns = boto3
import boto3
import os

sns = boto3.client('sns')

.client('sns')

def lambda_handlerdef lambda_handler(event, context):
    # Extract bucket and object info(event, context):
    # Extract bucket and object info from S3 event
    from S3 event
    record = event['Records'] record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key[0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object'] = record['s3']['object']['key']

    message = f"📁 New file uploaded to S3:

\['key']

    message = f"📁 New filenBucket: {bucket}\nKey: {key}"
    uploaded to S3:\ topic_arn = os.environ['SNS_TOPIC_ARN']

    response = snsnBucket: {bucket}\nKey: {key}"
    topic_arn = os.environ['SNS_TOPIC_ARN']

    response = sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='DubeNotify S3 Alert='DubeNotify S3 Alert'
    )

    return'
    )

    return {
        'status {
        'statusCode': 200,
       Code': 200,
        'body': f"Alert 'body': f"Alert sent for S3 upload sent for S3 upload: {response['MessageId']}"
: {response['MessageId']}"
    }

```


> ✅ This version sends alerts version sends alerts for **any file type for **any file type** uploaded to the S3 bucket.

---

** uploaded to the S3 bucket.

---

### 🧠 Version 3### 🧠 Version 3: Lambda with File: Lambda with File Type Filtering

This final version Type Filtering

This final version adds logic to only adds logic to only send alerts for send alerts for `.csv` files. It `.csv` files. It ignores other file ignores other file types to reduce noise.

```python types to reduce

import boto3
import noise.

```python
import boto3
import os

sns = boto3.client('sns')

def lambda_handler os

sns = boto3.client('sns')

(event, context):
    # Extract bucket and object infodef lambda_handler(event, context):
    # Extract bucket and object info from S3 event
    from S3 event
    record = event['Records'] record = event['Records'][0]
    bucket =[0]
    bucket = record['s3']['bucket'] record['s3']['bucket']['name']
    key['name']
    key = record['s3']['object'] = record['s3']['object']['key']

    # Filter: Only alert for['key']

    # Filter: Only alert for .csv files
    if .csv files
    if not key.lower(). not key.lower().endswith('.csv'):
endswith('.csv'):
        print(f"I        print(f"Ignored file: {key}")
        return {
            'statusCode': 200,
            'bodygnored file: {key': f"Ignored file}")
        return {
            'statusCode': 200: {key}"
        }

    message = f"📊 CSV file uploaded,
            'body': f"Ignored file: {key}"
        }

    message = f"📊 CSV file uploaded:\nBucket: {bucket:\nBucket: {bucket}\nKey: {key}"
    topic_arn = os.environ}\nKey: {key}"
    topic_arn = os.environ['SNS_TOPIC_ARN']

['SNS_TOPIC_ARN']

    response = sns    response = sns.publish(
        TopicArn=topic_arn,
       .publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='DubeNotify CSV Message=message,
        Subject='DubeNotify CSV Alert'
    )

    Alert'
    )

    return {
        return {
        'statusCode': 200 'statusCode': 200,
        'body': f"CSV alert sent,
        'body': f"CSV alert sent: {response['MessageId']}"
    }

```


> ✅ This version is used in the final setup and only sends alerts in the final setup and only sends alerts for `.csv` uploads for `.csv` uploads.


## 🧠 Why Include All Versions Include All Versions?



- Shows how the project evolved project evolved
- Helps others understand your thought process your thought process
- Makes it easy to reuse or modify the code later
 to reuse or modify the code later
- Demonstrates real-world development practices



🔐 IAM Inline Policy for Lambda Execution Role
Attach this inline policy to your Lambda’s IAM role:

```json


{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sns:Publish",
      "Resource": "arn:aws:sns:your-region:your-account-id:your-topic-name"
    }
  ]
}

```


📧 SNS Setup (via AWS CLI)
Create an SNS topic and subscribe your email:

bash
aws sns create-topic --name dubenotify-topic

aws sns subscribe \
  --topic-arn arn:aws:sns:your-region:your-account-id:dubenotify-topic \
  --protocol email \
  --notification-endpoint your.email@example.com
📩 You’ll receive a confirmation email — click the link to activate the subscription.



🪣 S3 Event Notification Setup (JSON Format)
Configure your S3 bucket to trigger Lambda on file uploads:

``` json
{
  "LambdaFunctionConfigurations": [
    {
      "Id": "NotifyOnCSVUpload",
      "LambdaFunctionArn": "arn:aws:lambda:your-region:your-account-id:function:dubenotify-function",
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

```

You can apply this via the AWS Console or using the put-bucket-notification-configuration CLI command.



🧱 Architecture Diagram: 

S3 Bucket ──▶ Lambda Function ──▶ SNS Topic ──▶ Email Notification

Diagrams can be created using tools like:

Lucidchart, Draw.io and Excalidraw


🧪 Testing
✅ Upload a .csv file → Email alert received

❌ Upload a .jpg or .txt file → No alert sent

🧭 Future Enhancements (Optional)

- Add Slack or SMS alerts
- Filter based on file size or content
- Use CloudWatch for logging and metrics
- Deploy via CloudFormation or Terraform



