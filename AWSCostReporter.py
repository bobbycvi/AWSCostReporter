import boto3
import datetime
import smtplib
import os
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tabulate import tabulate

# Email Configuration
email_sender = 'YOUR_EMAIL'
email_password = 'YOUR_EMAIL_PASSWORD'
email_recipient = 'RECIPIENT_EMAIL'

# Initialize AWS Cost Explorer Client
client = boto3.client('ce')

# Get the current date
end_date = datetime.datetime.now().date().isoformat()
# Get the date 3 months ago from the current date
start_date = (datetime.datetime.now() - datetime.timedelta(days=90)).date().isoformat()

# Fetch data from AWS Cost Explorer
response = client.get_cost_and_usage(
    TimePeriod={
        'Start': start_date,
        'End': end_date
    },
    Granularity='MONTHLY',
    Filter={
        'And': [
            {
                'Not': {
                    'Dimensions': {
                        'Key': 'CHARGE_TYPE',
                        'Values': ['Credit', 'SavingsPlanNegation', 'Tax']
                    }
                }
            },
            {
                'Dimensions': {
                    'Key': 'BILLING_ENTITY',
                    'Values': ['AWS']
                }
            }
        ]
    },
    Metrics=['UnblendedCost']
)

# Extract and format the data
results = []
for item in response['ResultsByTime']:
    amount = item['Total']['UnblendedCost']['Amount']
    unit = item['Total']['UnblendedCost']['Unit']
    results.append([item['TimePeriod']['Start'], amount, unit])

# Create a DataFrame
df = pd.DataFrame(results, columns=['Date', 'Amount', 'Unit'])

# Export data to a CSV file
df.to_csv('aws_costs.csv', index=False)

# Uncomment the below line if you want to export to Excel instead of CSV
# df.to_excel('aws_costs.xlsx', index=False)

# Send the file via email
msg = MIMEMultipart()
msg['From'] = email_sender
msg['To'] = email_recipient
msg['Subject'] = 'AWS Costs Report'

attachment = MIMEBase('application', 'octet-stream')
attachment.set_payload(open('aws_costs.csv', 'rb').read())
encoders.encode_base64(attachment)
attachment.add_header('Content-Disposition', 'attachment; filename="aws_costs.csv"')
msg.attach(attachment)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email_sender, email_password)
server.sendmail(email_sender, email_recipient, msg.as_string())
server.quit()

# Display the results in the terminal
print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
