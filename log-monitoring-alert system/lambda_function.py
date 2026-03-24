# Import built-in Python libraries
import json     # Used to format output responses
import boto3    # AWS SDK for Python (lets Lambda talk to AWS services)
import re       # Regular expressions (used to detect patterns in logs)

# Create AWS service clients (Allows Lambda to interact with AWS services)
s3 = boto3.client('s3')     # Used to read log files from S3
sns = boto3.client('sns')   # Used to send alert notifications

# This tells Lambda where to send alerts
SNS_TOPIC_ARN = "arn:aws:sns:us-east-2:244826541546:security-alerts"

# Pattern to detect failed login attempts
FAILED_LOGIN_PATTERN = r"Failed password"

# Pattern to detect IPv4 addresses
IP_PATTERN = r"\d+\.\d+\.\d+\.\d+"

# Number of failed attempts before triggering alert
THRESHOLD = 3


# Main Lambda function
# This runs automatically when a new file is uploaded to S3
def lambda_handler(event, context): 

    # Extract bucket name from event trigger
    bucket = event['Records'][0]['s3']['bucket']['name']

    # Extract file name (key) from event trigger
    key = event['Records'][0]['s3']['object']['key']

    # Get log file from S3
    response = s3.get_object(
        Bucket=bucket, 
        Key=key
    )

    # Read file contents and convert from bytes to text
    log_data = response['Body'].read().decode('utf-8')
    
     # Dictionary to store failed login attempts
    # Format:
    # { "IP_ADDRESS": count }
    failed_attempts = {}

    # Loop through each line of the log file
    for line in log_data.split('\n'):

        if re.search(FAILED_LOGIN_PATTERN, line):

            ip_match  = re.search(IP_PATTERN, line)

            if ip_match :

                ip_address = ip_match.group()

                failed_attempts[ip_address] = failed_attempts.get(ip_address, 0) + 1
    
    # List to store alert messages
    alerts = []

    # Check each IP against threshold
    for ip, count in failed_attempts.items():

        if count >= THRESHOLD:

            alerts.append(f"Multiple login failures from IP: {ip} ({count} attempts)")

     # If suspicious activity detected
    if alerts: 
        
        message = "\n".join(alerts)

        sns.publish(
    TopicArn="arn:aws:sns:us-east-2:244826541546:security-alerts",
    Subject="Security Alert Detected",
    Message=message
)

        # Return response to AWS Lambda logs
        return {
            'statusCode': 200,
            'body': json.dumps('Analysis complete')
        }
    
