# 🏗️ DubeNotify Architecture Overview

## 📦 Components

- **S3 Bucket** – Stores uploaded files
- **Lambda Function** – Triggered by S3 events, filters `.csv` files
- **SNS Topic** – Sends email alerts
- **IAM Roles** – Secure access between services

## 🔄 Flow Diagram

1. File uploaded to S3
2. S3 triggers Lambda
3. Lambda checks file type
4. If `.csv`, Lambda publishes to SNS
5. SNS sends email to subscriber

## 🔐 Security Design

- IAM roles scoped to minimum required permissions
- SNS topic restricted to known subscribers
- Lambda environment variables (if used) stored securely

## 🧭 Design Decisions

- Serverless architecture for scalability and cost-efficiency
- Email alerts chosen for simplicity and accessibility
- `.csv` filter to reduce noise and focus on meaningful uploads

## 🧱 Future Extensions

- Add Slack or SMS alerts
- Use CloudWatch for logging and metrics
- Deploy via CloudFormation or Terraform
