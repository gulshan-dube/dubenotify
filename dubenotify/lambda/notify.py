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
