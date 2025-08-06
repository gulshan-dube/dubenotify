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

```python
import boto3

def lambda_handler(event, context):
    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:your-region:your-account-id:your-topic-name'

    for record in event['Records']:
        s3_object_key = record['s3']['object']['key']
        if s3_object_key.endswith('.csv'):
            message = f"CSV file uploaded: {s3_object_key}"
            sns.publish(TopicArn=topic_arn, Message=message, Subject='CSV Upload Alert')
```

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



🧱 Architecture Diagram (Copy-Paste Friendly)

You can use this diagram in tools like diagrams.net, Lucidchart, or Mermaid:

+-------------+       (upload)       +--------------+
|             |  ───────────────▶   |              |
|   S3 Bucket |                     |   Lambda      |
|             | ◀─── trigger ─────  |   Function    |
+-------------+                     +--------------+
                                         │
                                         ▼
                                +----------------+
                                |     SNS Topic   |
                                +----------------+
                                         │
                                         ▼
                                +----------------+
                                | Email Subscriber|
                                +----------------+


🧪 Testing
✅ Upload a .csv file → Email alert received

❌ Upload a .jpg or .txt file → No alert sent

🧭 Future Enhancements (Optional)

- Add Slack or SMS alerts
- Filter based on file size or content
- Use CloudWatch for logging and metrics
- Deploy via CloudFormation or Terraform



